import boto3

class s3_input_topic:
    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.client = boto3.client("sns")
        self.response = None
    
    def create_topic(self):
        print("Creating input topic...")
        response = self.client.create_topic(
            Name = self.topic_name
        )
        self.TopicArn = (response["TopicArn"])
        return response
    
    def delete_topic(self):
        print("Deleting lambda input topic...")
        target_topic_arn = None

        for topic in self.client.list_topics()["Topics"]:
            if self.topic_name in topic["TopicArn"]:
                target_topic_arn = (topic["TopicArn"])

        response = self.client.delete_topic(
            TopicArn = target_topic_arn
        )

        return self.response

#Create Bucket for Debugging
if __name__ == "__main__":
    import time
    newtopic = s3_input_topic("talia-4452-f21-thien-upload-topic")
    newtopic.create_topic()
    time.sleep(10)
    newtopic.delete_topic()