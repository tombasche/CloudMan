from flask import Flask
from flask_restful import Api

from secrets import generate_flask_secret_key
from resources.s3 import S3
from resources.s3_list import S3List
from resources.ec2_list import EC2List
from resources.get_ec2 import GetEC2
from resources.create_ec2 import CreateEC2
from resources.stop_ec2 import StopEC2
from resources.start_ec2 import StartEC2
from resources.create_ec2_image import CreateEC2Image
from resources.promote_ec2 import PromoteEC2

app = Flask(__name__)
app.secret_key = generate_flask_secret_key()
api = Api(app)

# S3
api.add_resource(S3, '/s3', '/s3/<string:bucket_name>', methods=['GET', 'POST'])
api.add_resource(S3List, '/s3/all', '/s3/all', methods=['GET'])

# EC2
api.add_resource(EC2List, '/ec2/all', '/ec2/all/<string:region>/<string:config>', methods=['GET'])
api.add_resource(GetEC2, '/ec2', '/ec2/<string:region>/<string:instance_id>', methods=['GET'])
api.add_resource(CreateEC2, '/ec2/create', '/ec2/create/<string:region>', methods=['POST'])
api.add_resource(StopEC2, '/ec2/stop', '/ec2/stop/<string:region>', methods=['POST'])
api.add_resource(StartEC2, '/ec2/start', '/ec2/start/<string:region>', methods=['POST'])
api.add_resource(CreateEC2Image, '/ec2/image/new', '/ec2/image/new/<string:region>', methods=['POST'])
api.add_resource(PromoteEC2, '/ec2/promote', '/ec2/promote/<string:region>', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
