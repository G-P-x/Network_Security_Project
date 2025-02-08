import requests
import os
import sys
# Add the Clients directory to the path so I can import get_local_ip
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from get_local_ip import get_local_ip

URL = "https://" + get_local_ip() + ":5100"

good_data = {
    'username': 'username',
    'password': 'password',
    'altri dati': 'altri dati a caso',
}

try:
    response_2 = requests.post(URL + "/debug_path_post", json=good_data, verify=False)
    print(response_2.text)
    print(response_2.status_code)
except Exception as e:
    print(e)
