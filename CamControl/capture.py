import cv2, time, base64, io, json
from PIL import Image

start_time = time.time()
camera_index = 0

cap = cv2.VideoCapture(camera_index)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print(f"Error: Camera with index {camera_index} could not be opened.")
    exit()
    

while True:
    try:
        ret, frame = cap.read()
        if ret:
            file_name = f"TEST/cap-{int(time.time())}.webp"
            _, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 70])
            # img_bytes = io.BytesIO(buffer).getvalue()
            # img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            # with open("test.json", "w") as f:
            #     json.dump({"image": img_base64}, f)
            bio = io.BytesIO()
            bio.write(buffer.tobytes())
            bio.seek(0) 
            with open(file_name, 'wb') as f:
                f.write(bio.read())
            # cv2.imwrite(file_name, buffer.tobytes())
            # img =Image.open(file_name).convert("RGB")
            # img.save("processed.webp", "webp", quality=80)
            time.sleep(1)
        else:
            print("Failed to capture frame from camera.")
    except Exception as e:
        print(f"Exception during image capture: {e}")
        break
        
cap.release()
