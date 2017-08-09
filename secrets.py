import hashlib

# used for AWS authentication
ACCESS_KEY_ID = ''
ACCESS_KEY = ''

# nice little hash of the AWS keys
def generate_flask_secret_key():
    sha1 = hashlib.sha1()
    sha1.update(ACCESS_KEY.encode('utf-8'))
    sha1.update(ACCESS_KEY_ID.encode('utf-8'))
    return sha1.hexdigest()
