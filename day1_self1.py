import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


def load_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY") or ""
    print(f"[환경 확인] OPENAI_API_KEY 첫 5자: {api_key[:5] if api_key else 'None'}")
    return api_key


def build_scene_prompt() -> str:
    return (
        "wide shot, early morning alley, soft orange sunlight, "
        "wet pavement with fallen autumn leaves, old streetlamp still lit, "
        "quiet street, watercolor diary illustration"
    )


def generate_image(client: OpenAI, prompt: str) -> bytes:
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
    load_api_key()
    client = OpenAI()
    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")
    image_bytes = generate_image(client, prompt)
    print(f"[이미지 수신] {len(image_bytes):,} bytes")
    out_path = Path("outputs") / "scene01_dalle.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(image_bytes, out_path)
    print(f"[저장 완료] {out_path}")
