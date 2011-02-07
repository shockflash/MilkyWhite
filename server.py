import os
import shutil
import boto
from boto.s3.key import Key
from xml.etree.ElementTree import fromstring, tostring, Element
import settings
from lib import get_bucket, get_versioninfo

def install_packages():
    packages = [
        'mc',
        'rsync',
        'python-setuptools',
        'python-dev',
        'build-essential',
        'python-virtualenv',
        'libmysqlclient-dev',
        'libjpeg62-dev',
        'apache2',
        'libapache2-mod-wsgi',
        'nginx'
    ]

    os.system('apt-get update')
    os.system('apt-get -y upgrade')
    os.system('apt-get install -y ' + ' '.join(packages))


def compare_applications():
    """ If true, we stopped the servers because of an change, so they need
        to be started again at the end """

    group = settings.GROUP

    local = open(settings.APPS_LOCALINFO).read()
    remote = remote = get_versioninfo()

    """ Collect app list for local and remove """
    localApps = get_app_list(local)
    remoteApps = get_app_list(remote, group)

    """ First, check for apps to remove """
    for app, localVersion in localApps.items():
        found = False
        for remoteApp, version in remoteApps.items():
            if app == remoteApp:
                found = True
        if not found:
            uninstall(app)

    """ Now check for new apps """
    for app, version in remoteApps.items():
        found = False
        for localApp, localVersion in localApps.items():
            if app == localApp:
                found = True
        if not found:
            install(app, version)

    """ Now check for apps to upgrade """
    for app, version in remoteApps.items():
        diff = False
        for localApp, localVersion in localApps.items():
            if app == localApp and version != localVersion:
                diff = True
        if diff:
            upgrade(app, version)

    handle_webserver()

def get_app_list(filecontent, group = False):
    list = {}

    if filecontent.strip() == '':
        filecontent = '<info></info>'

    dom = fromstring(filecontent)
    for node in dom:
        if group and node.attrib['name'] != group:
            continue;

        for app in node:
            list[app.attrib['name']] = app.attrib['version']

    return list

GLOBAL_start_webserver = False

def stop_webserver():
    return # TODO 
    global GLOBAL_start_webserver

    if GLOBAL_start_webserver:
        return

    GLOBAL_start_webserver = True

    os.system('/etc/init.d/nginx stop')
    os.system('/etc/init.d/apache2 stop')

def handle_webserver():
    return # TODO 
    global GLOBAL_start_webserver

    if GLOBAL_start_webserver:
        os.system('/etc/init.d/apache2 start')
        os.system('/etc/init.d/nginx start')

def upgrade(app, version):
    print "UPGRADE " + app, version
    uninstall(app)
    install(app, version)

def uninstall(app):
    print "UNINSTALL " + app

    stop_webserver()

    local_dir = os.path.join(settings.APPS_LOCALDIR, app)

    os.system('cd ' + local_dir + ' && /bin/bash mwpackage/uninstall.sh')
    try:
        os.removedirs(local_dir)
    except:
        pass

    write_localinfo_remove(app)

def install(app, version):
    print "INSTALL " + app, version

    stop_webserver()

    local_dir = os.path.join(settings.APPS_LOCALDIR, app)
    try:
        os.makedirs(local_dir)
    except:
        pass

    localfile = os.path.join(local_dir, app + '.tar.bz2')

    """ Download file form S3 """
    bucket = get_bucket()
    k = Key(bucket)
    k.key = 'applications/' + app + '_' + version + '.tar.bz2'
    k.get_contents_to_file(open(localfile, 'w'))

    """ extract file """
    os.system('cd ' + local_dir + ' && tar -jxvf %s' % app + '.tar.bz2')
    os.unlink(localfile)

    """ Run install scrpt """
    os.system('cd ' + local_dir + ' && /bin/bash mwpackage/install.sh')

    """ write new version to config """
    write_localinfo_new(app, version)

def write_localinfo_remove(app):
    local = open(settings.APPS_LOCALINFO).read()

    if local.strip() == '':
        local = '<info><local></local></info>'

    dom = fromstring(local)

    """ remove and old entry, if exists """
    l = dom.find("local/")
    for application in l:
        if application.attrib['name'] == app:
            l.remove(application)

    open(settings.APPS_LOCALINFO, 'w').write(tostring(dom))

def write_localinfo_new(app, version):
    local = open(settings.APPS_LOCALINFO).read()

    if local.strip() == '':
        local = '<info><local></local></info>'

    dom = fromstring(local)

    """ remove and old entry, if exists """
    l = dom.find("local/")
    for application in l:
        if application.attrib['name'] == app:
            l.remove(application)

    appelement = Element('application')
    appelement.attrib['name'] = app
    appelement.attrib['version'] = version
    l.append(appelement)

    open(settings.APPS_LOCALINFO, 'w').write(tostring(dom))


install_packages()
compare_applications()
