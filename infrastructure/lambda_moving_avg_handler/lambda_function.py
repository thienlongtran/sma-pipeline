import boto3
import json
import time
import os

def wait_until_table_unactive(dynamodb_client):
    """
    Waits until the table is no longer writing any messages to ensure data integrity
    """
    while True:
        response = dynamodb_client.describe_table(
            TableName = os.environ.get("DYNAMODB_NAME")
        )
        
        if response["Table"]["TableStatus"] == "UPDATING":
            print("Table updating, waiting 5 seconds...")
            time.sleep(5)
        else:
            print("Table done updating...")
            break

def lambda_handler(event, context):
    """
    Reads message from SNS and processes the information to get Simple Moving Average

    Cases:
        message_length == 10: message gives the stock data - add to DynamoDB
        message_length == 3: message gives the type to Simple Moving Average to calculate - calculate SMA from parameters
    """
    message = event["Records"][0]["Sns"]["Message"]
    clean_message = message.split("b'")[1].split("\\r'")[0].replace(".US", "")
    message_array = clean_message.split(",")
    message_length = len(message_array)
    dynamodb_client = boto3.client("dynamodb")
    
    #DynamoDB Approach
    #--------------------------------------------------------#
    #Data Line
    if message_length == 10:
        response = dynamodb_client.put_item(
            TableName = os.environ.get("DYNAMODB_NAME"),
            Item = {
                "Ticker": {"S":message_array[0]},
                "Per": {"N":message_array[1]},
                "Date": {"N":message_array[2]},
                "Time": {"N":message_array[3]},
                "Date_Time": {"S":message_array[2] + "_" + message_array[3]},
                "Open": {"N":message_array[4]},
                "High": {"N":message_array[5]},
                "Low": {"N":message_array[6]},
                "Close": {"N":message_array[7]},
                "Vol": {"N":message_array[8]},
                "Openint":{"N":message_array[9]}
            }
        )
    
    #Ending Line
    elif message_length == 3:
        clean_message = clean_message.replace("<", "").replace(">", "")
        message_array = clean_message.split(",")
        
        wait_until_table_unactive(dynamodb_client)
        
        query = dynamodb_client.query(
            TableName = os.environ.get("DYNAMODB_NAME"),
            KeyConditionExpression = "Ticker = :ticker_name",
            ExpressionAttributeValues={
                ":ticker_name": {"S": message_array[0]}
            }
        )
        
        #Variables
        output = "<TICKER>,<PER>,<AVG_TYPE>,<QUOTE>,<DATE>,<TIME>,<AVG>,<VOL>\n"
        ticker_name = message_array[0]
        per = str(query["Items"][0]["Per"]["N"])
        avg_type = "SMA" + str(message_array[1])
        quote = message_array[2].replace("'", "")
        ma_period = int(message_array[1])
        
        #Setup Sum and Volume Array
        money_sum_array = [0] * query["Count"]
        vol_sum_array = [0] * query["Count"]
        
        for i in range(ma_period):
            money_sum_array[ma_period] += float(query["Items"][i][quote.title()]["N"])
            vol_sum_array[ma_period] += int(query["Items"][i]["Vol"]["N"])
            
        #Calculate Moving Average
        for i in range(ma_period, len(query["Items"])):
            output += "{TICKER},{PER},{AVG_TYPE},{QUOTE},{DATE},{TIME},{AVG},{VOL}\n".format(
                TICKER = ticker_name,
                PER = per,
                AVG_TYPE = avg_type,
                QUOTE = quote,
                DATE = str(query["Items"][i]["Date"]["N"]),
                TIME = str(query["Items"][i]["Time"]["N"]),
                AVG = "{:.2f}".format(money_sum_array[i] / ma_period),
                VOL = str(int(vol_sum_array[i] / ma_period))
            )
            
            #Dynamic Programming approach to storing sums
            if i < len(query["Items"])-1:
                money_sum_array[i+1] = money_sum_array[i] - float(query["Items"][i-ma_period][quote.title()]["N"]) + float(query["Items"][i][quote.title()]["N"])
                vol_sum_array[i+1] = vol_sum_array[i] - float(query["Items"][i-ma_period]["Vol"]["N"]) + float(query["Items"][i]["Vol"]["N"])
        
        #Write output to temporary file and send file to S3
        TEMP_PATH = "/tmp/"
        out = open(TEMP_PATH + ticker_name + "-" + avg_type + ".csv", "a")
        out.write(output)
        out.close()
        
        s3_client = boto3.client("s3")
        response = s3_client.put_object(
            Body = (open(TEMP_PATH + ticker_name + "-" + avg_type + ".csv", "rb")),
            Bucket = os.environ.get("BUCKET_NAME"),
            Key = (ticker_name + "-" + avg_type + ".csv")
        )
        
        print(response)
        
    #--------------------------------------------------------#
    
    
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
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda Moving Average Handler!")
    }