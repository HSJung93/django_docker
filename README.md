# Django와 Nginx Docker로 AWS EC2에 띄우기
* http://ec2-3-37-250-39.ap-northeast-2.compute.amazonaws.com:8000/
* 패키지 관리
  * `pip freeze > requirements.txt` 명령어로 패키지 관리
* ec2에서 docker 관리
  * `vim Dockerfile`로 도커 설정 파일 작성 후, `docker build -t django_docker/django .`로 태그를 주면서 이미지를 빌드한다. `docker image ls`로 확인 시 해당 태그의 이미지가 있으면 성공.
  * `docker run -d django_docker/django`로 해당 이미지를 데몬 형태로 실행 시킬 수 있다. 돌아가고 있는 이미지를 `docker ps`로 확인할 수 있다.