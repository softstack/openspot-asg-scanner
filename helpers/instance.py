from functools import reduce


def terminate_instance(client, instance_id):
    response = client.terminate_instances(
        InstanceIds=[instance_id]
    )

    return response


def get_instances(client, *ids):
    response = client.describe_instances(
        InstanceIds=ids
    )
    all_instances = reduce(lambda instances, reservation:
                           reservation['Instances'] + instances,
                           response['Reservations'], [])

    return all_instances

