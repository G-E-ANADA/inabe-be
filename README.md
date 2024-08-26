# inabe-be

inable프로젝트의 백엔드어플리케이션 레포입니다.

Inabel Backend는 구직 및 교육 게시글을 관리하고 검색할 수 있는 FastAPI 기반의 API 서버입니다. MongoDB를 사용하여 데이터를 저장하고 관리하며, CORS를 설정하여 여러 출처에서의 요청을 허용합니다.

### 폴더 구조

```
   inabel-be/
   │
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── config.py
   │   ├── database.py
   │   ├── models.py
   │   ├── schemas.py
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── job_posts.py
   │   │   └── edu_posts.py
   │   └── utils.py
   │
   ├── .env
   ├── .env.example
   ├── requirements.txt
   ├── README.md
   └── run.sh
```

---

## 설치 및 실행

### 1. 사전 요구사항

- Python 3.8 이상
- MongoDB 인스턴스

### 2. 환경 변수 설정

`.env` 파일을 프로젝트 루트에 생성하고, 아래와 같은 내용을 추가하세요:

```
MONGODB_URI=<YOUR_MONGODB_URI>
CORS_ORIGINS=http://localhost:1234,http://localhost:3000
```

.env.example 파일은 예시 환경 변수를 포함하고 있습니다.

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

아래 명령어를 사용하여 애플리케이션을 실행하세요:

```bash
./run.sh
```

이 명령어는 FastAPI 서버를 시작하고, MongoDB와 연결을 확인합니다.

### 5. API 사용

서버가 실행되면, 다음 주소로 API에 접근할 수 있습니다:

- 기본 주소: http://localhost:8000
- Swagger 문서: http://localhost:8000/docs
- ReDoc 문서: http://localhost:8000/redoc

---

### API 엔드포인트

- /job_posts/ : 구직 게시글 목록 조회
- /job_posts/search : 구직 게시글 검색
- /edu_posts/ : 교육 게시글 목록 조회
- /edu_posts/search : 교육 게시글 검색

### CORS 설정

CORS_ORIGINS 환경 변수에서 허용할 도메인을 설정할 수 있습니다. 기본값은 http://localhost:1234 입니다.

---

### 라이센스

이 프로젝트는 MIT License 하에 라이센스가 부여됩니다.

---

### 참고

권한 오류 발생시

```bash
bash: ./run.sh: Permission denied
```

이 오류는 `run.sh` 파일에 실행 권한이 없기 때문에 발생합니다.
`chmod` 명령어를 사용해 실행 권한을 부여한 후 다시 시도하면 해결됩니다.

다음 단계를 따라 실행 권한을 부여하세요:

1. **터미널에서 `chmod` 명령어 실행**:

```bash
chmod +x run.sh
```

이 명령어는 `run.sh` 파일에 실행 권한을 추가합니다.

2. **스크립트 실행**:

```bash
./run.sh
```

이제 실행 권한이 부여되어, 스크립트를 정상적으로 실행할 수 있을 것입니다.
