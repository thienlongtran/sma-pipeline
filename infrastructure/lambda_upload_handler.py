import boto3

class lambda_handler:
    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.client = boto3.client("lambda")
        self.response = None
    
    #Citation: learned how to create lambda function with .zip file from Stack Overflow
    #Link: https://stackoverflow.com/questions/63040090/create-aws-lambda-function-using-boto3-python-code
    def create_lambda(self):
        print("Creating Lambda upload handler...")
        self.response = self.client.create_function(
            FunctionName = self.handler_name,
            Runtime = "python3.9",
            Role = "arn:aws:iam::768907305587:role/robomaker_students",
            Handler = "lambda_function.lambda_handler",
            Description = "Parse lines of data from an S3 file trigger and publish to an SNS topic.",
            Timeout = 600,
            Code =  {
                        "ZipFile": open("./infrastructure/lambda_upload_handler/handler_code.zip", "rb").read()
                    }
        )
        return self.response
    
    def delete_lambda(self):
        print("Deleting Lambda upload handler...")
        self.response = self.client.delete_function(
            FunctionName = self.handler_name
        )
        return self.response
    
    #Citation: learned lack of permission as purpose for lambda trigger creation failure from Stack Overflow
    #Link: https://stackoverflow.com/questions/36973134/cant-add-s3-notification-for-lambda-using-boto3
    def add_s3_permission(self):
        print("Adding S3 invoke permission to Lambda upload handler...")
        self.client.add_permission(
            FunctionName = self.handler_name,
            StatementId = "lambda-invoke-func",
            Action = "lambda:InvokeFunction",
            Principal = "s3.amazonaws.com"
        )
    
    def add_sns_environment_variable(self, sns_arn):
        print("Adding SNS ARN environment variable to Lambda upload handler...")
        self.client.update_function_configuration(
            FunctionName = self.handler_name,
            Environment = {
                "Variables": {
                    "TOPIC_ARN": sns_arn
                }
            }
        )

#Create Function for Debugging
if __name__ == "__main__":
    import time
    newlambda = lambda_handler("upload-handler")
    newlambda.create_lambda()
    time.sleep(10)
    newlambda.delete_lambda()