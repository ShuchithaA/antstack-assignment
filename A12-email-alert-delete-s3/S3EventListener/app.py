import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

# initialize ses client, get sender n recipient email
ses_client = boto3.client('ses', region_name=os.getenv('REGION'))
sender = os.getenv('SENDER_EMAIL')
recipient = os.getenv('RECIPIENT_EMAIL')


def lambda_handler(event, context):
   #for each record check for delete  
    for record in event['Records']:
        if record['eventName'] == 'ObjectRemoved:Delete':
           bucket_name = record['s3']['bucket']['name']
           object_key = record['s3']['object']['key']
           #construct email    
           subject = f'File Deleted: {object_key}'
           body = f'A file was deleted from the bucket {bucket_name}. The deleted file was {object_key}.'
           
           try:
               # send mail using ses
               response = ses_client.send_email(
                  Source=sender,
                  Destination={
                      'ToAddresses': [recipient],
                  },
                  Message={
                      'Subject': {
                          'Data': subject,
                      },
                      'Body': {
                          'Text': {
                              'Data': body,
                          }
                      }
                  }
               )
           except ClientError as e:
               print(e.response['Error']['Message'])
           else:
               print("Email sent! Message Id:", response['MessageId'])
# call PutJobSuccessResult
    pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])