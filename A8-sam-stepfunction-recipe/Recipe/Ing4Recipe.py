import json
def lambda_handler(event, context):
   print("event", event)
   
   output_from_step_2 = event['output_from_step_2']
   if output_from_step_2:
    output= {
     "ingredient 4":"1.5 cup chilled milk, icecubes",
     "time_taken": 5,
     }
     
    output_from_step_4 = {
     "output_from_step_4": output
     }

    
    return {
     'statusCode': 200,
     'body': output_from_step_4
     }
    
    
   else:
       print("The key 'Payload' or 'body' does not exist in the event dictionary.")
       return {
           'statusCode': 400,
           'body': json.dumps({'error': 'The key "Payload" or "body" does not exist in the event dictionary.'})
       }
   
    
        
   