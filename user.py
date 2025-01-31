import requests

class user():
    def __init__(self, url = "http://127.0.0.1:5000/update/database" ):
        self.url_to_connect = url
        self.ip_address = self.url_to_connect.split('//')[1].split(':')[0]


        
url_1 = "http://127.0.0.1:5000"

good_data = {
    'username': 'username',
    'password': 'password'
}

response = requests.post(url_1 + '/update/database', json=good_data)

print(response.text + 'ciao')
