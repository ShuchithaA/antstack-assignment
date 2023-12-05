import pytest
import os
import sys
from unittest.mock import patch

current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, "..", "S3EventListener")
sys.path.append(app_dir)

import S3EventListener
from S3EventListener.app import lambda_handler




@patch('boto3.client')
def test_lambda_handler(mock_boto3_client):
   # Mock the SES client
   mock_ses_client = mock_boto3_client.return_value
   mock_ses_client.send_email.return_value = {
      'MessageId': 'test_message_id',
      'Source': os.getenv('SENDER_EMAIL')
    }

    # Set environment variables
   os.environ['SENDER_EMAIL'] = 'shuchitha.m@antstack.io'
   os.environ['RECIPIENT_EMAIL'] = '1rn19is150.shuchitham@gmail.com'
   # Mock the event and context
   event = {
       'Records': [
           {
           'eventName': 'ObjectRemoved:Delete',
           's3': {
               'bucket': {
                  'name': 'test_bucket'
               },
               'object': {
                  'key': 'test_key'
               }
           }
           }
       ]
   }
   context = {}

   # Call the function
   lambda_handler(event, context)

   # Assert that the send_email method was called with the correct arguments
   mock_ses_client.send_email.assert_called_once_with(
       Source=os.getenv('SENDER_EMAIL'),
       Destination={'ToAddresses': [os.getenv('RECIPIENT_EMAIL')]},
       Message={
           'Subject': {'Data': 'File Deleted: {test_key} '},
           'Body': {'Text': {'Data': 'A file was deleted from the bucket {test_bucket}. The deleted file was {test_key}.'}}
       }
   )
