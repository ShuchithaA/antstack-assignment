import json

def lambda_handler(event, context):
   # Extract ingredients and times from the event
   ingredients = [
       event[0]['output_from_step_3']['output_from_step_2_data']['output_from_step_1'].get('ingredient1'),
       event[0]['output_from_step_3']['output_from_step_2_data'].get('ingredient2'),
       event[0]['output_from_step_3'].get('ingredient3'),
       event[1].get('output_from_step_4').get('ingredient 4')
   ]
   times = [
       event[0]['output_from_step_3']['output_from_step_2_data']['output_from_step_1'].get('time_taken', 0),
       event[0]['output_from_step_3']['output_from_step_2_data'].get('time_taken', 0),
       event[0]['output_from_step_3'].get('time_taken', 0),
       event[1].get('output_from_step_4').get('time_taken', 0)
   ]
    
   # Calculate total time
   total_time = times[0] + times[1] + max(times[2], times[3])


   return {
       'ingredients': [ingredient for ingredient in ingredients if ingredient],
       'total_time': f"{total_time} mins"
   }
