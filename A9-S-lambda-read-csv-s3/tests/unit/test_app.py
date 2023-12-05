import os
import sys
import boto3
import pytest
from unittest import mock
from moto import mock_s3


current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, "..", "lambda-access-s3")
sys.path.append(app_dir)

import LambdaAccessS3
from LambdaAccessS3 import app 
from LambdaAccessS3.app import lambda_handler

@pytest.fixture
def s3_client():
   with mock_s3():
       yield boto3.client('s3', region_name='ap-south-1')

@pytest.fixture
def context():
   return object()

def test_lambda_handler(s3_client, context):
   # Create a mock S3 bucket and upload a file
   s3_client.create_bucket(Bucket='s-s3-csv-lambda',CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
   with open("C:\\Users\\Chini\\Downloads\\Sample-Spreadsheet-10-rows.csv", 'rb') as data:
    s3_client.put_object(Bucket='s-s3-csv-lambda', Key='Sample-Spreadsheet-10-rows.csv', Body=data)

   event = {} 
   response = lambda_handler(event, context)

   assert response['statusCode'] == 200
   assert response['body'] == 'File read successfully.'
   
def test_lambda_handler_non_existent_bucket(s3_client, context):
  event = {}
  with pytest.raises(Exception):
      lambda_handler(event, context)

def test_lambda_handler_non_existent_key(s3_client, context):
   s3_client.create_bucket(Bucket='s-s3-csv-lambda', CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
   event = {} 
   with pytest.raises(Exception):
       lambda_handler(event, context)

def test_lambda_handler_non_csv_file(s3_client, context):
  # Create a mock S3 bucket and upload a non-CSV file
  s3_client.create_bucket(Bucket='s-s3-csv-lambda', CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
  with open("C:\\Users\\Chini\\Downloads\\Testing lambda.docx", 'rb') as data:
   s3_client.put_object(Bucket='s-s3-csv-lambda', Key='Testing lambda.docx', Body=data)

  event = {} 
  with pytest.raises(Exception):
      lambda_handler(event, context)
      
def test_lambda_handler_empty_file(s3_client, context):
  # Create a mock S3 bucket and upload an empty file
  s3_client.create_bucket(Bucket='s-s3-csv-lambda', CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
  with open("C:\\Users\\Chini\\Downloads\\Blank-CSV-Template.csv", 'rb') as data:
   s3_client.put_object(Bucket='s-s3-csv-lambda', Key='Blank-CSV-Template.csv', Body=data)

  event = {} 
  with pytest.raises(Exception):
      lambda_handler(event, context)


