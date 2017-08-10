# CloudMan
Manage tagged EC2 instances for environment tracking. Also comes with simple S3 functionality. 

#Installation

- `virtualenv venv`
- `source <env_name>/bin/activate`
- `pip install -r requirements.txt`
- `python app.py`

### Authentication

In secrets.py fill in the blanks to authenticate with AWS

API Spec
========

### Create new instance

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

The tags specified in this instance creation allow instances to be identified in order to be stopped, started or promoted to the next stage via the API. These might be:
- dev
- test
- prod

### Promote instance

A dev instance can be promoted to a test environment and a test environment to production with the following API call:

`<url>/ec2/promote/<aws_region>` 
As this is a post request it might look like so:
```json
{
    "config-type" : "dev"
}
```
Any instances with this tag will now be promoted to a `test` environment. An `instance-id` parameter can also be specified in this request to only promote a single instance.

### Stop or start an instance

Instances can be stopped or started by with the following endpoints:

`<url>/ec2/stop|start/<aws_region>` 

The body would be something like this:
```json
{
    "config-type" : "dev"
}
```

to stop all dev instances. Note that an instance must be fully stopped before it can be started again. 

### Create an image

Images can also be created from an instance to enable instances to be cloned with the following endpoint. (Note due to a limitation of t2.micro I'm unable to actually clone anything for free)

`<url>/ec2/image/new/<aws_region`
The request might look like this (note you'll need the exact instance-id)
```json
{
    "instance-id": "i-03c977a9cfda8d629"
}
```

### Retrieve ec2 instance ids for a specific config

The following endpoint will get you the details of all instances for a specific config:

`<url>/ec2/all/<aws_region>/<config>`

It might return something like the following:

```json
{
    "instances": [
      {
        "type": "t2.micro",
        "instance_id": "i-03c977a9cfda8d629",
        "launch_time": "2017-08-10T06:04:50.000Z",
        "state": "stopped",
        "public_dns_name": ""
      }
    ]
}
```

### Retrieve single ec2 instance details

The following endpoint will get you the details of a single instance:

`<url>/ec2/<aws_region>/<instance_id>`

It might return something like the following:

```json
{
    "details": [
        {
            "type": "t2.micro",
            "instance_id": "i-03c977a9cfda8d629",
            "launch_time": "2017-08-10T06:04:50.000Z",
            "state": "stopped",
            "public_dns_name": ""
        }
    ],
    "instance": "i-03c977a9cfda8d629"
}
```