import boto3
import os
import argparse
from random import randint

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

def parse_args():
    """
    Use argparse to get amount of videos selected.
    """
    parser = argparse.ArgumentParser(description="Download data.")
    parser.add_argument(
        "amount",
        type=str,
        help="Amount of file to download",
    )

    args = parser.parse_args()

    return args

def download(file):
    name_v = os.path.join("Videos",os.path.split(file.key.replace(".tar",".tgz"))[1])
    name_a = os.path.join("Labels",os.path.split(file.key.replace(".tar",".txt"))[1])
    with open(f'{name_v}', 'wb') as data:
        dir = os.path.split(file.key)[1]
        bucket.download_fileobj(f"shot-type/keyframes/{dir}", data)
    with open(f'{name_a}', 'wb') as data:
        dir = os.path.split(file.key)[1].replace(".tar",".json")
        bucket.download_fileobj(f"shot-type/annotation/{dir}", data)

# download the training dataset
def make_dataset(num:str):
    i = 0
    if num == "all":   
        selection = list(range(1,1101))
    else:
        num = int(num)
        selection = [randint(1,200-num) for n in range(0,num)]
    for file in bucket.objects.filter(Prefix = 'shot-type/keyframes'):
        i += 1
        if i in selection:
            download(file)

if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists("Labels"):
        os.makedirs("Labels")
    if not os.path.exists("Videos"):
        os.makedirs("Videos")
    make_dataset(args.amount)