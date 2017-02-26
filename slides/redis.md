# Redis

---

### 박재완
#### jaewan.huey.park@gmail.com

* NextFloor 풀스택 게임 프로그래머 <!-- .element: class="fragment fade-in" -->
* 정체성의 혼란기를 격하게 격는 중 <!-- .element: class="fragment fade-in" -->
* AI 프로그래밍 하고 싶음 <!-- .element: class="fragment fade-in" -->

---

## 내용

* 들어가기 전에
* Redis?
* 주요기능
* 활용사례
* 주의사항

---

## 들어가기 전에

* Redis 공식 문서 번역이 대부분의 내용을 차지함 <!-- .element: class="fragment fade-in" -->
* 모든 명령어를 설명하지 않음 <!-- .element: class="fragment fade-in" -->
* 심화 기능을 물어보면 도망 갈 수 있음 <!-- .element: class="fragment fade-in" -->
* 프로젝트 사용 경험은 있음 <!-- .element: class="fragment fade-in" -->

---

## 몇가지 상황

---

### 상황 1

* 유저에게 공성전 정보를 보여주어야 함 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* 공성전 정보에는 현황, 길드정보, 유저정보등이 있음 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* 또 이 정보들을 조합해서 추가정보 생성  <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* 모든 요청마다 데이터베이스에서 정보를 가져와서 서버가 조합한다면? <!-- .element: class="fragment fade-in" data-fragment-index="4" -->

---

### 상황 2

* 공성전 결과에 따른 길드랭킹을 보여주어야 함 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

### 상황 3

* 가장 최근 100개의 공성전 통계를 보여주어야 함 <!-- .element: class="fragment fade-in" -->

---

## Redis?

In-memory data structure store (빠름) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

Database, Cahce, Message broker로 사용가능 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

Open source <!-- .element: class="fragment fade-in" data-fragment-index="3" -->

---

### 특징

* ANSI C로 작성 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* Linux, OS X, BSD를 지원함 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* Windows는 지원하지 않으나 Microsoft에서 유지중 <!-- .element: class="fragment fade-in" data-fragment-index="3" -->

---

### 주요기능

* Data structure <!-- .element: class="fragment fade-in" -->
* Transaction <!-- .element: class="fragment fade-in" -->
* LRU eviction <!-- .element: class="fragment fade-in" -->
* On-disk persistence <!-- .element: class="fragment fade-in" -->
* Replication <!-- .element: class="fragment fade-in" -->
* Cluster <!-- .element: class="fragment fade-in" -->

---

## Data structure

* Redis는 여러 종류의 data type을 지원 <!-- .element: class="fragment fade-in"-->

---

### Data structure 종류

* String <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* List <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* Set <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* Hash <!-- .element: class="fragment fade-in" data-fragment-index="4" -->
* Sorted set <!-- .element: class="fragment fade-in" data-fragment-index="5" -->

---

## Redis Key

_Redis는 key-value를 기본으로 데이터를 저장_ <!-- .element: class="fragment fade-in"-->

---

### Redis Key 특징

* Binary safe한 데이터 <!-- .element: class="fragment fade-in"-->
    * (문자열 뿐만 아니라 JPEG 같은 이미지도 사용가능)
* empty 문자열 허용 <!-- .element: class="fragment fade-in"-->
* 최대 허용 용량: 512 MB <!-- .element: class="fragment fade-in"-->
* Key는 자동으로 생성 및 삭제됨 <!-- .element: class="fragment fade-in"-->

---

### Redis String

* Binary safe한 데이터 <!-- .element: class="fragment fade-in"-->
    * (문자열 뿐만 아니라 JPEG 같은 이미지도 사용가능)
* 최대 허용 용량: 512 MB <!-- .element: class="fragment fade-in"-->

---

### Redis String 기본 명령어
* GET : data를 읽음, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* SET: data를 저장, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis String 기본 명령어

``` 
> SET mykey somevalue
OK

> GET mykey
"somevalue"
```

