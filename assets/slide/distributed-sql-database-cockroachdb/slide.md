## 분산 SQL 데이터베이스
## CockroachDB

jaewan.huey.park@gmail.com

---

## CockroachDB

![](/assets/slide/distributed-sql-database-cockroachdb/cockroachdb.png)

CockroachDB: 글로벌 비즈니스를위한 초탄성 SQL

https://www.cockroachlabs.com/

---

## CockroachDB 기능

- Distributed SQL
- Cloud Neutral
- Massive Scalability
- High Availability
- Geo-Distributed

---

## 먼저 사례를 살펴봅시다

- ??게임
	- 서버 통합 점검: 약 24시간
	- 서버 이전: 약 1시간

왜 이렇게 오래 걸릴까요?

---

## 원인은 물리적으로 분산된
## 데이터베이스 처리

데이터베이스 이야기를 조금 하겠습니다.

---

## 1960년대: 최초의 데이터베이스

- 계층구조에 대한 참조로 이루어진 레코드 집합
- 쿼리는 구조를 순회하며 시간을 소모해야 했음
- 논리적 스키마와 물리적 스키마가 독립되지 않음
	- 쿼리마다 모든 데이터를 다시 읽어야 함
- 많은 프로그래머가 필요

---

## 1970년대: SQL / RDBMS

- 관계형 모델이 이전 데이터베이스를 대체
	- 간단한 데이터 구조와 고레벨 SQL을 제공
	- 쿼리와 물리적 저장소는 분리됨
- 개발자 친화적
- 물리장비 하나에서 실행되게 설계

---

## 1980년대: SQL과 RDBMS의 성장

- SQL 데이터베이스는 성숙하여 업계를 점령
- 오브젝트 기반 데이터베이스가 시도되었으나 성과를 내지 못함
	- 복잡한 쿼리 지원 불가
	- 모든 시스템에서 공용되는 표준 API가 없음

---

## 2000년대 초반: 커스텀 샤딩

- 급속한 성장은 새로운 솔루션을 필요로 함
- 기업들은 커스텀한 미들웨어를 사용해 샤드된 단일 데이터베이스에 접근
- 샤드간의 트랜잭션은 불가능했고, 운영은 고통스러웠음

> ??게임이 여기 어딘가 있습니다.

---

## 2004+: NoSQL

- 계속적인 성장, 운영의 문제점은 새로운 시스템을 필요로 함
- 우선순위가 변경됨 - 큰 스케링과, 가용성이 다른 무엇보다 중요해짐
- 많은 다른 부분을 희생함
	- 관계형 모델(SQL을 사용하지 않고 커스텀 API 제공)
	- 트랜잭션과 인덱스가 없음(또는 매우 제한됨)
	- JOIN은 수동으로 해야 함

---

## 다시 ??게임

NoSQL을 사용하면 어떨까요?

실제로 NoSQL을 사용한 게임은 꽤 있습니다.

---

## 데이터베이스의 한계

기존 데이터베이스 솔루션은 애플리케이션 개발자에게 과도한 부담을 줍니다.

- Scale(sql)
- Fault tolerance(sql)
- Limited transactions(nosql)
- Limited indexes(nosql)
- Consistency issues(nosql)

---

## 강한 일관성과 트랜잭션

> 우리는 병목 현상이 발생할 때 트랜잭션 과다로 인해 성능 문제를 처리하는 것이, 트랜잭션 처리를 직접 해야하는 것보다 낫다고 생각합니다.

- 구글 스패너

---

## 2010년대: "NewSQL" / Distributed SQL

- SQL 문법을 모두 지원하는 분산 데이터베이스
- 두 세계의 장점을 결합하려고 시도
	- 모든 SQL 문법
	- 수평 확장과 고가용성
- 완전히 새로운 시스템으로 기존 데이터베이스를 활용하기가 어려움
- Google의 Spanner 시스템(2012년 배포)
- CockroachDB는 오픈소스로 2014년에 개발되었음

---

## 마지막으로 ??게임

만약 분산 SQL 데이터베이스가 ??게임에 적용되었다면 어땠을까요?

아래 기능은 더 쉽게 구현되고, 더 빠르게 동작했을 것입니다.

- ??게임
	- 서버 통합 점검: 약 24시간 -> ??
	- 서버 이전: 약 1시간 -> ??

---

## CockroachDB의 가능성

> 버전 2.1과 관리형 서비스 출시

- PostgreSQL 동일한 인터페이스 지원
- MySQL, PostgreSQL, csv에서 데이터 마이그레이션을 지원하는 툴 지원(Beta)
- Baidu, Kindred, Bose 등 사용사례가 늘어나고 있음

---

## 현실적인 제약사항

- 데이터베이스에게 안정성은 매우 중요한 항목
- 레퍼런스가 충분히 생기기 전에는 도전적인 프로젝트에서만 도입가능

---

## 재미있는 이야기

2012년에 구글을 퇴사하여 사진공유 플랫폼을 만들던 세 사람(Ben, Peter & Spencer)이 구글의 인프라를 그리워하며 만든 오픈소스 대체품

https://marsettler.com/2018/10/15/cockroachdb-blog-hello-world.html

---

## Q & A

---

## References

- https://github.com/cockroachdb/cockroach
- https://www.cockroachlabs.com/docs/stable/training/
