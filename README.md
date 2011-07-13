Chattle Chat App
================

Chattle is a small chat app to demonstrate the use of asynchronous responses with the webframework [Bottle](https://github.com/defnull/bottle). It uses [gevent](https://bitbucket.org/denis/gevent/overview) to allow many concurrent connections from chat clients to the chat server.


Dependencies
------------

Install bottle and gevent with `pip install bottle gevent`.

    $ python chattle.py


Open different Browser and start chatting!



If you want more control over the server setup, you may use `pip install gunicorn`:

    $ gunicorn --bind 0.0.0.0:8080 --worker-class gevent --workers 1 chattle

See [Gunicorn](http://gunicorn.org/) [documentation](http://gunicorn.org/configure.html) for more options like daemonizing or dropping privileges when started as root.

If you increase the number of workers you can experience the weirdness happening when every worker maintains his unshared copy of chat-history..
