import boto3

class s3_input_topic:
    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.client = boto3.client("sns")
        self.response = None
    
    def create_topic(self):
        print("Creating input topic...")
        self.response = self.client.create_topic(
            Name = self.topic_name
        )
        return self.response
    
    def delete_topic(self):
        print("Deleting lambda input topic...")

        response = self.client.delete_topic(
            TopicArn = self.get_topic_arn()
        )
        return response
    
    def get_topic_arn(self):
        for topic in self.client.list_topics()["Topics"]:
            if self.topic_name in topic["TopicArn"]:
                return topic["TopicArn"]

    def subscribe_lambda(self, FunctionArn):
        self.client.subscribe(
            TopicArn = self.get_topic_arn(),
            Protocol = "lambda",
            Endpoint = FunctionArn
        )

#Create Topic for Debugging
if __name__ == "__main__":
    import time
    newtopic = s3_input_topic("talia-4452-f21-thien-upload-topic")
    newtopic.create_topic()
    time.sleep(10)
    newtopic.delete_topic()