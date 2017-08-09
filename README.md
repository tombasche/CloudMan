# CloudMan
Manage AWS cloud storage and instances using a simple API

#Installation

- `virtualenv venv`
- `source <env_name>/bin/activate`
- `pip install -r requirements.txt`
- `python app.py`

### Authentication

In secrets.py fill in the blanks to authenticate with AWS

API Spec
========

### Create new instance - POST

`<url>/ec2/create/<aws_region>` where aws_region might be ap-southeast-2, eu-west-1 etc.


Example of request to create a new Amazon Linux t2.micro with a _very_ basic webpage:

```json
{
	"ami-image-id": "ami-10918173",
	"instance-type": "t2.micro",
	"key-name": "key-pair",
	"tags": {
		"config" : "dev"
	},
	"startup-script": "#!/bin/bash \nyum update -y \nyum install -y httpd \nservice httpd start \nchkconfig httpd on \necho '<html>this is a test</html>' > /var/www/html/index.html"
}
```

The tags specified in this instance creation allow instances to be identified in order to be stopped, terminated or cloned via the API. These might be:
- dev
- test
- prod

The idea here is that each tag specifies a certain config for a different environment. 