---

### Redis String 추가 명령어 (1/2)

* INCR : integer 1 증가, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* DECR : integer 1 감소, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* INCRBY : integer 값만큼 증가, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* DECRBY : integer 값만큼 감소, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis String 추가 명령어 (1/2)

```
> SET counter 100
OK

> INCR counter
(integer) 101

> INCR counter
(integer) 102

> INCRBY counter 50
(integer) 152
```

---

### Redis String 추가 명령어 (2/2)

* MSET : 여러 data를 동시에 저장, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* MGET : 여러 데이터를 동시에 가져옴, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

_Latency 감소에 효과적_ <!-- .element: class="fragment fade-in" -->

---

### Redis String 추가 명령어 (2/2)

```
> MSET a 10 b 20 c 30
OK

> MGET a b c
1) "10"
2) "20"
3) "30"
```

---

### 공용 명령어 (1/2)

_모든 타입에 공용으로 사용되는 명령어_ <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

* EXISTS : 데이터 존재여부 확인, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* DEL : 데이터를 동시에 삭제, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* TYPE : 데이터 타입 확인, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="4" -->

---

### 공용 명령어 (1/2)

```
> SET mykey hello
OK

> TYPE mykey
string

> EXISTS mykey
(integer) 1

> DEL mykey
(integer) 1

> EXISTS mykey
(integer) 0
```

---

### 공용 명령어 (2/2)

* EXPIRE : 만료시간 설정, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

###  공용 명령어 (2/2)

```
> SET key some-value
OK

> EXPIRE key 5
(integer) 1

> GET key (immediately)
"some-value"

> GET key (after sime time)
(nil)
```

---

### 공용 명령어 (2/2)

_추가적인 인자를 사용해 하나의 명령어로 만료시간을 설정할 수도 있음_

```
> SET key 100 EX 10
OK

> TTL key
(integer) 9
```

---

### EXPIRE 특징

* seconds, millisecons 두 종류의 정밀도 사용가능 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* On-disk persistence를 사용할 경우 서버가 중지되어 있던 시간은 계산되지 않음 (Redis가 유효기간이 지난 Key를 가지고 있을 수 있음) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis List

_List는 Linked List의 특징을 동일하게 가짐_ <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

* 데이터를 처음 또는 끝에 추가할 경우 유리 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* index로 데이터에 접근할 경우 불리 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis List 명령어 (1/3)

* LPUSH : List 왼쪽에 데이터 추가, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* LPOP : List 왼쪽의 데이터를 반환하고 삭제, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* LRANGE : List의 데이터를 반환, O(S+N) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
    * S: List 시작지점으로부터의 offset
    * N: 얻어 오는 데이터의 수

---


### Redis List 명령어 (1/3)

```
> RPUSH myslist A
(integer) 1

> RPUSH mylist B
(integer) 2

> LPUSH mylist first
(integer) 3

> LRANGE mylist 0 -1
1) "first"
2) "A"
3) "B"
```

---

### Redis List 명령어 (2/3)

* LTRIM : 선택된 인덱스 범위를를 제외한 데이터 삭제, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

_최근 몇 개의 데이터만 남기고 싶을 때 사용_ <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis List 명령어 (2/3)

```
> RPUSH mylist 1 2 3 4 5
(integer) 5

> LTRIM mylist 0 2
OK

> LRANGE mylist 0 -1
1) "1"
2) "2"
3) "3"
```

---

### Redis List 명령어 (3/3)

* BLPOP : blocking으로 동작하는 LPOP, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

_producer-consumer pattern을 효과적으로 구현가능_ <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Redis List 명령어 (3/3)

```
> BRPOP tasks 5
```

_데이터가 없어도 5초간 대기_ <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

### Redis List blocking 명령어 특징

* 여러 Client가 요청했을 경우 먼저 요청한 Client가 먼저 응답을 받음 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* 반환값에 key가 포함되어 있음 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* timeout이 되면 NULL이 반환됨 <!-- .element: class="fragment fade-in" data-fragment-index="3" -->

