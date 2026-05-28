import sys
import time
import requests
from datetime import date
from pathlib import Path

from guardrails import check_max_iter, check_timeout, check_predicate
from agents.video import status_kling, result_kling
from pipeline import picture_diary_pipeline

task_id_path = Path("kling_task_id.txt")
if not task_id_path.exists():
    print("오류: kling_task_id.txt 없음.")
    sys.exit(1)

task_id = task_id_path.read_text(encoding="utf-8").strip()
if not task_id:
    print("오류: task_id가 비어 있습니다.")
    sys.exit(1)

print(f"task_id: {task_id}")

start_ts = time.time()
iteration = 0
status = ""

while check_max_iter(iteration) and check_timeout(start_ts):
    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")
    if check_predicate(status):
        break
    if status == "FAILED":
        print("오류: 영상 생성 실패")
        sys.exit(1)
    time.sleep(5)
    iteration += 1

if not check_predicate(status):
    print("오류: 타임아웃 또는 최대 반복 횟수 초과")
    sys.exit(1)

video_url = result_kling(task_id)
print(f"video_url: {video_url}")

today = date.today().isoformat()
out_dir = Path("outputs") / today
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "scene_1.mp4"

resp = requests.get(video_url)
resp.raise_for_status()
out_path.write_bytes(resp.content)
print(f"저장 완료: {out_path} ({out_path.stat().st_size:,} bytes)")

diary_text = Path("diary.md").read_text(encoding="utf-8")
result = picture_diary_pipeline(diary_text, animate_first=False)
print(result)
