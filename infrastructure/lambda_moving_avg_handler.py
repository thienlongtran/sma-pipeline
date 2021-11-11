import boto3

class lambda_handler:
    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.client = boto3.client("lambda")
        self.response = None
    
    def create_lambda(self):
        print("Creating Lambda upload handler...")
        self.response = self.client.create_function(
            FunctionName = self.handler_name,
            Runtime = "python3.9",
            Role = "arn:aws:iam::768907305587:role/lambda-s3-role",
            Handler = "lambda_function.lambda_handler",
            Code =  {
                        "ZipFile": open("./lambda_upload_handler/handler_code.zip", "rb").read()
                    }
        )
        return self.response
    
    def delete_lambda(self):
        print("Deleting Lambda upload handler...")
        self.response = self.client.delete_function(
            FunctionName = self.handler_name
        )
        return self.response
    
    def add_s3_permission(self):
        print("Adding S3 invoke permission to Lambda...")
        self.client.add_permission(
                                    FunctionName = self.handler_name,
                                    StatementId = "lambda-invoke-func",
                                    Action = "lambda:InvokeFunction",
                                    Principal = "s3.amazonaws.com"
                                  )

#Create Function for Debugging
if __name__ == "__main__":
    import time
    newlambda = lambda_handler("moving-avg-handler")
    newlambda.create_lambda()
    time.sleep(10)
    newlambda.delete_lambda()