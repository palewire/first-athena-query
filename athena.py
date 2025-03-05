"""Utilities for working Amazon Athena."""

from __future__ import annotations

import io
import os
import time
import typing

import boto3
import pandas as pd


def create_database(
    database_name: str,
    verbose: bool = False,
) -> str:
    """Create Amazon Athena database.

    Args:
        database_name : str
            name of the database
        verbose : bool
            whether to print verbose output

    Returns:
        str : query execution id

    Example:
        >>> create_database("my_database", verbose=True)
    """
    if verbose:
        print(f"Creating {database_name} if it doesn't exist")
    return query(f"CREATE DATABASE IF NOT EXISTS {database_name}", verbose=verbose)


def drop_database(
    database_name: str,
    verbose: bool = False,
) -> str:
    """Drop Amazon Athena database.

    Args:
        database_name : str
            name of the database
        verbose : bool
            whether to print verbose output

    Returns:
        str : query execution id

    Example:
        >>> drop_database("my_database", verbose=True)
    """
    if verbose:
        print(f"Dropping {database_name} if it exists")
    return query(f"DROP DATABASE IF EXISTS {database_name}", verbose=verbose)


def create_table(
    database_name: str,
    table_name: str,
    field_list: list[list[str, str]],
    location: str,
    stored_as: typing.Literal["PARQUET", "CSV"] = "CSV",
    verbose: bool = False,
) -> str:
    """Create Amazon Athena table.

    Args:
        database_name : str
            name of the database
        table_name : str
            name of the table
        field_list : list[list[str, str]]
            list of field names and types. e.g. [["id", "INT"], ["name", "STRING"]].
            Reference for field types available at https://docs.aws.amazon.com/athena/latest/ug/data-types.html
        location : str
            s3 location of the data inside AWS S3 bucket. e.g. 's3://my-bucket/my-folder/' would be /my-folder/
        stored_as : str
            file format of the source data. e.g. "PARQUET" or "CSV"
        verbose : bool
            whether to print verbose output

    Returns:
        str : query execution id

    Example:
        >>> create_table(
        ...     "my_database",
        ...     "my_table",
        ...     [["id", "INT"], ["name", "STRING"]],
        ...     "/my-folder/",
        ...     verbose=True,
        ... )
    """
    # Create the SQL statement
    sql = f"CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (\n"
    for field in field_list:
        sql += f"    {field[0]} {field[1]},\n"
    sql = sql[:-2] + "\n)\n"
    sql += f"STORED AS {stored_as}\n"
    sql += f"LOCATION '{location}'"

    # Run the query
    if verbose:
        print(f"Creating Athena table: {database_name}.{table_name}")
    return query(sql, verbose=verbose)


def drop_table(
    database_name: str,
    table_name: str,
    verbose: bool = False,
) -> str:
    """Drop Amazon Athena table.

    Args:
        database_name : str
            name of the database
        table_name : str
            name of the table
        verbose : bool
            whether to print verbose output

    Returns:
        str : query execution id

    Example:
        >>> drop_table("my_database", "my_table", verbose=True)
    """
    # Drop the table if it exists
    if verbose:
        print(f"Dropping {database_name}.{table_name} if it exists")
    return query(f"DROP TABLE IF EXISTS {database_name}.{table_name}", verbose=verbose)


def get_dataframe(
    sql: str,
    verbose: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """Get pandas DataFrame from Amazon Athena query.

    Args:
        sql : str
            formatted string containing athena sql query
        verbose : bool
            whether to print verbose output
        **kwargs
            additional keyword arguments to pass to the dataframe

    Returns:
        pd.DataFrame : pandas DataFrame containing query results

    Example:
        >>> sql = "SELECT COUNT(*) FROM my_database.my_table"
        >>> df = get_dataframe(sql, verbose=True)
        >>> print(df.head())
    """
    # Run the query
    job_id = query(sql, verbose=verbose)

    # Connect to Amazon S3
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Download the file created by our query
    response = client.get_object(
        Bucket=os.getenv("AWS_S3_BUCKET_NAME"),
        Key=f"query-output/{job_id}.csv",
    )

    # Convert it to the file object
    file_obj = io.BytesIO(response["Body"].read())

    # Read the file into a pandas DataFrame
    if kwargs is None:
        kwargs = {}
    df = pd.read_csv(file_obj, **kwargs)

    # Return the DataFrame
    return df


def query(
    sql: str,
    wait: int = 10,
    verbose: bool = False,
) -> str:
    """Execute SQL query on Amazon Athena.

    Args:
        sql : str
            formatted string containing athena sql query
        wait : int
            number of seconds to wait between checking query status
        verbose : bool
            whether to print verbose output

    Returns:
        str : query execution id

    Example:
        >>> query("SELECT COUNT(*) FROM my_database.my_table", verbose=True)
    """
    # Create the Athena client
    client = boto3.client("athena", region_name=os.getenv("AWS_REGION_NAME"))

    # Set the destination as our temporary S3 workspace folder
    s3_destination = f"s3://{os.getenv('AWS_S3_BUCKET_NAME')}/query-output/"

    # Execute the query
    if verbose:
        print(f"Running query: {sql}")
    request = client.start_query_execution(
        QueryString=sql,
        ResultConfiguration={
            "OutputLocation": s3_destination,
        },
    )

    # Get the query execution id
    query_id = request["QueryExecutionId"]
    if verbose:
        print(f"Query ID: {query_id}")

    # Wait for the query to finish
    retry_count = 0
    while True:
        # Get the query execution state
        response = client.get_query_execution(QueryExecutionId=query_id)
        state = response["QueryExecution"]["Status"]["State"]

        # If it's still running, wait a little longer
        if state in ["RUNNING", "QUEUED"]:
            if verbose:
                print(f"Query state: {state}. Waiting {wait} seconds...")
            time.sleep(wait)
            retry_count += 1
        # If it failed, raise an exception
        else:
            break

    # Make sure it finished successfully
    if verbose:
        print(f"Query finished with state: {state}")
    assert state == "SUCCEEDED", f"query state is {state}"

    # Return the query id
    return query_id