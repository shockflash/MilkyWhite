import boto
from time import time
import os
from boto.s3.key import Key
from xml.etree.ElementTree import fromstring, tostring, Element
import settings
import sys
from lib import get_bucket, get_versioninfo


def upload(group, filename):
    bucket = get_bucket()

    basename = os.path.basename(filename)
    app, version = basename.replace('.tar.bz2', '').split('_')

    k = Key(bucket)
    k.key = 'applications/' + basename
    k.set_contents_from_filename(filename)

    versioninfo_update(group, app, version)
    print "Upload finished"

def version(group, app, version):
    bucket = get_bucket()

    list = bucket.list('applications/')

    found = False
    for appentry in list:
        appfile = os.path.basename(appentry.name).replace('.tar.bz2', '')

        s3app, s3version = appfile.split('_')
        if s3app == app and s3version == version:
            found = True

    if found:
        versioninfo_update(group, app, version)
        print "Version change done"
    else:
        print "\nApp '%s' in version '%s' not found!\n" % (app, version)

def remove(group, app):
    versioninfo_remove(group, app)
    print "\nApp '%s' was removed from group '%s'\n" % (app, group)

def info():
    xml = get_versioninfo()

    dom = fromstring(xml)

    for group in dom:
        print "Group: " + group.attrib['name']
        for app in group:
            print "  - App: " + app.attrib['name'], 'Version: ' + app.attrib['version']

# ------------------------------------------------------------------------------


def write_versioninfo(content):
    bucket = get_bucket()

    """ write new version.info and a backup file """
    k = Key(bucket)
    k.key = 'version.info'
    k.set_contents_from_string(content)

    k = Key(bucket)
    k.key = 'old/version.info_' + str(int(time()))
    k.set_contents_from_string(content)

def versioninfo_update(group, app, version):
    xml = get_versioninfo()

    dom = fromstring(xml)

    """ find group """
    groupxml = None
    for node in dom:
        if node.attrib['name'] == group:
            groupxml = node
    if groupxml == None:
        groupxml = Element('group')
        groupxml.attrib['name'] = group
        dom.append(groupxml)

    for node in groupxml:
        if node.attrib['name'] == app:
            groupxml.remove(node)

    appxml = Element('application')
    appxml.attrib['name'] = app
    appxml.attrib['version'] = version
    groupxml.append(appxml)

    write_versioninfo(tostring(dom))

def versioninfo_remove(group, app):
    xml = get_versioninfo()

    dom = fromstring(xml)

    """ find group """
    groupxml = None
    for node in dom:
        if node.attrib['name'] == group:
            groupxml = node
    if groupxml == None:
        groupxml = Element('group')
        groupxml.attrib['name'] = group
        dom.append(groupxml)

    for node in groupxml:
        if node.attrib['name'] == app:
            groupxml.remove(node)
    write_versioninfo(tostring(dom))


# ------------------------------------------------------------------------------


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ''
        print 'Comamnds: upload, version, remove, info'
        print 'Usage: python controller.py [command] [parameter...]  [...parameter]'
        print ''
        quit()

    if sys.argv[1] == 'upload':
        upload(sys.argv[2], sys.argv[3]);

    if sys.argv[1] == 'version':
        version(sys.argv[2], sys.argv[3], sys.argv[4]);

    if sys.argv[1] == 'remove':
        remove(sys.argv[2], sys.argv[3]);

    if sys.argv[1] == 'info':
        info()
