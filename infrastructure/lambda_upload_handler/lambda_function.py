import boto3
import json

def lambda_handler(event, context):
    
    client = boto3.client("s3")
    bucket_event = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]
    
    #Citation: learned how to read file line-by-line from Stack Overflow
    #Link: https://stackoverflow.com/questions/62699659/reading-file-line-by-line-from-s3-on-lambda-trigger
    for line in client.get_object(Bucket = bucket_event, Key = object_name)["Body"].read().split(b'\n'):
        print(line)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
