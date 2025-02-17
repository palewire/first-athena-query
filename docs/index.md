# First Athena Query

How to analyze millions of records in seconds with Amazon Web Services and SQL

## What you will learn

We’ve all been there. Excel locks up. Your dataframe can’t hang. And that damn SQL query has been running for two days now.

There’s no way around it. The database you're working on is just too big for your laptop to handle.

This tutorial offers a solution: Amazon Athena. Follow along to learn how the web service can rip through records with the power of SQL.

## Who can take it

This course is free. Previous experience working with Amazon Web Services and SQL will come in handy, but anyone with good attitude is qualified to take the class. You will be charged for the AWS resources you use, so a credit card is required.

## Table of contents

* [What is Athena?](#what-is-athena)
* [How do newsrooms use it?](#how-do-newsrooms-use-it)
* [Setting up an AWS account](#setting-up-an-aws-account)
* [Creating an s3 bucket to store data](#creating-an-s3-bucket-to-store-data)
* [Creating a database table in Athena](#creating-a-database-table-in-athena)
* [Running your first query](#running-your-first-query)
* [Automating queries with Python](#automating-queries-with-python)

## What is Athena?

Athena is the name for a cloud-computing tool offered by Amazon Web Services that allows you to query static data files using SQL. It can analyze extremely large datasets in seconds without a traditional server or database. While it does cost money, the prices are low and there are no fixed costs. You only pay for the data you store and the queries you run.

## How do newsrooms use it?

TK TK TK

## Setting up an AWS account

The first step is to create an Amazon Web Services account, if you don't already have one. Go to [aws.amazon.com](https://aws.amazon.com/) and click the button that says "Create an AWS account" in the upper right corner.

![AWS splash page](_static/aws-splash.png)

You'll provide a root email address and a name for the account. And then you'll be asked to verify your email. Then you'll enter a password, contact information and a payment method. You'll also have to verify your phone number. Once that's completed, you'll be congratulated for your wherewithal.

![AWS congrats](_static/aws-congrats.png)

Now you're ready to sign into the AWS Management Console, where you can access all of the services it offers.

![AWS console](_static/aws-console.png)


## Creating an s3 bucket to store data

You need to create a place to store your data. Amazon S3 is a cloud storage service that allows you to hold static files in a folder known as a bucket. Our next step is to create a bucket for the dataset we'll analyze in this tutorial.

You should go to the search bar at the top of the console and search "S3". Then click on the link it offers.

![AWS S3 search](_static/search-s3.png)

That will take you to a landing page for the service that will offer a large button that says "Create bucket." Click it.

![Bucket button](_static/bucket-button.png)

You can create a general purpose bucket with all of the default settings. Just make sure to give it a unique name. Then click "Create bucket" at the bottom of the form.

![Create bucket](_static/create-bucket.png)

Now you have a bucket. Click on its name to open it up.

![Bucket list](_static/bucket-list.png)

Now it's time to upload the data we'll be using in this tutorial, which is TK TK TK

## Creating a database table in Athena

TK TK TK

## Running your first query

TK TK TK

## Automating queries with Python

Running queries in Athena is great, but automating them in Python is even better. It could allow you run queries on a schedule, or to loop through a list of queries and run them without having to click buttons in the console.

Accessing Amazon Web Services with Python requires that you first establish an API key with permission to access the services you want to use. You can do that by clicking on the pulldown menu in the far upper right corner of the console and selecting "Security Credentials."

![Settings pulldown](_static/account-menu.png)

Then scroll down to the "Access keys" section and click the button that says "Create access key."

![Keys section](_static/keys-section.png)

Now you can create a root key pair by checking the box and clicking the button that says "Create access key."

![Keys section](_static/keys-consent.png)

The final screen will show you the key's ID and secret. I've redacted my pair in the example below.

![Keys screen](_static/redacted-keys.png)

Copy and paste them into a text file for safekeeping. You will not be able to see the secret key again. They are what Python will use to gain access to AWS from outside the console.

Now you will need to install `boto3`, the most popular Python tool for working with AWS. You can do that from your terminal with the pipenv Python package manager.

```bash
pipenv install boto3
```

In your project directory, create a file named `.env` to store you AWS credentials and other sensitive information. It should look like the following. Unless you changed the default settings when creating your S3 bucket, the region name should be `us-east-1`.

```bash
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
AWS_REGION_NAME=YOUR_REGION_NAME
AWS_S3_BUCKET_NAME=YOUR_BUCKET_NAME
```

Create a new file called `athena.py` in your text editor of choice, we prefer [VSCode](https://code.visualstudio.com/), and paste in the following code.

It is a utility function that will allow you to run queries in Athena from Python. Read it carefully and you'll see how it uses `boto3` to send a SQL query to Athena and store the results in a subdirectory of your bucket named `athena-workspace`.

```python
"""Utilities for working Amazon Athena."""

from __future__ import annotations

import os
import time

import boto3

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
    """
    # Create the Athena client
    client = boto3.client("athena", region_name=os.getenv("AWS_REGION_NAME"))

    # Set the destination as our temporary S3 workspace folder
    s3_destination = f"s3://{os.getenv('AWS_S3_BUCKET_NAME')}/athena-workspace/"

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
```

You can now access the function in other Python files by importing the file we've created. As a simple example, create a second file named `run.py` and toss in the following:

```python
import athena

sql = "SELECT * FROM database"
q_id = athena.query(sql, verbose=True)
print(q_id)
```

Run the file in your terminal.

```bash
pipenv run python run.py
```

Your terminal should print out its progress as it issues the query and waits for a response from Athena. After it finishes, it will print out the identifier for the result. Return to your S3 bucket in your web browser and you should see it after clicking into the `athena-workspace` subdirectory.

SCREENSHOT TK

If you download the file and open it in a spreadsheet you'll see the results.

SCREENSHOT TK

That's a good start, but it's hassle that we have to go look up the result ourselves with all that pointing and clicking. We'll get that done by adding another utility function that can download the query result and return a data table you can work with in Python.

First you'll want to install pandas, a popular Python library for working with data. You can do that with whatever Python package manager you prefer.

```bash
pipenv install pandas
```

Reopen `athena.py` and edit the top of the file, above the query function, as follows. Notice how the `io` import has been added at the top and the `pandas` import has been added after `boto3`.

```python
"""Utilities for working Amazon Athena."""

from __future__ import annotations

import io
import os
import time

import boto3
import pandas as pd


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
        kwargs
            additional keyword arguments to pass to the dataframe

    Returns:
        pd.DataFrame : pandas DataFrame containing query results
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
        Key=f"athena-workspace/{job_id}.csv",
    )

    # Convert it to the file object
    file_obj = io.BytesIO(response["Body"].read())

    # Read the file into a pandas DataFrame
    if kwargs is None:
        kwargs = {}
    df = pd.read_csv(file_obj, **kwargs)

    # Return the DataFrame
    return df
```



## About this class

This guide was prepared by [Ben Welsh](https://palewi.re/who-is-ben-welsh/) and [Katlyn Alo](https://www.linkedin.com/in/katalo/) for [a training session](https://schedules.ire.org/nicar-2025/index.html#2080) at the National Institute for Computer-Assisted Reporting’s 2025 conference in Minnapolis. Some of the copy was written with the assistance of GitHub’s Copilot, an AI-powered text generator. The materials are available as free and [open source on GitHub](https://github.com/palewire/first-athena-query).
