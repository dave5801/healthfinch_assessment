'''
Author: David Franklin
April 2018

This File contains classes which create an S3 bucket, 
assign it a random string as a name, and populate it
a directory of nicholas cage photos, just to be weird. 

'''
import boto
import os
import boto.s3
from boto.s3.key import Key
import string
import random

class S3BucketProperties(object):
    '''This class generates credentials and unique name for each S3 bucket.'''
    def __init__(self,url=None):
        '''class takes urls where photos are located'''
        self.url = url

    '''return list of nicholas cage photos.'''
    def get_list_of_photos_from_local_directory(self):
        if not os.path.isdir(self.url):
            return("Error: Url is not a Directory")
        else:
            return os.listdir(self.url)

    '''aws security credentials belong in environment variables - see python virtual environment'''
    def get_aws_credentials(self):
        return [os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY')]

    '''s3 buckets must have unique names'''
    def generate_unique_s3_bucket_name(self, size=20, chars=string.ascii_uppercase + string.digits):
        random_str = ''.join(random.choice(chars) for _ in range(size))
        return random_str.lower() + "-photo-directory-bucket"

class CreateNewS3Bucket(object):
    '''This class uses naming conventions, security credentials, and existing files
        to build an S3 bucket in AWS.'''
    def __init__(self,url=None):
        self.url = url #Url of photo directory is passed to properties.
        self.properties = S3BucketProperties(self.url) #new set of S3 properties
        list_of_aws_credentials = self.properties.get_aws_credentials()#get name, and credentials

        #connect using credentials
        resultant_object_from_s3_connection = boto.connect_s3(list_of_aws_credentials[0],
            list_of_aws_credentials[1])
           
        #new bucket name
        bucket_name = self.properties.generate_unique_s3_bucket_name()

        #create the bucket
        bucket = resultant_object_from_s3_connection.create_bucket(bucket_name,
         location=boto.s3.connection.Location.DEFAULT)

        #get list of photos
        list_of_photos = self.properties.get_list_of_photos_from_local_directory()

        #add photos to s3 bucket
        for photo in list_of_photos:
            a_photo_file = self.url + '/' + photo
            k = Key(bucket)
            k.key = photo
            k.set_contents_from_filename(a_photo_file,cb=None, num_cb=10)


if __name__ == '__main__':
    '''Main method to demonstrate function calls.'''
    testfile = "nicholas_cage/"
    test_s3_props = S3BucketProperties(testfile)
    print(test_s3_props.get_aws_credentials())
    print(test_s3_props.get_list_of_photos_from_local_directory())
    print(test_s3_props.generate_unique_s3_bucket_name())

    new_s3_bucket = CreateNewS3Bucket(testfile)