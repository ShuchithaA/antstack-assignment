1. store dataset in s3
2. check if dataset is loaded into ddb
3. if not loaded inject data into dynamodb and then query
3. else query through ddb 
4. generate report of hourly paid people and caluculate how much money they made anually
4. deploy api to trigger lambda to download report