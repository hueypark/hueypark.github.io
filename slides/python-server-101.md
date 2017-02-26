# Python과 함께하는
## 서버 사이드 애플리케이션

---

### 박재완
#### jaewan.huey.park@gmail.com
#### NextFloor 풀스택 게임 프로그래머

---

## 오늘 할 이야기

---

### 이런 걸 만들었습니다
https://github.com/HueyPark/Account-Book

---

### 왜?

- 뭔가 만들고 싶었는데... <!-- .element: class="fragment fade-in" -->
- 게임은 너무 어려웠습니다 <!-- .element: class="fragment fade-in" -->
- 기획 Lv.0 <!-- .element: class="fragment fade-in" -->

---

### 필요했던 기능

- 웹 프레임워크 <!-- .element: class="fragment fade-in" -->
- 데이터베이스 접근 <!-- .element: class="fragment fade-in" -->
- 인증 <!-- .element: class="fragment fade-in" -->

---

## 서버란 무엇인가?
### 클라이언트에게 네트워크를 통해 서비스를 제공하는 컴퓨터 또는 프로그램 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
#### -위키백과 <!-- .element: class="fragment fade-in" data-fragment-index="1" style="text-align:right;" -->

---

## 서버의 종류

- web server <!-- .element: class="fragment fade-in" -->
- application server <!-- .element: class="fragment fade-in" -->
- database <!-- .element: class="fragment fade-in" -->
- file server <!-- .element: class="fragment fade-in" -->
- 등등등... <!-- .element: class="fragment fade-in" -->

---

## 오늘 이야기할 서버
### APPLICATION SERVER <!-- .element: class="fragment fade-in" -->

---

## Application server란 무엇인가?
### 인터넷 상에서 HTTP를 통해 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
### 사용자 컴퓨터나 장치에 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
### 애플리케이션을 수행해주는 미들웨어 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
#### - 위키백과 <!-- .element: class="fragment fade-in" data-fragment-index="1" style="text-align:right;" -->

---

## Application server의 위치?

### Web server
### |
### Application server <!-- .element: class="fragment highlight-blue"-->
### |
### Database server

---

## Application server는
## 무엇으로 만들 수 있는가?

- Python <!-- .element: class="fragment fade-in" -->
- PHP <!-- .element: class="fragment fade-in" -->
- Java <!-- .element: class="fragment fade-in" -->
- Javascript <!-- .element: class="fragment fade-in" -->
- Scala <!-- .element: class="fragment fade-in" -->
- 등등등... <!-- .element: class="fragment fade-in" -->

---

## 왜 Python이죠?

- 팀에서 쓸 거 같았습니다 ㅜㅜ <!-- .element: class="fragment fade-in" -->
- 생산성이 좋은 거 같습니다 ;; <!-- .element: class="fragment fade-in" -->

---

## Python
### Python is a programming language that <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
### lets you work more quickly and <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
### integrate your systems more effectively. <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

## Python
### 당신을 더 빨리 일할수 있게 하고
### 시스템과 효과적으로 통합하게 해주는
### 프로그래밍 언어이다

---

## Python for games
### Python enabled us to create EVE Online, a massive multiplayer game, in record time. The EVE Online server cluster runs over 50,000 simultaneous players in a shared space simulation, most of which is created in Python. The flexibilities of Python have enabled us to quickly improve the game experience based on player feedback <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
#### said Hilmar Veigar Petursson of CCP Games. <!-- .element: class="fragment fade-in" data-fragment-index="1" style="text-align:right;" -->

---

## Python for games
### Python은 EVE Online을 기록적인 시간에 만들 수 있게 해주었다.
### 서버는 5만 명 이상의 가상 플레이어를 분할된 우주 공간에서 시뮬레이트했다.
### 유연성 덕분에 피드백을 반영해 빠르게 게임의 경험을 향상시킬 수 있었다.
#### said Hilmar Veigar Petursson of CCP Games. <!-- .element: style="text-align:right;" -->

---

## Python 살펴보기

---

### C++

```cpp
int doSomething() {
    auto a = getA();
a.do();
}
```

---

### C++

```cpp
int doSomething() {
    auto a = getA();
    a.do();
}
```

---

### C++

```cpp
int doSomething()
{
    auto a = getA();
    a.do();
}
```

---

### Python

```python
def do_something:
    a = gat_a()
    a.do()
```

---

### C++

```cpp
if (x > 0 && x < 10)
{
    doSomething();
}
```

---

### C++

```cpp
if (0 < x && x < 10)
{
    doSomething();
}
```

---

### Python

```python
if 0 < x < 10:
    do_something()
```

---

## Hello World

```python
print('Hello World')
```

---

## Python 첫인상
- 간결하다 <!-- .element: class="fragment fade-in" -->

---

## PyPI
### the Python Package Index <!-- .element: class="fragment fade-in" -->

---

### Repository of software
### for the Python programming language.

---

### There are currently 75837 packages here.

---

### Python에서 관리하는 패키지 모음집

---

### 이런게 됩니다
```
pip install Flask
pip install PyMySQL
pip install SQLAlchemy
pip install PyJWT
```
<!-- .element: class="fragment fade-in" -->

---

## Flask
### Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. <!-- .element: class="fragment fade-in" -->

---

## 문법 하나만 더!

---

## decorator 패턴
### 주어진 상황 및 용도에 따라 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
### 객체에 책임을 덧붙임 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

## decorator 패턴
```python
def decorater(func):
    def wrapper():
        print('Hello ' + func())

    return wrapper


def world():
    return 'World'

helloworld = decorater(world)
helloworld()
```

---

