from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def stop_instance(location, data):

    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": data['config-type'], "instance-state-name": "running"})
    try:
        conn.stop_instances(instance_ids=[instance.id for instance in instances])
    except EC2ResponseError as err:
        return err
    return 'Instances in {} config mode shutting down'.format(data['config-type'])


class StopEC2(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'config-type',
        type=str,
        required=True,
        help="A config type is required to stop an instance"
    )

    def post(self, location):
        data = StopEC2.parser.parse_args()
        message = stop_instance(location, data)
        return {"message": message}