import boto
from boto.s3.key import Key
from xml.etree.ElementTree import fromstring, tostring, Element
import settings

def get_bucket(key = settings.AWS_ACCESS_KEY_ID, secret = settings.AWS_SECRET_ACCESS_KEY,
               bucket_name = settings.AWS_BUCKET_NAME):

    conn = boto.connect_s3(key, secret)

    rs = conn.get_all_buckets()
    bucket = None
    for bucketentry in rs:
        if bucketentry.name == bucket_name:
            bucket = bucketentry

    return bucket


# ------------------------------------------------------------------------------


def get_versioninfo():
    bucket = get_bucket()

    """ get current version.info content """
    xml = ''
    try:
        k = Key(bucket)
        k.key = 'version.info'
        xml = k.get_contents_as_string()
    except:
        pass

    if xml.strip() == '':
        xml = '<info></info>';

    return xml
