def lambda_handler(event,context):
    print("event",event)
    if event['authorizationToken'] == 'abc123':
        auth = 'Allow'
    else:
        auth = 'Deny'
        
    if auth=='Allow':
        
        return generate_policy("user", "Allow", event['methodArn'])
        print("methodarn;", event['methodArn'])
    else:
        return generate_policy("user", "Deny", event['methodArn'])
        
        
def generate_policy(principal_id, effect, resource):
    policy = {
        "principalId": principal_id,  # Use the provided principal_id #generated for user #unique
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        },
        "context": {}  # Added a comma to separate context from policyDocument
    }
    print("policy", policy)
    return policy

