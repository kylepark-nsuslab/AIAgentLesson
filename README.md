# 📝 메모장 (Django Memo App)

Django 기반의 개인 메모장 웹 애플리케이션입니다. 사용자는 회원가입 후 로그인하여 개인 메모를 작성, 수정, 삭제할 수 있습니다.

## 🚀 주요 기능

- **사용자 인증**: 회원가입, 로그인, 로그아웃
- **메모 관리**: 메모 작성, 수정, 삭제, 목록 조회
- **개인화**: 사용자별 개인 메모 관리
- **반응형 UI**: Bootstrap을 활용한 모바일 친화적 인터페이스

## 🛠️ 기술 스택

### 백엔드
- **Django 5.2.3**: 웹 프레임워크
- **Python**: 백엔드 프로그래밍 언어
- **SQLite**: 데이터베이스 (개발용)

### 프론트엔드
- **Django Templates**: 서버사이드 렌더링
- **Bootstrap 5.3**: CSS 프레임워크
- **HTML5 & CSS3**: 마크업 및 스타일링

### 추가 라이브러리
- **django-crispy-forms**: 폼 스타일링
- **crispy-bootstrap5**: Bootstrap 5 지원

## 📁 프로젝트 구조

```
AIAgentLesson/
├── memoapp/                # Django 프로젝트 메인 디렉토리
│   ├── settings.py         # Django 설정
│   ├── urls.py            # 메인 URL 설정
│   ├── wsgi.py            # WSGI 설정
│   └── asgi.py            # ASGI 설정
├── memos/                  # 메모 앱
│   ├── models.py          # 데이터 모델
│   ├── views.py           # 뷰 로직
│   ├── urls.py            # URL 패턴
│   ├── forms.py           # 폼 정의
│   ├── admin.py           # 관리자 설정
│   └── migrations/        # 데이터베이스 마이그레이션
├── templates/              # HTML 템플릿
│   ├── base.html          # 기본 템플릿
│   ├── memos/             # 메모 관련 템플릿
│   └── registration/      # 인증 관련 템플릿
├── doc/                    # 프로젝트 문서
│   ├── spec.md            # 프로젝트 명세
│   ├── python-style.md    # Python 스타일 가이드
│   └── database-style.md  # 데이터베이스 스타일 가이드
└── manage.py              # Django 관리 스크립트
```

## 💾 데이터베이스 스키마

### Memo 모델
- `id`: Primary Key (자동 증가)
- `user`: Foreign Key (User 모델과 연결)
- `title`: 메모 제목 (CharField, max_length=100)
- `content`: 메모 내용 (TextField)
- `created_at`: 생성 일시 (auto_now_add=True)
- `updated_at`: 수정 일시 (auto_now=True)

### User 모델
Django 내장 User 모델 사용:
- `username`: 사용자명
- `email`: 이메일 주소
- `password`: 비밀번호 (해시화)

## 🔧 설치 및 실행 방법

### 1. 프로젝트 클론
```bash
git clone https://github.com/kylepark-nsuslab/AIAgentLesson.git
cd AIAgentLesson
```

### 2. 가상환경 설정 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install django
pip install django-crispy-forms
pip install crispy-bootstrap5
```

### 4. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 5. 관리자 계정 생성 (선택)
```bash
python manage.py createsuperuser
```

### 6. 개발 서버 실행
```bash
python manage.py runserver
```

### 7. 브라우저에서 접속
```
http://localhost:8000
```

## 📱 사용 방법

### 1. 회원가입 및 로그인
- 메인 페이지에서 "회원가입" 버튼 클릭
- 사용자명, 이메일, 비밀번호 입력
- 로그인하여 서비스 이용

### 2. 메모 작성
- 로그인 후 "새 메모" 버튼 클릭
- 제목과 내용 입력 후 저장

### 3. 메모 관리
- 메모 목록에서 메모 제목 클릭하여 상세 보기
- 메모 수정 또는 삭제 가능
- 개인 메모만 표시됨

## 🎨 화면 구성

### 메인 화면 (메모 목록)
- 네비게이션 바: 로고, 사용자 정보, 로그아웃 버튼
- 메모 목록: 제목과 작성 날짜 표시
- "새 메모" 버튼으로 메모 작성

### 메모 상세 화면
- 메모 제목, 내용, 작성/수정 날짜 표시
- 수정, 삭제, 목록 버튼 제공

### 메모 작성/수정 화면
- 제목과 내용 입력 폼
- 저장 및 취소 버튼

## 🎯 주요 URL 패턴

```
/                           # 메모 목록 (메인 페이지)
/signup/                    # 회원가입
/accounts/login/            # 로그인
/accounts/logout/           # 로그아웃
/memo/create/              # 메모 작성
/memo/<id>/                # 메모 상세 보기
/memo/<id>/edit/           # 메모 수정
/memo/<id>/delete/         # 메모 삭제
/admin/                    # 관리자 페이지
```

## 📋 개발 가이드라인

### Python 스타일 가이드
- 함수, 변수: 소문자 + 언더바 (`snake_case`)
- 클래스: 파스칼 케이스 (`PascalCase`)
- 들여쓰기: 공백 4개
- 문자열: 큰 따옴표 사용
- 주석: 한글로 작성

### 데이터베이스 스타일
- 테이블명: 소문자 + 언더바
- 모든 테이블: `id` 필드를 Primary Key로 사용
- 문자열 필드: `CharField` 또는 `TextField` 사용

### 파일 네이밍
- Python 파일: 소문자 + 언더바
- 템플릿 파일: 소문자 + 언더바
- 마크다운 파일: 소문자 + 하이픈

## 🔒 보안 고려사항

- 사용자 인증을 통한 메모 접근 제어
- CSRF 토큰을 활용한 폼 보안
- 사용자별 메모 격리 (다른 사용자의 메모 접근 불가)
- Django 기본 보안 설정 적용

## 🚀 배포 가이드

### 개발 환경
- Django 내장 개발 서버 사용 (`python manage.py runserver`)

### 프로덕션 환경 (권장)
- **웹 서버**: Nginx
- **WSGI 서버**: Gunicorn
- **데이터베이스**: PostgreSQL 또는 MySQL (SQLite 대신)
- **정적 파일**: Nginx를 통한 정적 파일 서빙

## 📞 문의 및 기여

프로젝트에 대한 문의사항이나 기여하고 싶으신 분들은 이슈를 등록해 주세요.

## 📄 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.

---

**개발자**: kylepark-nsuslab  
**최종 업데이트**: 2024년