import boto3
import os

# fetch credentials from env variablesenv
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# setup a AWS S3 client/resource
s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

# point the resource at the existing bucket
bucket = s3.Bucket('anyoneai-datasets')

# download the labels
for dirpath in os.listdir("/home/matias/Anyone/Final-Project/Data"):
    with open(f'{dirpath}.txt', 'wb') as data:
        bucket.download_fileobj(f'shot-type/annotation/{dirpath}.json', data)