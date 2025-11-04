# Corporate Collaboration MCP Server

**corp.collab.v1** (또는 corp.workspace.v1)

사내 공용 MCP 서버로, 일정/이메일/회의실 등 기업 협업 API를 통합하여 제공합니다.

## 기술 스택

- **FastMCP**: FastAPI 스타일의 데코레이터 기반 MCP 서버 프레임워크
- **Pydantic**: 타입 안전성과 데이터 검증
- **Python 3.10+**: 최신 Python 기능 활용

## 개요

이 MCP 서버는 다양한 사내 협업 도구들을 하나의 통합된 인터페이스로 제공합니다:

- **일정 관리**: 회의 생성, 가용 시간 검색, 참석자 관리
- **회의실 예약**: 회의실 검색, 예약, 가용성 확인
- **이메일**: 메일 전송, 드래프트 관리, 스레드 조회
- **디렉토리**: 사용자/그룹 검색, ID 정규화 (사번/메일/별칭 → 표준 ID)
- **작업 관리**: TODO/이슈 등록 (Jira, Notion 등 어댑터)
- **문서**: 문서 링크, 권한 확인 (선택)
- **정책**: 근무시간, 휴일, 권한, 스팸/대량발송 제한
- **유틸리티**: 타임존 변환, ICS 생성, 헬스체크, 멱등성

## 프로젝트 구조

```
src/corp_collab_mcp/
├── namespaces/          # 네임스페이스별 구현
│   ├── meetings/        # 일정/슬롯/이벤트
│   ├── rooms/           # 회의실/가용성/예약
│   ├── mail/            # 메일 전송/드래프트/스레드
│   ├── directory/       # 사용자/그룹 검색·정규화
│   ├── tasks/           # TODO/이슈 등록
│   ├── docs/            # 문서 링크/권한 (옵션)
│   ├── policies/        # 근무시간·휴일·권한·제한
│   └── utils/           # 타임존/ICS/헬스체크/멱등성
├── types/               # 공통 타입 정의
├── config/              # 설정 관리
├── utils/               # 공통 유틸리티
└── server.py            # MCP 서버 메인
```

## 네임스페이스 상세

### 1. meetings.*

일정 및 회의 관리

**Tools:**
- `meetings.create` - 새 회의 생성
- `meetings.get` - 회의 정보 조회
- `meetings.update` - 회의 수정
- `meetings.cancel` - 회의 취소
- `meetings.list` - 회의 목록 조회
- `meetings.findSlots` - 참석자 가능 시간 검색
- `meetings.getAvailability` - 사용자 가용성 조회

### 2. rooms.*

회의실 예약 및 관리

**Tools:**
- `rooms.search` - 회의실 검색
- `rooms.get` - 회의실 정보 조회
- `rooms.getAvailability` - 회의실 가용성 조회
- `rooms.reserve` - 회의실 예약
- `rooms.cancelReservation` - 예약 취소
- `rooms.listReservations` - 예약 목록
- `rooms.checkIn` - 회의실 체크인

### 3. mail.*

이메일 관리

**Tools:**
- `mail.send` - 이메일 전송
- `mail.createDraft` - 드래프트 생성
- `mail.updateDraft` - 드래프트 수정
- `mail.sendDraft` - 드래프트 전송
- `mail.get` - 이메일 조회
- `mail.getThread` - 스레드 조회
- `mail.search` - 이메일 검색
- `mail.reply` - 답장
- `mail.forward` - 전달

### 4. directory.*

사용자 및 그룹 디렉토리

**Tools:**
- `directory.searchUsers` - 사용자 검색
- `directory.getUser` - 사용자 조회
- `directory.getUserByEmail` - 이메일로 사용자 조회
- `directory.getUserByEmployeeId` - 사번으로 사용자 조회
- `directory.resolveIdentities` - **ID 정규화** (이메일/사번/별칭 → 표준 ID)
- `directory.searchGroups` - 그룹 검색
- `directory.getGroup` - 그룹 조회
- `directory.getGroupMembers` - 그룹 멤버 조회
- `directory.getOrgChart` - 조직도 조회
- `directory.getDirectReports` - 직속 부하 조회

