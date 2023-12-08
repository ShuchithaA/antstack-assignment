import pandas as pd
from io import StringIO
from boto3.dynamodb.conditions import Key
import boto3
import csv
from decimal import Decimal

def lambda_handler(event, context):
    print("event",event)
    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EmployeeReportGendata')
    control_table = dynamodb.Table('ControlTable')

   # Check if the data has already been loaded
    response_load_data_into_db = control_table.get_item(
       Key={
           'id': 'data_loaded'
       }
    )
    
    if 'Item' not in response_load_data_into_db:
       s3_obj = s3_client.get_object(Bucket='emp-dataset', Key='current-employee-names-salaries-and-position-titles.csv')
       csv_file = s3_obj['Body'].read().decode('utf-8')
    
       df = pd.read_csv(StringIO(csv_file))
       df = df.convert_dtypes()
    
       with table.batch_writer(overwrite_by_pkeys=['Name',]) as batch:
           for index, row in df.iterrows():
               item = row.to_dict()
               for key, value in item.items():
                  if isinstance(value, float):
                      item[key] = Decimal(str(value))
               batch.put_item(Item=item)
    
       # Mark the data as loaded
       control_table.put_item(
           Item={
               'id': 'data_loaded',
               'value': True
           }
       )

    #query the database  
    response_db_query = table.query(
     IndexName='SalaryOrHourlyIndex',
     KeyConditionExpression=Key('SalaryorHourly').eq('Hourly')
    )
    # filter items to include in report
    filtered_items = [
      {
          'Name': item['Name'],
          'Annual Salary': item['Hourly Rate'] * item['Typical Hours'] * 52
      }
      for item in response_db_query['Items']
    ]
    
    # Write the filtered results to a CSV file
    csv_buffer = StringIO()
    df_query_result = pd.DataFrame(filtered_items)
    df_query_result.to_csv(csv_buffer, index=False)
    
    csv_content = csv_buffer.getvalue()
    
    # Return the CSV content as a response
    return {
      'statusCode': 200,
      'headers': {
          'Content-Type': 'text/csv',
          'Content-Disposition': 'attachment; filename=output.csv'
      },
      'body': csv_content
    }