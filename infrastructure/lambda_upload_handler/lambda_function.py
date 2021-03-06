import boto3
import json
import time
import os

s3_client = boto3.client("s3")
sns_client = boto3.client("sns")
    
def publish_message(message):
    """
    Publishes message to target SNS
    """
    sns_client.publish(
        TopicArn = os.environ.get("TOPIC_ARN"),
        Message = message
    )
    
def lambda_handler(event, context):
    """
    Reads the S3 file triggering the event and sends to target SNS line-by-line
    """
    bucket_event = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]
    text_file = s3_client.get_object(Bucket = bucket_event, Key = object_name)["Body"].read().split(b'\n')
        
    for i in range(1, len(text_file)-1):
        publish_message(str(text_file[i]))
    
    #Delay sending of final message
    print("Sleeping for 20 seconds before sending final line...")
    time.sleep(20)
    print("Sending final line...")
    publish_message(str(text_file[len(text_file)-1]))
    print("All lines successfully sent to SNS.")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }