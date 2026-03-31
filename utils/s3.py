import boto3
from datetime import datetime
import json


def upload_to_s3(data):
    s3 = boto3.client('s3')

    bucket_name = 'relx-quotes-scrape'
    file_name = f"reports/report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    json_body = json.dumps(
        data,
        indent=2,              
        ensure_ascii=False 
    )

    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json_body,
        ContentType='application/json'
    )

    print(f"Uploaded to s3://{bucket_name}/{file_name}")