# Assignment 6

Use DynamoDB,Lambda,API-GW to implement URL Shortening

# DynamoDB Schema
Primary key (partitionkey: short_id (String))
GSI: original_url-index (partitionkey: original_url (String))

# Lambda
Create URL Shortening function
    convert URLs to short URLs and store them on dynamoDB
    Query short url to return original url
    Short urls must have redirection capability (i.e, through API endpoint)

# API-GW

Use GET Method for taking url as query param and returning short id and short url
Use GET method for taking short_id as query param and returning original_url
add a proxy route for redirecting short url




