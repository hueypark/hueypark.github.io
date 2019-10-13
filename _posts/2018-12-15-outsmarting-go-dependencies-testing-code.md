---
layout: post
title: "(번역) 카크로치디비(CockroachDB) 블로그 / Go 테스트 코드 의존성 압도적으로 관리하기"
date: 2018-12-15 00:00:00 +0900
tags: [cockroachdb, test]
---

원문: https://www.cockroachlabs.com/blog/outsmarting-go-dependencies-testing-code/

<!--more-->

---

읽는 시간: 9분

시스템이 자주 변경될 때 좋은 테스트를 작성하는 것은 까다롭습니다. Go의 테스트 인프라를 여러 모듈에서 사용하면 컴파일러에서 허용하지 않는 종속성 사이클을 유발할 수 있습니다. 이 글에서 이러한 종속성 사이클을 깨기 위해 만들어진 기술을 살펴보겠습니다.

## 배경지식

CockroachDB `go` 코드 기반은 다양한 패키지로 나뉩니다. 주요 패키지는 다음과 같습니다.

- `storage`: 로컬 저장소 인터페이스
- `kv`: 키밸류 저장소
- `sql`: SQL 계층(키밸류 상단에 있음)
- `server`: 네트워크 포트에 PostgreSQL 인터페이스를 노출하는 CockroachDB 노드 설정을 위한 고레벨 코드. 노드는 `kv`와 `sql` 서버를 포함합니다.

![](/assets/post/2018-12-15-outsmarting-go-dependencies-testing-code/img1.png)

우리는 `sql`과 `server` 패키지에 집중할 것입니다. `server` 패키지는 CockroachDB 노드의 SQL 서버 부분을 구성하기 때문에 `sql` 패키지에 의존합니다.

대부분의 `sql` 테스트는 테스트 서버를 만들어 일부 SQL 문을 실행하며 잠재적으로 내부 구현을 확인할 수 있습니다. 테스트 서버를 시작하기 위해 우리는 `server`의 코드를 활용하길 원합니다. 그러나 `sql` 패키지 테스트는 순환 종속성을 생성하므로 `server` 패키지에 의존할 수 없습니다.

이 문제는 CockroachDB에만 국한되지 않습니다. 테스트는 논리적인 경계를 넘나드는 경향이 있으므로 많은 대형 코드베이스는 이 문제를 마주할 수 있습니다. 아무튼, 사랑과 전쟁 그리고 테스트 코드에서는 모든 수단이 정당합니다.

## 첫 솔루션

첫 번째 솔루션은 블랙박스 테스팅을 위해 `Go`의 기능을 사용하는 것이었습니다(테스팅은 public 인터페이스에 대해서만 가능). `Go`에서 `sql` 패키지의 테스트를 `sql_test` 패키지의 일부로 선언 가능합니다. 의존성에 관한 한 별개의 패키지이므로 종속성 순환이 깨져서 `server`를 가져올 수 있습니다. 단점은 이 패키지에서 `sql` 내부에 접근할 수 없는 것입니다. 그래서 우리는 오직 테스트를 위해 내부 구조를 외부로 노출시키거나 `sql_test` 코드의 일부분을 분리하여 `sql` 테스트 코드로 옮겼습니다.

시간이 지날수록 이것은 점점 더 성가시게 되었습니다. 분산 SQL 구현을 위한 새 `distsql` 패키지에 대한 작업을 시작했을 때 우리는 테스트를 위해 많은 패키지 내부구조를 다시 노출해야 했습니다. 더 나은 솔루션이 필요해졌습니다.

## 더 나은 솔루션을 향하여

우리는 `sql` 패키지 내부에 직접 접근할 수 있는 곳에서 `sql` 테스트를 작성하는 것을 원했습니다. 테스트 서버를 인스턴싱하기 위해 `server` 코드를 호출하는 유일한 방법은 `sql`이나 `server`에 의존하지 않지만 그들 사이에 간접적으로 인터페이싱하는데 사용할 수 있는 심 계층을 사용하는 것입니다.

![](/assets/post/2018-12-15-outsmarting-go-dependencies-testing-code/img2.png)

