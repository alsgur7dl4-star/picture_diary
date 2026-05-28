from pathlib import Path
import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-27" / "scene_1.png"

PROMPT = (
    "A bus moves past the bus stop, sunlight reflects on the side mirror, steady camera"
)

print(type(PROMPT))
print(PROMPT)

if not IMAGE_PATH.exists():
    raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {IMAGE_PATH}")

print(f"업로드 중: {IMAGE_PATH}")
image_url = fal_client.upload_file(str(IMAGE_PATH))
print(f"업로드 완료: {image_url}")

print("Kling submit 중...")
task_id = submit_kling(image_url, PROMPT)
print(f"task_id: {task_id}")

Path("kling_task_id.txt").write_text(task_id, encoding="utf-8")
print("kling_task_id.txt 저장 완료")
