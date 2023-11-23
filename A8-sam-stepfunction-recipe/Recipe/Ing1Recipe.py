import json

def lambda_handler(event, context):
    print("event:" ,event)
    output = {
        "ingredient1":"frozen 1tbsp chocolate",
        "time_taken": 5 
    }
    
    output_from_step_1 = {
    "output_from_step_1": output
    }
    
    return {
        'statusCode': 200,  
        'body': output_from_step_1
    }