import requests

class user():
    def __init__(self, url = "http://127.0.0.1:5000/update/database" ):
        self.url_to_connect = url
        self.ip_address = self.url_to_connect.split('//')[1].split(':')[0]


        
url = "https://10.50.172.110:5100"

good_data = {
    'username': 'username',
    'password': 'password',
    'altri dati': 'altri dati a caso',
}

# response = requests.get(url + "/debug_path_get", verify=False)
# print(response.status_code)
# print(response.text)
try:
    response_2 = requests.post(url + "/debug_path_post", json=good_data, verify=False)
    print(response_2.text)
    print(response_2.status_code)
except Exception as e:
    print(e)

# connect directly to the flask server
# response = requests.post("https://127.0.0.1:5000/debug_path_post", json=good_data, verify=False)
# print(response.text)
# print(response.status_code)