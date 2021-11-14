import boto3
import json
import time
import os

def lambda_handler(event, context):
    
    s3_client = boto3.client("s3")
    sns_client = boto3.client("sns")
    bucket_event = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]
    
    #Citation: learned how to read file line-by-line from Stack Overflow
    #Link: https://stackoverflow.com/questions/62699659/reading-file-line-by-line-from-s3-on-lambda-trigger
    for line in s3_client.get_object(Bucket = bucket_event, Key = object_name)["Body"].read().split(b'\n'):
        
        #Sleep for 10 seconds before sending on final line
        if len(str(line).split(",")) == 3:
            print("Sleeping for 10 seconds before sending final line...")
            time.sleep(10)
            print("Sending final line...")
    
        response = sns_client.publish(
            TopicArn = os.environ.get("TOPIC_ARN"),
            Message = str(line)
        )
                
    print("All lines successfully sent to SNS.")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
