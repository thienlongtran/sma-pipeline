import boto3

class s3_input_bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')
    
    def create_bucket(self):
        response = self.client.create_bucket(
            Bucket = self.bucket_name
        )
        print(response)
        return response
    
    def delete_bucket(self):
        self.clear_bucket()
        response =  self.client.delete_bucket(
            Bucket = self.bucket_name
        )
        print(response)
        return response

    #Citation: learned how to clear s3 bucket with boto3 from Stack Overflow
    #Link: https://stackoverflow.com/questions/43326493/what-is-the-fastest-way-to-empty-s3-bucket-using-boto3/43328646
    def clear_bucket(self):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket_name)
        bucket.objects.all().delete()

    def print_bucket_name(self):
        print(self.bucket_name)

newbucket = s3_input_bucket("talia-4452-f21-thien-upload")
newbucket.create_bucket()
newbucket.delete_bucket()