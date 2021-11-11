import boto3

class s3_output_bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3")
        self.response = None
    
    def create_bucket(self):
        print("Creating output bucket...")
        response = self.client.create_bucket(
            Bucket = self.bucket_name
        )
        return response
    
    def delete_bucket(self):
        print("Deleting S3 output bucket...")
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

#Create Bucket for Debugging
if __name__ == "__main__":
    import time
    newbucket = s3_output_bucket("talia-4452-f21-thien-output-bucket")
    newbucket.create_bucket()
    time.sleep(10)
    newbucket.delete_bucket()