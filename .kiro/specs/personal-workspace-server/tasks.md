# Implementation Plan: Personal Workspace Server

## Overview

Flask Blueprint 기반의 모듈형 개인 업무 웹 서버를 구현한다. 프로젝트 기본 구조를 먼저 세팅하고, 데이터 모델 → 서비스 로직 → API 라우트 → 프론트엔드 UI 순서로 점진적으로 구현한다.

## Tasks

- [x] 1. 프로젝트 기본 구조 및 설정
  - `personal-workspace/` 디렉토리 구조 생성
  - `requirements.txt` 작성 (Flask, requests, hypothesis, pytest)
  - `app/config.py` 작성 (Config 클래스, 환경변수 로딩)
  - `app/__init__.py` 작성 (App Factory: create_app, DB 초기화, Blueprint 등록)
  - `run.py` 엔트리포인트 작성
  - `.env` 파일 템플릿 작성 (N8N_WEBHOOK_URL, SECRET_KEY)
  - _Requirements: 1.1, 1.2, 1.4, 5.5_

- [x] 2. 데이터 모델 및 DB 초기화
  - [x] 2.1 SQLite DB 초기화 및 Base 모델 구현
    - `app/models/base.py` 작성 (DB 연결, 테이블 생성)
    - _Requirements: 6.1, 6.2_
  - [x] 2.2 Conversation, Message 모델 구현
    - `app/modules/chat/models.py` 작성
    - Conversation: id, title, created_at, updated_at
    - Message: id, conversation_id, role, content, created_at
    - JSON 직렬화 메서드 (to_dict) 구현
    - _Requirements: 6.3, 6.4_
  - [ ]* 2.3 Message JSON 직렬화 round-trip property test 작성
    - **Property 8: Message JSON serialization round-trip**
    - **Validates: Requirements 6.4**

- [x] 3. ChatService 비즈니스 로직 구현
  - [x] 3.1 ChatService 기본 CRUD 구현
    - `app/modules/chat/service.py` 작성
    - create_conversation, get_conversations, delete_conversation
    - send_message, get_messages 구현
    - _Requirements: 3.1, 4.1, 4.3, 4.4_
  - [x] 3.2 메시지 유효성 검증 구현
    - 빈 문자열 및 공백 문자열 전송 차단 로직
    - _Requirements: 3.2_
  - [x] 3.3 n8n webhook 호출 로직 구현
    - `_call_n8n_webhook` 메서드: HTTP POST, JSON payload, 타임아웃 처리
    - webhook payload에 사용자 메시지 + 대화 컨텍스트 포함
    - 오류 처리 (ConnectionError, Timeout, HTTP 에러)
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [ ]* 3.4 ChatService property tests 작성
    - **Property 1: Message persistence round-trip**
    - **Validates: Requirements 3.1, 6.1, 6.3**
    - **Property 2: Empty/whitespace message rejection**
    - **Validates: Requirements 3.2**
    - **Property 3: Conversation creation produces valid conversation**
    - **Validates: Requirements 4.1**
    - **Property 4: Conversation deletion removes all associated data**
    - **Validates: Requirements 4.4**
    - **Property 5: Message retrieval returns correct conversation messages**
    - **Validates: Requirements 4.3**
  - [ ]* 3.5 Webhook 관련 property tests 작성
    - **Property 6: Webhook payload contains message and context**
    - **Validates: Requirements 5.2**
    - **Property 7: Webhook error handling**
    - **Validates: Requirements 5.4**

- [x] 4. Checkpoint - 모델 및 서비스 테스트 확인
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. API 라우트 구현
  - [x] 5.1 Chat Blueprint 및 라우트 구현
    - `app/modules/chat/__init__.py` Blueprint 정의
    - `app/modules/chat/routes.py` 라우트 핸들러 구현
    - GET /chat (페이지 렌더링)
    - GET/POST /chat/api/conversations
    - DELETE /chat/api/conversations/<id>
    - GET/POST /chat/api/conversations/<id>/messages
    - _Requirements: 3.1, 4.1, 4.3, 4.4, 5.1_
  - [ ]* 5.2 API 라우트 unit tests 작성
    - 각 엔드포인트 응답 코드 및 JSON 형식 검증
    - _Requirements: 3.1, 3.2, 4.1, 4.3, 4.4_

- [x] 6. 프론트엔드 UI 구현
  - [x] 6.1 기본 레이아웃 및 사이드바 구현
    - `app/templates/base.html` 작성 (사이드바 + 콘텐츠 영역)
    - `app/static/css/main.css` 작성 (미니멀 화이트 테마, 파스텔 톤, 둥근 모서리, 부드러운 그림자)
    - 사이드바에 등록된 모듈 목록 표시, 활성 모듈 강조
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 7.1, 7.2, 7.3_
  - [x] 6.2 채팅 인터페이스 구현
    - `app/modules/chat/templates/chat/chat.html` 작성
    - `app/modules/chat/static/css/chat.css` 작성
    - `app/modules/chat/static/js/chat.js` 작성
    - 대화 목록 사이드패널, 메시지 영역, 입력 프롬프트 구현
    - 메시지 전송 (Enter/버튼), 로딩 인디케이터, 자동 스크롤
    - 사용자/AI 메시지 시각적 구분
    - 대화 생성/선택/삭제 기능
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4_

- [x] 7. 데이터 영속성 검증
  - [ ]* 7.1 데이터 영속성 property test 작성
    - **Property 9: Data persistence across app restart**
    - **Validates: Requirements 6.2**

- [x] 8. Final checkpoint - 전체 테스트 및 통합 확인
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
