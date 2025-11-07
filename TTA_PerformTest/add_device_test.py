import requests
import json

api_url = 'https://api.c-hub.info/api/user/device/'


for i in range(1,300):
    try:
        response = requests.post(api_url+str(50+i)+"/", json={
            "name": f"tta_device_{i}",
            "type": "IML",
            "serial_key": "SU1M#MjEwMzIyNA==#2103224"
        })

        print(f"STATUS CODE {response.status_code}")
        print(f"HEADER: {response.headers}")

        if response.status_code == 200 or response.status_code == 201:
            print("REQ SUCCESS")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print("REQ FAILURE")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"EXCEPTION ERROR in {i}: {str(e)}")