우리는 그 개념을 사용하는 간단한 [개념증명](https://github.com/RaduBerinde/playground/tree/777beb8/test_dep_prototype)을 했습니다. [server](https://github.com/RaduBerinde/playground/tree/777beb8/test_dep_prototype/server)와 [sql](https://github.com/RaduBerinde/playground/tree/777beb8/test_dep_prototype/sql) 패키지는 지금까지 설명한 실제 패키지를 나타냅니다. [testingshim](https://github.com/RaduBerinde/playground/blob/777beb80c7e5933f89ee1fd28216717f93e0a856/test_dep_prototype/server/testingshim/testserver.go)은 `sql` 테스트를 통해 접근하고자 하는 `server` 기능을 위한 인터페이스를 정의합니다. 그러나 실제로 `server` 또는 `sql`에 의존하지 않습니다. `sql`에 정의된 타입을 사용하거나 반환해야 하는 메소드는 `interface{}`를 사용하여 간접적으로 표현할 수 있습니다.

```go
package testingshim

// TestServerInterface defines test server functionality that tests need.
type TestServerInterface interface {
  SQLSrv() interface{}
  // Other needed stuff goes here.
}

// TestServerFactory encompasses the actual implementation of the shim
// service.
type TestServerFactory interface {
  // New instantiates a test server instance.
  New() TestServerInterface
}
```

이 계층은 핵심은 전역 상태입니다. `serviceImpl`은 `InitTestServerFactory`를 통해 인터페이스의 외부 에서 설정될 수 있습니다.

```go
var serviceImpl TestServerFactory

// InitTestServerFactory should be called once to provide the implementation
// of the service. It will be called from a xx_test package that can import the
// server package.
func InitTestServerFactory(impl TestServerFactory) {
  serviceImpl = impl
}

func NewTestServer() TestServerInterface {
  return serviceImpl.New()
}
```

이 아이디어는 `sever`가 `TestServerFactory`를 구현하고, `server`와 `testingshim` 모두에 접근할 수 있는 것이 `InitTestServerFactory`를 호출하여 `NewTestServer`와 같은 함수를 호출하는 `sql` 테스트를 허용합니다. "이 방법"을 우리는 한동안 사용했습니다. 하지만...

## 핵

퍼즐의 마지막 조각은 `sql_test` 패키지를 허용하는 블랙박스 테스팅 기능을 중심으로 하지만 더 독착정인 방법입니다. `go test` [문서](https://golang.org/cmd/go/#hdr-Test_packages)는 다음과 같이 설명합니다.

> 접미사 "_test"가 있는 패키지를 선언한 테스트 파일은 별도의 패키지로 컴파일된 다음 기본 테스트 바이너리와 링크되어 실행됩니다.

그러므로 우리가 `server`를 사용하는 `sql_test` 코드를 가진다면, `server` 코드 또한 테스트에 포함됩니다. `Go`는 단지 `sql`의 일부로 된 테스트에서만 접근을 막습니다. 여기서 "아하!"는 `TestMain()`입니다. `TestMain`은 테스트하기 전에 추가 설정을 수행하는데 사용할 수 있는 선택적 기능입니다. `TestMain`은 `sql` 또는 `sql_test` 패키지 중 하나에 있을 수 있습니다. `sql`에 넣으면 `sql` 테스트를 실행하기 전에 `server`에 접근하는 초기화 코드를 실행할 수 있습니다!

- 참고: `TestMain`의 대안은 `sql_test` 파일에서 `init()` 함수를 사용하는 것입니다.

이것은 [개념증명](https://github.com/RaduBerinde/playground/tree/777beb8/test_dep_prototype)으로 다시 설명됩니다. `sql_test` 패키지에서 [TestMain](https://github.com/RaduBerinde/playground/blob/777beb8/test_dep_prototype/sql/sql_test.go#L18)은 `server`와 `testingshim`에 동시에 접근합니다. `TestSrvInstance` 글로벌을 `server`에 의해 구현된 타입으로 초기화 할 수 있습니다.

```go
func TestMain(m *testing.M) {
  ..
  testingshim.InitTestServerFactory(server.TestServerFactory)
  ..
}
```

그리고 `sql` [테스트](https://github.com/RaduBerinde/playground/blob/777beb8/test_dep_prototype/sql/foo_test.go)가 `testingshim.NewTestServer()`을 사용합니다.

```go
package sql
..
func TestFoo(t *testing.T) {
   testingshim.NewTestServer().SQLSrv().(*SQLServer).Woof()
}
```

의존성 그래프는 아래와 같습니다.

![](/assets/post/2018-12-15-outsmarting-go-dependencies-testing-code/img3.png)

[본격적인 변화](https://github.com/cockroachdb/cockroach/pull/6473)는 더 복잡하지만, 이 간단한 원칙을 따릅니다. 의존성 없는 `testingshim` 패키지를 만드는 한 번의 노력은 앞으로 테스트를 쉽게 작성하게 하는 가치가 있습니다. 특히 우리는 [다른 패키지](https://github.com/cockroachdb/cockroach/pull/6561/files#diff-dbca7145ea6bc0b0e6eac8de3e536d2f)에서 같은 프레임워크를 쉽게 사용할 수 있었습니다.

`Go` 코더 여러분 - 같은 문제에 마주쳤을 때 이 트릭이 유용하다면 우리에게 알려주십시오!