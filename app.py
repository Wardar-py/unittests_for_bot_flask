from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import os
import flask
import flask_sqlalchemy
import flask_socketio
from flask import Response

import bot
import time
db = None

MESSAGES_RECEIVED_CHANNEL = None

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = flask_socketio.SocketIO(app)
def config():

    #----------------------------------------------------------------------------------------------------------------------


    socketio.init_app(app, cors_allowed_origins="*")
    dotenv_path = join(dirname(__file__), 'sql.env')
    load_dotenv(dotenv_path)
    os.environ['SQL_USER']= "test"
    sql_user = os.environ['SQL_USER']
    MESSAGES_RECEIVED_CHANNEL = 'messages received'
    os.environ['SQL_PASSWORD'] = "test"
    sql_pwd = os.environ['SQL_PASSWORD']
    os.environ['USER'] = "test"
    dbuser = os.environ['USER']
    os.environ['DATABASE_URL'] = "https://stackoverflow.com/questions/31582750/" \
                                 "python-mock-patch-os-environ-and-return-value"
    database_uri = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://webuser:web_password@localhost/webuser_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #--------------------------------------------------------------------------------------------------------
    db = flask_sqlalchemy.SQLAlchemy(app)
    db.init_app(app)
    db.app = app
    Response = bot.chat()

    # class User(db.Model):
    #     __tablename__ = 'users'
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String, unique=True, nullable=False)
    #     email = db.Column(db.String, unique=True, nullable=False)
    #     message = db.Column(db.String(255), unique=False, nullable=False)
    #     stamp = db.Column(db.TIME, unique=True, nullable=False)
    #     from_name = db.Column(db.String(255), unique=False)
    #     from_avatar = db.Column(db.String(255), unique=False)
    #     db.session.add(User(name="Flask", email="example@example.com"))
    #     db.session.commit()

        # users = User.query.all()

    try:
        db.session.execute(
            """CREATE TABLE messages (
                id serial PRIMARY KEY,
                message VARCHAR ( 255 ) NOT NULL,
                stamp TIMESTAMP NOT NULL,
                from_name VARCHAR ( 255 ),
                from_avatar VARCHAR ( 255 ));""")
        db.session.commit()
    except:
        print("messages db created")
    else:
        print("something wrong")
users = set()
#---------------------------------------------------------------------------------------------------------------------------------------------


def emit_all_messages(channel):
    #messages = visov()
    messages = []
    socketio.emit(channel, {
        'messages': messages,
        'users': len(users)
    })


def visov():
    a = [[db_user.message, str(db_user.stamp), db_user.from_name, db_user.from_avatar]
     for db_user in db.session.execute('message')]
    return a
#---------------------------------------------------------------------------------------------------------------------------------------------


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

#---------------------------------------------------------------------------------------------------------------------------------------------


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

#---------------------------------------------------------------------------------------------------------------------------------------------

@socketio.on('new message input')
def on_new_message(data):

    now = datetime.now()
    new_message = data["message"]
    new_name = data["name"]
    new_avatar = data["avatar"]
    #message(new_message, new_name, new_avatar, now)

    message_value = str(new_message)

    if(message_value[:2] == '!!'):
        now = datetime.now()
        response = Response.response(data["message"]).replace('\'', '\'\'')
        #session(response, now)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

def message(new_message,new_name, new_avatar, now):
    db.session.execute("INSERT INTO messages (message, stamp, from_name, from_avatar) VALUES ('" +
                       new_message + "','" + str(now) + "', '" + new_name + "', '" + new_avatar + "');")
    db.session.commit()

def session(response, now):
    db.session.execute("INSERT INTO messages (message, stamp, from_name) VALUES ('" +
                       response + "','" + str(now) + "', 'bot');")
    db.session.commit()
#---------------------------------------------------------------------------------------------------------------------------------------------


@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")



if __name__ == '__main__':
    config()
    socketio.run(
        app,
        host=os.getenv('IP', '127.0.0.1'),
        port=int(os.getenv('PORT', 8082)),
        debug=True
    )
