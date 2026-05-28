import base64
import time
import requests
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
import fal_client

load_dotenv()

COMMON_STYLE = (
    "watercolor diary illustration, soft gray-blue morning palette, "
    "a single young man waiting quietly, consistent main character, "
    "quiet early morning bus stop atmosphere"
)


def _call_openai_image(prompt: str) -> bytes:
    client = OpenAI()
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="medium",
        n=1,
    )
    return base64.b64decode(response.data[0].b64_json)


def _call_flux(prompt: str, seed: int = 42) -> str:
    result = fal_client.run(
        "fal-ai/flux/schnell",
        arguments={"prompt": prompt, "num_images": 1, "seed": seed},
    )
    return result["images"][0]["url"]


def generate_image(
    prompt: str,
    output_path: str | None = None,
    model: str = "dalle",
    seed: int = 42,
) -> str:
    if output_path is None:
        auto_dir = Path("outputs") / "ab_test"
        auto_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(auto_dir / f"{model}_seed{seed}_{int(time.time() * 1000)}.png")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    m = model.lower()
    if m in ("dalle", "openai", "gpt-image-1"):
        image_bytes = _call_openai_image(prompt)
        out.write_bytes(image_bytes)
    elif m == "flux":
        url = _call_flux(prompt, seed=seed)
        resp = requests.get(url)
        resp.raise_for_status()
        out.write_bytes(resp.content)
    else:
        raise ValueError(f"지원하지 않는 모델: {model}")

    return str(out)


def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    saved = []
    for scene in scenes:
        scene_id = scene["scene_id"]
        prompt = scene["prompt_en"] + ", " + COMMON_STYLE
        out_path = str(out_dir / f"scene_{scene_id}.png")
        try:
            print(f"[{scene_id}/4] 생성 중: {scene['scene_kr']}")
            path = generate_image(prompt, out_path, model=model)
            print(f"  -> 저장: {path}")
            saved.append(Path(path))
        except Exception as e:
            print(f"  [오류] scene_{scene_id} 실패: {e}")
    return saved
