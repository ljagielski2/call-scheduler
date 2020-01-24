import os

import boto3

from cs import CONFIG


CLIENT = boto3.client(
    "sns",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-east-1")


def send_sms(phone_number, message):
    phone_number = '+1' + phone_number

    if bool(CONFIG['SMS']):
        CLIENT.publish(
            PhoneNumber=phone_number,
            Message=message)
        print('SMS message sent to {}'.format(phone_number))
    else:
        print('SMS disabled in dev environment')
