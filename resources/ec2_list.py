from boto.ec2 import connect_to_region
from flask_restful import Resource

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions


def get_all_instances(config: str, region: str) -> dict:
    """
    Function to return all ec2 instances in a particular region by a certain tag.

    :param config: The config type - refer to `tags.py` for the list of valid tags.
    :param region: The AWS region to get ec2 instances for
    :return: Collection of all instances for the region.
    """
    instance_dict = {'instances': []}
    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": config})
    for instance in instances:
        instance_dict['instances'].append({'instance_id': instance.id,
                                           'type': instance.instance_type,
                                           'state': instance.state,
                                           'public_dns_name': instance.public_dns_name,
                                           'launch_time': instance.launch_time})
    return instance_dict


class EC2List(Resource):
    """A resource representing the fetching of a list of ec2 instances """

    def get(self, region: str, config: str) -> dict:
        """Return the details of all ec2 instances for a specific tag / config type for a region."""

        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        instances = get_all_instances(config, region)
        return instances
