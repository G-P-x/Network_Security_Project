import requests

SERVER_IP_ADDRESS = "192.168.1.56"

url_2 = f"http://{SERVER_IP_ADDRESS}:5100/update/database"

bad_data = {
    'username': 'user',
    'password': 'password',
}

response = requests.post(url_2, json=bad_data)
# response = requests.get(f"http://{SERVER_IP_ADDRESS}:5100/")
print(response.text)