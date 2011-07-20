# -*- coding: utf-8 -*-

import bottle
from bottle import route, redirect, static_file, response, request
from gevent import monkey; monkey.patch_all()
from gevent.event import Event
from gevent.pywsgi import WSGIServer
import json
import logging

try:
    from collections import OrderedDict
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


msgs = [
    {
        'from': 'server',
        'content': 'Yori!'
    },
    {
        'from': 'server',
        'content': 'whzz uup?'
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

    start = int(request.params.get('start')) or 0

    while True:
        new_msgs = msgs[start:]

        if len(new_msgs) == 0:
            event_new_msg.wait()
        else:
            event_new_msg.clear()
            break

    response.content_type = 'application/json;'
    return json.dumps(new_msgs, indent=4)


@route('/msgs', method='POST')
def get_items():

    data = json_loads(request.body.getvalue())

    msgs.append(data)
    event_new_msg.set()

    return


if __name__ == "__main__":
    app = bottle.default_app()

    print 'Serving on 8080...'
    WSGIServer(('', 8080), app).start()

    print 'Serving on 8443...'
    WSGIServer(('', 8443), app, keyfile='server.key', certfile='server.crt').serve_forever()

else:
    application = bottle.default_app()
