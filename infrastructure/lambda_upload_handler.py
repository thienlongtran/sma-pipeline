import boto3

class lambda_handler:
    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.client = boto3.client('lambda')
    
    #Citation: learned how to create lambda function with .zip file from Stack Overflow
    #Link: https://stackoverflow.com/questions/63040090/create-aws-lambda-function-using-boto3-python-code

    def create_lambda(self):
        response = self.client.create_function(
            FunctionName = self.handler_name,
            Runtime = 'python3.9',
            Role = 'arn:aws:iam::768907305587:role/lambda-s3-role',
            Handler = 'lambda_handler',
            Code =  {
                        'ZipFile': open("./lambda_upload_handler/handler_code.zip", "rb").read()
                    }
        )
        print(response)
        return response


newlambda = lambda_handler("upload-handler")
newlambda.create_lambda()