import json
import sys
from datetime import date
from pathlib import Path

from agents.image import batch_generate

model = "openai"

# --- 입력 파일 로드 ---
input_path = Path("scene_extracted.json")
if not input_path.exists():
    fallback = Path("outputs/scene_test.json")
    if fallback.exists():
        input_path = fallback
        print(f"scene_extracted.json 없음 → 대체 파일 사용: {fallback}")
    else:
        print("오류: scene_extracted.json 파일을 찾을 수 없습니다.")
        sys.exit(1)

data = json.loads(input_path.read_text(encoding="utf-8"))
scenes = data.get("scenes", [])

if not scenes:
    print("오류: scenes 배열이 비어 있습니다.")
    sys.exit(1)

today = date.today().isoformat()
out_dir = Path("outputs") / today

print(f"모델: {model}")
print(f"출력 폴더: {out_dir}")
print(f"장면 수: {len(scenes[:4])}\n")

saved_paths = batch_generate(scenes[:4], model, out_dir)

print(f"\n총 {len(saved_paths)}장 저장 완료:")
for p in saved_paths:
    print(f"  {p}")
