import requests
import boto3
from io import StringIO
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
S3_BUCKET = "first-athena-query"
S3_PREFIX = "raw-data-filtered-columns"
AWS_REGION = "us-east-2"

# API Configuration
API_ENDPOINT = "https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/csv"
YEARS = [2018, 2019, 2020, 2021, 2022]
LOAN_PURPOSES = [1, 2, 31, 32, 4, 5]

SELECTED_COLUMNS = [
    "activity_year",
    "lei",
    "state_code",
    "county_code",
    "census_tract",
    "derived_loan_product_type",
    "derived_dwelling_category",
    "derived_ethnicity",
    "derived_race",
    "derived_sex",
    "action_taken",
    "purchaser_type",
    "preapproval",
    "loan_type",
    "loan_purpose",
    "lien_status",
    "reverse_mortgage",
    "open-end_line_of_credit",
    "business_or_commercial_purpose",
    "loan_amount property_value  income",
    "debt_to_income_ratio",
    "applicant_credit_score_type",
]

# Initialize S3 Client
s3_client = boto3.client(
    "s3", 
    region_name=AWS_REGION,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY")
)

def file_exists_in_s3(file_path):
    """
    Accepts an S3 file key ("path", e.g. "raw-data/some-file.json") and checks if the file exists in the S3 bucket.
    """
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=f"{file_path}")
        return True
    
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise

def fetch_data(params):
    """
    Fetches CSV data from the HMDA API using the provided year and loan purpose parameters.
    Note: as of writing, this HMDA endpoint only accepts a min of 1 param, maximum of 2 — despite how large these files are.
    """
    print(f"Fetching data for {params["years"]}: loan purpose {params["loan_purposes"]}")
    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()
    return response.text

def filter_csv_data_in_chunks(csv_data):
    """
    Processes large CSV data in chunks, keeping only selected columns.
    Returns the filtered CSV as a string.
    """
    csv_buffer = StringIO(csv_data)
    output_buffer = StringIO()

    first_chunk = True  # Used to write headers only once

    # Process in chunks
    chunk_iter = pd.read_csv(csv_buffer, dtype=str, chunksize=100000)  # Adjust chunk size as needed

    for chunk in chunk_iter:
        # Get only the columns that exist in this chunk
        available_columns = [col for col in SELECTED_COLUMNS if col in chunk.columns]
        
        if available_columns:  # Only process if at least one desired column exists
            filtered_chunk = chunk[available_columns]
            filtered_chunk.to_csv(output_buffer, index=False, header=first_chunk, mode="a")
            first_chunk = False  # Ensure header is only written once

    return output_buffer.getvalue()

def upload_to_s3(csv_data, filename, year):
    """
    Uploads data as CSV to S3 bucket. Path is determined by the year and loan purpose, e.g. "raw-data/2021/hmda_data_loan_purpose_1.csv"
    """
    filtered_csv_data = filter_csv_data_in_chunks(csv_data)  # Filter large CSV in chunks
    
    csv_buffer = StringIO(filtered_csv_data)
    s3_client.put_object(Bucket=S3_BUCKET, Key=f"{S3_PREFIX}/{year}/{filename}", Body=csv_buffer.getvalue())
    print(f"Uploaded {year} {filename} to S3")

# Iterate through parameters and process API responses
for year in YEARS:
    for loan_purpose in LOAN_PURPOSES:
        params = {
            "years": year,
            "loan_purposes": loan_purpose,
        }

        filename = f"hmda_data_loan_purpose_{loan_purpose}.csv"
        file_path = f"{S3_PREFIX}/{year}/{filename}"

        # This is a just-in-case measure because these files are so big that there's a decent chance there'll
        # be a disruption in the middle of fetching them, and we'll have to start again. This way we can skip
        # files that have already been fetched.
        if file_exists_in_s3(file_path):
            print(f"File {file_path} already exists in S3. Skipping...")
            continue

        try:
            csv_data = fetch_data(params)
            upload_to_s3(csv_data, filename, year)
        except Exception as e:
            print(f"Error processing params {params}: {e}")
