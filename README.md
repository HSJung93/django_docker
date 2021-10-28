# Django와 Nginx Docker로 AWS EC2에 띄우기
* http://ec2-3-37-250-39.ap-northeast-2.compute.amazonaws.com
* 패키지 관리
  * `pip freeze > requirements.txt` 명령어로 패키지 관리
* ec2에서 docker 관리
  * `vim Dockerfile`로 도커 설정 파일 작성 후, `docker build -t django_docker/django .`로 태그를 주면서 이미지를 빌드한다. `docker image ls`로 확인 시 해당 태그의 이미지가 있으면 성공.
  * `docker run -p 8000:8000 -d django_docker/django`로 해당 이미지를 데몬 형태로 실행 시킬 수 있다. `-p` 옵션으가 ec2포트번호:도커포트번호 로 연결해준다. 돌아가고 있는 이미지를 `docker ps`로 확인할 수 있다.
  * docker-compose.yml 
    * volumes 옵션: 도커가 멈추어도 파일들을 유지하기 위해서 도커 서버와 밖의 우분투 서버를 연결 시킨다. 도커 이미지가 죽어도 파일이 유지가 되고, 보통 db를 도커로 띄울 때에 설정한다. 
    * depends_on 옵션: nginx가 uwsgi를 가지고 도커로 떠야 nginx가 소켓을 찾기 때문에, 장고 -> nginx 순으로 작동되어야 한다. 마찬가지로 db -> 장고 순으로 작동해야한다.