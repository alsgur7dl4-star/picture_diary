import json
from datetime import date
from pathlib import Path

from ab_test import compute_p95, run_ab_test

BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "travel"
N_CALLS = 1


def build_prompt(scene: dict, prompt_style: dict) -> str:
    parts: list[str] = []

    diary_sentence = scene.get("diary_sentence", "").strip()
    if diary_sentence:
        parts.append(diary_sentence)

    visual_focus = scene.get("visual_focus", "").strip()
    if visual_focus:
        parts.append(visual_focus)

    style_parts = [
        prompt_style.get("shot"),
        prompt_style.get("angle"),
        prompt_style.get("lighting"),
        prompt_style.get("lens_or_style"),
        prompt_style.get("mood"),
    ]
    style_str = ", ".join(s for s in style_parts if s)
    if style_str:
        parts.append(style_str)

    addons = scene.get("prompt_addons", [])
    if addons:
        parts.append(", ".join(addons))

    return ", ".join(parts)


def main() -> None:
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"
    domain_data = json.loads(domain_path.read_text(encoding="utf-8"))

    prompt_style = domain_data.get("prompt_style", {})
    scenes = domain_data.get("scenes", [])
    if not scenes:
        raise ValueError(f"{domain_path}에 scene이 없습니다.")

    first_scene = scenes[0]
    prompt = build_prompt(first_scene, prompt_style)
    print(f"[프롬프트] {prompt}\n")

    print(f"[A/B 테스트 시작] domain={DOMAIN_NAME}, n_calls={N_CALLS}")
    ab_result = run_ab_test(prompt, n_calls=N_CALLS)

    p95_a = compute_p95(ab_result["a_latencies"])
    p95_b = compute_p95(ab_result["b_latencies"])
    p95_latency_s = max(p95_a, p95_b)

    results = {
        "domain": DOMAIN_NAME,
        "prompt": prompt,
        "seed_a": ab_result["seed_a"],
        "seed_b": ab_result["seed_b"],
        "a_latencies": ab_result["a_latencies"],
        "b_latencies": ab_result["b_latencies"],
        "p95_a": p95_a,
        "p95_b": p95_b,
        "p95_latency_s": p95_latency_s,
        "n_calls": ab_result["n_calls"],
    }

    results_path = BASE_DIR / "ab_test_results.json"
    results_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[저장] {results_path}")

    cost_per_image = "~"
    total_cost_usd = "~"

    report_lines = [
        "# 그림일기 파이프라인 5일 누적 비용 보고서",
        "",
        "## 기본 정보",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        "| 작성 세션 | Day 5 self1 |",
        f"| 선택 도메인 | {DOMAIN_NAME} |",
        f"| A seed | {ab_result['seed_a']} |",
        f"| B seed | {ab_result['seed_b']} |",
        f"| A/B 호출 수 | A {len(ab_result['a_latencies'])}회 / B {len(ab_result['b_latencies'])}회 |",
        "| 사용 모델 | flux |",
        "",
        "## 5일 누적 비용",
        "",
        "| Day | 주요 작업 | 호출 수 | 단가 또는 추정 단가 | 합계 |",
        "|---|---|---:|---:|---:|",
        "| Day 1 | 환경 확인과 첫 호출 | 미정 | ~ | ~ |",
        "| Day 2 | 장면 JSON 생성 | 미정 | ~ | ~ |",
        "| Day 3 | 이미지 생성 | 미정 | ~ | ~ |",
        "| Day 4 | 영상 생성 | 미정 | ~ | ~ |",
        f"| Day 5 self1 | 도메인 A/B 테스트 | {len(ab_result['a_latencies']) + len(ab_result['b_latencies'])} | ~ | ~ |",
        "| 합계 | | 미정 | | ~ |",
        "",
        "## P95 지연",
        "",
        "| 그룹 | seed | 호출 수 | P95 지연 |",
        "|---|---:|---:|---:|",
        f"| A | {ab_result['seed_a']} | {len(ab_result['a_latencies'])} | {p95_a:.3f}초 |",
        f"| B | {ab_result['seed_b']} | {len(ab_result['b_latencies'])} | {p95_b:.3f}초 |",
        "",
        "## README로 옮길 값",
        "",
        "| 항목 | 값 |",
        "|---|---:|",
        f"| p95_latency_s | {p95_latency_s:.3f} |",
        f"| cost_per_image | {cost_per_image} |",
        f"| total_cost_usd | {total_cost_usd} |",
        "",
    ]
    report_path = BASE_DIR / "cost_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"[저장] {report_path}")

    print("\n[요약]")
    print(f"  p95_a = {p95_a:.3f}s")
    print(f"  p95_b = {p95_b:.3f}s")
    print(f"  p95_latency_s = {p95_latency_s:.3f}s")


if __name__ == "__main__":
    main()
