import requests
        
url = "http://127.0.0.1:5100"

try:
    response_2 = requests.get(url)
    print(response_2.text)
    print(response_2.status_code)
except Exception as e:
    print(e)

# connect directly to the flask server
# response = requests.post("http://127.0.0.1:5000/debug_path_post", json=good_data)
# print(response.text)
# print(response.status_code)