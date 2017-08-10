from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .tags import get_next_tag
from .aws_regions import regions


def promote_instance(data: dict, region: str) -> dict:
    """
    Function to promote an instance. This alters the tags from dev -> test or test -> prod.

    :param data: The POST data specifying either the entire tag set or a specific instance.
    :param region: The AWS region the instance is in.
    :return: Confirmation message which may have detail either a success or fail.
    """

    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    incoming_config = data['config-type']

    # get a list of instances based on the config
    if data['instance-id'] is None:
        instances = conn.get_only_instances(
            filters={"tag:config": incoming_config})
    else:
        # get a single instance by the id if it's specified
        try:
            instances = conn.get_only_instances(instance_ids=data['instance-id'])
        except EC2ResponseError:
            return {'message': 'Instance does not exist - have you double checked the region and id?'}

    try:
        for instance in instances:
            instance.remove_tag('config')
            instance.add_tag('config', get_next_tag(incoming_config))
    except EC2ResponseError:
        return {'message': 'An error has occurred adding and removing tags.'}
    return {'message': 'Instances: {} have been promoted'.format(instances)}


class PromoteEC2(Resource):
    """A resource representing the promotion of a tagged EC2 instance. """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'config-type',
        type=str,
        required=True,
        help="A config type is required to promote an instance"
    )
    parser.add_argument(
        'instance-id',
        type=str,
        required=False
    )

    def post(self, region: str) -> dict:
        """Return the response from attempting to promote a tagged instance."""

        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        data = PromoteEC2.parser.parse_args()
        return promote_instance(data, region)
