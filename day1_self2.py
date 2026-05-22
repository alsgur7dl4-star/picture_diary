import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

SCENE_BASE = (
    "early morning alley, wet pavement with fallen autumn leaves, "
    "old streetlamp still lit, quiet street, watercolor diary illustration"
)

def build_prompt_variants() -> list[tuple[str, str]]:
    variants: list[tuple[str, str]] = [
        (
            "scene01_ws.png",
            f"wide shot, eye-level angle, rim light, {SCENE_BASE}",
        ),
        (
            "scene01_cu.png",
            f"close-up shot, eye-level angle, soft front light, {SCENE_BASE}",
        ),
        (
            "scene01_low.png",
            f"low angle shot, backlit, dramatic atmosphere, {SCENE_BASE}",
        ),
    ]
    return variants


def call_dalle(client: OpenAI, prompt: str) -> bytes:
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="medium",
        n=1,
    )
    return base64.b64decode(response.data[0].b64_json)


def save_image(image_bytes: bytes, out_path: Path) -> None:
    out_path.write_bytes(image_bytes)


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    variants = build_prompt_variants()
    for filename, prompt in variants:
        print(f"[호출 시작] {filename} ...")
        try:
            image_bytes = call_dalle(client, prompt)
            save_image(image_bytes, output_dir / filename)
            print(f"[저장 완료] {filename} ({len(image_bytes):,} bytes)")
        except Exception as e:
            print(f"[실패] {filename}: {e}")
            continue

    print("\n끝. outputs/ 폴더에서 3장을 비교해 보세요.")
