import json

file_name = "DM400-1-1763618764.json"

try:

    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)


    devdatas = data["data"]
    for devdata in devdatas:
        if devdata['device']['status'] == "PRINTING":
            print("---------------------------------------------------------------------")
            print(f"SENSOR: {devdata['sensor']}")
            print(f"DEVICE: {devdata['device']}")
            print(f"PRINT: {devdata['print']}")
            print("---------------------------------------------------------------------")
except FileNotFoundError:
    print(f"오류: 파일 '{file_name}'을(를) 찾을 수 없습니다.")
except json.JSONDecodeError:
    print(f"오류: 파일 '{file_name}'의 JSON 형식이 올바르지 않습니다.")
except Exception as e:
    print(f"파일을 처리하는 중 오류가 발생했습니다: {e}")