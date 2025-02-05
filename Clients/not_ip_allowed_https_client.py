import requests
       
URL = "https://10.50.172.110:5100"

good_data = {
    'username': 'username',
    'password': 'password',
    'altri dati': 'altri dati a caso',
}

# response = requests.get(url + "/debug_path_get", verify=False)
# print(response.status_code)
# print(response.text)
try:
    response_2 = requests.post(URL + "/debug_path_post", json=good_data, verify=False)
    print(response_2.text)
    print(response_2.status_code)
except Exception as e:
    print(e)
