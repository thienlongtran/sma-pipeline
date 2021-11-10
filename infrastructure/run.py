import sys
import lambda_upload_handler
import s3_input

S3_INPUT_BUCKET = s3_input.s3_input_bucket("talia-4452-f21-thien-upload-bucket")
LAMBDA_UPLOAD_HANDLER = lambda_upload_handler.lambda_handler("upload-handler")

def create_infrastructure():
    LAMBDA_UPLOAD_HANDLER.create_lambda()
    S3_INPUT_BUCKET.create_bucket()

def destroy_infrastructure():
    LAMBDA_UPLOAD_HANDLER.delete_lambda()
    S3_INPUT_BUCKET.delete_bucket()

if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_infrastructure()
    elif sys.argv[1] == "destroy":
        destroy_infrastructure()