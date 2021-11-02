# 원티드x위코드 프리온보딩 AIMMO 과제

- 백엔드 1팀 (쿠티드프리온보딩)

- 팀원: 문승준, 김지훈, 양가현



## 사용 기술 스택

- Python 3.8
- Django 3.2
- Django-cors-headers 3.10
- PyJWT 2.3
- bcrypt 3.2
- Django 1.3
- MongoDB 5.0
- postman
- mongodb compass



## 구현 목표

- 원티드 지원 과제 내용 포함 (게시글 CRUD)

- 게시글 카테고리

- 게시글 검색

- 대댓글(1 depth)

  - 대댓글 pagination

- 게시글 읽힘 수

  - 같은 User가 게시글을 읽는 경우 count 수 증가하면 안 됨

- Rest API 설계

- Unit Test

- 1000만건 이상의 데이터를 넣고 성능테스트 진행 결과 필요

  

## 프로젝트 구조 및 구현 방법

### AIMMO-Project 개요

- Python을 기반으로 Django 프레임워크를 활용한 게시글과 댓글 CRUD 기능 REST API 개발

- 유저 생성과 인증, 인가 기능 개발

  

### DB와 모델링

- 필수 기술스택인 MongoDB로 구현

- 유저 정보는 이름, 이메일, 패스워드 관리

- 게시물과 대댓글 기능 구현을 위한 데이터 관리 

  

### users app

- 유저 회원가입을 위한 SignUpView class 작성 (bcrypt로 비밀번호 암호화)

- 유저 로그인을 위한 LogInView class 작성 (JWT 토큰 생성)

- 유저 인가를 위한 login_decorator를 utils.py에 작성

  

### posts app

#### 게시글

- 글 작성, 카테고리별 조회, 검색어로 조회 기능 (페이지네이션)
- 글 내용 조회 및 조회수 count 기능 (같은 유저일 경우 증가 안함)
- 글 수정, 삭제 기능 

#### 대댓글

- 댓글 CRUD 기능 (페이지네이션)
- 대댓글 CRUD 기능



### Unit Test

- tests.py에 테스트 코드 작성

- 함수 단위별 success, fail case 테스트 완료

  

### Integration Test

- Postman과 Httpie 활용
- Postman Document [링크](https://documenter.getpostman.com/view/17676214/UVBzn9Mt)



## 배포

- AWS EC2 서버
- MongoDB Atlas
- gunicorn
- 배포 서버 주소 ->  **52.79.51.199:8000**



## API 호출&응답 예시



### 회원관리
<img width="512" alt="스크린샷 2021-11-03 오전 2 24 56" src="https://user-images.githubusercontent.com/72376931/139914937-653b2011-13da-47d0-92f8-9b10084fcc1a.png">

<img width="512" alt="스크린샷 2021-11-03 오전 2 25 47" src="https://user-images.githubusercontent.com/72376931/139915040-b4196fc2-b926-47d0-8071-83579bc286d2.png">

### 게시글

<img width="512" alt="스크린샷 2021-11-03 오전 2 28 06" src="https://user-images.githubusercontent.com/72376931/139915423-46ee456e-9bb3-4768-a61a-3c919b3cc5d6.png">
<img width="512" alt="스크린샷 2021-11-03 오전 2 26 19" src="https://user-images.githubusercontent.com/72376931/139915130-80637cd8-0ad7-4fef-82fd-56ac123d8f9b.png">


<img width="512" alt="스크린샷 2021-11-03 오전 2 29 03" src="https://user-images.githubusercontent.com/72376931/139915637-7fce8274-870b-4585-8dd8-b9f3b6bc664d.png">

<img width="512" alt="스크린샷 2021-11-03 오전 2 29 11" src="https://user-images.githubusercontent.com/72376931/139915666-c391f1cd-ba24-4bb8-94b6-ea0fe46a0cb1.png">

<img width="512" alt="스크린샷 2021-11-03 오전 2 29 26" src="https://user-images.githubusercontent.com/72376931/139915703-462b6019-3848-4272-9197-48abd1e3cba7.png">



<img width="512" alt="스크린샷 2021-11-03 오전 2 29 39" src="https://user-images.githubusercontent.com/72376931/139915748-cef21e87-ed1d-470c-a542-dcbe2fd0c0c0.png">

### 댓글

<img width="512" alt="스크린샷 2021-11-03 오전 2 30 39" src="https://user-images.githubusercontent.com/72376931/139915929-d89b5bde-8305-4a0a-b8c4-79708d89b2ec.png">


<img width="512" alt="스크린샷 2021-11-03 오전 2 30 53" src="https://user-images.githubusercontent.com/72376931/139915959-a4ffd563-00cc-4ce1-8cff-d2870efe5b62.png">

<img width="512" alt="스크린샷 2021-11-03 오전 2 31 09" src="https://user-images.githubusercontent.com/72376931/139916002-382efba6-e21f-457e-9f96-7040d47a5a83.png">


<img width="512" alt="스크린샷 2021-11-03 오전 2 31 21" src="https://user-images.githubusercontent.com/72376931/139916032-5e9a6355-054c-442d-867f-29d0874254eb.png">


### 대댓글



<img width="512" alt="스크린샷 2021-11-03 오전 2 32 02" src="https://user-images.githubusercontent.com/72376931/139916141-c252b3ce-0987-4649-aaac-4762fb834eec.png">
<img width="512" alt="스크린샷 2021-11-03 오전 2 32 13" src="https://user-images.githubusercontent.com/72376931/139916172-b448f4e5-f4fe-4b5b-8de3-adf6c74b7a70.png">
<img width="512" alt="스크린샷 2021-11-03 오전 2 32 46" src="https://user-images.githubusercontent.com/72376931/139916268-019106ce-1cd7-4901-afd4-625c912dda5e.png">


<img width="512" alt="스크린샷 2021-11-03 오전 2 32 58" src="https://user-images.githubusercontent.com/72376931/139916302-ac2be853-bf81-4e7c-9574-b52327e94dc9.png">




