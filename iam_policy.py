"""
IAM boto examples:
In this example we create a group that provides access
to all EC2 and S3 resources and actions and then add a
user to that group.
"""
import boto

#
# First create a connection to the IAM service
#
iam = boto.connect_iam()

#
# Now create a group for EC2/S3 users.
# This group will allow members to use all EC2 and S3 functionality
#
lambda_policy = """
{
   "Statement":[{
      "Effect":"Allow",
      "Action":["lambda:*", "s3:*"],
      "Resource":"*"
      }
   ]
}"""
