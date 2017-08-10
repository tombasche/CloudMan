from flask import Flask
from flask_restful import Api
from secrets import generate_flask_secret_key
from resources.s3 import S3
from resources.s3_list import S3List
from resources.ec2_list import EC2List
from resources.get_ec2 import GetEC2
from resources.create_ec2 import CreateEC2
from resources.stop_ec2 import StopEC2
from resources.create_ec2_image import CreateEC2Image


app = Flask(__name__)
app.secret_key = generate_flask_secret_key()
api = Api(app)


api.add_resource(S3, '/s3', '/s3/<string:location>/<string:bucket_name>', methods=['GET', 'POST'])
api.add_resource(S3List, '/s3/all', '/s3/all', methods=['GET'])

api.add_resource(EC2List, '/ec2/all', '/ec2/all/<string:location>/<string:config>', methods=['GET'])
api.add_resource(GetEC2, '/ec2', '/ec2/<string:location>/<string:instance_id>', methods=['GET'])
api.add_resource(CreateEC2, '/ec2/create', '/ec2/create/<string:location>', methods=['POST'])
api.add_resource(StopEC2, '/ec2/stop', '/ec2/stop/<string:location>', methods=['POST'])
api.add_resource(CreateEC2Image, '/ec2/image/new', '/ec2/image/new/<string:location>', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)