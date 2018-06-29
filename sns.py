import os

import boto3


CLIENT = boto3.client(
    "sns",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-east-1")


def send_sms(phone_number, message):
    phone_number = '+1' + phone_number

    CLIENT.publish(
        PhoneNumber=phone_number,
        Message=message)
    print('SMS message sent to {}'.format(phone_number))
