import numpy as np
import os
from skimage import io, measure
from stl import mesh # numpy-stl 라이브러리 사용

def create_3d_object_from_slices(slice_dir, output_filename, isolevel=0.5):
    """
    2D 슬라이스 이미지 폴더에서 3D 오브젝트(.stl)를 생성합니다.

    :param slice_dir: 2D 슬라이스 이미지 파일들이 있는 디렉토리 경로
    :param output_filename: 생성될 .stl 파일의 이름
    :param isolevel: Marching Cubes 알고리즘에 사용할 임계값 (0.0~1.0 사이, 이미지 값에 따라 조정 필요)
    """
    
    # 1. 이미지 로드 및 3D 볼륨 스택 생성
    
    # 디렉토리 내의 모든 이미지 파일 이름을 알파벳 순서(순서대로)로 가져옵니다.
    files = sorted([f for f in os.listdir(slice_dir) if f.endswith(('.png', '.tif', '.jpg'))])
    
    if not files:
        print(f"오류: '{slice_dir}' 디렉토리에서 이미지 파일을 찾을 수 없습니다.")
        return

    # 첫 번째 이미지를 로드하여 데이터 타입과 크기를 확인합니다.
    first_slice = io.imread(os.path.join(slice_dir, files[0]), as_gray=True)
    slices = [first_slice]

    # 나머지 이미지를 로드하고 스택에 추가합니다.
    for filename in files[1:]:
        img = io.imread(os.path.join(slice_dir, filename), as_gray=True)
        slices.append(img)
    
    # 2D 슬라이스들을 쌓아 3D NumPy 배열 (볼륨)을 생성합니다. (Z, Y, X 축)
    volume = np.stack(slices, axis=0)

    # 볼륨 데이터를 0.0과 1.0 사이로 정규화합니다. (Marching Cubes에 유리)
    volume = volume.astype(np.float64) / volume.max()
    
    print(f"3D 볼륨 생성 완료. 크기: {volume.shape}")

    # 2. Marching Cubes 알고리즘 적용 (표면 재구성)
    
    # isolevel(임계값)을 기준으로 메쉬의 꼭짓점(verts)과 면(faces)을 추출합니다.
    # isolevel보다 높은 값은 오브젝트 내부, 낮은 값은 외부로 간주됩니다.
    verts, faces, normals, values = measure.marching_cubes(
        volume,      # 3D 볼륨 데이터
        level=isolevel, # 임계값 (이 값으로 오브젝트와 배경을 구분)
        spacing=(1.0, 1.0, 1.0) # 픽셀 간격. 실제 물리적 간격이 있다면 여기에 지정합니다.
    )

    print(f"Marching Cubes 적용 완료. 꼭짓점 수: {len(verts)}, 면 수: {len(faces)}")

    # 3. .stl 파일 생성 및 저장
    
    # numpy-stl 라이브러리를 사용하여 메쉬 객체를 생성합니다.
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    
    for i, f in enumerate(faces):
        # 면(face)은 꼭짓점(vertex) 인덱스를 나타냅니다.
        for j in range(3):
            mesh_data.vectors[i][j] = verts[f[j],:]

    # STL 파일로 저장
    mesh_data.save(output_filename)
    
    print(f"3D 오브젝트 파일이 '{output_filename}'으로 성공적으로 저장되었습니다. 🎉")

# --- 사용 예시 ---
# 1. 'slices'라는 이름의 폴더를 만들고, 거기에 순서대로 된 슬라이스 이미지 파일들을 넣습니다.
#    예: slice_001.png, slice_002.png, ..., slice_N.png

# 2. 함수 호출
slice_directory = "slices" # 이미지 슬라이스가 있는 폴더 경로
output_file = "reconstructed_object.stl"
isolevel_value = 0.5 # 이미지의 특성에 맞게 이 값을 조정해야 할 수 있습니다.

create_3d_object_from_slices(slice_directory, output_file, isolevel_value) 
# 실제 사용 시 위 주석을 해제하고 실행하세요.