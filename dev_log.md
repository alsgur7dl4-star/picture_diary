# Day 1 self1 개발 기록

- 배운 점: 프롬프트를 변수로답아서 AI한테 요청한후 모델을지정한후 사용하는법을 배웟습니다.
- 막힌 점: 노트북에 그래픽카드가없어서 나중에 수업을위해 SSH를 사용해서 집에 있는 컴퓨터로 진행하다보니 깃허브에 올리는도중 오류가발생했습니다. 깃허브에 SSH를 등록해서 해결했습니다
- 내일 시도할 것: 같은 일기 장면을 샷, 앵글, 조명만 바꿔서 비교해 본다.
- 강사 비유 연결: .env는 잠긴 서랍처럼 API 키를 코드 밖에 안전하게 보관하고, Python 코드는 실행할 때 그 값을 불러와 사용한다.

## Day 1 self2 기록

- 마음에 든 부분: 나의 생각대로의 이미지가 나온거같다.
- 바꾸고 싶은 부분: 이미지의 도로부분에서 분리대와 도로가 어색해서 도로분리대와 도로를 조금더 넓게 수정하고싶다.
- 오늘 추가 생성: scene01_ws.png, scene01_cu.png, scene01_low.png 3장을 생성했다.
- 가장 차이가 크게 보인 변형: low angle + backlit 변형이 버스가 다가오는 느낌을 가장 극적으로 보여 주었다.
- Day 2에서 다시 쓰고 싶은 장면 후보: 이른 아침 버스정류장에서 혼자 앉아 있고, 초록색 버스가 천천히 다가오는 장면.

## 응답 구조 비교 메모

- OpenAI gpt-image-1: response.data[0].b64_json을 base64.b64decode()로 변환해 저장한다.
- fal.ai FLUX: result["images"][0]["url"]에서 이미지 URL을 꺼내 저장한다.

## Day 2 self1 기록

- 오늘 만든 파일: scene_draft.md, day2_self1.py
- 장면 1: 버스정류장 전체 분위기를 보여 주기 위해 WS, eye-level, soft, 24mm를 선택했다.
- 장면 2: 젖은 보도블록과 낙엽을 자세히 보여 주기 위해 CU, high, soft, 85mm를 선택했다.
- 장면 3: 혼자 앉아 있는 인물의 행동을 보여 주기 위해 MS, eye-level, rim, 50mm를 선택했다.
- 장면 4: 초록색 버스가 다가오는 장면을 극적으로 보이게 하기 위해 WS, low, backlit, leading line, 35mm를 선택했다.
- 가장 어려웠던 선택: 장면마다 shot과 lens를 다르게 골라 단조롭지 않게 만드는 점이 어려웠다.
- 다음 self2에서 확인할 것: scene_draft.md의 4장면을 JSON으로 변환하고, 이미지 생성 시 gpt-image-1 방식으로 저장되는지 확인한다.

## Day 2 self2 — scene_prompts.json + fal.ai 첫 호출

- 완료 시각: 17:00
- 생성 파일: scene_prompts.json, day2_self2.py, outputs/scene01_fal.png
- FLUX vs 기존 이미지 생성 차이: fal.ai는 result["images"][0]["url"]에서 이미지 URL을 꺼내고, OpenAI gpt-image-1은 response.data[0].b64_json을 base64로 디코딩해 저장한다.
- 막힌 부분: 없음

## Day 3 self1

- agents/scene.py로 diary.md에서 4장면 scenes JSON을 추출했다.
- scene_extracted.json을 Day 3 self2 이미지 생성 입력으로 사용할 준비를 했다.
- 사람이 직접 만든 scene_prompts.json과 GPT가 자동 추출한 scene_extracted.json을 비교했다.
- 막힌 부분: 없음

## Day 3 self2

- 사용 모델: openai(gpt-image-1)
- COMMON_STYLE: watercolor diary illustration, soft gray-blue morning palette, a single young man waiting quietly, consistent main character, quiet early morning bus stop atmosphere
- 생성 결과: outputs/2026-05-27/scene_1~4.png
- 재시도한 장면: 없음
- Day 4 입력 가능 여부: 가능

## Day 4 self1

- 동기는 먼저한 결과가 나올떄까지 기다리는것이고 비동기는 앞에 결과가 나오지않았어도 다른 작업을 실행하는것입니다.
- 가드레일은 반복 횟수, 시간, 상태 조건, 비용을 제한해서 API 호출이 계속 반복되는 문제를 막는 역할을 한다.

## Day 4 self2

- Kling은 이미지와 프롬프트를 받아 그기반으로 짧은 영상을 만들어 주는 API이라는걸 알게되었다
- submit 후에는 바로 영상이 나오는 것이 아니라 task_id를 받아 status로 상태를 확인하고, 완료되면 result에서 영상 URL을 받는다.
- picture_diary_pipeline()은 일기 -> 장면 -> 이미지 -> 영상 -> 결과 저장 흐름을 하나로 묶는 함수라고 정리했다.
- Day 5 self1 도메인 후보는 여행 기록으로 할거같다.

## Day 5 self1

- 선택 도메인: travel(여행)
- seed A/B: 42 / 137
- A 호출 수: 1 또는 3
- B 호출 수: 1 또는 3
- p95_latency_s: 실행 후 cost_report.md에서 확인
- cost_per_image: 실행 후 cost_report.md에서 확인
- total_cost_usd: 실행 후 cost_report.md에서 확인
- 다음 작업: Day 5 self2에서 README 운영 지표 표에 위 값을 반영
