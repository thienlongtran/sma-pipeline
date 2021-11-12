import boto3
import json

def lambda_handler(event, context):
    
    s3_client = boto3.client("s3")
    bucket_event = event["Records"][0]["s3"]["bucket"]["name"]
    object_name = event["Records"][0]["s3"]["object"]["key"]
    
    sns_client = boto3.client("sns")
    
    #Citation: learned how to read file line-by-line from Stack Overflow
    #Link: https://stackoverflow.com/questions/62699659/reading-file-line-by-line-from-s3-on-lambda-trigger
    for line in s3_client.get_object(Bucket = bucket_event, Key = object_name)["Body"].read().split(b'\n'):
        print(line)
        response = sns_client.publish(
                                     TopicArn = "arn:aws:sns:us-east-1:176966333216:nyssa-4452-f21-thien-sns-sync",
                                     Message = str(line)
                                     )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
