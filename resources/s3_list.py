from boto.s3.connection import S3Connection
from flask_restful import Resource

from secrets import ACCESS_KEY, ACCESS_KEY_ID


def get_all_buckets() -> dict:
    """
    Function to fetch all buckets - the API doesn't seem to support fetching them for a specific region so here it's
    global.
    :return: Collection of buckets in S3
    """

    bucket_dict = {'buckets': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)
    buckets = conn.get_all_buckets()
    for bucket in buckets:
        bucket_dict['buckets'].append({'bucket_name': bucket.name})
    return bucket_dict


class S3List(Resource):
    """A resource representing the retrieval of all S3 buckets."""

    def get(self):
        """Return the details of all S3 buckets"""

        return get_all_buckets()
