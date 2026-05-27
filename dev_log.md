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
