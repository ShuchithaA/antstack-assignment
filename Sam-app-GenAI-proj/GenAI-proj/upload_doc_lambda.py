import boto3
import requests
import uuid

def lambda_handler(event, context):
  s3_client = boto3.client('s3')
  
  object_name = str(uuid.uuid4()) # Generate a unique object name
  document = event['body']

  # Generate the presigned URL
  response = s3_client.generate_presigned_post(
      Bucket = 'bucket-name',
      Key = object_name,
      ExpiresIn = 10 
  )

  # Upload file to S3 using presigned URL
  files = { 'file': document}
  upload_to_s3 = requests.post(response['url'], data=response['fields'], files=files)
  
  return {
      'statusCode': 200,
      'body': upload_to_s3.status_code
  }
