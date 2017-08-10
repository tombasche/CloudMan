from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions


def start_instance(data: dict, region: str) -> dict:
    """
    Function to start one or more running ec2 instances based on the config type.

    :param data: POST data with the parameters of what instances to start up
    :param region: The AWS Region of the instance(s)
    :return: Confirmation message saying whether the action completed or an error occurred.
    """

    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": data['config-type'], "instance-state-name": "stopped"})

    if len(instances) == 0:
        return {'message': 'No instances found with that config type - nothing to do'}

    try:
        conn.start_instances(instance_ids=[instance.id for instance in instances])
    except EC2ResponseError:
        return {'message': 'Instance could not be started'}

    return {'message': 'Instances in {} config mode starting up'.format(data['config-type'])}


class StartEC2(Resource):
    """ A resource representing starting an EC2 instance. """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'config-type',
        type=str,
        required=True,
        help="A config type is required to start an instance"
    )

    def post(self, region: str) -> dict:
        """ Return a message indicating if starting the instance was successful or failed."""
        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        data = StartEC2.parser.parse_args()
        return start_instance(data, region)
