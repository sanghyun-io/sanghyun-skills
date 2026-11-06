# Plan Subdivider

> **복잡한 계획을 구조화된 실행 가능한 작업으로 자동 변환**

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/sanghyun-io/sanghyun-skills)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/sanghyun-io/sanghyun-skills?style=social)](https://github.com/sanghyun-io/sanghyun-skills/stargazers)

[English](README.md) | **한국어**

**Plan Subdivider**는 대규모 계획을 관리 가능한 순차 작업으로 자동 분해하고, 체크리스트, 검증 단계, 네비게이션을 제공하는 Claude Code 플러그인입니다.

---

## 🎯 왜 Plan Subdivider인가?

**이전** 😰:
```
계획: 사용자 인증 구현
- User 엔티티 설정
- 리포지토리 생성
- 서비스 레이어 구현
- REST API 추가
- 테스트 작성
```

**이후** ✨:
```
~/.claude/plans/user-authentication/
├── 01-user-entity.md          ✓ 명확한 목표
├── 02-user-repository.md      ✓ 단계별 체크리스트
├── 03-auth-service.md         ✓ 검증 명령어
├── 04-auth-controller.md      ✓ 다음 작업 네비게이션
└── 05-integration-tests.md    ✓ 완료 조건
```

각 작업 파일은 다음을 포함합니다:
- **명확한 목표** — 정확히 무엇을 만들어야 하는지 알 수 있음
- **실행 가능한 체크리스트** — 단계별 구현 가이드
- **검증 명령어** — 각 단계 검증 가능
- **작업 네비게이션** — 작업 간 원활한 흐름

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| **🤖 자동 세분화** | Claude가 계획을 분석하여 최적의 작업 분해 제안 |
| **📋 스마트 체크리스트** | 각 작업마다 상세한 실행 가능 체크리스트 생성 |
| **🔗 작업 네비게이션** | 이전/다음 링크로 순차 실행 지원 |
| **✅ 내장 검증** | 작업별 자동 생성 검증 명령어 |
| **🚦 Pre-work 워크플로우** | 구현 시작 전 Claude가 세분화 제안 |
| **🔀 Git 워크플로우 설정** | 작업 환경 선택: 현재 브랜치, 새 브랜치, 또는 git worktree |
| **📐 규칙 기반 구조** | 모든 계획에 일관된 형식 적용 |

---

## 🚀 빠른 시작

### 1. 설치

**방법 A: CLI (권장)**

```bash
# 마켓플레이스 추가
/plugin marketplace add sanghyun-io/sanghyun-skills

# 플러그인 설치
/plugin install plan-subdivider@sanghyun-skills
```

**방법 B: UI**

1. `/plugin` 실행
2. **Marketplaces** 탭 → **"Add Marketplace"** 클릭
3. 입력: `https://github.com/sanghyun-io/sanghyun-skills.git`
4. 플러그인 목록에서 `plan-subdivider` 설치

끝! 플러그인이 첫 실행 시 자동으로 규칙을 `.claude/rules/`에 설치합니다.

### 2. 계획 생성

```bash
/plan JWT를 사용한 사용자 인증 구현
```

Claude가 인터뷰를 진행하고 구조화된 계획을 생성합니다.

### 3. 세분화

```bash
/subdivide
```

Claude가:
1. 계획 구조 분석
2. 작업 분해 제안
3. 확인 요청
4. 체크리스트가 포함된 작업 파일 생성

### 4. 실행

첫 번째 작업을 열고 코딩 시작:

```bash
~/.claude/plans/your-plan/01-first-task.md
```

체크리스트를 따라가고, 검증 명령어를 실행하고, 완료되면 "다음 작업"을 클릭!

---

## 📸 출력 예시

### 메인 계획 파일

```markdown
# 사용자 인증 구현

## 실행 계획 목차

| # | 작업명 | 파일 | 상태 |
|:-:|--------|------|:----:|
| 1 | **User 엔티티** | [01-user-entity.md](./auth/01-user-entity.md) | ✓ |
| 2 | **User 리포지토리** | [02-user-repository.md](./auth/02-user-repository.md) | 🔄 |
| 3 | **인증 서비스** | [03-auth-service.md](./auth/03-auth-service.md) | ⏳ |
| 4 | **인증 컨트롤러** | [04-auth-controller.md](./auth/04-auth-controller.md) | ⏳ |
| 5 | **통합 테스트** | [05-tests.md](./auth/05-tests.md) | ⏳ |
```

### 예시: 작업 파일 (01-user-entity.md)

```markdown
# Task 1: User 엔티티

> **순서**: 1/5
> **이전 작업**: (없음 - 첫 작업)
> **다음 작업**: Task 2: User 리포지토리 (./02-user-repository.md)

---

## 목표

데이터베이스 영속성을 위한 JPA 어노테이션을 포함한 User 엔티티 생성

---

## 체크리스트

### 1. 엔티티 클래스 생성
- [ ] `domain/` 패키지에 `User.kt` 생성
- [ ] `@Entity` 어노테이션 추가
- [ ] 필드 정의: id, email, password, roles, createdAt
  ```kotlin
  @Entity
  data class User(
      @Id @GeneratedValue
      val id: Long? = null,
      val email: String,
      val password: String,
      // ...
  )
  ```
- [ ] 검증 어노테이션 추가

### 2. 데이터베이스 스키마
- [ ] 마이그레이션 스크립트 `V001__create_users_table.sql` 생성
- [ ] `./gradlew flywayMigrate`로 마이그레이션 테스트

---

## 검증

```bash
./gradlew build
./gradlew test
```

---

## 다음 작업

**Task 2: User 리포지토리** (./02-user-repository.md)



---

## 🎨 동작 방식

```
┌─────────────────────────────────────────────────────────────┐
│  나: "/plan 기능 X 구현"                                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Claude: 구조화된 계획 생성                                │
│  - 요구사항 수집                                            │
│  - 아키텍처 설계                                            │
│  - 구현 단계                                                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  나: "구현 시작"                                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Claude: "이 계획은 5개 작업입니다. /subdivide 실행?"       │
│  나: "네" ✓                                                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Plan Subdivider: 작업 파일 생성                           │
│  01-task.md → 02-task.md → 03-task.md → ...                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  나: 명확한 가이드와 함께 작업을 순차적으로 실행            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 포함된 내용

### 플러그인 구성요소

```
plan-subdivider/
├── .claude-plugin/
│   ├── plugin.json              # 플러그인 메타데이터
│   └── marketplace.json         # 마켓플레이스 설정
├── rules/
│   ├── plan-structure.md        # 계획 구조 규칙
│   └── rule-format.md           # 규칙 형식 표준
├── skills/
│   └── plan-subdivide/
│       └── SKILL.md             # /subdivide 명령어
├── scripts/
│   └── install-rules.sh         # 자동 설치 스크립트
├── hooks/
│   └── hooks.json               # 설치 후 자동화
└── examples/
    └── sample-plan.md           # 예제 계획
```

### 자동 설치되는 규칙

플러그인 설치 시 이 규칙들이 `.claude/rules/`에 복사됩니다:

- **`plan-structure.md`**: 계획 파일 구조, 작업 템플릿, 세분화 기준 정의
- **`rule-format.md`**: 일관된 규칙 파일 형식 보장

---

## 🔧 설정

### 설치 모드

규칙이 설치될 위치 선택:

```bash
# 전역 (기본값) - 모든 프로젝트에서 사용 가능
/plugin install plan-subdivider@sanghyun-skills

# 프로젝트 - 팀과 git으로 공유
/plugin install plan-subdivider@sanghyun-skills --scope project

# 로컬 - 프로젝트 전용, gitignored
/plugin install plan-subdivider@sanghyun-skills --scope local
```

### 세분화 기준

다음 조건을 만족하는 계획은 자동으로 세분화됩니다:
- 작업 ≥ 3개
- 다중 파일 수정
- 복잡한 구현 단계

`.claude/rules/plan-structure.md`에서 기준 커스터마이징 가능

### 권장 권한 설정

Plan Subdivider를 원활히 사용하려면 `~/.claude/settings.json`에 다음 권한을 추가하세요:

```json
{
  "permissions": {
    "allow": [
      "Write(~/.claude/plans/**)",
      "Edit(~/.claude/plans/**)",
      "Write(**/.claude/plans/**)",
      "Edit(**/.claude/plans/**)"
    ]
  }
}
```

**왜 이 권한이 필요한가요?**
- `Write(~/.claude/plans/**)`: 세분화된 작업 파일 생성 허용
- `Edit(~/.claude/plans/**)`: 계획 상태 및 체크리스트 업데이트 허용
- `**/.claude/plans/**`: 프로젝트 레벨 계획 디렉토리

**Windows 사용자**: Windows 스타일 경로도 추가하세요:
```json
"Write(C:/Users/사용자이름/.claude/plans/**)",
"Edit(C:/Users/사용자이름/.claude/plans/**)"
```

---

## 🤝 통합

### 연동 가능

- **Claude Plan Mode**: 네이티브 계획 생성 워크플로우

### Pre-work 워크플로우

계획 실행 시 Claude가 자동으로:

1. **작업 개수 확인**: 작업 ≥ 3개 → `/subdivide` 제안
2. **복잡도 확인**: 다중 파일 변경 → `/review` 제안
3. **확인 요청**: `AskUserQuestion` 도구 사용

---

## 📚 사용 예시

### 예시 1: REST API 개발

**입력**:
```bash
/plan 블로그 포스트용 CRUD REST API 생성
```

**출력**:
```
blog-api/
├── 01-post-entity.md
├── 02-post-repository.md
├── 03-post-service.md
├── 04-post-controller.md
├── 05-exception-handling.md
└── 06-integration-tests.md
```

### 예시 2: 데이터베이스 마이그레이션

**입력**:
```bash
/plan MongoDB에서 PostgreSQL로 사용자 데이터 마이그레이션
```

**출력**:
```
mongodb-to-postgres/
├── 01-schema-design.md
├── 02-migration-script.md
├── 03-data-validation.md
├── 04-cutover-plan.md
└── 05-rollback-procedure.md
```

---

## 🐛 문제 해결

### 규칙이 설치되지 않음

```bash
# 플러그인을 재설치하여 규칙 설치 트리거
/plugin install plan-subdivider@sanghyun-skills
```

### `/subdivide`가 인식되지 않음

1. 플러그인이 설치되어 있는지 확인:
   ```bash
   /plugin list
   ```

2. 마켓플레이스가 등록되어 있는지 확인:
   ```bash
   /plugin   # Marketplaces 탭에서 plan-subdivider가 있는지 확인
   ```

3. Claude Code 재시작

### 세분화가 작동하지 않음

1. 먼저 Plan 모드 종료: `/exit` 입력 또는 계획 완료
2. 계획 파일 존재 확인: `ls ~/.claude/plans/*.md`
3. 규칙 파일 확인: `ls .claude/rules/plan-structure.md`

---

## 🌟 이 프로젝트에 별을 주세요!

Plan Subdivider가 도움이 되었다면:

- ⭐ **별**을 주셔서 지원을 보여주고 다른 사람들이 발견할 수 있도록 도와주세요
- 🐛 **이슈 보고**로 플러그인 개선에 기여해주세요
- 💡 **기능 제안**으로 더 나은 플러그인을 만들어주세요
- 🤝 **풀 리퀘스트**로 직접 기여해주세요

여러분의 별은 Plan Subdivider가 [ClaudeMarketplaces.com](https://claudemarketplaces.com/)에서 발견되는 데 도움이 됩니다!

---

## 📝 변경 이력

버전 히스토리는 [CHANGELOG.md](CHANGELOG.md)를 참조하세요.

---

## 🤝 기여하기

기여를 환영합니다! 다음 단계를 따라주세요:

1. 저장소 포크
2. 기능 브랜치 생성
3. 변경사항 작성
4. 풀 리퀘스트 제출

---

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

---

## 🙏 감사의 말

- Claude Code 커뮤니티를 위해 제작
- GTD(Getting Things Done) 방법론에서 영감을 받음
- Claude Sonnet 4.5 기반

---

## 📞 지원

- **이슈**: [GitHub Issues](https://github.com/sanghyun-io/sanghyun-skills/issues)
- **토론**: [GitHub Discussions](https://github.com/sanghyun-io/sanghyun-skills/discussions)
- **이메일**: ppkimsanh@gmail.com

---

**Claude Code를 위해 ❤️로 제작**

⭐ **이 저장소에 별을 주세요** - Plan Subdivider를 더 많은 사람들이 발견할 수 있도록!
