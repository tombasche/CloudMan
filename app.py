from flask import Flask, request
from flask_restful import Api
from secrets import generate_flask_secret_key
from resources.s3 import S3
from resources.s3List import S3List

from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = generate_flask_secret_key()
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(S3, '/s3', '/s3/<string:location>/<string:bucket_name>', methods=['GET', 'POST'])
api.add_resource(S3List, '/s3/all', '/s3/all', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)