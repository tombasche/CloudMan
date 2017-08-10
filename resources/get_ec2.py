from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions


def get_instance(instance_id: str, region: str) -> dict:
    """
    Function to retrieve details about a specific ec2 instance by its id

    :param instance_id: The id of the ec2 instance (typically something like i-xxxxxxxxxx )
    :param region: The AWS region the instance is in
    :return: Details about the requested instance or a message saying it couldn't be found
    """
    instance_dict = {'instance': instance_id, 'details': []}
    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)

    try:
        instances = conn.get_only_instances(instance_ids=instance_id)
    except EC2ResponseError:
        return {'message': 'Instance does not exist - have you double checked the region and id?'}

    for instance in instances:
        instance_dict['details'].append({'instance_id': instance.id,
                                         'type': instance.instance_type,
                                         'state': instance.state,
                                         'public_dns_name': instance.public_dns_name,
                                         'launch_time': instance.launch_time})

    return instance_dict


class GetEC2(Resource):
    """A resource representing the retrieval of an EC2 instance. """
    def get(self, instance_id: str, region: str) -> dict:
        """Return the details of a specific EC2 instance, or an error message detailing what failed."""

        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        return get_instance(instance_id, region)