### 5. tasks.*

작업 관리 (Jira, Notion 등 어댑터)

**Tools:**
- `tasks.create` - 작업 생성
- `tasks.get` - 작업 조회
- `tasks.update` - 작업 수정
- `tasks.delete` - 작업 삭제
- `tasks.search` - 작업 검색
- `tasks.addComment` - 댓글 추가
- `tasks.assign` - 작업 할당

### 6. docs.* (선택)

문서 관리

**Tools:**
- `docs.search` - 문서 검색
- `docs.get` - 문서 조회
- `docs.getPermissions` - 권한 조회
- `docs.share` - 문서 공유
- `docs.checkAccess` - 접근 권한 확인
- `docs.revokeAccess` - 접근 권한 취소

### 7. policies.*

정책 및 제한 사항

**Tools:**
- `policies.getWorkingHours` - 근무시간 조회
- `policies.listHolidays` - 휴일 목록
- `policies.isWorkingDay` - 근무일 확인
- `policies.getRateLimits` - 요청 제한 조회
- `policies.checkRateLimit` - 요청 제한 확인
- `policies.getSpamPolicy` - 스팸 정책 조회
- `policies.checkPermission` - 권한 확인
- `policies.getPermissions` - 사용자 권한 목록

### 8. utils.*

유틸리티 기능

**Tools:**
- `utils.convertTimezone` - 타임존 변환
- `utils.getTimezoneInfo` - 타임존 정보
- `utils.listTimezones` - 타임존 목록
- `utils.generateICS` - ICS 파일 생성
- `utils.parseICS` - ICS 파일 파싱
- `utils.healthCheck` - 헬스체크
- `utils.generateIdempotencyKey` - 멱등성 키 생성
- `utils.validateIdempotencyKey` - 멱등성 키 검증

## 설치

```bash
# 의존성 설치
pip install -e .

# 개발 의존성 포함 설치
pip install -e ".[dev]"
```

## 설정

`.env` 파일을 생성하여 설정을 구성합니다:

```bash
cp .env.example .env
```

주요 설정 항목:

```env
# API 설정
CORP_API_BASE_URL=https://api.corp.internal
CORP_API_KEY=your_api_key_here
CORP_API_TIMEOUT=30

# 인증
AUTH_TYPE=oauth2  # or api_key, basic
OAUTH_CLIENT_ID=
OAUTH_CLIENT_SECRET=

# 기능
ENABLE_SPAM_FILTER=true
ENABLE_RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=60

# 로깅
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 실행

### Transport 방식 선택

이 서버는 두 가지 통신 방식을 지원합니다:

1. **stdio (표준 입출력)**: MCP 클라이언트와 프로세스 간 통신
2. **HTTP**: 네트워크를 통한 통신 (FastMCP 내장 HTTP 서버)

`.env` 파일에서 `TRANSPORT` 설정으로 선택할 수 있습니다.

### HTTP 모드 (권장)

```bash
# .env 파일 설정
TRANSPORT=http
WS_HOST=0.0.0.0
WS_PORT=8765

# 서버 실행
python -m corp_collab_mcp.server
```

서버가 `http://0.0.0.0:8765`에서 실행됩니다.

### stdio 모드

```bash
# .env 파일 설정
TRANSPORT=stdio

# 서버 실행
python -m corp_collab_mcp.server
```

### FastMCP 클라이언트로 테스트

```bash
# 툴 목록 확인
python -m corp_collab_mcp.client list-tools

# 툴 호출
python -m corp_collab_mcp.client call-tool meetings.list_meetings \
  --args '{"user_id": "user123", "start": "2025-01-01", "end": "2025-01-31"}'
```

### MCP 클라이언트 설정

#### HTTP 사용 시 (Claude Desktop 등)

