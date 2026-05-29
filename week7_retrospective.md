# 그림일기 프로젝트 — 5일 결과 회고

## Day별 핵심 산출물

| Day   | 핵심 산출물 (파일)                                                                     | 실행 확인                                                             |
| ----- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Day 1 | `diary.md`, `scene_draft.md`                                                           | gpt-image-1 / flux 각 첫 이미지 생성 확인 (`outputs/scene01_*.png`)   |
| Day 2 | `scene_prompts.json`, `scene_draft_seed.md`                                            | shot·angle·lighting 포함 4장면 프롬프트 작성, flux 호출               |
| Day 3 | `agents/scene.py`, `agents/image.py`, `scene_extracted.json`                           | `extract_scenes()`로 일기→4장면 자동 추출, `validate_scenes()` 통과   |
| Day 4 | `agents/video.py`, `guardrails.py`                                                     | `generate_video()` submit→status→result 폴링으로 `scene_1.mp4` 생성   |
| Day 5 | `pipeline.py`, `ab_test.py`, `day5_self1.py`, `ab_test_results.json`, `cost_report.md` | 파이프라인 통합 실행, `run_ab_test()`로 p95 2.666초 산출, 리포트 생성 |

## 잘 된 점

- `agents/`로 장면·이미지·영상 단계를 모듈 분리해 단계별로 교체·테스트 가능.
- `.env` + `load_dotenv()`로 키를 코드 밖으로 분리하고 `.gitignore`로 제외.
- A/B 지연 측정과 P95 계산을 `ab_test.py`로 분리해 재현 가능.
- `pipeline.py`에서 장면별 `try/except`로 한 장면 실패가 전체를 막지 않도록 격리.

## 개선할 점

- `cost_report.md`의 단가·총비용이 아직 `~`(미측정). 단가 기준일을 포함해 실제 비용을 채워야 함.
- 프롬프트가 한국어 `diary_sentence` + 영어 어휘 혼재(`agents`/`day5_self1.py`). flux는 영어 선호라 선두 한국어 문장 처리 검토 필요.
- A/B `n_calls=1`이라 P95 표본이 부족. 호출 수를 늘려 재측정 필요.

## 다음 주 시도할 것

- 호출당 토큰/이미지 수를 기록해 비용 자동 집계.
- travel 도메인에서 golden hour vs blue hour 변형 비교.
- 표본을 늘린 A/B 재측정 후 기준선(baseline) 저장.

## GitHub 저장소

- URL: https://github.com/alsgur7dl4-star/picture_diary

## 참고: 학습 개념 연결

| 비유 카드                | 연결 파일/코드                       | 설명                               |
| ------------------------ | ------------------------------------ | ---------------------------------- |
| 잠긴 서랍 (.env)         | `.env`, `load_dotenv()`              | API 키를 코드 밖에서 안전하게 보관 |
| 레시피 (프롬프트)        | `SYSTEM_PROMPT` in `agents/scene.py` | LLM에게 출력 형식을 지시           |
| 조립 라인 (파이프라인)   | `pipeline.py`                        | 장면 → 이미지 → 영상 순서로 조립   |
| 전문가 팀 (에이전트)     | `agents/` 폴더                       | 각 단계를 담당하는 모듈            |
| 카메라 앵글 (shot/angle) | `scene_draft.md`, `prompt_en`        | WS/MS/CU, eye-level/low/high 조합  |
| 조명 (lighting)          | `prompt_en`                          | soft/rim/backlit으로 분위기 조절   |
| 안전벨트 (가드레일)      | `guardrails.py`                      | 반복·시간·비용 제한                |
| 택배 추적 (비동기 폴링)  | `agents/video.py`                    | submit → status → result           |
| 도감 (JSON 스키마)       | `domains/travel_prompts.json`        | 도메인별 시각 어휘 정리            |
| 번역가 (prompt_en)       | `extract_scenes()`                   | 한국어 일기를 영문 프롬프트로 변환 |