---

## Redis Hash

* Redis Hash는 자료구조 Hash를 기반으로 구현 <!-- .element: class="fragment fade-in" -->
* key-value 쌍으로 구성되어 있음 <!-- .element: class="fragment fade-in" -->
* 오브젝트를 나타내기 편함 <!-- .element: class="fragment fade-in" -->
* Hash에 저장할수 있는 인자의 수에는 제한이 없음 <!-- .element: class="fragment fade-in" -->

---

### Redis Hash 명령어

* HSET : Hash에 데이터를 저장, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* HGET : Hash에서 데이터를 가져옴, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* HMSET : Hash에 여러 데이터를 저장, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* HGETALL: Hash의 모든 데이터를 가져옴, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="4" -->

---

### Redis Hash 명령어

```
> HMSET user:1000 name antirez birthyear 1977 verified 1
OK

> HGET user:1000 name
"antirez"

> HGET user:1000 birthyear
"1977"

> HGETALL user:1000
1) "name"
2) "antirez"
3) "birthyear"
4) "1977"
5) "verified"
6) "1"
```

---

## 쉬는 시간입니다

---

## Redis Set

* 정렬되지 않은 Redis String의 집합 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* Set 안의 인자가 하나임을 보장함 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

### Reids Set 명령어

* SADD : Set에 데이터를 저장, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* SMEMBERS : Set에서 모든 데이터를 가져옴, O(N) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* SISMEMBER : Set의 데이터 존재유무 확인, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* SPOP: Set에서 무작위 데이터를 반환하고 지움, O(1) <!-- .element: class="fragment fade-in" data-fragment-index="4" -->

---

### Reids Set 명령어

```
> SADD myset 1 2 3
(integer) 3

> SMEMBERS myset
1. 3
2. 1
3. 2
```

---

### Reids Set 명령어

```
> SISMEMBER myset 3
(integer) 1

> SISMEMBER myset 30
(integer) 0
```

---

## Redis Sorted set

* 정렬이 되어있는 Set임 <!-- .element: class="fragment fade-in" -->
* 인자들은 score를 가지며 이를 기준으로 정렬됨 <!-- .element: class="fragment fade-in" -->
* Skip list와 Hash table 함께 사용해서 구현 <!-- .element: class="fragment fade-in" -->

---

### Redis Sorted set 명령어

* ZADD : Sorted set에 score와 데이터로 이루어진 데이터를 저장, O(log(N)) <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* ZRANK: Sorted set내 데이터의 rank를 반환, O(log(N)) <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* ZRANGE : 인덱스를 이용하여 score 오름차순으로 데이터 반환, O(log(N)+M) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->

---

### Redis Sorted set 명령어

```
> ZADD hackers 1940 "Alan Kay"
(integer) 1

> ZADD hackers 1957 "Sophie Wilson"
(integer 1)

> ZADD hackers 1953 "Richard Stallman"
(integer) 1
```

---

### Redis Sorted set 명령어

```
> ZRANK hackers "Richard Stallman"
(integer) 2
```

---

### Redis Sorted set 명령어

```
> ZRANGE hackers 0 -1
1) "Alan Kay"
2) "Richard Stallman"
3) "Sophie Wilson"
```

---

## 기타 명령어

* Bitmaps <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
    * bit 연산을 지원하는 명령어 집합
    * String 자료구조 사용
* HyperLogLogs <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
    * 매우 적은 메모리로 집합의 원소 개수를 추정하기 위한 명령어 집합
    * String 자료구조 사용

---

## Replication

Master-Slave replication 지원 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

### Master-Slave replication 목적

* 데이터베이스 읽기 Scale out <!-- .element: class="fragment fade-in" -->
* 데이터베이스 이중화 <!-- .element: class="fragment fade-in" -->
* 등등등... <!-- .element: class="fragment fade-in" -->

---

### Replication 특징

