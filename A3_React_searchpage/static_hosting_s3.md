#create bucket on s3
#upload files
#set bucket permissions

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::assign3-react-search-page/*"
        }
    ]
}

#configure static hosting on S3
