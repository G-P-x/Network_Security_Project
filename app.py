from flask import Flask, request
from database.database_interface import db_interface
from threading import Thread
import time

app = Flask(__name__)
db = db_interface()

app_2 = Flask(__name__) # by default one server can only listen to one port


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.get('/message/<sms>')
def return_message(sms: str):
    print(sms)
    new = input(': ')
    return f'<p style="color: red;">{new}</p>'

@app.post('/update/database')
def new_user():
    data = request.get_json()
    if db.write(**data):
        return 'Data has been saved!'
    return 'Data has not been saved!'

@app_2.post('/update/database')
def new_user():
    data = request.get_json()
    if db.write(**data):
        return 'Data has been saved!'
    return 'Data has not been saved!'

def run_server(**kwargs):
    application = kwargs['application']
    assert isinstance(application, Flask)
    port_int = kwargs['port']
    assert isinstance(port_int, int)
    application.run(port=port_int, debug=True, use_reloader=False)

if __name__ == '__main__':
    # thread_1 = Thread(target=run_server, kwargs={'application':app, 'port': 5000, })
    # thread_1.start()
    app.run(port=5000, debug=True, use_reloader=False)