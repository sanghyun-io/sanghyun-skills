# 흐름 데이터 JSON 스키마

`scripts/render.py` 가 검증하고 `assets/template.html` 이 그린다. 완성 예시는 `assets/example-shop.json` (가상의 쇼핑몰 회원가입 + 첫 주문 흐름).

## 최상위

```json
{
  "title": "회원가입 + 첫 주문 흐름 - 화면/버튼별 API 호출",
  "meta": ["진입: `https://...` | FE `repo` | BE `repo` 커밋 `abc1234` 기준", "두 번째 줄"],
  "legend": [{"text": "공용 HTTP 클라이언트", "tone": "purple", "desc": "401 이면 로그인 화면으로"}],
  "cols": [ ... ],
  "edges": [ ... ],
  "risks": ["**제목:** 내용 `code`", "..."]
}
```

- `meta`, `risks` 는 인라인 마크업 두 가지만 지원한다: `` `code` ``, `**bold**`. 나머지는 이스케이프된다.
- `legend` 는 기본 범례(진행/오류/되돌아감/메서드/강조) 뒤에 붙는 프로젝트 고유 태그 설명이다. 없으면 생략.
- `risks` 가 비면 "점검 결과" 섹션이 사라진다.

## cols: 왼쪽에서 오른쪽 순서

```json
{"title": "Step 1", "sub": "회원 정보", "nodes": [ ... ]}
```

한 열 = 한 화면 단계 또는 한 갈래 묶음. 열이 많아도 가로 스크롤로 본다. 분기가 많은 단계는 "Step 2" / "Step 2 갈래" 처럼 두 열로 나누면 화살표가 덜 꼬인다.

## node

```json
{"id": "submit", "kind": "button", "title": "[가입하기] 버튼",
 "trig": "onSubmit SignupForm.vue:88",
 "desc": "선택. 호출이 없을 때 무엇을 하는지",
 "calls": [ ... ]}
```

| 필드 | 값 |
|---|---|
| `id` | 전체에서 유일. edges 가 참조 |
| `kind` | `screen` 화면 진입 / `button` 버튼·입력 / `system` 내부 처리·외부 콜백 / `end` 종료 화면 / `fail` 실패·오류 모달 |
| `trig` | 트리거(이벤트 핸들러, 파일:라인). 모노스페이스로 표시 |
| `calls` | 이 노드에서 나가는 호출. 순서가 의미 있으면 `p` 앞에 `(1)` `(2)` 를 붙인다 |

## call

```json
{"m": "POST", "p": "/api/v1/orders",
 "fe": "api/order.ts:10", "be": "routes/orders.py:20",
 "auth": {"level": "none", "text": "선택: 배지 문구 덮어쓰기"},
 "tags": [{"text": "공용 HTTP 클라이언트", "tone": "purple"}],
 "note": "1줄 동작 설명", "risk": "있으면 빨간 글씨", "highlight": true}
```

- `m`: `GET POST PUT PATCH DELETE` 는 색이 정해져 있다. 외부 SDK·PG·서버 간 콜백은 `EXT`.
- `auth.level`: `none` 인증 없음(초록) / `cond` 조건부(주황) / `login` 로그인 필요(파랑) / `admin` 관리자(보라) / `unknown` 확인 못 함(회색). 코드로 확인 못 했으면 반드시 `unknown`.
- `tags.tone`: `green orange red blue purple gray`.
- `risk` 가 있으면 카드가 분홍색, `highlight: true` 면 빨간 테두리(장애 지점 등 한 두 곳만).

## edges

```json
{"from": "submit", "to": "cart", "label": "201 + 토큰", "type": "fwd"}
```

- `type`: `fwd` 진행(회색) / `err` 오류·실패(빨강) / `back` 되돌아감(점선, 라벨은 hover 때만).
- 라벨은 출발 노드 오른쪽 빈칸에 붙는다. 20자 안팎으로 줄이고 자세한 조건은 노드 `desc` 에 둔다.
- 두 열 이상 건너뛰는 화살표는 자동으로 도식 아래 통로로 돌아간다. 같은 열 안의 세로 화살표 라벨은 hover 때만 보인다.
- 같은 출발점에서 나가는 화살표 수만큼 노드 오른쪽 변을 균등 분할해 출발점을 잡는다. 4개를 넘으면 라벨이 겹치니 노드를 쪼갠다.

## render.py 가 잡는 오류

id 중복·누락, 알 수 없는 kind/type/auth.level/tone, call 의 m/p/fe/be 누락, edges 의 존재하지 않는 노드 참조, 화살표가 하나도 없는 고립 노드.
