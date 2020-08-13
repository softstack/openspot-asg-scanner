from helpers import instance, spot, asg as autoscaling_group


def ensure(asg):
    instances_ids = autoscaling_group.get_instances_ids(asg)
    machines = instance.get_instances(*instances_ids)
    for machine in machines:
        if instance.is_ondemand(machine):
            spot_request = spot.get_spot_request(instance['InstanceId'])
            if not spot_request:
                spot.create_spot_request(instance)
                continue
            if spot.request_is_active(spot_request):
                spot_machines = instance.get_instances(spot_request['InstanceId'])
                if spot_machines:
                    if instance.is_running(spot_machines[0]):
                        autoscaling_group.change_instances(
                            machine['InstanceId'],
                            spot_request['InstanceId'],
                            asg['AutoScalingGroupName']
                        )
                        instance.terminate_instance(instance['InstanceId'])
                else:
                    spot.cancel_spot_request(spot_request['SpotInstanceRequestId'])


def scan(event, context):
    all_asg = autoscaling_group.list_openspot_asg()
    for asg in all_asg:
        ensure(asg)
