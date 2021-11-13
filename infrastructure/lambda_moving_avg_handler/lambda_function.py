import boto3
import json
import re

def lambda_handler(event, context):
    message = event["Records"][0]["Sns"]["Message"]
    clean_message = message.split("b'")[1].split("\\r'")[0]
    message_array = clean_message.split(",")
    
    print("Message: " + clean_message)
    print(message_array)
    print("Message length: " + str(len(message_array)))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
