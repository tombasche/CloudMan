from boto.ec2 import connect_to_region
from flask_restful import Resource
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def get_all_instances(location, config):

    instance_dict = {'instances': []}
    conn = connect_to_region(location, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    instances = conn.get_only_instances(filters={"tag:config": config})
    for instance in instances:
        instance_dict['instances'].append({'instance_id': instance.id,
                                           'type': instance.instance_type,
                                           'state': instance.state,
                                           'public_dns_name': instance.public_dns_name,
                                           'launch_time': instance.launch_time})
    return instance_dict


class EC2List(Resource):

    def get(self, location, config):
        instances = get_all_instances(location, config)
        return instances
