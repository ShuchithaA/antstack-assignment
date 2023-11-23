import json
def lambda_handler(event, context):
   print("event", event)
 
   output_from_step_1 = event['output_from_step_1']
   if output_from_step_1:
   
       output= {
           "ingredient2": "2 tbsp coffee powder",
           "time_taken": 1,
           "output_from_step_1": output_from_step_1 
        
        }
       output_from_step_2 = {
        "output_from_step_2": output
        }
        
       return {
           'statusCode': 200,
           'body': output_from_step_2
       }
   else:
       print("The key 'Payload' or 'body' does not exist in the event dictionary.")
       return {
           'statusCode': 400,
           'body': json.dumps({'error': 'The key "Payload" or "body" does not exist in the event dictionary.'})
       }
    
    

   

    

    
    
    
    
    
    
    
    
    
    
