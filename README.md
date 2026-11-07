# Hearthstone Across The Timeways API

하스스톤 **시간의 길 너머로 (Across the Timeways)** 카드 데이터입니다. [Hearthstone-legacy-API](https://github.com/qxwd565/Hearthstone-legacy-API)와 동일한 `schema: 1` 형식을 사용합니다.

- 통합 카드 목록: [`cards.json`](cards.json)
- 원본 상세 데이터: [`source/Across The Timeways/`](source/Across%20The%20Timeways/)
- 원화 폴더: [`art/`](art/) (원화 파일은 없음)

총 **258장**, 수집 가능 **183장**, 수집 불가능 **75장**을 포함합니다.

**원화는 업로드하지 않았습니다.** 모든 카드의 `art`는 `""`이고, `art/`에는 빈 폴더 유지용 `.gitkeep`만 존재합니다.

향후 원화 파일은 **카드 ID가 아니라 이미지 실제 바이트의 SHA-256 해시**로 저장합니다. 이미지 내용 변경 시 파일명이 바뀌므로 오래된 이미지 캐시와 충돌하지 않습니다. 메타데이터의 `id`/`dbfId`는 카드 식별 및 덱 코드 연결용으로 유지합니다.

`portrait`는 게임 내부 리소스 식별자이며 이미지 URL이 아닙니다. `nativeTags`·`relatedDbfIds` 및 전체 원본 기록은 보존했습니다.
