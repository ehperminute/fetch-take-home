import boto3
import os
import json
from config import ENDPOINT_URL, REGION, QUEUE_URL


# Set up environment variables for dummy AWS credentials
os.environ["AWS_ACCESS_KEY_ID"] = "access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "secret_key"

# Initialize SQS client with the local endpoint and a region
sqs = boto3.client("sqs", endpoint_url=ENDPOINT_URL,
                   region_name=REGION)


def poll():
    return 'Messages' in sqs.receive_message(QueueUrl=QUEUE_URL)

def sqs_get_messages(max_messages = 10):
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=max_messages
    )
    messages = tuple()
    if response.get("Messages"):
        messages = response['Messages']
        #removing messages we obtained from the queue
        for message in response["Messages"]:
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"])
    return messages



def extract_entries():
    messages = sqs_get_messages()
    for msg in messages: print(msg)
    return [json.loads(message['Body']) for message in messages]
