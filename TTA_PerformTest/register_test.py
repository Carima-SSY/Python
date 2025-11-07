import requests
import json

api_url = 'https://api.c-hub.info/api/user/register/'


for i in range(1,300):
    try:
        response = requests.post(api_url, json={
            "username" : f"testuser{i}",
            "email" : f"tta_test{i}@gmail.com",
            "password" : f"tta_password{i}",
            "phonenumber" : f"010-{i:04d}-{1000-i:04d}",
            "organ" : "worker",
            "organ_department": "QC",
            "organ_position": "-",
            "organ_detail": "-"
        })

        print(f"STATUS CODE {response.status_code}")
        print(f"HEADER:** {response.headers}")

        if response.status_code == 200 or response.status_code == 201:
            print("REQ SUCCESS")
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print("REQ FAILURE")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"EXCEPTION ERRO in {i}: {str(e)}")