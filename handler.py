import boto3
from helpers import instance
from functools import reduce

ec2_client = boto3.client('ec2')
asg_client = boto3.client('asg')


def scan(event, context):
    teste.chama()
