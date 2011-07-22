# -*- coding: utf-8 -*-

import bottle
from bottle import route, redirect, static_file, response, request
from gevent import monkey; monkey.patch_all()
from gevent.event import Event
from gevent.pywsgi import WSGIServer
import json
import logging
from restkit import Resource

try:
    from collections import OrderedDict # py2.7 only
except ImportError:
    from ordereddict import OrderedDict

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='chattle.log',level=logging.DEBUG)


def json_loads(string):
    return json.loads(string, object_pairs_hook=OrderedDict);

def json_dumps(data):
    return json.dumps(data, indent=4)

def printj(data):
    print json_dumps(data)


# planned: couchdb_ressource
#     uuid, update_seq, _changes

# api-layer so choosing backends is possible 
#    in-memory, couchdb
#    mutltiple backends possible. provide different functionality e.g. search
#
# api-layer
#    since - datetime or seq_number
#    uuid
#    hash
#    seperate meta


couchdb = Resource('http://localhost:5984/')
try:
    couchdb.put('chattle/')
except:
    pass

couchdb_chattle = Resource('http://localhost:5984/chattle/')





msgs = [
    {
        'from': 'server',
        'content': 'Welcome to Chattle!'
    }
]

event_new_msg = Event()

@route('/')
def index(name='World'):
    return open('_res/chattle.html')


@route('/_res/:path#.+#')
def server_static(path):
    return static_file(path, root='_res/')


@route('/msgs', method='GET')
def get_items():

    # for now sequence_number
    # later also datetime


    since = request.params.get('since') or - 5

    if since < 0:
        r = json_loads(couchdb_chattle.get().body_string(charset='utf-8'))
        update_seq = r['update_seq']
        since = max(0, update_seq + since)

    r = json_loads(couchdb_chattle.get('_changes', since=since, include_docs="true", feed="longpoll").body_string(charset='utf-8'))
    print(r)

    response.content_type = 'application/json;'
    return json.dumps(r, indent=4)


@route('/msgs', method='POST')
def get_items():

    data = json_loads(request.body.getvalue())

    if '_id' not in data:
        r = json_loads(couchdb.get('_uuids').body_string(charset='utf-8'))
        data['_id'] = r[u'uuids'][0] # getone?

        couchdb_chattle.put(path=data['_id'], payload=json_dumps(data)) # force overwrite


    msgs.append(data)
    event_new_msg.set()

    return


if __name__ == "__main__":
    app = bottle.default_app()

    print 'Serving on 8080...'
    WSGIServer(('', 8080), app).start()

    print 'Serving on 8443...'
#    WSGIServer(('', 8443), app, keyfile='server.key', certfile='server.crt').serve_forever()
    WSGIServer(('', 8443), app, keyfile='/etc/ssl/private/ssl-cert-snakeoil.key', certfile='/etc/ssl/certs/ssl-cert-snakeoil.pem').serve_forever()

else:
    application = bottle.default_app()
