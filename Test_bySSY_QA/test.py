from rdkit import Chem
from rdkit.Chem import Draw
import os

# 1. 분자 데이터 설정
smiles_list = [
    "C[C@@H](O)C(=O)O",  # L-Lactic acid (S-form)
    "C[C@H](O)C(=O)O",   # D-Lactic acid (R-form)
]

# Legends (분자 개수와 일치하는지 확인)
legends = [
    "(S)-Lactic Acid (L-젖산)", 
    "(R)-Lactic Acid (D-젖산)" 
]

# SMILES를 Mol 객체로 변환
mols_raw = [Chem.MolFromSmiles(s) for s in smiles_list]

# 2. 유효성 검사 및 필터링
valid_mols = [m for m in mols_raw if m is not None]

if len(valid_mols) != len(mols_raw):
    print("주의: 일부 SMILES가 유효하지 않아 제외되었습니다.")
    
if not valid_mols:
    print("오류: 유효한 분자가 없어 이미지를 생성할 수 없습니다.")
    exit()

# 3. 이미지 생성 (Boost.Python 오류가 발생하는 부분)
print(f"유효한 분자 {len(valid_mols)}개로 이미지를 생성합니다...")
img = Draw.MolsToGridImage(
    valid_mols,  
    molsPerRow=2,
    subImgSize=(350, 350),
    # 필터링된 valid_mols에 맞게 legends를 슬라이싱하거나 재구성해야 합니다.
    # 이 경우, 모든 분자가 유효하므로 legends 전체를 사용합니다.
    legends=legends, 
    use_svg=False
)

# 4. 파일 저장 
file_name = 'optical_isomers_lactic_acid.png'
save_path = os.path.join(os.getcwd(), file_name)

try:
    img.save(save_path)
    print(f"이미지 저장 성공: {save_path}")
except Exception as e:
    print(f"이미지 저장 중 오류 발생: {e}")