## decorator 패턴
```python
def decorater(func):
    def wrapper():
        print('Hello ' + func())

    return wrapper


@decorater
def world():
    return 'World'

world()
```

---

## Flask Hello World
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

app.run()
```

---

## PyMySQL
### pure-Python MySQL client library <!-- .element: class="fragment fade-in" -->

---

## PyMySQL
```python
import pymysql

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

connection.commit()
connection.close()
```

---

### 음... 뭔가 너무 힘듭니다

---

## SQLAlchemy
### SQLAlchemy is the Python SQL toolkit <!-- .element: class="fragment fade-in" -->
### and Object Relational Mapper <!-- .element: class="fragment fade-in" -->

---

### ORM은 종교전쟁 진행중...
[ORM의 사실과 오해](http://okky.kr/article/286812) <!-- .element: class="fragment fade-in" -->

---

### ORM의 장점

- 데이터가 객체지향적으로 추상화된다 <!-- .element: class="fragment fade-in" -->
- 생산성이 높다 <!-- .element: class="fragment fade-in" -->
- 이론적으로 데이터베이스 따른 의존성이 없어진다 <!-- .element: class="fragment fade-in" -->

---

### SQLAlchemy 기능소개
- 객체 테이블 매핑 <!-- .element: class="fragment fade-in" -->
- 세션 관리, SQL 생성 <!-- .element: class="fragment fade-in" -->
- 테이블 생성, 삭제 <!-- .element: class="fragment fade-in" -->
- 더 있지만 써본것만... <!-- .element: class="fragment fade-in" -->

---

### 객체 테이블 매핑

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(64), unique=True)
```
---

### 세션 관리, 쿼리

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
```

---

### 세션 관리, 쿼리

```python
session = Session()

user = User(nickname='hueypark')
session.add(user)

session.commit()
```

---

### 세션 관리, 쿼리

```python
session = Session()

user = session.query(User).filter_by(name='hueypark').one()
session.delete(user)

session.commit()
```

---

### 테이블 생성, 삭제

```python
from sqlalchemy import create_engine
from .models import Base

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)
```

---

## PyJWT
### Python library which allows you to encode and decode JSON Web Tokens (JWT) <!-- .element: class="fragment fade-in" -->

---

## JSON Web Token
### JSON Web Tokens are an open, industry standard method for representing claims securely between two parties. <!-- .element: class="fragment fade-in" -->

---

## Token based authentication
### ?? <!-- .element: class="fragment fade-in" -->

---

## 누가 사용하나요?
### Facebook, Twitter, Google+, Github ... <!-- .element: class="fragment fade-in" -->

---

## 또 어떤 방법이 있죠?
### Session based authentication

---

### Session based authentication의 동작
1. 유저 -> 서버: 로그인, 서버는 유저정보를 session에 저장 <!-- .element: class="fragment fade-in" -->
2. 유저 <- 서버: session id <!-- .element: class="fragment fade-in" -->
3. 유저 -> 서버: 요청에 session id를 포함, 서버는 session에서 유저정보를 확인 후 응답 <!-- .element: class="fragment fade-in" -->

---

### Session based authentication의 문제점
- 부하 <!-- .element: class="fragment fade-in" -->
    - 유저가 인증할 때마다 서버에 인증정보를 저장
    - session을 유지하는 행위는 서버에 부하로 작용
- 확장성 <!-- .element: class="fragment fade-in" -->
    - session 정보가 메모리에 있다면 확장성에 문제
    - 공유되는 메모리의 한계가 서버 확장의 한계로 작용

---

### Token based authentication의 동작
1. 유저 -> 서버: 로그인, 서버는 유저정보를 기반으로 암호화된 token 생성 <!-- .element: class="fragment fade-in" -->
2. 유저 <- 서버: token을 클라이언트에 전달 <!-- .element: class="fragment fade-in" -->
3. 유저 -> 서버: 요청에 token을 포함, 서버는 token을 통해 유저정보 확인<!-- .element: class="fragment fade-in" -->

---

### 아직 잘 모르겠어요. 뭐가 다르죠?

---

## Token!
### 토큰이 유저정보를 가지고 있습니다! <!-- .element: class="fragment fade-in" -->

---

### Token은 세 부분으로 나누어짐
- HEADER <!-- .element: class="fragment fade-in" -->
- PAYLOAD <!-- .element: class="fragment fade-in" -->
- SIGNATURE <!-- .element: class="fragment fade-in" -->

---

### 이렇게 생겼습니다
#### eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. <!-- .element: class="fragment highlight-current-blue"-->
#### eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6. <!-- .element: class="fragment highlight-current-blue"-->
#### TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFO <!-- .element: class="fragment highlight-current-blue"-->

---

### HEADER에는 암호화 알고리즘과, 타입이 base64로 인코딩
```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

---

### PAYLOAD에는 데이터를 base64로 인코딩
```json
{
    "name": "John Doe",
    "admin": true
}
```

---

### SIGNATURE에 아래 결과를 base64로 인코딩
```
HS256(HEADER + "." + PAYLOAD, secretKey)
```

---

## Token과 함께 해서 가능한 일

- 서버는 상태 없음! 확장성! <!-- .element: class="fragment fade-in" -->
- 권한의 전달 (암호 없이!) <!-- .element: class="fragment fade-in" -->
    - Facebook 글쓰기 등

---

## PyJWT

```python
from jwt import encode

token = encode({'userid': userid}, JWT_SECRET, algorithm=JWT_ALGORITHMS)
```

---

## PyJWT

```python
from jwt import decode

decoded = decode(token, JWT_SECRET, algorithms=JWT_ALGORITHMS)
userid = decoded['userid']
```

---

## Q & A
