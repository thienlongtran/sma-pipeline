import sys
from infrastructure import lambda_upload_handler
from infrastructure import s3_input
from infrastructure import sns_sync
from infrastructure import lambda_moving_avg_handler
from infrastructure import s3_output
from infrastructure import dynamodb_stock_data

class aws_project_infrastructure:
    def __init__(self, prefix):
        self.PREFIX = prefix
        self.S3_INPUT_BUCKET = s3_input.s3_input_bucket(self.PREFIX + "-4452-f21-thien-upload")
        self.LAMBDA_UPLOAD_HANDLER = lambda_upload_handler.lambda_handler(self.PREFIX + "-4452-f21-thien-upload-handler")
        self.SNS_MIDDLE_MAN = sns_sync.sns_sync(self.PREFIX + "-4452-f21-thien-sns-sync")
        self.LAMBDA_MOVING_AVG_HANDLER = lambda_moving_avg_handler.lambda_handler(self.PREFIX + "-4452-f21-thien-moving-avg-handler")
        self.DYNAMODB_STOCK_DATA = dynamodb_stock_data.dynamodb_stock_data(self.PREFIX + "-4452-f21-thien-stock-data")
        self.S3_OUTPUT_BUCKET = s3_output.s3_output_bucket(self.PREFIX + "-4452-f21-thien-results")

    def create_infrastructure(self):
        """
        Setup the AWS services and resources
        """
        self.S3_INPUT_BUCKET.create_bucket()
        self.LAMBDA_UPLOAD_HANDLER.create_lambda()
        self.LAMBDA_UPLOAD_HANDLER.add_s3_permission()
        self.S3_INPUT_BUCKET.add_lambda_trigger(self.LAMBDA_UPLOAD_HANDLER.response["FunctionArn"])
        self.SNS_MIDDLE_MAN.create_topic()
        self.LAMBDA_UPLOAD_HANDLER.add_sns_environment_variable(self.SNS_MIDDLE_MAN.get_topic_arn())
        self.LAMBDA_MOVING_AVG_HANDLER.create_lambda()
        self.LAMBDA_MOVING_AVG_HANDLER.add_sns_permission()
        self.SNS_MIDDLE_MAN.subscribe_lambda(self.LAMBDA_MOVING_AVG_HANDLER.response["FunctionArn"])
        self.DYNAMODB_STOCK_DATA.create_table()
        self.S3_OUTPUT_BUCKET.create_bucket()
        self.LAMBDA_MOVING_AVG_HANDLER.add_environment_variable(
            self.DYNAMODB_STOCK_DATA.table_name,
            self.S3_OUTPUT_BUCKET.bucket_name
            )

    def destroy_infrastructure(self):
        """
        Cleanup the AWS services and resources
        """
        self.S3_INPUT_BUCKET.delete_bucket()
        self.LAMBDA_UPLOAD_HANDLER.delete_lambda()
        self.SNS_MIDDLE_MAN.delete_topic()
        self.LAMBDA_MOVING_AVG_HANDLER.delete_lambda()
        self.DYNAMODB_STOCK_DATA.delete_table()
        self.S3_OUTPUT_BUCKET.delete_bucket()

if __name__ == "__main__":

    #Setup Prefix
    prefix = str(input("Enter prefix: "))
    if len(prefix) > 0:
        pass
    else:
        #Default Prefix
        prefix = "kara"

    #Setup Base
    aws_base_infrastructure = aws_project_infrastructure(prefix)

    #Setup Infrastructure
    if sys.argv[1] == "create":
        aws_base_infrastructure.create_infrastructure()
    elif sys.argv[1] == "destroy":
        aws_base_infrastructure.destroy_infrastructure()
    else:
        print("Error: parameter must be either 'create' or 'destroy'")
        exit()