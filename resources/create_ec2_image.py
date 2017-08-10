from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID
from .aws_regions import regions


def create_image(data: dict, region: str) -> dict:
    """
    Function to create an AMI image of a specific ec2 instance.
    Note: If the image exists already it will be copied to a new image.

    :param data: The POST data with the parameters to create the AMI image
    :param region: The AWS region the image will be created in.
    :return: Confirmation message which may have details from either the new image or the copy, or an error message.
    """
    conn = connect_to_region(region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    # as this returns a list, get the single element
    instance = conn.get_only_instances(instance_ids=data['instance-id'])[0]
    new_image_name = '{}-image'.format(instance.tags['config'])

    try:
        image_id = instance.create_image(name=new_image_name)
    except EC2ResponseError as err:
        if err.error_code == 'InvalidAMIName.Duplicate':
            image_id = conn.copy_image(
                region, instance.image_id, name='{}-image-copy'.format(instance.tags['config'])
            ).image_id
            return {'message': '{} already exists - creating a copy: {}'.format(new_image_name, image_id)}
        else:
            return {'message': err}
    return {'message': 'Created image: {} for instance {}'.format(image_id, data['instance-id'])}


class CreateEC2Image(Resource):
    """A resource representing the creation of an EC2 AMI image from a specific instance. """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'instance-id',
        type=str,
        required=True,
        help="An instance id is required to create an image"
    )

    def post(self, region: str) -> dict:
        """Return the details of a newly created or copied EC2 AMI image, or an error message detailing what failed."""

        if region not in regions:
            return {"message": "Not a valid AWS Region"}

        data = CreateEC2Image.parser.parse_args()
        return create_image(data, region)
