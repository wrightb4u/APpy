# System modules
from datetime import datetime

# 3rd party modules
from flask import (
    make_response,
    abort
)

import firebase_admin
from firebase_admin import (
    credentials,
    firestore
)

import os

f = open("serviceaccount.json", "w")
f.write(os.environ.get('SERVICEACCOUNT'))
f.close()

cred = credentials.Certificate('./serviceaccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({
#  u'first': u'Ada',
#  u'last': u'Lovelace',
#  u'born': 1815
#})

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
SPEED = {
    "speed/blackbox": {
        "hostname": "blackbox",
        "download": "200 Mbps",
        "upload": "20 Mbps",
        "timestamp": get_timestamp()
    },
    "speed/blackbox1": {
        "hostname": "blackbox1",
        "download": "200 Mbps",
        "upload": "20 Mbps",
        "timestamp": get_timestamp()
    },
    "speed/blackbox2": {
        "hostname": "blackbox2",
        "download": "200 Mbps",
        "upload": "20 Mbps",
        "timestamp": get_timestamp()
    }
}


def read_all():
    HOSTS_REF = db.collection(u'speed')
    HOSTS = HOSTS_REF.get()
    return [u'{} => {}'.format(host.id,host.to_dict()) for host in sorted(HOSTS)]

def read_one(hostname):
    if hostname in SPEED:
        host = SPEED.get(hostname)

    else:
        abort(404, 'Host with last name {hostname} not found'.format(
            hostname=hostname))

    return host


def create(host):
    hostname = host.get('hostname', None)
    download = host.get('download', None)
    upload = host.get('upload', None)

    if hostname not in SPEED and hostname is not None:
        SPEED[hostname] = {
            'hostname': hostname,
            'download': download,
            'upload': upload,
            "timestamp": get_timestamp()
        }
        return make_response('{hostname} successfully created'.format(
            hostname=hostname), 201)

    else:
        abort(406, 'Host with hostname {hostname} already exists'.format(
            hostname=hostname))


def update(hostname, host):
    if hostname in SPEED:
        SPEED[hostname]['download'] = host.get('download')
        SPEED[hostname]['upload'] = host.get('upload')
        SPEED[hostname]['timestamp'] = get_timestamp()

        return SPEED[hostname]

    else:
        abort(404, 'Host with hostname {hostname} not found'.format(
            hostname=hostname))


def delete(hostname):
    if hostname in SPEED:
        del SPEED[hostname]
        return make_response('{hostname} successfully deleted'.format(
            hostname=hostname), 200)

    else:
        abort(404, 'Host with hostname {hostname} not found'.format(
            hostname=hostname))
