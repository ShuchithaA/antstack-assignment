Initialize SES client with the region specified in the environment variable 'REGION'
Get the sender and recipient email addresses from the environment variables 'SENDER_EMAIL' and 'RECIPIENT_EMAIL'
Define the main function 'lambda_handler' that takes 'event' and 'context' as parameters
   For each record in the 'event' records:
    Check if the event name is 'ObjectRemoved:Delete'
    If it is, get the bucket name and object key from the record
    Construct the subject and body of the email
    Send the email using the SES client
       1. If the email is sent successfully, print the message ID of the email
       2. If there is an error, print the error message