* 2.8버전부터는 비동기 replication을 지원 <!-- .element: class="fragment fade-in" -->
* Master는 복수의 Slave를 가질 수 있음 <!-- .element: class="fragment fade-in" -->
* Slave는 다른 Slave를 가질 수 있음 <!-- .element: class="fragment fade-in" -->
* Replication이 Master의 작업을 Blocking하지 않음 <!-- .element: class="fragment fade-in" -->
* Slave만 on-disk persistance를 지원하게 설정할 수 있음 <!-- .element: class="fragment fade-in" -->

---

## LRU eviction

* 캐시로 사용될 때 오래된 데이터를 삭제하는 방법 <!-- .element: class="fragment fade-in" -->
* LRU 알고리즘의 근사를 사용함 <!-- .element: class="fragment fade-in" -->

---

### Eviction policy 설정

* noeviction: 메모리가 초과할 경우 error <!-- .element: class="fragment fade-in" -->
* allkeys-lru: 모든 Key에 대해 LRU 알고리즘 사용 <!-- .element: class="fragment fade-in" -->
* volatile-lru: expire값이 설정된 key중 LRU 알고리즘 사용 <!-- .element: class="fragment fade-in" -->
* allkeys-random: 무작위 key 삭제 <!-- .element: class="fragment fade-in" -->
* volatile-random: expire값이 설정된 무작위 key 삭제 <!-- .element: class="fragment fade-in" -->
* volatile-ttl: expire값이 설정된 key 중 가장 짧은 생존시간을 가진 key를 삭제 <!-- .element: class="fragment fade-in" -->

---

## Transaction

---

### Transaction 특징

* roll back 기능을 지원하지 않음 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* Lua script를 통한 Transaction도 지원함 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->

---

## On-disk persistence

Redis persistence는 두가지 옵션을 제공함 <!-- .element: class="fragment fade-in" -->

---

## On-disk persistence

* RDB: 일정 시간 간격으로 데이터의 snapshot을 만드는 방식 <!-- .element: class="fragment fade-in" -->
* AOF: 모든 쓰기 operation을 저장해 놓았다가 서버가 재시작할 때 데이터를 새로 만드는 방식 <!-- .element: class="fragment fade-in" -->

---

### RDB의 장점

* RDB는 장애 복구에 유리함, 하나의 파일을 저장해 놓는 것만으로 데이터 백업이 가능 <!-- .element: class="fragment fade-in" -->
* RDB는 Redis의 performance를 최대로 이끌어 냄 <!-- .element: class="fragment fade-in" -->
* 서버 재시작이 빠름 <!-- .element: class="fragment fade-in" -->

---

### RDB의 단점

* RDB는 snapshot 사이의 데이터를 보존할 수 없음 <!-- .element: class="fragment fade-in" -->
* 만약 이 문제를 없애려고 snapshot 간격을 줄이면 performance 문제가 발생함 <!-- .element: class="fragment fade-in" -->

---

### AOF의 장점

* 설정에 따라 데이터를 쿼리 단위 또는 초 단위로 보존할 수 있음 <!-- .element: class="fragment fade-in" -->
* 모든 operation을 저장하기 때문에 이해하기 쉬운 데이터가 저장됨 <!-- .element: class="fragment fade-in" -->

---

### AOF의 단점

* AOF 파일은 일반적으로 RDB 파일에 비해 큼 <!-- .element: class="fragment fade-in" -->
* RDB 방식에 비해 실행 중 performance가 떨어짐 <!-- .element: class="fragment fade-in" -->
* 서버 재시작이 느림 <!-- .element: class="fragment fade-in" -->

---

## Redis Cluster

_데이터베이스 클러스터를 지원함_ <!-- .element: class="fragment fade-in" -->

---

### Cluster란 무엇인가?

여러 대의 컴퓨터를 연결하여 마치 하나의 컴퓨터처럼 사용하는 기술 <!-- .element: class="fragment fade-in" -->

---

### 데이터베이스에서 Cluster란?

