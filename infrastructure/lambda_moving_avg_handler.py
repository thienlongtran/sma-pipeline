import boto3

class lambda_handler:
    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.client = boto3.client("lambda")
        self.response = None
    
    def create_lambda(self):
        print("Creating Lambda moving/rolling average handler...")
        self.response = self.client.create_function(
            FunctionName = self.handler_name,
            Runtime = "python3.9",
            Role = "arn:aws:iam::768907305587:role/robomaker_students",
            Handler = "lambda_function.lambda_handler",
            Description = "Save lines of stock data to a DynamoDB table, and calculate Simple Moving Average at end of file.",
            Timeout = 600,
            Code =  {
                        "ZipFile": open("./infrastructure/lambda_moving_avg_handler/handler_code.zip", "rb").read()
                    }
        )
        return self.response
    
    def delete_lambda(self):
        print("Deleting Lambda moving/rolling average handler...")
        self.response = self.client.delete_function(
            FunctionName = self.handler_name
        )
        return self.response
    
    def add_sns_permission(self):
        print("Adding permission for Lambda moving/rolling average handler to read SNS...")
        self.client.add_permission(
            Action = "lambda:InvokeFunction",
            FunctionName = self.handler_name,
            Principal = "sns.amazonaws.com",
            StatementId = "sns-invoke-lambda"
        )

    def add_environment_variable(self, dynamodb_name, bucket_name):
        print("Adding S3 & DynamoDB environment variable to Lambda moving/rolling average handler...")
        self.client.update_function_configuration(
            FunctionName = self.handler_name,
            Environment = {
                "Variables": {
                    "DYNAMODB_NAME": dynamodb_name,
                    "BUCKET_NAME": bucket_name
                }
            }
        )

#Create Function for Debugging
if __name__ == "__main__":
    import time
    newlambda = lambda_handler("moving-avg-handler")
    newlambda.create_lambda()
    time.sleep(10)
    newlambda.delete_lambda()