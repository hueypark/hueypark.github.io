# Docker
## 함께하면 당신도 SysAdmin

---

## 자기소개

- 박재완
- jaewan.huey.park@gmail.com
- Python, PHP, C++

---

## 약

---

### 사장님이 이제부터 젠킨스를 쓰라고 합니다.

``` python
docker run -p 8080:8080 -p 50000:50000 --name jenkins jenkins
```

---

## 약 2

---

## 사장님이 이번에는 redmine을 쓰라고 합니다.

``` python
docker run -p 3000:3000 --name redmine redmine
```

---

## 사장님이 이번에는...

게임서버, 웹서버, 디비, 캐시, 푸시, 등등등 짬뽕으로 잘 버무려서... 부탁해 내일아침에 보자고...

---

## Contents

1. 새로운 기술을 도입하는 법
2. Docker
3. Demo
4. Q & A

---

## 새로운 기술을 도입하는 법

---

### 1. 학습

---

### 2. 사용

---

### 3. 전파

---

![내전](/slides/docker/war.jpg)

---

## 새로운 기술을 도입하는 법

1. 학습
2. 사용
3. 전파
4. 내전

---

## 새로운 기술을 도입하는 법 ???

---

### 사례 1.

빌드는 사람이 하는 일 아닌가요?

---

#### 계속되는 빌드에 지친 프로그래머

---

#### Jenkins라 불리는 구세주 발견
#### 자동화 -> 평화

---

### 사례 2.

PHP의 친구는 notepad++

---

#### PHP...
#### notepad++ 과 함께 (feat. log)
#### 참디버깅의 고통이란 이런것이다

---

#### PHP Tools for Visual Studio 과 함께
#### breakpoint -> 평화

---

### 사례 3.

개발은 역시 서버에서!

---

#### 서버에 환경을 구축하고 모두가 한마음으로 ...

---

#### 로컬에 환경을 구축하려면 nginx, PHP, 기타 등등 의존성 ...
#### 성공한 자만이 로컬에서 개발할 수 있을 지어다

---

#### 이 때 !

---

## Docker

![](/slides/docker/docker_real.jpg)

---

## Docker란 무엇인가?
![](/slides/docker/docker_logo.png)

---

### Docker는 애플리케이션의
### 빌드, 배포, 실행을 도와주는 오픈 플랫폼

---

### 비슷한 친구로는
### chef, puppet and vagrant 등이 있다고 함

---

## 누가 주도하는가?

---

### Docker Inc.
### +
### Open source community

---

## 장점

1. 관리가 쉽다.
2. 배포가 쉽다.
3. 빠르다.
4. 풍부한 생태계가 존재한다.

---

## 1. 관리가 쉽다.

### DockerFile을 이용해
### 환경에 대한 이력추적이 가능하다

``` DockerFile
FROM ubuntu:14.04

MAINTAINER hueypark <jaewan.huey.park@gmail.com>

RUN apt-get update

RUN apt-get install -y language-pack-en-base

RUN apt-get install -y software-properties-common

RUN LC_ALL=en_US.UTF-8 add-apt-repository ppa:ondrej/php

RUN apt-get update

RUN apt-get install -y nginx
RUN apt-get install -y php7.0-fpm

ADD Docker/conf/php.ini /etc/php/7.0/php.ini
ADD Docker/conf/default /etc/nginx/sites-available/default
ADD Docker/scripts/start.sh /start.sh

COPY Code/ /var/www/html/

EXPOSE 80
```

---

## 2. 배포가 쉽다.

### 한번 빌드한 Docker Image를 이용
### 여러 컨테이너를 생성 가능하다
![](/slides/docker/docker_image.jpg)

---

## 3. 빠르다.

### Docker Container에서 상세히 설명

---

## 4. 풍부한 생태계가 존재한다.

### 300,000개 이상의
### Dockerized app이 Docker Hub에 존재함

https://hub.docker.com/explore/

---

## 주요 기능 소개

---

## Docker Image

---

### Image는 읽기 전용의 템플릿,
### Container를 생성하기 위해 사용

---

### Docker는 이미지를
### 쉽게!
### 만들고!
### 업데이트하고!
### 배포!
### 할 수 있는 기능을 제공

---

## Docker Container

---

### Container는 독립된 디렉토리와 비슷하다

---

### 애플리케이션 실행에 필요한
### 모든 내용을 소유하고 있으며

---

### Image로부터 생성된다

---

![](/slides/docker/containers.jpg)

---

## 가상머신과는 다르다!
## 가상머신과는!
![](/slides/docker/image_vs_vm.jpg)

---

### Host OS 위에 Hypervisor를 통해
### Guest OS를 전체설치하고
### 가상화하는 것이 아니라

---

### 같은 OS에서 Docker Engine에
### 의해 프로세스 격리

---

### 성능차가 거어어의 없다고 함

---

## 가상머신
![](/slides/docker/vm.png)

---

## Docker
![](/slides/docker/docker.png)

---

## 데모

---

### 순서

1. ubuntu:14.04로부터 이미지를 만들고
2. nginx 설치
3. php 설치
4. 설정파일 설정
5. 코드 복사
6. 80번 포트 열기
7. 실행
8. container 분신술은 다음에...

---

![](/slides/docker/demo_gods.png)

---

## Cheats

1. docker build -t slides .
2. docker run -p 80:80 -it --name slides slides

---

## Q & A
