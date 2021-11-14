import sys
import lambda_upload_handler
import s3_input
import sns_sync
import lambda_moving_avg_handler
import s3_output
import dynamodb_stock_data

PREFIX = "rita"
S3_INPUT_BUCKET = s3_input.s3_input_bucket(PREFIX + "-4452-f21-thien-upload")
LAMBDA_UPLOAD_HANDLER = lambda_upload_handler.lambda_handler(PREFIX + "-4452-f21-thien-upload-handler")
SNS_MIDDLE_MAN = sns_sync.sns_sync(PREFIX + "-4452-f21-thien-sns-sync")
LAMBDA_MOVING_AVG_HANDLER = lambda_moving_avg_handler.lambda_handler(PREFIX + "-4452-f21-thien-moving-avg-handler")
DYNAMODB_STOCK_DATA = dynamodb_stock_data.dynamodb_stock_data(PREFIX + "-4452-f21-thien-stock-data")
S3_OUTPUT_BUCKET = s3_output.s3_output_bucket(PREFIX + "-4452-f21-thien-results")

def create_infrastructure():
    S3_INPUT_BUCKET.create_bucket()
    LAMBDA_UPLOAD_HANDLER.create_lambda()
    LAMBDA_UPLOAD_HANDLER.add_s3_permission()
    S3_INPUT_BUCKET.add_lambda_trigger(LAMBDA_UPLOAD_HANDLER.response["FunctionArn"])
    SNS_MIDDLE_MAN.create_topic()
    LAMBDA_UPLOAD_HANDLER.add_sns_environment_variable(SNS_MIDDLE_MAN.get_topic_arn())
    LAMBDA_MOVING_AVG_HANDLER.create_lambda()
    LAMBDA_MOVING_AVG_HANDLER.add_sns_permission()
    SNS_MIDDLE_MAN.subscribe_lambda(LAMBDA_MOVING_AVG_HANDLER.response["FunctionArn"])
    DYNAMODB_STOCK_DATA.create_table()
    LAMBDA_MOVING_AVG_HANDLER.add_dynamodb_environment_variable(DYNAMODB_STOCK_DATA.response["TableDescription"]["TableName"])
    #TODO: CREATE CONNECTION BETWEEN LAMBDA MOVING AVG HANDLER AND S3 RESULT OUTPUT
    S3_OUTPUT_BUCKET.create_bucket()

def destroy_infrastructure():
    S3_INPUT_BUCKET.delete_bucket()
    LAMBDA_UPLOAD_HANDLER.delete_lambda()
    SNS_MIDDLE_MAN.delete_topic()
    LAMBDA_MOVING_AVG_HANDLER.delete_lambda()
    DYNAMODB_STOCK_DATA.delete_table()
    S3_OUTPUT_BUCKET.delete_bucket()

if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_infrastructure()
    elif sys.argv[1] == "destroy":
        destroy_infrastructure()