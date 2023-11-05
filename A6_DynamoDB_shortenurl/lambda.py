import traceback
import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')

table_name = 's_url_shortener'
table = dynamodb.Table(table_name)

document_client = boto3.client('dynamodb', region_name='ap-south-1')

def generate_short_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def urlToshort_id(original_url, full_api_gateway_url):
    global short_id
    try:
        # Check if the original_url already exists in the GSI
        response = document_client.query(
            TableName=table_name,
            IndexName='original_url-index',
            KeyConditionExpression="original_url = :s",
            ExpressionAttributeValues={":s": {"S": original_url}}
        )

        if "Items" in response and isinstance(response["Items"], list) and len(response["Items"]) > 0:
            item = response["Items"][0]
            short_id = item["short_id"]["S"]
            short_url = f"{full_api_gateway_url}/{short_id}"  # Append short ID to URL path
    
            response_data = {
                'short_id': short_id,
                'short_url': short_url
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response_data)
            }

        # URL does not exist, generate a new short ID
        else:
            short_id = generate_short_id()
            short_url = f"{full_api_gateway_url}/{short_id}"  # Append short ID to URL path

            item = {
                'short_id':  {"S": short_id},
                'original_url': {"S": original_url}
            }

            document_client.put_item(TableName=table_name, Item=item)

            response_data = {
                'short_id': short_id,
                'short_url': short_url
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response_data)
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def short_idtourl(short_id,op):
    print("short id", short_id)
    print("op",op)
    if short_id is not None:
        try:
            response = document_client.query(
                TableName=table_name,
                KeyConditionExpression="short_id = :s",
                ExpressionAttributeValues={":s": {"S": short_id}}
            )
            print("response", response)

            if "Items" in response and isinstance(response["Items"], list) and len(response["Items"]) > 0:
                item = response["Items"][0]
                original_url = item["original_url"]["S"]
                # print("original_url", original_url)
                
                if op=='a':

                    return{
                        'statusCode':200,
                        'body': json.dumps(original_url)
                    }

                elif op=='b' :
                    return {
                        'statusCode': 302,
                        'headers': {
                            'Location': original_url
                        }
                    }
                
            else:
                return{
                    'statusCode':404,
                    'body':json.dumps("original URL not found")
                }
                # print("Original URL not found in the response.")
        except Exception as e:
            # Log the error for debugging
            print(f"Error: {e}")
            traceback.print_exc()
            return {
                'statusCode': 500,
                'body': 'Internal server error'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid input'
        }

def lambda_handler(event, context):
    print("event", json.dumps(event))
    print("context",(context))
   
    # Extract the query string directly from the event
    global full_api_gateway_url,op

    stage = event.get('requestContext', {}).get('stage')
    domain_name = event.get('requestContext', {}).get('domainName')
    # Construct the full API Gateway URL with the short ID a s part of the path
    full_api_gateway_url = f"https://{domain_name}/{stage}"
   
    param=event.get('queryStringParameters',{})
    if param:
        print("query")
        url=param.get('url',{})
        short_id=param.get('short_id',{})
        
        if url:
            
            return urlToshort_id(url,full_api_gateway_url)
        elif short_id:
            
            print("short id", short_id)
            return short_idtourl(short_id,op='a')
        else:
            print("redirection")
            path_parameters = event.get('pathParameters', {})
            short_id = path_parameters.get('proxy')
            if short_id:
              print("short id",short_id)
              return short_idtourl(short_id,op='b')
            else:
              return{
                  'statusCode': 400,
                  'body': 'Invalid input'
              }













   
  
    
    
