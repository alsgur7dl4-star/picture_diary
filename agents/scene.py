import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """You are a scene extraction assistant for a picture diary application.

Extract exactly 4 scenes from the diary text provided by the user.

Return ONLY a JSON object with no additional text, explanation, or markdown.
The JSON must follow this exact structure:

{
  "scenes": [
    {
      "scene_id": 1,
      "scene_kr": "장면 설명 (한국어)",
      "prompt_en": "English image generation prompt including shot type, camera angle, lighting, and watercolor diary illustration style"
    },
    ...
  ]
}

Rules:
- The top-level key must be "scenes".
- There must be exactly 4 scene objects.
- scene_id must be an integer from 1 to 4.
- scene_kr must be a Korean description of the scene.
- prompt_en must be written entirely in English.
- prompt_en must include: shot type (e.g. wide shot, close-up, medium shot), camera angle (e.g. eye-level, low angle, bird's eye view), lighting description (e.g. soft morning light, golden hour, dim interior light), and end with "watercolor diary illustration style".
- Do not include any text outside the JSON object."""


def extract_scenes(diary_text: str) -> list[dict]:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1500,
    )
    data = json.loads(response.choices[0].message.content)
    return data.get("scenes", [])


_PROMPT_KEYWORDS = {
    "shot": ["shot", "close-up", "close up"],
    "angle": ["angle", "level", "view"],
    "lighting": ["light", "morning", "evening", "golden", "soft", "dim", "bright", "sky"],
    "watercolor diary illustration": ["watercolor diary illustration"],
}


def validate_scenes(scenes: list[dict]) -> list[str]:
    errors = []
    if len(scenes) != 4:
        errors.append(f"장면 수 오류: 4개여야 하지만 {len(scenes)}개입니다.")
    for i, scene in enumerate(scenes):
        for field in ("scene_id", "scene_kr", "prompt_en"):
            if field not in scene:
                errors.append(f"장면 {i + 1}: '{field}' 필드가 없습니다.")
        if "scene_id" in scene and scene["scene_id"] != i + 1:
            errors.append(f"장면 {i + 1}: scene_id가 {i + 1}이어야 하지만 {scene['scene_id']}입니다.")
        if "prompt_en" in scene:
            prompt = str(scene["prompt_en"]).strip().lower()
            if not prompt:
                errors.append(f"장면 {i + 1}: 'prompt_en'이 비어 있습니다.")
            else:
                for concept, keywords in _PROMPT_KEYWORDS.items():
                    if not any(kw in prompt for kw in keywords):
                        errors.append(f"장면 {i + 1}: prompt_en에 '{concept}' 표현이 없습니다.")
    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"scenes": scenes}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
