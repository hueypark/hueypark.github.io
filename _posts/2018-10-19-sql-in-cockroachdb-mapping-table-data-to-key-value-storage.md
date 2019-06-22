---
layout: post
title: "(번역) 칵로치디비(CockroachDB) 블로그 / CockroachDB에서의 SQL: 테이블 데이터를 키밸류 저장소에 매핑시키기"
date: 2018-10-19
tags: ["cockroachdb"]
---

원문: https://www.cockroachlabs.com/blog/sql-in-cockroachdb-mapping-table-data-to-key-value-storage/

Written by [Peter Mattis](https://www.cockroachlabs.com/author/peter-mattis/), [Tamir Duberstein](https://www.cockroachlabs.com/author/tamir-duberstein/) on Sep 16, 2015

<!--more-->

SQL? CockroachDB는 키밸류 저장소가 아닌가요?!?

과거에는 CockroachDB를 분산 및 트랜잭션 처리가 가능한 키밸류 저장소로 설명했습니다. 우리의 최종목표는 키밸류 API가 아니며, 몇 달 전부터 고수준의 데이터 API를 작업하기 시작했습니다. 풍부한 구조를 지원하기 시작하면서, 데이터를 조작하고 접근하기 위해 SQL을 지원할 것이라 예상했습니다. 이후 약간의 검토를 통해 피할수 없는 일이라 판단하고, SQL을 향해 최고속으로 나아갔습니다.

SQL 시스템에는 쿼리구문분석, 쿼리계획, 쿼리실행, 트랜잭션 및 영구저장과 같은 많은 구성요소가 있습니다. CockroachDB의 SQL 시스템은 내부 키밸류 저장소의 상단에 구축되어 정렬된 모노리틱 키밸류 맵을 활용하여 모든 SQL 테이블 데이터와 인덱스를 저장합니다. 이 글은 CockroachDB가 SQL 데이터를 키밸류 저장소로 매핑하는 것에 중점을 두고 매핑이 SQL 기능을 구현하는 방법을 보여줍니다. 향후 글에서는 쿼리분석, 계획 및, 실행에 관해 이야기하겠습니다.

SQL 테이블은 로우(컬럼의 집합)의 집합입니다. 각 컬럼은 타입(bool, int, float, string, bytes)을 가집니다. 테이블에는 로우의 범위를 효율적으로 검색할 수 있도록 연관된 인덱스가 있습니다. 이것은 키밸류 API와 전혀 달라 보입니다. 어떻게 SQL 테이블 데이터를 키밸류 저장소에 매핑할까요?

가장 중요한 점: CockroachDB 내부 키밸류 API는 여러가지 연산을 지원하며, 이 글에서 그 중 몇가지를 알아보겠습니다:

* `ConditionalPut(key, value, expected-value)` - 기존 값이 예상과 같을 경우에만 새로운 값을 설정합니다.
* `Scan(start-key, end-key)` - 시작(포함)과 종료(제외) 사이의 모든 키를 검색합니다.

CockroachDB에서 키와 밸류는 모두 무제한 바이트 값을 포함할 수 있습니다. 계속 살펴봅시다!

**키 인코딩**

SQL 테이블 데이터를 키밸류에 매핑하기 위한 기본 방법은 컬럼 데이터를 문자열로 인코딩하는 것입니다. 예를 들어, `<1, 2.3, "four">`의 튜플이 주어지면 이 문자열을 다음과 같이 인코딩합니다:

`/1/2.3/"four"`

가독성을 향상시키기 위해 값 사이에 슬래시 기호를 사용했습니다. 동작방식에 대해 설명할 수도 있지만, 간결함을 목적으로 구현이 아닌 속성에 관해서만 설명하겠습니다. 인코딩된 키는 각 키의 필드가 구분되게 정렬됩니다.

`/1/2.3/"four"`

`/2/3.1/"six"`

`/10/4.6/"seven"`

만약 이 문자열들을 그냥 정렬한다면 `/10/...` 이 `/2/...` 보다 먼저 나오게 됩니다. 인코딩이 이처럼 먼저 나오지 않게 하는 것은 약간의 마술처럼 보일 수 있는데, 자세한 내용에 관심이 있다면 [util/encoding](https://github.com/cockroachdb/cockroach/tree/master/util/encoding) 패키지의 {Encode,Decode}{Varint,Float,Bytes,Null}를 참조하십시오.

이 인코딩 도구를 이용하여 SQL 테이블 데이터의 인코딩을 살펴봅시다. CockroachDB에서 각 테이블에는 고유한 64비트 정수 ID가 할당되어 있습니다. 이 테이블 ID는 테이블과 연관된 모든 키의 접두사로 사용됩니다. 이제 다음 테이블과 데이터를 보겠습니다

```sql
CREATE TABLE test (
      key       INT PRIMARY KEY,
      floatVal  FLOAT,
      stringVal STRING
)

INSERT INTO test VALUES (10, 4.5, "hello")
```

모든 CockroachDB의 테이블은 기본키를 가져야 합니다. 기본키는 하나 이상의 컬럼으로 구성됩니다. 위 `test` 테이블에서는 하나의 컬럼으로 구성되어 있습니다. 일반컬럼(기본키가 아닌)의 키는 기본키를 접두사, 컬럼이름을 접미사로 설정한 후 분할해 저장합니다. `<10, 4.5, "hello">`는 `test` 테이블에 다음과 같이 저장됩니다.

|키|밸류|
|---|---|
|/test/10/floatVal|4.5|
|/test/10/stringVal|"hello"|

위 표에서, 우리는 `/test/`로 테이블 ID를 표현하고, `/floatVal`와 `/stringVal`를 컬럼 ID를 표현합니다(테이블의 모든 컬럼은 테이블 내에서 고유한 ID를 가집니다.). 기본키는 인코딩시 테이블 ID 바로 뒤에 옵니다. 이것이 CockroachDB SQL 구현에서 인덱스 스캔의 기본입니다.

내부를 살펴보면, 메타데이터를 볼 수 있습니다:

|설명|ID|
|---|---|
|test Table ID|1000|
|key Column ID|1|
|floatVal Column ID|2|
|stringVal Column ID|3|

숫자 형식의 키밸류 쌍은 다음과 같습니다:

|Key|Value|
|---|---|
|/1000/10/2|4.5|
|/1000/10/3|"hello"|

이 글의 나머지 부분에서는 키의 상징적 형식(문자열)을 이용할 것입니다.

\[키에 대한 공통 접두어 `/1000/10`이 저장소를 낭비하고 있지만, 기본 스토리지 엔진인 [RocksDB](https://rocksdb.org/)는 키의 접두어 압축을 통해 거의 모든 오버헤드를 제거합니다.\]

눈치가 빠른 독자라면 컬럼에 키밸류 쌍 정보가 있기 때문에 기본키를 따로 저장하는 것이 필요하지 않다는 것을 알 수 있을 것입니다. 사실, CockroachDB는 이것을 제거합니다.

특정 로우에 대한 모든 키는 기본키 접두사로 인하여 근처에 저장됩니다(키밸류 데이터는 정렬된 모노리틱 맵에 저장되므로 이 속성에 드는 비용은 `없습니다`.). 이렇게 하면 접두사의 Scan을 통하여 특정 행의 값을 검색할 수 있습니다. 이것이 CockroachDB가 내부적으로 하는 일입니다.

쿼리:

`SELECT * FROM test WHERE key = 10`

는 아래와 같이 변경됩니다.:

`Scan(/test/10/, /test/10/Ω)`

이 Scan은 로우에 대한 두개의 키를 검색합니다. `Ω`는 마지막 가능한 키를 의미하는 접미사입니다. 쿼리 실행 엔진은 키를 디코딩하여 행을 재구성합니다.

**Null 컬럼 밸류**

컬럼 값은 명시적으로 `NOT NULL`로 표시되지 않는 한, `NULL`일 수 있습니다. CockroachDB는 `NULL` 값을 저장하지 않으며, `NULL`을 나타내는 키밸류 값이 없음을 이용합니다. 행의 기본키가 아닌 모든 열이 `NULL`이면 아무 키도 저장하지 않으며, 이 문제를 해결하기 위해 모든 로우에 항상 컬럼 ID 접미사가 없는 센티넬키를 저장합니다. 예를 들어 `<10, 4.5, "hello">`의 경우 센티넬키는 `/test/10`이 됩니다. 짜잔!

**보조 인덱스**

지금까지 보조 인덱스를 무시했습니다. 이제 살펴봅시다:

`CREATE INDEX foo ON test (stringVal)`

이렇게 하면 stringVal 컬럼에 보조 인덱스가 만들어집니다. 인덱스에 유니크 속성을 선언하지 않았으므로 중복 값이 허용됩니다. 테이블의 로우와 비슷하게, 모든 인덱스 데이터를 테이블 ID 접두사가 있는 키에 저장합니다. 하지만 우리는 인덱스 데이터를 로우 데이터와 분리하고자 합니다. 기본키 인덱스를 포함하여 각 인덱스에 대해 고유한 인덱스 ID를 도입하여 이를 수행합니다(미안하지만, 이전에 거짓말을 했습니다!).

위 예에서 사용한 키는 약간 길어집니다:

|Key|Value|
|---|---|
|/test/primary/10|Ø|
|/test/primary/10/floatVal|4.5|
|/test/primary/10/stringVal|"hello"|

그리고 인덱스 foo에 대한 단일 키가 생깁니다:

|Key|Value|
|---|---|
|/test/foo/"hello"/10|Ø|

이 인코딩에서 기본키 값 `/10`을 접미사로 사용한 이유가 궁금할 수 있습니다. `foo`와 같은 유니크하지 않은 인덱스의 경우, 이것은 같은 값이 여러 로우에 표현되는데 필요합니다. 기본키는 고유하므로, 고유하지 않은 키의 접미사로 추가하면 키가 고유해집니다. 일반적으로, 고유하지 않은 인덱스의 경우, CockroachDB는 기본키의 인덱스 중 보조 인덱스에 포함되지 않은 모든 컬럼을 포함시킵니다.

이제 테이블에 `<4, NULL, "hello">`를 삽입하면 어떤 일이 발생하는지 봅시다:

|Key|Value|
|---|---|
|/test/primary/4|Ø|
|/test/primary/4/stringVal|"hello"|
|/test/foo/"hello"/4|Ø|

모든 테이블 데이터는 다음과 같습니다:

|Key|Value|
|---|---|
|/test/primary/4|Ø|
|/test/primary/4/stringVal|"hello"|
|/test/primary/10|Ø|
|/test/primary/10/floatVal|4.5|
|/test/primary/10/stringVal|"hello"|
|/test/foo/"hello"/4|Ø|
|/test/foo/"hello"/10|Ø|

보조 인덱스는 SELECT 처리 중에 작은 키 세트를 스캔하는데 사용됩니다:

`SELECT key FROM test WHERE stringVal = "hello"`

쿼리 플래너는 stringVal에 인덱스가 있음을 확인하고 이를 다음으로 변환합니다:

`Scan(/test/foo/"hello"/, /test/foo/"hello"/Ω)`

이것은 아래 키를 검색합니다.

|Key|Value|
|---|---|
|/test/foo/"hello"/4|Ø|
|/test/foo/"hello"/10|Ø|

이 키들이 stringVal 컬럼뿐만 아니라, 기본키 컬럼키도 포함함을 알 수 있습니다. CockroachDB는 기본키 컬럼키도 확인하고 불필요한 전체 행 조회를 피합니다.

마지막으로, 유니크 인덱스가 인코딩되는 방법을 살펴보겠습니다. 이전에 만든 인덱스 foo 대신 `uniqueFoo`를 생성합니다.

`CREATE UNIQUE INDEX uniqueFoo ON test (stringVal)`

유니크하지 않은 인덱스와 달리, 유니크 인덱스의 키는 인덱스의 컬럼으로만 구성됩니다. 키에 저장된 값은 인덱스 일부가 아닌 모든 키본키 컬럼의 인코딩입니다. 테스트 테이블의 두 행은 다음과 같이 인코딩됩니다.

|Key|Value|
|---|---|
|/test/uniqueFoo/"hello"|/4|
|/test/uniqueFoo/"hello"|/10|

유니크 제약 조건 위반을 나타내는 키가 이미 존재하는지 여부를 감지하기 위해 키를 작성할 때 `ConditionalPut`을 사용합니다.

이것이 CockroachDB가 SQL 데이터를 키밸류 저장소에 매핑하는 방법에 대한 간단한 설명입니다. 쿼리분석, 계획 및 실행에 대한 내용은 향후 게시물을 확인해주십시오.

_키밸류 저장소 위에 SQL을 구현하는 아이디어는 CockroachDB에만 국한된 것이 아닙니다. 이것은 MySQL의 InnoDB, Sqlite4 및 기타 데이터베이스의 본질적인 디자인입니다._
