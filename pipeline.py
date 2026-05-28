import json
from datetime import date
from pathlib import Path

from agents.scene import extract_scenes
from agents.image import generate_image
from agents.video import generate_video

COMMON_STYLE = (
    "watercolor diary illustration, soft gray-blue morning palette, "
    "a single young man waiting quietly, consistent main character, "
    "quiet early morning bus stop atmosphere"
)


def picture_diary_pipeline(
    diary_text: str,
    model: str = "dalle",
    animate_first: bool = True,
) -> dict:
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    scenes = extract_scenes(diary_text)

    image_paths: list[str] = []
    for i, scene in enumerate(scenes, 1):
        prompt = scene["prompt_en"] + ", " + COMMON_STYLE
        output_path = str(out_dir / f"scene_{i}.png")
        try:
            path = generate_image(prompt, output_path, model=model)
            image_paths.append(path)
        except Exception as e:
            print(f"[오류] scene_{i} 이미지 생성 실패: {e}")

    video_paths: list[str] = []
    if animate_first and image_paths:
        video_path = str(out_dir / "scene_1.mp4")
        try:
            path = generate_video(image_paths[0], video_path)
            video_paths.append(path)
        except Exception as e:
            print(f"[오류] 영상 생성 실패: {e}")

    result = {
        "scenes": scenes,
        "images": image_paths,
        "videos": video_paths,
    }

    Path("results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return result
