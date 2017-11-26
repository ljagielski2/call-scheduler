import boto3
import os

client = boto3.client(
    "sns",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-east-1")


def send_sms(phoneNumber, message):
    phoneNumber = '+1' + phoneNumber
    client.publish(
        PhoneNumber=phoneNumber,
        Message=message)
    print('SMS message sent to {}'.format(phoneNumber))
