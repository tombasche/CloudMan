from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions
from .tags import valid_tags


def create_instance(data: dict, region: str) -> dict:
    """
    Function to create an EC2 instance in a specified region with parameters.

    :param data: The POST data with the parameters to create the new instance
    :param region: The AWS region the instance will be created in.
    :return: Confirmation message which may have either the new instance id or an error message.
    """

    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    try:
        new_instance = conn.run_instances(data['ami-image-id'],
                                          key_name=data['key-name'],
                                          instance_type=data['instance-type'],
                                          user_data=data['startup-script']
                                          )

        new_instance_id = str(new_instance.instances[0].id)
        new_instance.add_tags(data['tags'])

        return {"details": [{
            "instance_id": new_instance_id,
        }]}
    except EC2ResponseError as err:
        return {"error": err}


class CreateEC2(Resource):
    """A resource representing the creation of an EC2 instance. """

    parser = reqparse.RequestParser()

    parser.add_argument(
        'ami-image-id',
        type=str,
        required=True,
        help="EC2 requires an image id to be supplied"
    )

    parser.add_argument(
        'key-name',
        type=str,
        required=True,
        help="EC2 requires the name of the key-pair used to SSH into the instance"
    )

    parser.add_argument(
        'instance-type',
        type=str,
        required=True,
        help="Please specify the instance type"
    )

    parser.add_argument(
        'tags',
        type=dict,
        required=True,
        help="Tags are required and must be on of the following: {}".format([tag for tag in valid_tags])
    )

    parser.add_argument(
        'startup-script',
        type=str,
        required=True,
        help="Please supply a startup script for this instance (will be run as root). Separate lines with \\n"
    )

    def post(self, region: str) -> dict:
        """Return the details of a newly created EC2 instance, or an error message detailing what failed."""

        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        data = CreateEC2.parser.parse_args()
        return {"instance": create_instance(data, region)}

