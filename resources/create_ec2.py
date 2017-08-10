from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def add_tags_to_instance(instance, tags):
    instance.add_tags(tags)


def create_instance(data, location):

    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)

    try:
        new_instance = conn.run_instances(data['ami-image-id'],
                                          key_name=data['key-name'],
                                          instance_type=data['instance-type'],
                                          user_data=data['startup-script']
                                          )

        new_instance_id = str(new_instance.instances[0].id)
        add_tags_to_instance(new_instance.instances[0], data['tags'])

        return {"details": [{
            "instance_id": new_instance_id,
        }]}
    except EC2ResponseError as err:
        return err


class CreateEC2(Resource):
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
        help="Tags are required to create this instance"
    )

    parser.add_argument(
        'startup-script',
        type=str,
        required=True,
        help="Supply a startup script for this instance"
    )

    def post(self, location):
        data = CreateEC2.parser.parse_args()
        instance_details = create_instance(data, location)
        return {"instance": instance_details}