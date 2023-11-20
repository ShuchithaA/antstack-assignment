import json
import traceback
import boto3
import string
import random
pipeline = boto3.client('codepipeline')

dynamodb = boto3.resource('dynamodb')

table_name = 's_url_shortener'
table = dynamodb.Table(table_name)

document_client = boto3.client('dynamodb', region_name='ap-south-1')

def generateShortID():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def urlToShortID(OriginalURL, full_api_gateway_url):
    global ShortID
    try:
        # Check if the OriginalURL already exists in the GSI
        response = document_client.query(
            TableName=table_name,
            IndexName='OriginalURLIndex',
            KeyConditionExpression="OriginalURL = :s",
            ExpressionAttributeValues={":s": {"S": OriginalURL}}
        )

        if "Items" in response and isinstance(response["Items"], list) and len(response["Items"]) > 0:
            item = response["Items"][0]
            ShortID = item["ShortID"]["S"]
            ShortURL = f"{full_api_gateway_url}/{ShortID}"  # Append short ID to URL path
    
            response_data = {
                'ShortID': ShortID,
                'ShortURL': ShortURL
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response_data)
            }

        # URL does not exist, generate a new short ID
        else:
            ShortID = generateShortID()
            ShortURL = f"{full_api_gateway_url}/{ShortID}"  # Append short ID to URL path

            item = {
                'ShortID':  {"S": ShortID},
                'OriginalURL': {"S": OriginalURL}
            }

            document_client.put_item(TableName=table_name, Item=item)

            response_data = {
                'ShortID': ShortID,
                'ShortURL': ShortURL
            }
            return {
                'statusCode': 200,
                'body': json.dumps(response_data)
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
def ShortIDredirect(ShortID):
    if ShortID is not None:
        try:
            response = document_client.query(
                TableName=table_name,
                KeyConditionExpression="ShortID = :s",
                ExpressionAttributeValues={":s": {"S": ShortID}}
            )
            print("response", response)

            if "Items" in response and isinstance(response["Items"], list) and len(response["Items"]) > 0:
                item = response["Items"][0]
                OriginalURL = item["OriginalURL"]["S"]
                # print("OriginalURL", OriginalURL)
                return {
                    'statusCode': 302,
                    'headers': {
                        'Location': OriginalURL
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
    url=param.get('url',{})

    if url:
        
        return urlToShortID(url,full_api_gateway_url)
    
    else:
        path_parameters = event.get("pathParameters", {})
        if path_parameters:
            ShortID = path_parameters.get("proxy",None)
            if ShortID:
                return ShortIDredirect(ShortID)
            else:
                return{
                'statusCode': 400,
                'body': 'Invalid input'
            }
    response = pipeline.put_job_success_result(
       jobId=event['CodePipeline.job']['id']
   )
    return response
