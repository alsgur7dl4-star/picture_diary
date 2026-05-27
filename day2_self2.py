import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client


def load_keys() -> None:
    load_dotenv()
    key = os.getenv("FAL_KEY")
    if not key:
        print("[오류] FAL_KEY가 .env 파일에 없습니다. .env에 FAL_KEY=... 를 추가해 주세요.")
        raise SystemExit(1)
    print(f"FAL_KEY: {key[:5]}...")


def load_first_prompt() -> str:
    path = Path("scene_prompts.json")
    if not path.exists():
        print("[오류] scene_prompts.json 파일을 찾을 수 없습니다.")
        raise SystemExit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    if not scenes:
        print("[오류] scene_prompts.json에 scenes 항목이 비어 있습니다.")
        raise SystemExit(1)
    return scenes[0]["prompt_en"]


def call_flux_schnell(prompt: str) -> str:
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={"prompt": prompt, "num_images": 1},
    )
    return result["images"][0]["url"]


def save_image(url: str, out_path: Path) -> None:
    response = requests.get(url)
    response.raise_for_status()
    out_path.write_bytes(response.content)


if __name__ == "__main__":
    load_keys()

    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt}")

    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url}")

    out_path = Path("outputs") / "scene01_fal.png"
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")
