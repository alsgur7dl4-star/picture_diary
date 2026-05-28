# Picture Diary

## 프로젝트 소개

일기 텍스트를 입력하면 장면 추출 → 이미지 생성 → 영상 생성을 자동으로 수행하는 멀티 LLM 파이프라인 프로젝트입니다.

## 빠른 시작

```bash
uv sync
# .env 파일에 API 키 설정
python pipeline.py
```

`.env` 파일에 다음 키를 설정합니다:

```
OPENAI_API_KEY=your-key-here
FAL_KEY=your-key-here
```

## 결과 미리보기

생성된 이미지는 `outputs/` 폴더에 저장됩니다.

| 장면 | 설명 | 파일 |
|------|------|------|
| 1 | 이른 아침 버스정류장 전경 | `outputs/2026-05-27/scene_1.png` |
| 2 | 젖은 보도블록 위 낙엽 | `outputs/2026-05-27/scene_2.png` |
| 3 | 벤치에서 음악 듣는 인물 | `outputs/2026-05-27/scene_3.png` |
| 4 | 초록색 버스 도착 | `outputs/2026-05-27/scene_4.png` |

## 파일 구조

```
picture_diary/
├── pipeline.py              # 전체 파이프라인 실행 진입점
├── agents/
│   ├── __init__.py
│   ├── scene.py             # 일기 → 장면 JSON 추출
│   ├── image.py             # 장면 → 이미지 생성
│   └── video.py             # 이미지 → 영상 생성 (비동기 폴링)
├── guardrails.py            # 반복/시간/비용 제한 가드레일
├── domains/
│   └── travel_prompts.json  # 여행 도메인 프롬프트
├── outputs/                 # 생성 결과물 (이미지, 영상)
├── .env                     # API 키 (커밋 금지)
├── .gitignore
├── README.md
└── week7_retrospective.md   # 5일 학습 회고
```

## 도메인 응용

여행 블로그 도메인을 선택했습니다. `domains/travel_prompts.json`에 여행 장면에 특화된 프롬프트 어휘(golden hour, wide landscape, soft natural lighting 등)를 정의하여 여행 기록 스타일의 이미지를 생성합니다.

## 보안 체크리스트

- [x] API 키는 `.env` 파일에만 저장하고 `load_dotenv()`로 로드
- [x] `.gitignore`에 `.env` 포함
- [x] 코드에 API 키 하드코딩 없음
- [x] README에 실제 API 키 값 없음
