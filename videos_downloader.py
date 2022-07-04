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

# download the training dataset
i = 0
for file in bucket.objects.filter(Prefix = 'shot-type/keyframes'):
    i += 1
    if i > 32:
        break
    if i > 24:
        name = os.path.split(file.key.replace(".tar",".tgz"))[1]
        with open(f'{name}', 'wb') as data:
            bucket.download_fileobj(file.key, data)
