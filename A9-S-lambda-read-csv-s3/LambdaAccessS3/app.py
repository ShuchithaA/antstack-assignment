import boto3
import csv

def lambda_handler(event, context):
  
  s3 = boto3.client('s3', region_name='ap-south-1')
  bucket_name = 's-s3-csv-lambda'
  file_key = 'Sample-Spreadsheet-10-rows.csv' 
   # Check if the file has a .csv extension
  if not file_key.endswith('.csv'):
    return {
        'statusCode': 400,
        'body': 'File is not a CSV file.'
    }
  try:
      response = s3.get_object(Bucket=bucket_name, Key=file_key)
      
      csv_content = response['Body'].read().decode('utf-8',errors="ignore")
      if not csv_content:
        return {
            'statusCode': 400,
            'body': 'File is empty.'
        }
    

      # Use csv.reader to read the CSV content
      reader = csv.reader(csv_content.splitlines())
      for row in reader:
          print(row)

      return {
          'statusCode': 200,
          'body': 'File read successfully.'
      }
  except Exception as e:
     raise e
 
 
 




