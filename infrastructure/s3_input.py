import boto3

client = boto3.client('s3')

class s3_input_bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
    
    def create_bucket(self):
        response = client.create_bucket(
            Bucket = self.bucket_name
        )
        print(response)
        return response
    
    def delete_bucket(self):
        response =  client.delete_bucket(
            Bucket = self.bucket_name
        )
        print(response)
        return response

    def printBucketName(self):
        print(self.bucket_name)

newbucket = s3_input_bucket("talia-4452-f21-thien-upload")
newbucket.create_bucket()
newbucket.delete_bucket()