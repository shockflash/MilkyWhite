def get_bucket():
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

    rs = conn.get_all_buckets()
    bucket = None
    for bucketentry in rs:
        if bucketentry.name == settings.AWS_BUCKET_NAME:
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
