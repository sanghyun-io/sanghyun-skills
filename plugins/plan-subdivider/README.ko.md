# Plan Subdivider

큰 계획을 순서가 있는 작업 파일로 나눠, 이번 세션이나 다음 세션에서 하나씩 실행할 수 있게 한다. 작업 파일마다 목표, 체크리스트, 완료 기준, 검증 명령, 이전·다음 작업 링크가 들어가고, 메인 계획에는 목차가 붙는다.

[English](README.md)

## 설치

```
/plugin marketplace add sanghyun-io/sanghyun-skills
/plugin install plan-subdivider@sanghyun-skills
```

이 플러그인은 스킬 하나만 추가한다. 훅이 없고, 세션 시작 때 파일을 쓰지 않는다.

## 사용법

1. 계획을 만든다 (plan mode, 또는 `~/.claude/plans/` 에 저장된 계획).
2. 작업이 3개 이상인 계획을 실행하기 전에 Claude 가 세분화를 제안한다. 직접 요청해도 된다 ("이 계획 작업 파일로 나눠줘") 또는 `/plan-subdivider:plan-subdivide [plan_path]`.
3. Claude 가 나눌 작업 목록을 보여 주고 승인을 받은 뒤 파일을 만든다:

```
~/.claude/plans/
├── user-authentication.md          # 메인 계획 + 작업 목차
└── user-authentication/
    ├── 01-user-entity.md
    ├── 02-user-repository.md
    ├── 03-auth-service.md
    ├── 04-auth-controller.md
    └── 05-integration-tests.md
```

4. 다음 단계(Task 01 시작 / 전체 검토 / 나중에)를 고르고, 시작하면 작업 위치(현재 디렉토리 / 새 브랜치 / git worktree)를 고른다.

몇 분이면 끝나는 작업, 파일 하나 수정, 너무 얽혀서 나눌 수 없는 작업에는 쓰지 않는다.

## 선택: Pre-work 질문 강제

기본은 스킬 설명을 보고 Claude 가 세분화를 제안하는 방식이라, 가끔 바로 구현에 들어갈 수 있다. "작업 3개 이상인 계획은 실행 전에 반드시 묻고, 스스로 판단해 건너뛰지 않는다" 를 강제하려면 규칙 파일을 직접 복사한다:

```bash
cp "<플러그인 폴더>/rules/plan-structure.md" ~/.claude/rules/      # 모든 프로젝트
cp "<플러그인 폴더>/rules/plan-structure.md" .claude/rules/        # 이 프로젝트만
```

`<플러그인 폴더>` 는 `/plugin` (Installed 탭) 또는 `~/.claude/plugins/cache/sanghyun-skills/plan-subdivider/` 에서 찾는다.

## 권한 (선택)

작업 파일마다 권한 질문이 뜨지 않게 하려면 `settings.json` 에 계획 폴더 쓰기를 허용한다:

```json
{ "permissions": { "allow": ["Write(~/.claude/plans/**)"] } }
```

## 1.x 에서 업그레이드

- 명령이 `/subdivide` 에서 `/plan-subdivider:plan-subdivide` 로 바뀌었다.
- 규칙 파일을 `.claude/rules/` 에 자동 복사하지 않는다. 이전 버전이 프로젝트의 `.claude/rules/` 에 남긴 `plan-structure.md`, `rule-format.md` 는 위의 강제 규칙을 쓸 게 아니면 지워도 된다.

[CHANGELOG.md](CHANGELOG.md) 참고.

## 라이선스

MIT
