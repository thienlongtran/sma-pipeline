import boto3

class dynamodb_stock_data:
    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.client("dynamodb")
        self.response = None

    def create_table(self):
        print("Creating DynamoDB table...")
        self.response = self.client.create_table(
            AttributeDefinitions = [
                {
                    "AttributeName": "Ticker",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "Date_Time",
                    "AttributeType": "S"
                }
            ],
            TableName = self.table_name,
            KeySchema = [
                {
                    "AttributeName": "Ticker",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "Date_Time",
                    "KeyType": "RANGE"
                }
            ],
            BillingMode = "PAY_PER_REQUEST"
        )
        return self.response
    
    def delete_table(self):
        print("Deleting DynamoDB table...")
        self.response = self.client.delete_table(
            TableName = self.table_name
        )
        return self.response

#Create Function for Debugging
if __name__ == "__main__":
    import time
    newtable = dynamodb_stock_data("stock-data")
    newtable.create_table()
    time.sleep(10)
    newtable.delete_table()