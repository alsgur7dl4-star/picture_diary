# 글로 쓰는 그림일기 — Picture Diary

## 프로젝트 소개

한국어 일기 한 편을 입력하면 4개 장면으로 나눠 수채화풍 이미지와 짧은 영상으로 만들어 주는 멀티 에이전트 파이프라인입니다.

## 빠른 시작

```bash
# 1. 의존성 설치
uv sync                         # 또는: pip install -r requirements.txt

# 2. .env 파일에 API 키 설정 (커밋 금지 — .gitignore로 제외됨)
#    OPENAI_API_KEY=your-key-here
#    FAL_KEY=your-key-here
```

```python
# 3. 파이프라인 실행 (예시)
from pathlib import Path
from pipeline import picture_diary_pipeline

diary = Path("diary.md").read_text(encoding="utf-8")
picture_diary_pipeline(diary, model="flux")   # 결과는 outputs/<날짜>/ 에 저장
```

- 장면 추출: `agents/scene.py` (gpt-4o-mini)
- 이미지 생성: `agents/image.py` (gpt-image-1 또는 flux/schnell)
- 영상 생성: `agents/video.py` (kling, 비동기 폴링)

## 결과 미리보기

생성 결과물(`outputs/`)은 용량과 보안을 이유로 `.gitignore`로 제외되어 있습니다.
따라서 **GitHub에는 이미지/영상이 포함되지 않으며, 로컬에서 파이프라인을 실행하면 생성됩니다.**

로컬 실행 시 다음 경로에 4개 장면이 만들어집니다(파일은 저장소에 없음):

| 장면 | 설명                      | 로컬 생성 경로               |
| ---- | ------------------------- | ---------------------------- |
| 1    | 이른 아침 버스정류장 전경 | `outputs/<날짜>/scene_1.png` |
| 2    | 젖은 보도블록 위 낙엽     | `outputs/<날짜>/scene_2.png` |
| 3    | 벤치에서 음악 듣는 인물   | `outputs/<날짜>/scene_3.png` |
| 4    | 초록색 버스 도착          | `outputs/<날짜>/scene_4.png` |
| 영상 | 1번 장면 기반 짧은 영상   | `outputs/<날짜>/scene_1.mp4` |

## 운영 지표

5일 누적 비용은 `cost_report.md`를 기준으로 정리했습니다(단가 기준일: 2026-05-29). 아직 단가를 측정하지 않은 항목은 `~`로 둡니다(가짜 값 없음).

| Day   | 주요 작업           | 호출 수 | 단가 또는 추정 단가 | 합계 |
| ----- | ------------------- | ------: | ------------------: | ---: |
| Day 1 | 환경 확인과 첫 호출 |    미정 |                   ~ |    ~ |
| Day 2 | 장면 JSON 생성      |    미정 |                   ~ |    ~ |
| Day 3 | 이미지 생성         |    미정 |                   ~ |    ~ |
| Day 4 | 영상 생성           |    미정 |                   ~ |    ~ |
| Day 5 | 도메인 A/B 테스트   |       2 |                   ~ |    ~ |
| 합계  |                     |    미정 |                     |    ~ |

README 이관 값:

| 항목           |    값 |
| -------------- | ----: |
| p95_latency_s  | 2.666 |
| cost_per_image |     ~ |
| total_cost_usd |     ~ |

## A/B 테스트 요약

동일 프롬프트에 seed만 바꿔 flux/schnell 지연을 비교했습니다(출처: `ab_test_results.json`).

| 그룹 | seed | P95 지연(초) |
| ---- | ---: | -----------: |
| A    |   42 |        2.666 |
| B    |  137 |        1.768 |

- 대표 지연(README 이관): **p95_latency_s = 2.666초** (= max(p95_a, p95_b))
- 호출 수: 그룹당 1회 (n_calls = 1)
- 프롬프트는 A·B 동일하며 seed만 다릅니다.

## 도메인 응용

선택한 도메인은 여행 입니다(`domains/travel_prompts.json`). 여행 기록 스타일에 맞춘 공통 시각 어휘를 정의해 4개 장면 프롬프트에 적용합니다.

- 공통 스타일: wide / eye-level / golden hour·soft natural lighting / 35mm wide-angle lens / warm·nostalgic·wanderlust
- 각 장면은 한국어 `diary_sentence` + 영어 `visual_focus` + 영어 `prompt_addons`로 구성됩니다.
- 예) 장면 1 — "이른 아침 버스정류장에서 혼자 버스를 기다렸다." + `empty bus stop at dawn` + `golden hour lighting, quiet street, travel blog photography`

## 파일 구조

```
picture_diary/
├── pipeline.py              # 장면 추출 → 이미지 → 영상 통합 함수
├── main.py                  # 실행 스텁
├── agents/
│   ├── scene.py             # 일기 → 4장면 JSON 추출
│   ├── image.py             # 장면 → 이미지 생성
│   └── video.py             # 이미지 → 영상 생성 (비동기 폴링)
├── guardrails.py            # 반복/시간/비용 제한 가드레일
├── domains/
│   └── travel_prompts.json  # travel 도메인 시각 어휘
├── ab_test.py               # seed A/B 지연 측정 + P95 계산
├── day5_self1.py            # A/B 실행 + 결과·비용 리포트 생성
├── ab_test_results.json     # A/B 측정 결과
├── cost_report.md           # 5일 누적 비용 + P95 리포트
├── final_check.py           # push 전 .env 안전 점검
├── day1_self1.py            # 실습 산출물
├── day1_self2.py            # 실습 산출물
├── day2_self1.py            # 실습 산출물
├── day2_self2.py            # 실습 산출물
├── day3_self1.py            # 실습 산출물
├── day3_self2.py            # 실습 산출물
├── day4_self1.py            # 실습 산출물
├── day4_self2.py            # 실습 산출물
└── day5_self1.py            # 실습 산출물
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── README.md
└── week7_retrospective.md
```

`outputs/`와 `.env`는 `.gitignore`로 제외되어 저장소에 포함되지 않습니다.

## 보안

- API 키는 `.env`에만 두고 `load_dotenv()`로 로드합니다(코드·문서에 하드코딩 없음).
- `.gitignore`에 `.env`가 포함되어 있고, `python final_check.py`로 push 전 노출 여부를 점검합니다.

## 라이선스

MIT License
