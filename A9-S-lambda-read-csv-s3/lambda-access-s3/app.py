import boto3
import csv

def lambda_handler(event, context):
  
  s3 = boto3.client('s3')
  bucket_name = 's-s3-csv-lambda'
  file_key = 'Sample-Spreadsheet-10-rows.csv' 

  try:
      response = s3.get_object(Bucket=bucket_name, Key=file_key)
      csv_content = response['Body'].read().decode('utf-8',errors="ignore")

      # Use csv.reader to read the CSV content
      reader = csv.reader(csv_content.splitlines())
      for row in reader:
          print(row)

      return {
          'statusCode': 200,
          'body': 'File read successfully.'
      }
  except Exception as e:
      return {
          'statusCode': 500,
          'body': str(e)
      }
