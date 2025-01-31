from flask import Flask, request
from database.database_interface import db_interface
from threading import Thread
import time

db = db_interface()
app_2 = Flask(__name__) # by default one server can only listen to one port


@app_2.route('/')
def hello_world():
    return "<p>Hello, World!</p>"


@app_2.post('/update/database')
def new_user():
    data = request.get_json()
    if db.write(**data):
        return 'Data has been saved!'
    return 'Data has not been saved!'

if __name__ == '__main__':
    # thread_2 = Thread(target=run_server, kwargs={'application':app_2, 'port': 5001,})
    # thread_2.start()
    app_2.run(port=5001, debug=True, use_reloader=False)