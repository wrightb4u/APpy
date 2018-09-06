# This is the speed module that supports all of the REST actions for the
# SPEED collection

# System modules
from datetime import datetime
import os

# 3rd party modules
from flask import (
    make_response,
    abort
)

import google.cloud.exceptions

import firebase_admin

from firebase_admin import (
    credentials,
    firestore
)

# Due to limitations of the Firestore SDK and for security reasons, we have to
# write the file needed to access the Firestore DB using the ENV variable that
# contains the secret details
f = open("serviceaccount.json", "w")
f.write(os.environ.get('SERVICEACCOUNT'))
f.close()

# Authenticate and initialize the Firestore DB
cred = credentials.Certificate('./serviceaccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Preliminary Test Data to serve with our API
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


# This function responds to a request for /api/speed with the complete list of
# hosts by returning a json string
def read_all():
    HOSTS_REF = db.collection(u'speed')
    HOSTS = HOSTS_REF.get()
    return [u'{} => {}'.format(host.id,host.to_dict()) for host in HOSTS]

# This function responds to a request for /api/speed/{hostname} with a json
# string of the host (if one exists) or a 404 if the host does not exist
def read_one(hostname):
    doc_ref = db.collection(u'speed').document(hostname)
    try:
        host = doc_ref.get()
        return [u'{} => {}'.format(host.id,host.to_dict())]
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
        abort(404, 'Host with hostname {hostname} not found'.format(hostname=hostname))

    return host

# This function creates a new host entry
def create(host):
    hostname = host.get('hostname', None)
    download = host.get('download', None)
    upload = host.get('upload', None)
    key = host.get('key', None)
    # Get hostname from Firestore
    doc_ref = db.collection(u'speed').document(hostname)

    if key != os.environ.get('KEY'):
        abort(403, 'Access Denied')
    # If hostname exists, through 406 error, else, create the host
    try:
        doc = doc_ref.get()
        abort(406, 'Host with hostname {hostname} already exists'.format(hostname=hostname))
    except google.cloud.exceptions.NotFound:
        data = {
            u'hostname': hostname,
            u'download': download,
            u'upload': upload,
            u'timestamp': get_timestamp()
        }
        db.collection(u'speed').document(hostname).set(data)
        return make_response('{hostname} successfully created'.format(
            hostname=hostname), 201)

# This function updates a host entry
def update(hostname, host):
    if hostname in SPEED:
        SPEED[hostname]['download'] = host.get('download')
        SPEED[hostname]['upload'] = host.get('upload')
        SPEED[hostname]['timestamp'] = get_timestamp()

        return SPEED[hostname]

    else:
        abort(404, 'Host with hostname {hostname} not found'.format(
            hostname=hostname))

# This function deletes a host entry
def delete(hostname):
    if hostname in SPEED:
        del SPEED[hostname]
        return make_response('{hostname} successfully deleted'.format(
            hostname=hostname), 200)

    else:
        abort(404, 'Host with hostname {hostname} not found'.format(
            hostname=hostname))
