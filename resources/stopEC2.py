from boto.ec2 import connect_to_region
from boto.ec2.connection import EC2ResponseError
from flask_restful import Resource, reqparse
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def stop_instance(location, config_type):

    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": config_type, "instance-state-name": "running"})
    try:
        conn.stop_instances(instance_ids=[instance.id for instance in instances])
    except EC2ResponseError:
        return None
    return 'Instances shutting down'


class StopEC2(Resource):

    def get(self, location, config_type):
        message = stop_instance(location, config_type)
        if message:
            return {"message": message}

        return {"message": "There was an error stopping the ec2 instance"}, 200