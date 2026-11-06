---
name: api-flow-diagram
description: |
  사용자 흐름(가입, 신청, 결제, 온보딩 등)을 FE·BE 코드에서 끝까지 추적해, 화면·버튼마다 어떤 API 가 호출되는지를 왼쪽→오른쪽 흐름도 HTML 로 만든다. 분기 화살표(진행/오류/되돌아감), 엔드포인트별 FE·BE 파일:라인, 인증 요구, 위험 지점, 전체 엔드포인트 표를 한 파일에 담는다.
  Use when the user mentions API 흐름도, 호출 흐름 도식, 화면별 API, 버튼별 엔드포인트, 어떤 API 가 호출되는지 정리, 시퀀스 정리, 흐름 도식화, 플로우차트, API 호출 점검, user flow API map, endpoint flow diagram, call flow chart, or asks to trace every API called during a user journey (FE+BE) and draw it.
  Do NOT trigger for DB ERD, infra architecture diagrams, or a single endpoint question.
---

# API Flow Diagram

한 사용자 흐름의 화면·버튼 → API 호출 → 분기를 코드에서 추적하고, 데이터 JSON 하나로 흐름도 HTML 을 만든다. 그리는 코드는 고정(`assets/template.html`)이고, 매번 바뀌는 것은 데이터뿐이다.

## 규칙

- DO: 추적은 Sonnet 서브에이전트에 맡기고([trace-prompt](references/trace-prompt.md)), 메인은 핵심 주장 2~3개를 파일:라인으로 직접 확인한 뒤 그린다.
- DO: 기준 커밋(배포본 sha)을 `meta` 에 적는다. 인증·분기는 커밋마다 달라진다.
- DO: 코드로 확인 못 한 인증은 `auth.level: "unknown"`. 추측은 note 에 "(추측)".
- DO: 산출물은 프로젝트의 git 에서 제외된 임시 폴더(예: `tmp-debug/`)에 로컬 파일로.
- DO NOT: HTML·SVG 를 손으로 다시 짜지 않는다. 데이터만 바꾸고 `render.py` 를 돌린다. 레이아웃 문제는 template 을 고친다.
- DO NOT: artifact·외부 공유로 올리지 않는다(사용자가 직접 요청할 때만).
- DO NOT: `.env`·DB 를 열어 확인하지 않는다. 필요하면 "확인 못 함" 으로 risks 에 남긴다.

## 빠른 시작

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/api-flow-diagram"   # user 스킬로 설치했다면 ~/.claude/skills/api-flow-diagram
PYTHONIOENCODING=utf-8 python $S/scripts/render.py tmp-debug/<name>-flow.json tmp-debug/<name>-flow.html
```

예시 데이터로 바로 확인: `python $S/scripts/render.py $S/assets/example-shop.json tmp-debug/example.html`.
스크립트 자체 점검: `python $S/scripts/render.py --self-test`.

## 워크플로우

1. **범위 확정**: 흐름 이름, 진입점(URL·라우트), FE repo, BE repo 와 기준 커밋, 특히 볼 점(예: 비로그인 401). 대화 맥락에 없을 때만 묻는다.
2. **추적 위임**: [trace-prompt](references/trace-prompt.md) 를 채워 Sonnet 에이전트에 보낸다. 출력은 [data-schema](references/data-schema.md) 형식 JSON.
3. **검증**: 결론을 좌우하는 주장(장애 지점, 인증 조건)을 직접 열어 확인. 틀리면 데이터를 고친다.
4. **렌더**: JSON 을 `tmp-debug/<name>-flow.json` 에 저장하고 `render.py` 실행. 검증 오류가 나오면 데이터를 고쳐 다시.
5. **눈으로 확인**: Playwright 는 `file:` 이 막혀 있으니 `python -m http.server <포트> --bind 127.0.0.1` 로 `tmp-debug/` 를 띄워 넓은 뷰포트(3000px+) 스크린샷. 라벨이 노드를 덮거나 화살표가 꼬이면 노드를 쪼개거나 열을 나눈다. 끝나면 서버를 끈다.
6. **보고**: HTML 경로, 열/호출/화살표 수, 직접 확인한 것과 에이전트 보고에만 기댄 것을 구분해 전한다.

## References

- **데이터 스키마**: 최상위·열·노드·호출·화살표 필드, 허용 값, 라벨 길이·분기 수 가이드, render.py 검증 항목. JSON 을 만들거나 고칠 때. See [references/data-schema.md](references/data-schema.md)
- **추적 위임 프롬프트**: 서브에이전트에 보낼 프롬프트 틀과 돌아온 뒤 할 일. 2단계에서. See [references/trace-prompt.md](references/trace-prompt.md)
- **예시 데이터**: 가상의 쇼핑몰 회원가입 + 첫 주문 흐름(5열/7호출/13화살표). 열을 어떻게 나누고 라벨을 얼마나 줄이는지 감 잡을 때. See [assets/example-shop.json](assets/example-shop.json)
