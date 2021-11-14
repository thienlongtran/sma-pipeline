import boto3
import json
import time
import os

def lambda_handler(event, context):
    message = event["Records"][0]["Sns"]["Message"]
    clean_message = message.split("b'")[1].split("\\r'")[0]
    message_array = clean_message.split(",")
    message_length = len(message_array)
    dynamodb_client = boto3.client("dynamodb")
    
    #DynamoDB Approach
    if message_length == 10:
        print("Writing to DynamoDB...")
        response = dynamodb_client.put_item(
            TableName = "kara-4452-f21-thien-stock-data",
            Item = {
                "Ticker": {"S":message_array[0]},
                "Per": {"N":message_array[1]},
                "Date": {"N":message_array[2]},
                "Time": {"N":message_array[3]},
                "Open": {"N":message_array[4]},
                "High": {"N":message_array[5]},
                "Low": {"N":message_array[6]},
                "Close": {"N":message_array[7]},
                "Vol": {"N":message_array[8]},
                "Openint":{"N":message_array[9]}
            }
        )
        print(response)
    
    #Global Variable Approach
    """
    global TEST_MESSAGE
    
    #Regular Data Line
    if message_length == 10:
        TEST_MESSAGE = TEST_MESSAGE + str(message_array) + "\n"

    #Ending Line
    elif message_length == 3:
        time.sleep(15)
        print("EOF")
        print("Message length: " + str(message_length))
        print(TEST_MESSAGE)
        TEST_MESSAGE = ""
    """   

    
    
    #Temp Path Approach
    """
    TICKER_NAME = message_array[0]
    #Init Directory
    if not os.path.exists(TEMP_PATH):
        print("Creating temp directory...")
        os.mkdir(TEMP_PATH)
        
    #Init File
    if not os.path.exists(TEMP_PATH +  TICKER_NAME + ".txt"):
        print("Creating text file...")
        open(TEMP_PATH + TICKER_NAME + ".txt", "x")

    out = open(TEMP_PATH + TICKER_NAME + ".txt", "a")
    
    #Regular Data Line
    if message_length == 10:
        print("Writing message to file of length: : " + str(message_length))
        TEST_MESSAGE = TEST_MESSAGE + str(message_array)
        out.write(str(message_array))
        out.close()

    #Ending Line
    elif message_length == 3:
        time.sleep(10)
        print("EOF")
        print("Message length: " + str(message_length))
        
        print(TEST_MESSAGE)
        
        r = open(TEMP_PATH + TICKER_NAME + ".txt", "r")
        for line in r:
            print(line)
        
        print("Removing file...")
        os.remove(TEMP_PATH + TICKER_NAME + ".txt")
        r.close()
        out.close()
    """
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
