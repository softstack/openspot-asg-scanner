import boto3
from functools import reduce

client = boto3.client('ec2')


def terminate_instance(instance_id):
    response = client.terminate_instances(
        InstanceIds=[instance_id]
    )

    return response


def is_running(instance):
    return instance['State']['Name'] == 'running'


def is_ondemand(instance):
    return not instance.get('InstanceLifecycle', None)


def get_instances(*ids):
    response = client.describe_instances(
        InstanceIds=ids
    )
    all_instances = reduce(lambda instances, reservation:
                           reservation['Instances'] + instances,
                           response['Reservations'], [])

    return all_instances

