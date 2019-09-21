## 거대한 단일 MMORPG 서버

[marsettler.com](https://marsettler.com)

---

## 이야기할 내용

1. 거대한 단일 MMORPG 서버
2. 기획 고려사항
3. 서버 고려사항과 해법
4. 데이터베이스 고려사항과 해법
5. 마무리하며

---

## 1. 거대한 단일 MMORPG 서버

는 정확히 무엇을 말하는 건가요?

---

### MMORPG를 먼저 정의해 봅시다

#### <span class="fragment">대규모 다중 사용자 온라인 롤플레잉 게임</span>

<span class="fragment">World of Warcraft,</span> <span class="fragment">EVE Online,</span> <span class="fragment">듀랑고,</span> <span class="fragment">검은사막,</span> <span class="fragment">...</span>

---

### MMORPG 서버 정의: 엔지니어링 측면

<span class="fragment">한 지역 내에서 X명의 유저가 상호작용</span>

<span class="fragment">X가 어느 정도이면 MMORPG 일까요?</span>

<span class="fragment">이 발표는 수백에서 수천명으로 가정합니다</span>

---

### 그러면 거대한 단일 MMORPG 서버란?

일반적인 서버와 가장 큰 차이는

서버들 사이에 있는 <span class="fragment" style="color:LightSkyBlue">물리적인 격리</span>

---

### 일반적인 MMORPG는

성능한계 해소를 위해 물리적으로 격리된 서버를 운영

<span class="fragment" style="color:LightSkyBlue">서로 다른 서버의 유저는 상호작용할 수 없음</span>

---

### 거대한 단일 MMORPG 서버는

이런 상호작용의 한계를 극복한 서버

---

## 잠깐 용어 정리

- 월드: 게임이 구현한 세상 전체
- 노드: 단일 물리서버
- 클러스터: 노드의 모음
- 지역: 노드 안에 있는 일정 지역

---

### 사례 1.

- 동시에 한 노드에서 플레이 가능한 유저 수: 10,000여명
- 노드간 데이터를 공유하여 언제든지 옮겨 다닐 수 있음

---

### 사례 2.

- 동시에 한 지역에서 플레이 가능한 유저 수: 100명
- 일점 이벤트가 발생할 때마다 100명의 유저를 모아줌
- 가까운 관계의 유저는 이벤트 발생 시에 같은 지역을 선택 가능

---

### 사례 3.

- 동시에 한 노드에서 플레이 가능한 유저 수: 거의 무한대?
- 좁은 지역에 많은 유저가 모이면 해당 지역의 시간이 느리게 감

---

### 사례 4.

- 한 노드에서 플레이 가능한 유저 수: 100여 명
- 유저가 늘어나면 노드가 늘어나고 노드간 이동이 어느정도 자유로움

---

### 이 사례 모두를

#### 거대한 단일 MMORPG 서버로 정의하고

#### 개발할 때 일반적으로 생기는 <span style="color:LightSkyBlue">고려사항</span>과

#### 그 <span style="color:LightSkyBlue">해결법</span>들을 알아보겠습니다.

---

## 2. 기획 고려사항

---

### 늘어나는 유저에 따른 인구밀도 증가

- 채널 방식
	- 다수의 게임이 쉽게 채용하고 있는 방식
	- 한 지역을 유저들이 직접 상호작용할 수 없는 여러 채널로 분리
- 절차적 지역 생성
	- 지역을 정해진 규칙에 따라 절차적으로 생성

---

### 특정 자산(부동산, 랭킹 등)의

희소성이 <span style="color:LightSkyBlue">너무 높아짐</span>

---

### 기존의 운영 노하우 적용 불가

<span class="fragment">신규유저의 격차를 줄이기 위한 신서버 오픈 등</span>

---

### 기획 고려사항은

기본만 알아보고 넘어갑니다

---

## 3. 서버 고려사항과 해법

---

### 매우 단순화된 서버

클라이언트 🤝 서버 🤝 데이터베이스

---

### 서버를 확장할 때 선택지

- 스케일 업<span class="fragment"> (단일장비 성능 개선 / 물리적 한계 명확함)</span>
- 스케일 아웃<span class="fragment" style="color:LightSkyBlue"> (여러 장비를 사용해서 부하분산)</span>

---

### 거대한 단일 MMORPG 서버는

궁극적으로 우리는 <span style="color:LightSkyBlue">스케일 아웃</span>을 필요로 함

---

#### HTTP 기반의 서비스들은 게임에 매우 자연스럽게

#### 스케일 아웃을 합니다. <span style="color:LightSkyBlue">왜 그럴까요?</span>

---

#### HTTP 기반의 서버는 기본적으로

#### <span style="color:LightSkyBlue">스테이트리스(상태가 없음)</span>

##### <span class="fragment" data-fragment-index="1">엄밀히 따지면 다른 무언가에게 위임</span>

##### <span class="fragment" data-fragment-index="1">(데이터베이스, 캐시 등)</span>

---

### TCP 기반의 MMORPG 서버도

### <span style="color:LightSkyBlue">스테이트리스</span>하게 만들 순 없을까요?

<span class="fragment">상태를 매우 자주 변경하기 때문에 쉽지 않음</span>

---

### 그렇다면 상태변경이 자주 일어나는 부분과

### 그렇지 않은 부분을 분리하면 어떨까요?

---

### 상태변경이 자주 일어나는 부분

- <span class="fragment">현재 HP</span>
- <span class="fragment">지역 내에서 이동중인 발사체</span>
- <span class="fragment">남은 총알의 수</span>
- <span class="fragment">등등등...</span>

---

### 상태변경이 자주 일어나지 않는 부분

- <span class="fragment">나의 모든 아이템 목록</span>
- <span class="fragment">나의 모든 퀘스트 목록</span>
- <span class="fragment">하루에 한 번 변경되는 이벤트 목록</span>
- <span class="fragment">등등등...</span>

---

### 사실 우리는 근 몇 년간의 개발에서

### 이미 많은 경험을 쌓음

#### <span class="fragment" style="color:LightSkyBlue">인게임</span					<a href="/tags/" class="btn"></span>Tags</a>
#### <span class="fragment" style="color:LightSkyBlue">아웃게임</sp					<a href="/tags/" class="btn"></span>Tags</a>n>

---

### 그렇다면 스테이이트풀한 부분(지역)은
### 어떻게 관리할까요

#### 지역이 다르면 <span style="color:LightSkyBlue">물리적으로 분산된 장비</span>에서 동작

---

### 지구 지역에서 화성 지역으로의 이동은

### 어떻게 처리할까요?

---

### 게임의 특성에 따라 달라지지만

### 일반적으로 두가지 중 하나를 선택해야 함

1. 특정 서버가 다운되면 유저 플레이 불가
2. 한 유저가 동시에 두 지역에 있는 것을 허용

---

### 월드의 구성

- 심리스가 아닌 월드
- 심리스 월드

---

### 심리스가 아닌 월드

- 지역 간 이동시 멈춤과 로딩이 발생

- 다른 지역 유저끼리 직접적인 상호작용 불가능

---

### 심리스 월드

- 지역 간 이동시 멈춤과 로딩이 없음

- 다른 지역 유저끼리 직접적인 상호작용 가능

---

### 심리스 월드 사례를 찾아보면

<span style="color:LightSkyBlue">단일 물리장비</span>에서

여러 코어를 효율적으로 사용하는 것에 초점

<span class="fragment" style="color:LightSkyBlue" data-fragment-index="1">여러 물리장비</span><span class="fragment" data-fragment-index="1">를 이용한 심리스 월드 구현?</span>

---

### 적용범위를 물리엔진으로 한정해서 고민

---

### 물리엔진 동작(매우 간략화한)

1. 오브젝트를 수집<span class="fragment" style="color:LightSkyBlue">(이 부분만 공유하면?)</span>
2. 물리 데이터를 계산
3. 데이터 기반으로 오브젝트를 업데이트

---

### 데모

https://github.com/hueypark/marsettler/tree/0.1

---

### 예상되는 고려사항

- 네트워크 부하
- 멀티쓰레드 환경에서 발생하는 이슈의 극대화

---

## 4. 데이터베이스 고려사항과 해법

---

### 데이터베이스의 스케일아웃의 경우

이미 여러 도메인에서 많은 연구가 진행됨

---

### 많이 사용되는 옵션은 크게 두 가지

- RDBMS 사용하며 스케일아웃(샤딩)과, 분산 트랜잭션 직접 처리
- NoSQL 사용(이벤츄얼 컨시스턴시 고려 필요)

---

### RDBMS의 사용하며 스케일아웃(샤딩)과, 분산 트랜잭션 직접 처리

---

#### 샤딩은 같은 테이블 스키마를 가진 데이터를

#### 다수의 데이터베이스에 분산하여 저장하는 방법

---

### 고려사항

- 유저의 데이터를 어떤 데이터베이스에 저장?
- 특정 데이터베이스에 부하가 몰리지 않게 하는 방법?
- 등등...

---

### 그래도 스케일아웃의 경우
### 범용적인 해법이 어느정도 정해져 있음

<span class="fragment">스케일인이 필요한 상황?</span>
<span class="fragment" style="color:LightSkyBlue">(빠르게 도주합니다.)</span>

---

### 분산 트랜잭션

트랜잭션은 <span style="color:LightSkyBlue">논리적 묶여진 단위작업</span>으로

데이터베이스가 제공하는 기능이지만,

2개 이상의 물리장비에서는 직접 구현 필요

---

### 예: 유저간 거래

1. A 유저 아이템 지급 <span class="fragment" style="color:LightSkyBlue">(직후에 장애가 발생하면?)</span>
2. B 유저 아이템 제거
3. A 유저 돈 감소
4. B 유저 돈 증가

---

### 이런 방법은 어떨까요?

1. BEGIN: 작업시작
2. END: 작업종료
3. PREPARE: 준비
4. COMMIT: 커밋

---

### 예: 유저간 거래 2

1. BEGIN
	- A 유저 아이템 지급하고 비활성화
	- A 유저 아이템 활성화 로그 추가
	- B 유저 아이템 비활성화
	- B 유저 아이템 삭제 로그 추가
	- A 유저 돈 감소용 로그 추가
	- B 유저 돈 증가용 로그 추가
2. END
3. PREPARE
	- 로그가 정상적으로 기록되었는지 확인
4. COMMIT
	- 관련 데이터를 락하고 적용
	- 중도에 실패시 로그 기반으로 모두 롤백

---

### 동작할까요?

 <span class="fragment">실제 서비스에는 더 많은 예외상황이 있음</span>

 <span class="fragment">개발 난이도 급상승</span>

---

### NoSQL 사용

- NoSQL을 한 마디로 정의하긴 어려움
- 일반적인 특징으로 수평 확장이 가능하지만 <span style="color:LightSkyBlue">이벤츄얼 컨시스턴시</span>에 대한 고려가 필요

---

### 이벤츄얼 컨시스턴시?

#### 한국어로는 최종 일관성이나,
#### 궁극적 일관성으로 불리기도 함
#### 뭔가 멋져보이는 이름이지만 사람 잡는 동작방식

---

### 극단적인 예

1. 보유 골드 1000
	- 1번 서버의 사냥으로 골드 100을 획득 1100
	- 2번 서버의 유저에게서 100원짜리 검 구매 900
2. 음?

--- 

#### 이처럼 단순한 예는 프로그래머가 통제할 수 있겠지만
#### MMORPG는 매우 다양한 컨텐츠를 가지고 있음

---

[이벤츄얼 컨시스턴시 풍자](https://www.reddit.com/r/Database/comments/avz1xk/eventual_consistency/)

---

### 어떤 방식을 사용하던
### 이 문제들을 모두 해결해야 함

#### <span class="fragment">누가?</span> <span class="fragment">프로그래머가!</span>
#### <span class="fragment" style="color:LightSkyBlue"> 그러면 기능은 누가?</span>

---

### 또 다른 해법

---

### 카크로치디비!

#### 오픈소스로 작성된, 클라우드 기반의 SQL 데이터베이스
#### 스케일 아웃, ACID 트랜잭션의 강한 일관성, SQL 제공

https://github.com/cockroachdb/cockroach

---

### NewSQL이라고 불리는
### 유사한 제품이 여러 개 있음

<span class="fragment" style="color:LightSkyBlue">선택은 당신의 몫</span>

<span class="fragment" style="color:LightSkyBlue">NoSQL이라고 불리는 데이터베이스들이 얼마나 서로 다른지 고려해보기 바랍니다.</span>

---

### 마무리하며

1. 거댄한 단일 MMORPG 서버
2. 기획 고려사항
3. 서버 고려사항과 해법
4. 데이터베이스 고려사항과 해법

---

### 누구나 그럴싸한 계획을 가지고 있다. 얼굴에 한방 쳐맞기 전까지는.

---

## 감사합니다.

[marsettler.com](https://marsettler.com)
