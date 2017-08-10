from boto.s3.connection import S3Connection, S3ResponseError
from flask_restful import Resource, reqparse

from secrets import ACCESS_KEY, ACCESS_KEY_ID


def get_bucket(bucket_name: str) -> dict:
    """
    Function to retrieve a bucket from S3 by name.S3 buckets can only be created globally using the
    boto library.

    :param bucket_name: The DNS-compliant name for the bucket to be retrieved.
    :return: Details of the bucket being retrieved or an error message if it is not found.
    """

    bucket_dict = {'bucket_name': bucket_name, 'contents': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)

    try:
        bucket = conn.get_bucket(bucket_name)
    except S3ResponseError:
        return {'message': 'The bucket specified was not found.'}

    for key in bucket:
        bucket_dict['contents'].append({'filename': key.key})
    return bucket_dict


def create_bucket(data: dict) -> dict:
    """
    Function to create a new bucket on S3 in a specific location. S3 buckets can only be created globally using the
    boto library.

    :param data: The POST data containing the DNS-compliant name for the bucket to be created
    :return: Details of the bucket being created or an error message if it is not.
    """

    bucket_dict = {'bucket_name': data['bucket_name'], 'details': [], 'contents': []}
    conn = S3Connection(ACCESS_KEY_ID, ACCESS_KEY)
    try:
        bucket = conn.create_bucket(data['bucket_name'])
    except:  # really broad exception but it seems like the S3ConnectionError doesn't 'exist' when creating a bucket.
        return {'message':
                'There was an error creating the bucket - perhaps the name is already in use or not DNS compliant'}
    return bucket_dict


class S3(Resource):
    """A resource representing an S3 bucket."""

    def get(self, bucket_name: str) -> dict:
        """Return the details of a specific S3 bucket by name or an error if it couldn't be found."""

        return get_bucket(bucket_name)

    parser = reqparse.RequestParser()
    parser.add_argument(
        'bucket-name',
        type=str,
        required=True,
        help="Please specify the name of the S3 bucket to create"
    )

    def post(self) -> dict:
        """Return the details of a newly created S3 bucket by name or an error if it couldn't be created."""

        data = S3.parser.parse_args()
        return create_bucket(data['bucket-name'])

