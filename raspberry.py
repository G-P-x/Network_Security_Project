import requests

url_2 = "http://127.0.0.1:5001"

bad_data = {
    'username': 'user',
    'password': 'password',
}

response_2 = requests.post(url_2 + '/update/database', json=bad_data)
print(response_2.text)