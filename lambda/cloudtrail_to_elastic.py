"""
Lambda Function: CloudTrail to Elasticsearch
Triggered by S3 ObjectCreated events.
Parses CloudTrail logs and sends them to Elasticsearch.
"""

import json
import gzip
import os
import boto3
import urllib.request

s3 = boto3.client("s3")

ES_ENDPOINT = os.environ["ES_ENDPOINT"] ES_API_KEY = os.environ["ES_API_KEY"] ES_INDEX = os.environ.get("ES_INDEX", "cloudtrail-logs")

def send_to_elasticsearch(document):
    url = f"{ES_ENDPOINT}/{ES_INDEX}/_doc"
    data = json.dumps(document).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"ApiKey {ES_API_KEY}"
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            response.read()
    except Exception as e:
        print(f"Failed to index document: {e}")
        raise


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        print(f"Processing file: s3://{bucket}/{key}")

        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"]

        with gzip.GzipFile(fileobj=body) as gz:
            file_content = gz.read().decode("utf-8")

        cloudtrail_json = json.loads(file_content)

        for event_record in cloudtrail_json.get("Records", []):
            send_to_elasticsearch(event_record)

    return {
        "statusCode": 200,
        "body": "CloudTrail logs indexed successfully"
    }
