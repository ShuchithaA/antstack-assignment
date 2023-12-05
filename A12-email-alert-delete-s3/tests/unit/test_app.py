import pytest
from unittest.mock import patch, MagicMock
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, "..", "S3EventListener")
sys.path.append(app_dir)

import S3EventListener.app

@patch('S3EventListener.app.os.getenv')
@patch('S3EventListener.app.boto3.client')
def test_lambda_handler(mock_boto3_client, mock_getenv):
  # Mock the environment variables
  mock_getenv.side_effect = ['ap-south-1', 'sender@example.com', 'recipient@example.com']

  # Mock the SES client
  mock_ses_client = MagicMock()
  mock_boto3_client.return_value = mock_ses_client

  # Mock the event
  event = {
      'Records': [
          {
              'eventName': 'ObjectRemoved:Delete',
              's3': {
                'bucket': {'name': 'my-bucket'},
                'object': {'key': 'my-object'}
              }
          }
      ]
  }

  # Call the lambda handler
  S3EventListener.app.lambda_handler(event, {})

  # Assert that the send_email method was called with the correct arguments
  mock_ses_client.send_email.assert_called_once_with(
      Source='sender@example.com',
      Destination={'ToAddresses': ['recipient@example.com']},
      Message={
          'Subject': {'Data': 'File Deleted: my-object'},
          'Body': {'Text': {'Data': 'A file was deleted from the bucket my-bucket. The deleted file was my-object.'}}
      }
  )
