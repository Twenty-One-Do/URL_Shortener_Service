# URL Shortener Service

## 📜 목차

1. [인프라 다이어그램](#인프라-다이어그램)
2. [API 문서](#API-문서)
3. [실행](#실행)
5. [기능 구현 설명](#기능-구현-설명)

## 👨‍💻 인프라 다이어그램
![개인 프로젝트 (14)](https://github.com/user-attachments/assets/8e5188f2-296b-4573-88de-c5dc484c9e78)

## 📃 API 문서

Domain: http://to.plz-readme.com/
Swagger: [http://to.plz-readme.com/docs](http://to.plz-readme.com/docs)

## 🖥 실행

배포 환경을 실행하려면 프로젝트의 루트 디렉토리에서 아래의 명령어를 입력하세요:

``
docker-compose up -build
``

## 🛠 기능 구현 설명

### 🥇 필수 기능: 단축 URL 생성

### 🥇 필수 기능: 원본 URL 리디렉션

### 🥈 추가 요구사항: DB 선택과 구조
최종적으로 Redis와 PostgreSQL을 데이터베이스로 채택했습니다.

GET 요청이 많고 빠른 응답 속도가 중요하기 때문에 인메모리 데이터베이스인 Redis가 필수적이라고 판단했습니다.

![Blank diagram - Page 1](https://github.com/user-attachments/assets/cd221524-a7ff-4fa0-b7d7-71d28a79cfa5)

단순히 Shorten Key와 URL을 매핑하면 original URL의 base_url 부분이 많이 중복되므로 base_url과 path 부분을 분리하여 저장하는 것이 더 효율적이라고 판단했습니다.

기존 서비스 중이던 URL 단축 사이트에서 동일한 URL을 입력했을 때 동일한 Key가 나오지 않는 경우가 있었는데, 이는 Short URL 별로 통계를 분리하기 위함이었습니다. 따라서 하나의 URL에 여러 Key를 생성할 수 있도록 설계했습니다.

### 🥉 보너스 기능: URL 키 만료 기능
![image](https://github.com/user-attachments/assets/aee9ff3a-6c40-49d3-b7f6-577d059163ac)

`POST /shorten` 요청의 본문에 만료 일자를 포함하면 해당 키에 대한 만료일이 지정됩니다.

![image](https://github.com/user-attachments/assets/f47d9dbf-f382-4232-a4db-a9c75656ffcc)

해당 만료일이 지난 후 `GET /<short_key>` 요청 시 404 상태 코드와 함께 URL이 소멸되었다는 메시지를 반환합니다.

### 🥉 보너스 기능: 통계 기능
![image](https://github.com/user-attachments/assets/ea9a5d27-d087-49e3-b2b3-3629a15e6a3e)

`GET /<short_key>` 요청 시 요청 헤더의 `user-agent`를 기반으로 클라이언트의 기기를 식별하여 데이터를 저장합니다.

`GET /stats/<short_key>` 요청 시 단축 키의 조회 수뿐만 아니라 각 기기별 조회 수도 반환합니다.

이때 GET 요청의 비즈니스 로직이 많아졌기 때문에 조회 정보를 저장하는 로직을 비동기 처리하여 응답 속도를 높였습니다.

### 🥉 보너스 기능: 테스트 코드

### 🏆 개인적으로 추가한 기능: Redis 캐싱

`GET /<short_key>` 요청 시 데이터베이스 접근 시간을 최소화 하고 URL을 조립(base_url, path 분리됨)하는데 소요되는 시간을 줄이기 위해, 조립된 URL을 캐시화하여 불러오는 시간을 단축했습니다. 캐시에 없던 key에 리디렉션 요청을 받으면 해당 키와 조립된 URL을 캐시에 저장합니다.