_일반적으로 아래와 같은 목적을 달성하기 위해 구성됨_ <!-- .element: class="fragment fade-in" -->

* 고가용성: 특정 노드에 장애가 발생해도 서비스가 지속됨 <!-- .element: class="fragment fade-in" -->
* 병렬처리: 큰 작업을 분할하여 여러 노드에서 할 수 있음 <!-- .element: class="fragment fade-in" -->
* 성능향상: 대규모 데이터에 대한 처리를 효율적으로 할 수 있음 <!-- .element: class="fragment fade-in" -->

---

## 다시 몇가지 상황

---

### 상황 1

* 유저에게 공성전 정보 보여주어야 함 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* 공성전 정보에는 점령 현황, 각 길드정보, 길드의 유저 정보등이 있음  <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* 또 이 정보들을 조합해서 전투현황 정보를 생성함  <!-- .element: class="fragment fade-in" data-fragment-index="3" -->
* 모든 요청마다 데이터베이스에서 정보를 가져와서 서버가 조합한다면? <!-- .element: class="fragment fade-in" data-fragment-index="4" -->

---

### Redis String을 캐시로 사용

* GET : data를 읽음, O(1) <!-- .element: class="fragment fade-in" -->
* SET: data를 저장, O(1) <!-- .element: class="fragment fade-in" -->

_데이터를 가져올 때 Redis에 저장해 놓고 캐시로 사용_ <!-- .element: class="fragment fade-in" -->

_데이터에 변동이 발생하면 Key를 이용해 캐시 삭제_ <!-- .element: class="fragment fade-in" -->

---

### 상황 2

* 공성전 결과에 따른 길드랭킹을 보여주어야 함 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->

---

### Redis Sorted set 사용

* ZRANK: Sorted set내 데이터의 rank를 반환, O(log(N)) <!-- .element: class="fragment fade-in" -->

_길드점수를 score로 Sorted set에 저장_ <!-- .element: class="fragment fade-in" -->

---

### 상황 3

* 가장 최근 100개의 공성전 통계를 보여주어야 함 <!-- .element: class="fragment fade-in" -->

---

### Redis List 사용

* LPUSH : List 왼쪽에 데이터 추가, O(1) <!-- .element: class="fragment fade-in" -->
* LPOP : List 왼쪽의 데이터를 반환하고 삭제, O(1) <!-- .element: class="fragment fade-in" -->
* LRANGE : List의 데이터를 반환, O(S+N) <!-- .element: class="fragment fade-in" -->
* LTRIM : 선택된 인덱스 범위를를 제외한 데이터 삭제, O(N) <!-- .element: class="fragment fade-in" -->

_LPUSH로 데이터를 저장_ <!-- .element: class="fragment fade-in" -->

_LTRIM을 이용해 불필요한 데이터 삭제_ <!-- .element: class="fragment fade-in" -->

---

## 주의사항

---

### Redis는 싱글 쓰레드로 작동함

* Redis는 대부분 싱글 쓰레드로 디자인되어 있음 <!-- .element: class="fragment fade-in" data-fragment-index="1" -->
* 대부분의 경우에 단일 요청에 대한 응답이 매우 빠르므로 전체 성능에 영향을 주지 않음 <!-- .element: class="fragment fade-in" data-fragment-index="2" -->
* 새로운 명령어를 사용하게 된다면 시간 복잡도 확인 및 검증과정이 필요함 (KEYS, SORT, LREM, SUNION 등 주의) <!-- .element: class="fragment fade-in" data-fragment-index="3" -->

---

### 하나의 서버를 두가지 용도로 사용할때
### (캐시, 데이터베이스)

* 왠만하면... 안하는 것이... <!-- .element: class="fragment fade-in" -->
* LRU eviction 설정 필요 <!-- .element: class="fragment fade-in" -->
    * volatile-lru, volatile-random, volatile-ttl 중

---

## 참고자료

* http://redis.io

---

## 질문과 답변