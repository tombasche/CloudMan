from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def create_image(location, data):

    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instance = conn.get_only_instances(instance_ids=data['instance-id'])[0]
    new_image_name = '{}-image'.format(instance.tags['config'])
    try:
        image_id = instance.create_image(name=new_image_name)
    except EC2ResponseError as err:
        if err.error_code == 'InvalidAMIName.Duplicate':
            image_id = conn.copy_image(location, instance.image_id, name='{}-image-copy'.format(instance.tags['config'])).image_id
            return '{} already exists - creating a copy: {}'.format(new_image_name, image_id)
        else:
            return None
    return 'Created image: {} for instance {}'.format(image_id, data['instance-id'])


class CreateEC2Image(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'instance-id',
        type=str,
        required=True,
        help="An instance id is required to create an image"
    )

    def post(self, location):
        data = CreateEC2Image.parser.parse_args()
        message = create_image(location, data)
        return {"message": message}
