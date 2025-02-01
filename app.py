from flask import Flask, request
from database.database_interface import db_interface
from threading import Thread
import time

app = Flask(__name__)
db = db_interface()


@app.post('/update/database')
def new_user():
    data = request.get_json()
    if db.sign_in(**data):
        return 'Data has been saved!'
    return 'Data has not been saved!'

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)