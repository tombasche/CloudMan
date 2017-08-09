from boto.s3.connection import S3Connection, S3ResponseError
from flask_restful import Resource
from secrets import ACCESS_KEY, ACCESS_KEY_ID
from resources.aws_regions import regions


def get_bucket(bucket_name, location):
    bucket_dict = {'bucket_name': bucket_name, 'contents': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)

    try:
        bucket = conn.get_bucket(bucket_name, location=location)
    except S3ResponseError:
        return None

    for key in bucket:
        bucket_dict['contents'].append({'filename': key.key, 'location': location})
    return bucket_dict


def create_bucket(new_bucket_name, location):
    bucket_dict = {'bucket_name': new_bucket_name, 'details': [], 'contents': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)
    try:
        bucket = conn.create_bucket(new_bucket_name, location=location)
    except:
        return None
    bucket_dict['details'].append({'location': bucket.get_location()})
    return bucket_dict


class S3(Resource):

    def get(self, bucket_name, location):

        if location not in regions:
            return {"message": location + " is not a valid region"}

        bucket = get_bucket(bucket_name, location)
        if bucket:
            return bucket
        return {"message": "No matching bucket found"}, 200

    def post(self, bucket_name, location):

        if location not in regions:
            return {"message": location + " is not a valid region"}

        bucket = create_bucket(bucket_name, location)
        if bucket:
            return bucket
        return {"message": "New bucket was not created successfully"}, 200

