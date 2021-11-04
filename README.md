# 장고를 이용한 블로그 개발
## 개요
* http://ec2-3-37-250-39.ap-northeast-2.compute.amazonaws.com
* 필수 스펙
  * 메인 페이지 : `/` path를 게시판 페이지로 연결하였습니다. 
  * 글 쓰기 수정 기능
    * 쓰기 : `pybo/views.py`의 `question_create()` 
    * 수정 : `pybo/views.py`의 `question_modify()`
  * 글 목록 삭제 기능
    * 삭제 : `pybo/views.py`의 `question_delete()`, jquery-3.4.1로 알림창을 생성하도록 하였습니다.
  * 댓글 기능 : `pybo/views.py`의 `answer_create()`, `answer_modify()`, `answer_delete()`
* 옵션 스펙
  * ui 디자인 : 부트스트랩 4.5.3를 사용하였습니다. `static`, `templates`에 html/css/js 파일을 관리하였습니다.
  * 관리자 도구 : django에서 기본적으로 제공하는 admin page를 사용합니다.
  * rss : `/feed`에 구현
  * trackback
* **인증절차 없이 로그인이 되어 있다는 가정하에 작업**
* 시간이 남아서 URL Shortner도 구현하였습니다.

## 클라우드 서비스를 이용한 배포
* EC2에서 도커 컴포즈로 Django, Nginx 두개의 도커로 구동하였습니다.
* 도커 컴포즈 yml파일 설정
  * 도커 컴포즈 yml파일에서 포트 설정, uwsgi 설정 및 연결
  * volumes 옵션: 도커가 멈추어도 파일들을 유지하기 위해서 도커 서버와 밖의 우분투 서버를 연결 시킨다. 도커 이미지가 죽어도 파일이 유지가 되고, 보통 db를 도커로 띄울 때에 설정한다. 
  * depends_on 옵션: nginx가 uwsgi를 가지고 도커로 떠야 nginx가 소켓을 찾기 때문에, 장고 -> nginx 순으로 작동되어야 한다. 마찬가지로 db -> 장고 순으로 작동해야한다.
  * **해당 설정 파일들은 이곳 깃허브에는 없고 ec2에 있습니다.**

```
# docker-compose.yml
version: '3'
services:

    nginx:
        container_name: nginx
        build: ./nginx
        image: docker-server/nginx
        restart: always
        ports:
          - "80:80"
        volumes:
          - ./server_dev:/srv/docker-server
          - ./log:/var/log/nginx
        depends_on:
          - django

    django:
        container_name: django
        build: ./server_dev
        image: docker-server/django
        restart: always
        command: uwsgi --ini uwsgi.ini
        volumes:
          - ./server_dev:/srv/docker-server
          - ./log:/var/log/uwsgi
```

* Django 도커 파일 설정
  * 도커 내부로 nginx 설정 파일을 복사 후 CMD로 명령어 실행
```
# ~/docker_server/nginx/Dockerfile
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

#EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

* Nginx 도커 파일 설정
  * python 버전 설정 후 도커 내부 파일 설정
  * requirements.txt의 패키지 설치
```
# /docker-server/server_dev/Dockerfile
FROM python:3.6.7  # 생성하는 docker의 python 버전

ENV PYTHONUNBUFFERED 1 

RUN apt-get -y update 
RUN apt-get -y install vim # docker 안에서 vi 설치 안해도됨

RUN mkdir /srv/docker-server # docker안에 srv/docker-server 폴더 생성
ADD . /srv/docker-server # 현재 디렉토리를 srv/docker-server 폴더에 복사

WORKDIR /srv/docker-server # 작업 디렉토리 설정

RUN pip install --upgrade pip # pip 업글
RUN pip install -r requirements.txt # 필수 패키지 설치
```

* uwsgi 파일 설정
  * socket 명과 모듈 명을 내 프로젝트에 맞게 적어준다. 
```
# ~/docker-server/server_dev/uwsgi.ini
[uwsgi]
socket = /srv/docker-server/apps.sock
master = true

processes = 1
threads = 2

chdir = /srv/docker-server
module = server_dev.wsgi

logto = /var/log/uwsgi/uwsgi.log
log-reopen = true

vacuum = true
```

* `docker-compose up -d --build`로 데몬으로 빌드