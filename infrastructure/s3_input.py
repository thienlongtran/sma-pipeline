import boto3

class s3_input_bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3")
        self.response = None
    
    def create_bucket(self):
        print("Creating input bucket...")
        response = self.client.create_bucket(
            Bucket = self.bucket_name
        )
        return response
    
    def delete_bucket(self):
        print("Deleting S3 input bucket...")
        self.clear_bucket()
        self.response =  self.client.delete_bucket(
            Bucket = self.bucket_name
        )
        return self.response

    #Citation: learned how to clear s3 bucket with boto3 from Stack Overflow
    #Link: https://stackoverflow.com/questions/43326493/what-is-the-fastest-way-to-empty-s3-bucket-using-boto3/43328646
    def clear_bucket(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket_name)
        bucket.objects.all().delete()

    def add_lambda_trigger(self, lambda_arn):
        print("Adding S3 as Lambda Trigger...")
        self.response = self.client.put_bucket_notification_configuration(
            Bucket = self.bucket_name,
            NotificationConfiguration= {"LambdaFunctionConfigurations":[
                {
                    "LambdaFunctionArn": lambda_arn,
                    "Events": ["s3:ObjectCreated:Put"]
                }
            ]}
        )

    def print_bucket_name(self):
        print(self.bucket_name)

#Create Bucket for Debugging
if __name__ == "__main__":
    import time
    newbucket = s3_input_bucket("talia-4452-f21-thien-upload-bucket")
    newbucket.create_bucket()
    time.sleep(10)
    newbucket.delete_bucket()