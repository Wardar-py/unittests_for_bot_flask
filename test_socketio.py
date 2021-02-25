import json
import unittest
import os
from os.path import join, dirname

import flask
from dotenv import load_dotenv
import flask_socketio
from flask import Flask, session, request, json as flask_json
from flask_socketio import SocketIO, send, emit
from unittest import TestCase, mock
from app import *
from app import socketio, app, emit_all_messages, users

MESSAGES_RECEIVED_CHANNEL = 'messages received'
app = Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)
app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@socketio.on('connect')
def on_connect():
    print('Someone connection +++++++')
    socketio.emit('connected', {
        'test': 'Connected'
    })

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    print('Someone disconnected +++++++')

@socketio.on('new user input')
def on_user_signin(data):
    print("Got an event for new user input with data:", data)
    users.add(data["id"])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('new user output')
def on_user_logout(data):
    print("Got an event for new user output with data:", data)
    users.remove(data["id"])
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")



#---------------------------------------------------------------------------------------------------------------------------------------------




class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch.dict(os.environ, {"SQL_USER": "mytemp"})
    @mock.patch.dict(os.environ, {"SQL_PASSWORD": "mytemp"})
    @mock.patch.dict(os.environ, {"USER": "mytemp"})
    @mock.patch.dict(os.environ, {"DATABASE_URL": "mytemp"})
    @mock.patch.dict(os.environ, {"SQLALCHEMY_DATABASE_URI": "mytemp"})
    def test_connect(self):
        client = socketio.test_client(app)

        self.assertTrue(client.is_connected())

        self.assertNotEqual(client.sid)
        # received = client.get_received()
        # self.assertEqual(len(received), 3)
        # self.assertEqual(received[0]['args'], 'connected')
        # self.assertEqual(received[1]['args'], '{}')
        # self.assertEqual(received[2]['args'], '{}')
        client.disconnect()
        self.assertFalse(client.is_connected())


    def test_send(self):
        client = socketio.test_client(app)
        client.get_received()
        client.send('echo this message back')
        received = client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'echo this message back')

    def test_disconnect(self):

        global disconnected
        disconnected = None
        client = socketio.test_client(app)
        client.disconnect()
        self.assertEqual(disconnected, '/')

    def test_send_json(self):
        client1 = socketio.test_client(app)

        client1.get_received()

        client1.send({'a': 'b'}, json=True)
        received = client1.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args']['a'], 'b')


    def test_broadcast(self):
        client1 = socketio.test_client(app)
        client2 = socketio.test_client(app)
        client3 = socketio.test_client(app, namespace='/test')
        client2.get_received()
        client3.get_received('/test')
        client1.emit('my custom broadcast event', {'a': 'b'}, broadcast=True)
        received = client2.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(len(received[0]['args']), 1)
        self.assertEqual(received[0]['name'], 'my custom response')
        self.assertEqual(received[0]['args'][0]['a'], 'b')
        self.assertEqual(len(client3.get_received('/test')), 0)

    def test_delayed_init(self):
        app = Flask(__name__)
        socketio = SocketIO(allow_upgrades=False, json=flask_json)

    def test_error_handling_default(self):
        client = socketio.test_client(app, namespace='/unused_namespace')
        client.get_received('/unused_namespace')
        global error_testing_default
        error_testing_default = False
        client.emit("error testing", "", namespace='/unused_namespace')
        self.assertTrue(error_testing_default)

    def test_on_emit_message(self):
        app = on_new_message()

