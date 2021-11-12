import sys
import lambda_upload_handler
import s3_input
import sns_middle_man
import lambda_moving_avg_handler
import s3_output

PREFIX = "nyssa"
S3_INPUT_BUCKET = s3_input.s3_input_bucket(PREFIX + "-4452-f21-thien-upload")
LAMBDA_UPLOAD_HANDLER = lambda_upload_handler.lambda_handler(PREFIX + "-4452-f21-upload-handler")
SNS_MIDDLE_MAN = sns_middle_man.s3_input_topic(PREFIX + "-4452-f21-sns-middle-man")
LAMBDA_MOVING_AVG_HANDLER = lambda_moving_avg_handler.lambda_handler(PREFIX + "-4452-f21-moving-avg-handler")
S3_OUTPUT_BUCKET = s3_output.s3_output_bucket(PREFIX + "-4452-f21-thien-results")

def create_infrastructure():
    S3_INPUT_BUCKET.create_bucket()
    LAMBDA_UPLOAD_HANDLER.create_lambda()
    LAMBDA_UPLOAD_HANDLER.add_s3_permission()
    S3_INPUT_BUCKET.add_lambda_trigger(LAMBDA_UPLOAD_HANDLER.response["FunctionArn"])
    SNS_MIDDLE_MAN.create_topic()
    #TODO: CREATE CONNECTION BETWEEN MIDDLE MAN AND MOVING AVG HANDLER
    LAMBDA_MOVING_AVG_HANDLER.create_lambda()
    SNS_MIDDLE_MAN.subscribe_lambda(LAMBDA_MOVING_AVG_HANDLER.response["FunctionArn"])
    LAMBDA_MOVING_AVG_HANDLER.add_sns_trigger(SNS_MIDDLE_MAN.response["TopicArn"])
    #TODO: CREATE CONNECTION BETWEEN LAMBDA MOVING AVG HANDLER AND S3 RESULT OUTPUT
    S3_OUTPUT_BUCKET.create_bucket()

def destroy_infrastructure():
    S3_INPUT_BUCKET.delete_bucket()
    LAMBDA_UPLOAD_HANDLER.delete_lambda()
    SNS_MIDDLE_MAN.delete_topic()
    LAMBDA_MOVING_AVG_HANDLER.delete_lambda()
    S3_OUTPUT_BUCKET.delete_bucket()

if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_infrastructure()
    elif sys.argv[1] == "destroy":
        destroy_infrastructure()