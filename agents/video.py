import time
import requests
from pathlib import Path

from dotenv import load_dotenv
import fal_client

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"


def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    handler = fal_client.submit(
        KLING_MODEL,
        arguments={
            "image_url": image_url,
            "prompt": prompt,
            "duration": duration,
        },
    )
    return handler.request_id


def status_kling(request_id: str) -> str:
    s = fal_client.status(KLING_MODEL, request_id)
    if isinstance(s, fal_client.Queued):
        return "IN_QUEUE"
    elif isinstance(s, fal_client.InProgress):
        return "IN_PROGRESS"
    elif isinstance(s, fal_client.Completed):
        return "FAILED" if s.error else "COMPLETED"
    return "UNKNOWN"


def result_kling(request_id: str) -> str:
    result = fal_client.result(KLING_MODEL, request_id)
    return result["video"]["url"]


def generate_video(image_path: str, output_path: str) -> str:
    image_url = fal_client.upload_file(image_path)
    prompt = "slow zoom in, gentle camera movement, cinematic, soft motion"

    request_id = submit_kling(image_url, prompt)

    for _ in range(60):
        status = status_kling(request_id)
        if status == "COMPLETED":
            break
        if status == "FAILED":
            raise RuntimeError(f"영상 생성 실패: {request_id}")
        time.sleep(5)
    else:
        raise TimeoutError(f"영상 생성 시간 초과: {request_id}")

    video_url = result_kling(request_id)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(video_url)
    resp.raise_for_status()
    out.write_bytes(resp.content)

    return str(out)
