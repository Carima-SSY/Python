import cv2, os, shutil, zipfile
import numpy as np

def create_preview_zip(src_folder, output_file):
    if os.path.exists(f"{src_folder}/preview_temp"): shutil.rmtree(f"{src_folder}/preview_temp")
    os.makedirs(f"{src_folder}/preview_temp")
    
    images = [img for img in os.listdir(src_folder) if img.endswith((".jpg", ".png", ".jpeg", ".webp"))]
    images.sort()
    
    files_to_zip = images[-30:]
    
    for filename in files_to_zip:
        src_path = os.path.join(src_folder, filename)
        dst_path = os.path.join(f"{src_folder}/preview_temp", filename)
        shutil.copy2(src_path, dst_path) # 파일 복사 (메타데이터 포함)
        
    with zipfile.ZipFile(f"{output_file}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(f"{src_folder}/preview_temp"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, f"{src_folder}/preview_temp"))
                
def create_timelapse(image_folder, output_file, fps):

    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".png", ".jpeg", ".webp"))]
    images.sort()
    
    if not images:
        print(f"Error: No images found in {image_folder}")
        return

    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # XVID, MJPG ...
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)
        video.write(image)

    video.release()
    cv2.destroyAllWindows()

IMAGE_DIR = './TEST/' 
OUTPUT_VIDEO = 'timelapse_video.mp4' 
FRAME_RATE = 15

try:
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
        print(f"'{IMAGE_DIR}' folder was created...")
    else:
        create_timelapse(IMAGE_DIR, OUTPUT_VIDEO, FRAME_RATE)
        create_preview_zip(IMAGE_DIR, "preview_images")
except Exception as e:
    print(f"An error occurred: {e}")