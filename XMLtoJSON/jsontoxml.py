import json
import xmltodict
import os
from collections import OrderedDict

def convert_json_file_to_xml(json_file_path, root_name=None):
    """
    JSON 파일을 읽어 XML로 변환하고, 같은 경로에 새 XML 파일로 저장합니다.
    
    :param json_file_path: 입력 JSON 파일의 전체 경로
    :param root_name: XML 문서의 최상위 루트 태그 이름 (JSON이 단일 루트를 가지면 None)
    """
    try:
        # 1. 파일 읽기 및 딕셔너리 로드 (순서 유지를 위해 OrderedDict 사용)
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data_dict = json.load(json_file, object_pairs_hook=OrderedDict)
        
        # 2. XML 변환을 위한 최종 딕셔너리 준비
        if root_name:
            # 루트 이름이 지정된 경우, 전체 딕셔너리를 해당 이름으로 감쌉니다.
            final_dict = {root_name: data_dict}
        else:
            # JSON 자체가 단일 루트를 가진 경우 (예: {"RecipeManager": {...}}) 그대로 사용합니다.
            final_dict = data_dict
            
        # 3. XML 문자열 생성
        xml_data = xmltodict.unparse(final_dict, 
                                     full_document=True, 
                                     pretty=True)
        
        # XML 선언 변경 (선택 사항: <?xml version="1.0" standalone="yes"?> 로 변경)
        xml_data = xml_data.replace(
            '<?xml version="1.0" encoding="utf-8"?>', 
            '<?xml version="1.0" standalone="yes"?>'
        )

        # 4. 출력 파일 경로 설정
        # 입력 파일 경로에서 확장자만 .xml로 변경합니다.
        base_name = os.path.splitext(json_file_path)[0]
        xml_file_path = base_name + '.xml'
        
        # 5. XML 파일 저장
        with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_data)
        
        print(f"✅ 변환 완료 및 저장: '{json_file_path}' -> '{xml_file_path}'")
        
    except FileNotFoundError:
        print(f"❌ 오류: 파일을 찾을 수 없습니다. 경로를 확인하세요: {json_file_path}")
    except json.JSONDecodeError:
        print(f"❌ 오류: JSON 파일 형식이 올바르지 않습니다: {json_file_path}")
    except Exception as e:
        print(f"❌ 변환 중 오류 발생: {e}")

convert_json_file_to_xml('result.json')