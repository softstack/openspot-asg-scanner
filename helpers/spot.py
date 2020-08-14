import boto3

client = boto3.client('ec2')
INSTANCE_ORIGIN_TAG = 'openspot-instance-origin'


def create_spot_request(instance, instance_type):
    security_groups_ids = [
        security_group['GroupId'] for security_group in instance['SecurityGroups']
    ]

    response = client.request_spot_instances(
       InstanceCount=1,
       LaunchSpecification={
           "ImageId": instance['ImageId'],
           "InstanceType": instance_type,
           "Monitoring": {
               'Enabled': True if instance['Monitoring'] == 'enabled' else False,
           },
           'SecurityGroupIds': security_groups_ids,
           'Placement': {
               'AvailabilityZone': instance['Placement']['AvailabilityZone'],
               'GroupName': instance['Placement']['GroupName'],
               'Tenancy': 'default'
           },
           'SubnetId': instance['SubnetId'],
       },
       InstanceInterruptionBehavior="terminate",
       TagSpecifications=[
           {
               'ResourceType': 'spot-instances-request',
               'Tags': [
                   {
                       'Key': INSTANCE_ORIGIN_TAG,
                       'Value': instance['InstanceId']
                   }
               ]
           }
       ]
    )

    return response


def get_spot_request(origin_instance_id):
    response = client.describe_spot_instance_requests(
        Filters=[
            {
                'Name': f'tag:{INSTANCE_ORIGIN_TAG}',
                'Values': [origin_instance_id]
            }
        ]
    )

    requests = response['SpotInstanceRequests']

    requests = list(filter(
        lambda request: request['State'] == 'active' or request['State'] == 'pending',
        requests
    ))

    return requests[0] if len(requests) else None


def cancel_spot_request(spot_request_id):
    response = client.cancel_spot_instance_requests(
        SpotInstanceRequestIds=[spot_request_id]
    )
    return response


def request_is_active(spot_request):
    return spot_request['State'] == 'active'


def select_instance_types(machines):
    return ['t3.medium', 't2.micro']

