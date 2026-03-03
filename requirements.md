# Requirements Document

## Introduction

개인 업무용 웹 서버로, 다양한 업무 기능을 모듈 형태로 쉽게 추가/제거할 수 있는 확장 가능한 플랫폼이다. 첫 번째 기능으로 Open WebUI 스타일의 채팅 인터페이스를 제공하며, 백엔드는 n8n webhook을 통해 AI 응답을 처리한다. 디자인은 Apple/Notion 스타일의 미니멀 화이트 테마를 적용한다.

## Glossary

- **Workspace_Server**: 개인 업무용 웹 서버 애플리케이션 전체
- **Plugin_System**: 기능 모듈을 동적으로 추가/제거할 수 있는 플러그인 아키텍처
- **Chat_Module**: Open WebUI 스타일의 채팅 인터페이스 기능 모듈
- **Chat_Interface**: 사용자가 프롬프트를 입력하고 응답을 확인하는 웹 UI 컴포넌트
- **N8N_Webhook**: n8n 워크플로우 자동화 도구의 HTTP webhook 엔드포인트
- **Conversation**: 하나의 채팅 세션에 포함된 메시지들의 집합
- **Message**: 사용자 또는 AI가 생성한 하나의 채팅 메시지

## Requirements

### Requirement 1: 모듈형 플러그인 아키텍처

**User Story:** As a 개발자, I want 기능을 독립적인 모듈로 분리하여 관리, so that 새로운 기능을 쉽게 추가하거나 기존 기능을 제거할 수 있다.

#### Acceptance Criteria

1. THE Workspace_Server SHALL 각 기능을 독립적인 모듈(Blueprint)로 분리하여 등록하는 구조를 제공한다
2. WHEN 새로운 기능 모듈이 추가될 때, THE Plugin_System SHALL 기존 코드 수정 없이 모듈을 등록하고 활성화한다
3. WHEN 기능 모듈이 제거될 때, THE Plugin_System SHALL 다른 모듈에 영향 없이 해당 모듈만 비활성화한다
4. THE Workspace_Server SHALL 각 모듈의 라우트, 템플릿, 정적 파일을 독립적으로 관리한다

### Requirement 2: 미니멀 화이트 테마 UI

**User Story:** As a 사용자, I want Apple/Notion 스타일의 깔끔한 인터페이스, so that 시각적으로 편안하게 업무 도구를 사용할 수 있다.

#### Acceptance Criteria

1. THE Chat_Interface SHALL 화이트 배경에 부드러운 그림자(box-shadow)를 적용하여 요소가 떠 있는 느낌을 제공한다
2. THE Chat_Interface SHALL 모든 UI 요소에 둥근 모서리(border-radius 12px 이상)를 적용한다
3. THE Chat_Interface SHALL 차분한 파스텔 톤 포인트 컬러를 사용한다
4. THE Chat_Interface SHALL 충분한 여백(padding, margin)을 활용하여 정보가 한눈에 들어오도록 한다
5. THE Chat_Interface SHALL 반응형 레이아웃을 제공하여 다양한 화면 크기에서 사용 가능하다

### Requirement 3: 채팅 인터페이스

**User Story:** As a 사용자, I want Open WebUI와 유사한 채팅 인터페이스, so that 프롬프트를 입력하고 AI 응답을 편리하게 확인할 수 있다.

#### Acceptance Criteria

1. WHEN 사용자가 프롬프트를 입력하고 전송 버튼을 클릭하거나 Enter를 누를 때, THE Chat_Interface SHALL 메시지를 전송하고 대화 목록에 표시한다
2. WHEN 빈 메시지를 전송하려 할 때, THE Chat_Interface SHALL 전송을 방지하고 현재 상태를 유지한다
3. THE Chat_Interface SHALL 사용자 메시지와 AI 응답을 시각적으로 구분하여 표시한다
4. WHEN AI 응답을 대기하는 동안, THE Chat_Interface SHALL 로딩 인디케이터를 표시한다
5. THE Chat_Interface SHALL 대화 히스토리를 스크롤 가능한 영역에 표시한다
6. WHEN 새로운 메시지가 추가될 때, THE Chat_Interface SHALL 자동으로 최신 메시지로 스크롤한다

### Requirement 4: 대화 관리

**User Story:** As a 사용자, I want 여러 대화를 생성하고 관리, so that 주제별로 대화를 분리하여 관리할 수 있다.

#### Acceptance Criteria

1. WHEN 사용자가 새 대화 버튼을 클릭할 때, THE Chat_Module SHALL 새로운 빈 대화를 생성하고 활성화한다
2. THE Chat_Interface SHALL 사이드바에 대화 목록을 표시한다
3. WHEN 사용자가 대화 목록에서 대화를 선택할 때, THE Chat_Interface SHALL 해당 대화의 메시지 히스토리를 표시한다
4. WHEN 사용자가 대화를 삭제할 때, THE Chat_Module SHALL 해당 대화와 관련 메시지를 제거한다

### Requirement 5: n8n Webhook 연동

**User Story:** As a 사용자, I want 채팅 메시지가 n8n webhook을 통해 처리, so that n8n 워크플로우를 활용한 AI 응답을 받을 수 있다.

#### Acceptance Criteria

1. WHEN 사용자가 메시지를 전송할 때, THE Chat_Module SHALL n8n webhook URL로 HTTP POST 요청을 전송한다
2. THE Chat_Module SHALL webhook 요청에 사용자 메시지와 대화 컨텍스트를 JSON 형식으로 포함한다
3. WHEN n8n webhook이 응답을 반환할 때, THE Chat_Module SHALL 응답을 파싱하여 대화에 AI 메시지로 추가한다
4. IF n8n webhook 호출이 실패하거나 타임아웃이 발생하면, THEN THE Chat_Module SHALL 사용자에게 오류 메시지를 표시하고 재시도 옵션을 제공한다
5. THE Chat_Module SHALL n8n webhook URL을 환경 변수 또는 설정 파일을 통해 구성 가능하게 한다

### Requirement 6: 대화 데이터 저장

**User Story:** As a 사용자, I want 대화 내용이 저장, so that 서버를 재시작해도 이전 대화를 확인할 수 있다.

#### Acceptance Criteria

1. WHEN 메시지가 추가될 때, THE Chat_Module SHALL 메시지를 데이터베이스에 즉시 저장한다
2. WHEN 서버가 재시작될 때, THE Chat_Module SHALL 저장된 대화 목록과 메시지를 복원한다
3. THE Chat_Module SHALL 각 메시지에 타임스탬프, 발신자 유형(사용자/AI), 내용을 저장한다
4. THE Chat_Module SHALL 메시지를 JSON 형식으로 직렬화하여 저장한다

### Requirement 7: 네비게이션 시스템

**User Story:** As a 사용자, I want 기능 모듈 간 쉬운 네비게이션, so that 다양한 업무 도구를 빠르게 전환할 수 있다.

#### Acceptance Criteria

1. THE Workspace_Server SHALL 좌측 사이드바에 등록된 모듈 목록을 아이콘과 함께 표시한다
2. WHEN 사용자가 사이드바에서 모듈을 선택할 때, THE Workspace_Server SHALL 해당 모듈의 페이지로 전환한다
3. THE Workspace_Server SHALL 현재 활성화된 모듈을 시각적으로 강조 표시한다
