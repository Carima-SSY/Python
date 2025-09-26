import json
import xmltodict

def xml_to_json(xml_file_path, json_file_path):
    """
    XML 파일을 JSON 파일로 변환합니다.
    """
    try:
        # 1. XML 파일 읽기
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_data = xml_file.read()
            
        # 2. xmltodict를 사용하여 XML 데이터를 파이썬 딕셔너리로 변환
        # xmltodict.parse()는 XML을 딕셔너리로 변환합니다.
        data_dict = xmltodict.parse(xml_data)
        
        # 3. json.dumps()를 사용하여 딕셔너리를 JSON 문자열로 변환
        # indent=4는 가독성을 높이기 위해 JSON 출력을 예쁘게(pretty print) 만듭니다.
        json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)
        
        # 4. JSON 문자열을 파일에 쓰기
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
        
        print(f"✅ 변환 완료: '{xml_file_path}' -> '{json_file_path}'")
        
    except FileNotFoundError:
        print(f"❌ 오류: 파일을 찾을 수 없습니다. 경로를 확인하세요: {xml_file_path}")
    except Exception as e:
        print(f"❌ 변환 중 오류 발생: {e}")


xml_to_json('SaveFile.xml', 'result1.json')