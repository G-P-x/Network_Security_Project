from flask import Flask, request
# from database.database_interface import db_interface

app = Flask(__name__)
# db = db_interface()

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/debug_path_get', methods=['GET'])
def debug_path_get():
    return "Data sended through a get request!"

@app.route('/debug_path_post', methods=['POST'])
def debug_path():
    try: 
        print(request)
        data = request.get_json()
        print(data)
        return "Data received!"
    except Exception as e:
        print(e)
        return "Data not received!"

# @app.post('/sign_in')
# def new_user():
#     data = request.get_json()
#     if db.sign_in(**data):
#         return 'Data has been saved!'
#     return 'Data has not been saved!'

# @app.post('/login')
# def get_user():
#     data = request.get_json()
#     if db.login(**data):
#         return 'User found!'
#     return 'User not found!'


if __name__ == '__main__':
    # app.run(host= "0.0.0.0",port=5000, debug=True, use_reloader=False) # accept conncetion from virtual machine
    # curl 192.168.1.56:5000 on virtual machine
    app.run(port=5000, debug=True, use_reloader=True) # accept connection from local machine only,
    # let's test if the virtual machine can connect to the firewall that can connect to the flask server
    
    # app.run(ssl_context=('cert.pem', 'key.pem'),port=5000, debug=True, use_reloader=True) # run this to enable https on this server