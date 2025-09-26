from PIL import Image
import base64

img = Image.open("Preview_TFR.png")
#img.save("output.png", optimize=True)


# 원하는 크기로 조절 (예: 가로 800px, 세로 자동 비율)
new_width = 180
w_percent = new_width / float(img.size[0])
new_height = int((float(img.size[1]) * float(w_percent)))
img_resized = img.resize((new_width, new_height), Image.LANCZOS)

# 저장
img_resized.save("output.webp", format="WEBP", quality=80)

# WebP 파일 읽기 (바이너리 모드)
with open("output.webp", "rb") as image_file:
    encoded_bytes = base64.b64encode(image_file.read())

# 문자열로 디코딩 (utf-8)
encoded_str = encoded_bytes.decode('utf-8')

# 출력
print(encoded_str)