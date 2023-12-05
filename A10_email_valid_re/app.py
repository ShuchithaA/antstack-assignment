import re

def lambda_handler(event, context):
   email = event['email']
   email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
   # regex split email in four parts to check validity
   # recipient name, @ ,domain, top level domain
   
   if re.match(email_regex, email):
       return {
           'statusCode': 200,
           'body': 'Email is valid.'
       }
   else:
       return {
           'statusCode': 400,
           'body': 'Email is not valid.'
       }
