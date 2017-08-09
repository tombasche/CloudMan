from boto.s3.connection import S3Connection
from flask_restful import Resource
from secrets import ACCESS_KEY, ACCESS_KEY_ID


def get_all_buckets():
    bucket_dict = {'buckets': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)
    buckets = conn.get_all_buckets()
    for bucket in buckets:
        bucket_dict['buckets'].append({'bucket_name': bucket.name})
    return bucket_dict


class S3List(Resource):

    def get(self):
        buckets = get_all_buckets()
        return buckets
