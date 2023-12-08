import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError

# initialize ses client, get sender n recipient email
ses_client = boto3.client('ses', region_name=os.getenv('REGION'))
s3_client = boto3.client('s3')
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
          try:
              # Generate presigned URL for the image
              image_url = s3_client.generate_presigned_url(
                 'get_object',
                 Params={'Bucket': 'bucket-email-format', 'Key': 'aws_s3.png'},
                 ExpiresIn=3600 # URL expires in 1 hour
              )
          except ClientError as e:
              print(e.response['Error']['Message'])
          body = f"""
             <html>
             <body>
                 <h1>File Deletion Notification</h1>
                 <img src="{image_url}" alt="AWS Image" width="500" height="600">
                 <p>A file was deleted from the bucket <strong>{bucket_name}</strong>. The deleted file was <strong>{object_key}</strong>.</p>
             </body>
             </html>
            """

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
                        'Html': {
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
# pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])
