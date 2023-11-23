import json
def lambda_handler(event, context):
   print("event", event)
   
   output_from_step_2 = event['output_from_step_2']
   if output_from_step_2:
   # Process input and generate additional output
    output= {
     "ingredient3": "4tbsp powdered sugar",
     "time_taken": 3,
     "output_from_step_2_data": output_from_step_2 
     
     }
    output_from_step_3 = {
     "output_from_step_3": output
     }
     
    
 
    # Return the output to be passed to the next stage in Step Functions
    return {
     'statusCode': 200,
     'body': output_from_step_3
     }
   else:
       print("The key 'Payload' or 'body' does not exist in the event dictionary.")
       return {
           'statusCode': 400,
           'body': json.dumps({'error': 'The key "Payload" or "body" does not exist in the event dictionary.'})
       }