```json
{
  "mcpServers": {
    "corp-collab": {
      "url": "http://localhost:8765",
      "env": {
        "CORP_API_KEY": "your_key_here"
      }
    }
  }
}
```

#### stdio 사용 시

```json
{
  "mcpServers": {
    "corp-collab": {
      "command": "python",
      "args": ["-m", "corp_collab_mcp.server"],
      "env": {
        "CORP_API_KEY": "your_key_here",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

## 개발

### 코드 포맷팅

```bash
black src/
ruff check src/ --fix
```

### 타입 체크

```bash
mypy src/
```

### 테스트

```bash
pytest
```

## 구현 가이드

현재 프로젝트는 **스켈레톤 구조**만 구성되어 있습니다. 각 핸들러 함수는 `NotImplementedError`를 발생시킵니다.

### FastMCP 사용법

이 프로젝트는 FastMCP를 사용하여 간결한 코드로 MCP 서버를 구현합니다:

```python
# 기존 MCP SDK 방식 (복잡함)
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Any:
    # 수동으로 라우팅 로직 구현 필요
    if name == "meetings.create":
        return await create_meeting(**arguments)
    # ...

# FastMCP 방식 (간단함)
@mcp.tool()
async def create_meeting(params: CreateMeetingRequest) -> Meeting:
    """Create a new calendar event/meeting."""
    # Pydantic 모델이 자동으로 JSON Schema로 변환됨
    # 함수 시그니처와 docstring이 자동으로 툴 정의가 됨
```

### 구현 순서

1. **인증 구현** (`config/settings.py`)
   - API 키, OAuth 등 인증 방식 구현

2. **API 클라이언트 구현**
   - 각 네임스페이스별 실제 API 호출 구현
   - `httpx` 또는 다른 HTTP 클라이언트 사용

3. **핸들러 구현**
   - `namespaces/*/handlers.py` 파일의 각 함수 구현
   - API 응답을 타입 모델로 변환
   - Pydantic 모델을 파라미터로 사용하면 FastMCP가 자동으로 검증

4. **정책 검증**
   - `policies` 네임스페이스의 정책 검증 로직 구현
   - 스팸 필터, 레이트 리밋 등

5. **에러 처리**
   - 각 API의 에러를 적절한 MCP 에러로 변환
   - 재시도 로직 구현

6. **테스트**
   - 단위 테스트 작성
   - 통합 테스트 작성

## 확장성

### 새 네임스페이스 추가

1. `src/corp_collab_mcp/namespaces/` 아래에 새 디렉토리 생성
2. `types.py`, `handlers.py`, `__init__.py` 파일 생성
3. `server.py`의 `register_namespaces()` 함수에 툴 등록 추가

예시:
```python
# server.py
def register_namespaces() -> None:
    from corp_collab_mcp.namespaces import new_namespace

    mcp.tool()(new_namespace.handlers.some_function)
```

### 새 Tool 추가

FastMCP를 사용하면 매우 간단합니다:

1. 해당 네임스페이스의 `types.py`에 Pydantic 모델 정의
2. `handlers.py`에 async 함수 구현
3. `server.py`에서 `mcp.tool()` 데코레이터로 등록

예시:
```python
# namespaces/meetings/types.py
class CreateMeetingRequest(BaseModel):
    title: str
    attendees: list[str]
    time_range: TimeRange

# namespaces/meetings/handlers.py
async def create_meeting(params: CreateMeetingRequest) -> Meeting:
    """Create a new calendar event/meeting."""
    # 구현...
    pass

# server.py
mcp.tool()(meetings.handlers.create_meeting)
```

FastMCP가 자동으로:
- 함수 이름을 툴 이름으로 변환 (create_meeting)
- Docstring을 툴 설명으로 사용
- Pydantic 모델을 JSON Schema로 변환
- 타입 검증 및 변환 처리

## 라이선스

MIT

## 지원

문제가 발생하면 이슈를 등록해주세요.
