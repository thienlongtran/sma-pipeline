import boto3
import json
import time

def lambda_handler(event, context):
    message = event["Records"][0]["Sns"]["Message"]
    clean_message = message.split("b'")[1].split("\\r'")[0]
    message_array = clean_message.split(",")
    message_length = len(message_array)
    
    #Ending Line
    if message_length == 3:
        time.sleep(10)
        print("EOF")
        print("Message length: " + str(message_length))
        print(message_array)
        
    #Regular Data Line
    elif message_length == 10:
        print("Message length: " + str(message_length))
        print(message_array)
        

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
