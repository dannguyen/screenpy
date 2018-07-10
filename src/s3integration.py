"""
currently not used by main screenpy.py for now
"""


import boto3

S3_BUCKET = 'cdan.danwin.com'
S3_DOMAIN = 'http://cdan.danwin.com.s3-website-us-east-1.amazonaws.com/'
S3_DEFAULT_SUBFOLDER = 'screenpy-caps'


def generate_s3_keyname(destname):
    """ simply returns join with default s3 subfolder and destname """
    return join(S3_DEFAULT_SUBFOLDER, destname)

def generate_s3_url(destname):
    return join(S3_DOMAIN, generate_s3_keyname(destname))




def to_s3(srcname, destname, fileext=None):
    """
    MIME header based on destname extension by default, e.g.
      'image/png' for 'example.png'

    Returns the S3 URL for easy reference
    """
    fileext = fileext or splitext(destname)[1][1:]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET)
    key = bucket.Object(generate_s3_keyname(destname))
    with open(srcname, 'rb') as data:
        key.upload_fileobj(data, {'ACL': 'public-read',
                                  'ContentType': 'image/%s' % fileext})
    return generate_s3_url(destname)
