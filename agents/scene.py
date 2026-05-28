import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


SYSTEM_PROMPT = """
당신은 일기 텍스트를 분석하여 그림일기용 4장면을 추출하는 어시스턴트입니다.

출력은 반드시 JSON 객체여야 하며 다음 스키마를 따르세요:
{
  "scenes": [
    {
      "scene_id": int,
      "scene_kr": "한국어 1줄 장면 설명",
      "prompt_en": "영문 이미지 프롬프트 1줄"
    }
  ]
}

반드시 4개 장면을 추출하세요.
scene_id는 반드시 1, 2, 3, 4 순서로 작성하세요.
scene_kr은 반드시 한국어로 작성하세요.
prompt_en은 반드시 영어로 작성하세요.

prompt_en에는 반드시 다음 요소를 포함하세요:
- wide shot, medium shot, close-up 중 하나
- eye-level, low angle, high angle 중 하나
- soft lighting, rim lighting, backlit lighting 중 하나
- watercolor diary illustration
- quiet everyday mood

장면은 일기 내용의 시간 흐름이 보이도록 구성하세요.
같은 주인공과 같은 동네 분위기가 유지되도록 작성하세요.
민감한 개인정보, 실제 주소, 전화번호, 계정 정보는 포함하지 마세요.

설명 문장 없이 JSON 객체만 반환하세요.
"""


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 없습니다. .env 파일에 OPENAI_API_KEY=... 형식으로 추가하세요."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": diary_text,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1500,
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)

    scenes = data.get("scenes", [])

    if not isinstance(scenes, list):
        raise ValueError("응답 JSON의 scenes 값이 리스트가 아닙니다.")

    return scenes


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면 × 필수 3필드(scene_id, scene_kr, prompt_en)를 충족하는지 검증합니다."""
    errors: list[str] = []
    required_fields = ["scene_id", "scene_kr", "prompt_en"]

    if len(scenes) != 4:
        errors.append(f"장면 수가 4개가 아닙니다. 현재 장면 수: {len(scenes)}")

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            errors.append(f"장면 {index}: 객체 형식이 아닙니다.")
            continue

        for field in required_fields:
            if field not in scene:
                errors.append(f"장면 {index}: {field} 필드가 없습니다.")
            elif scene[field] in ("", None):
                errors.append(f"장면 {index}: {field} 값이 비어 있습니다.")

        if scene.get("scene_id") != index:
            errors.append(
                f"장면 {index}: scene_id가 {index}이 아닙니다. 현재 값: {scene.get('scene_id')}"
            )

        prompt_en = scene.get("prompt_en", "")
        if isinstance(prompt_en, str):
            lower_prompt = prompt_en.lower()

            has_shot = any(
                word in lower_prompt
                for word in ["wide shot", "medium shot", "close-up", "close up"]
            )
            has_angle = any(
                word in lower_prompt
                for word in ["eye-level", "eye level", "low angle", "high angle"]
            )
            has_lighting = any(
                word in lower_prompt
                for word in [
                    "soft lighting",
                    "rim lighting",
                    "backlit",
                    "backlit lighting",
                ]
            )
            has_style = "watercolor diary illustration" in lower_prompt

            if not has_shot:
                errors.append(f"장면 {index}: prompt_en에 shot 표현이 없습니다.")
            if not has_angle:
                errors.append(f"장면 {index}: prompt_en에 angle 표현이 없습니다.")
            if not has_lighting:
                errors.append(f"장면 {index}: prompt_en에 lighting 표현이 없습니다.")
            if not has_style:
                errors.append(
                    f"장면 {index}: prompt_en에 watercolor diary illustration 스타일이 없습니다."
                )

    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장합니다."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            {"scenes": scenes},
            file,
            ensure_ascii=False,
            indent=2,
        )
