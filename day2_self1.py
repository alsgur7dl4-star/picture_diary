import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]


def load_draft(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def count_scenes(text: str) -> int:
    return len(re.findall(r"^## 장면 \d+", text, re.MULTILINE))


def check_fields(text: str, scene_idx: int) -> list[str]:
    sections = re.split(r"^## 장면 \d+.*$", text, flags=re.MULTILINE)
    # sections[0]: 헤딩 이전 텍스트, sections[1]: 장면 1, sections[2]: 장면 2, ...
    if scene_idx >= len(sections):
        return REQUIRED_FIELDS[:]
    section = sections[scene_idx]
    return [f for f in REQUIRED_FIELDS if not re.search(rf"^\s*-\s+{f}\s*:", section, re.MULTILINE)]


if __name__ == "__main__":
    draft_path = Path("scene_draft.md")
    if not draft_path.exists():
        print("scene_draft.md 파일이 없습니다. picture_diary 폴더에서 실행해 주세요.")
        sys.exit(1)

    text = load_draft(draft_path)
    n = count_scenes(text)
    print(f"[검출] 장면 수: {n}")

    all_ok = True
    for i in range(1, n + 1):
        missing = check_fields(text, i)
        if missing:
            print(f"장면 {i}: 누락 필드 -> {', '.join(missing)}")
            all_ok = False
        else:
            print(f"장면 {i}: OK")

    if all_ok:
        print("[완료] 모든 장면 OK이면 self2로 진행하세요.")
    else:
        print("[경고] 누락 필드를 채운 뒤 다시 실행하세요.")
