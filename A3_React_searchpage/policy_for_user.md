# create a usr with attaching a policy to have access for S3 and lambda
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:*",
                "s3:*"
            ],
            "Resource": "*"
        }
    ]
}