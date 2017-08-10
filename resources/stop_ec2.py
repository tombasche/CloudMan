from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions


def stop_instance(data: dict, region: str) -> dict:
    """
    Function to stop one or more running ec2 instances based on the config type.

    :param data: POST data with the parameters of what instances to shut down
    :param region: The AWS Region of the instance(s)
    :return: Confirmation message saying whether the action completed or an error occurred.
    """

    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": data['config-type'], "instance-state-name": "running"})
    try:
        conn.stop_instances(instance_ids=[instance.id for instance in instances])
    except EC2ResponseError:
        return {'message': 'Instance could not be shut down'}
    return {'message': 'Instances in {} config mode shutting down'.format(data['config-type'])}


class StopEC2(Resource):
    """ A resource representing stopping an EC2 instance. """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'config-type',
        type=str,
        required=True,
        help="A config type is required to stop an instance"
    )

    def post(self, region: str) -> dict:
        """ Return a message indicating if stopping the instance was successful or failed."""
        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        data = StopEC2.parser.parse_args()
        return stop_instance(data, region)
