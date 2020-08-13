import boto3

client = boto3.client('autoscaling')


def change_instances(ondemand_instance_id, spot_instance_id, asg_name):
    client.detach_instances(
        InstanceIds=[ondemand_instance_id],
        AutoScalingGroupName=asg_name,
        ShouldDecrementDesiredCapacity=True,
    )

    client.attach_instances(
        InstanceIds=[spot_instance_id],
        AutoScalingGroupName=asg_name,
    )


def list_openspot_asg():
    all_asg_response = client.describe_auto_scaling_groups()
    all_asg = all_asg_response['AutoScalingGroups']
    filtered_asg = list(filter(lambda asg: _filter_tagged_asg(asg), all_asg))
    return filtered_asg


def get_instances_ids(asg):
    return [instance['InstanceId'] for instance in asg['Instances']]


def _filter_tagged_asg(asg):
    return [
        True for tag in asg['Tags'] if tag['Key'] == 'openspot' and tag['Value'] == 'enabled'
    ]


