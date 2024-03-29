from .utils import zoho_auth
import os
import boto3
import json
from datetime import datetime
BUCKET = os.environ['BUCKET']


def main(event, context):
    s3 = boto3.client('s3')
    path = 'departments'
    try:
        now = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        result = zoho_auth.main(path)
        response = result['body']['data']

        s3.put_object(
            Body=str(json.dumps(response)),
            Bucket=BUCKET,
            Key=f'{path}/{now}.json'
        )
    except Exception as e:
        return str(e)
