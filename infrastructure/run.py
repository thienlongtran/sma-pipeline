import sys
import lambda_upload_handler
import s3_input
import sns_middle_man

S3_INPUT_BUCKET = s3_input.s3_input_bucket("talia-4452-f21-thien-upload-bucket")
LAMBDA_UPLOAD_HANDLER = lambda_upload_handler.lambda_handler("upload-handler")
SNS_MIDDLE_MAN = sns_middle_man.s3_input_topic("stock-middle-man")

def create_infrastructure():
    LAMBDA_UPLOAD_HANDLER.create_lambda()
    S3_INPUT_BUCKET.create_bucket()
    LAMBDA_UPLOAD_HANDLER.add_s3_permission()
    S3_INPUT_BUCKET.add_lambda_trigger(LAMBDA_UPLOAD_HANDLER.response["FunctionArn"])
    SNS_MIDDLE_MAN.create_topic()


def destroy_infrastructure():
    LAMBDA_UPLOAD_HANDLER.delete_lambda()
    S3_INPUT_BUCKET.delete_bucket()
    SNS_MIDDLE_MAN.delete_topic()

if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_infrastructure()
    elif sys.argv[1] == "destroy":
        destroy_infrastructure()