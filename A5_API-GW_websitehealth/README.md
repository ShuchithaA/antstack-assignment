# Assignment 5
For website health lambda executed on Assignment 2,
        
    checks health of website every one hour

    Cron expression: 0 * * * ? *

    Attach ROLE with 2 POLICIES:

    1. AWSLambdaBasicExecutionRole
    2. Lambda invocation (user-defined)

Add API-GW trigger to send requests via endpoint for website health check
Include following configurations in API-GW

    Query string parameter: to take website url as input
    HTTP request headers: to pass metadata
    API key: Authentication
        create api key and attach it to a usage plan
        attach the usage plan to your api endpoint in method request
        x-api-key include in header of request
    Authorizer: Using Lambda function for authentication
        include authorizationToken in header

    request body against a model: tryout for future use case...

