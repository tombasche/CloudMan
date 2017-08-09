from boto.ec2 import connect_to_region
from flask_restful import Resource, reqparse
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def add_tags_to_instance(instance, tags):
    instance.add_tags(tags)


def create_instance(data, location):

    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    new_instance = conn.run_instances(data['ami-image-id'],
                                      key_name=data['key-name'],
                                      instance_type=data['instance-type'],
                                      )

    new_instance_id = str(new_instance.instances[0].id)
    add_tags_to_instance(new_instance.instances[0], data['tags'])

    return new_instance_id


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

    def post(self, location):
        data = CreateEC2.parser.parse_args()
        new_instance_id = create_instance(data, location)
        if new_instance_id:
            return {"instance": new_instance_id}

        return {"message": "There was an error creating the ec2 instance"}, 200