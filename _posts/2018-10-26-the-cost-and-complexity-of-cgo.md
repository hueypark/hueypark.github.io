---
layout: post
title: "(번역) 카크로치디비(CockroachDB) 블로그 / cgo의 비용과 복잡성"
date: 2018-10-26
tags: ["go", "cockroachdb"]
---

원문: https://www.cockroachlabs.com/blog/the-cost-and-complexity-of-cgo/

<!--more-->

Written by [Tobias Schottdorf](https://www.cockroachlabs.com/author/tobias-schottdorf/) on Dec 9, 2015

[Cgo](https://blog.golang.org/c-go-cgo)는 [Go](https://golang.org/)에서 매주 중요한 부분입니다. 이것으로 Go가 아닌 부분(정확하게는 C 바인딩이 있는 부분)을 호출할 수 있습니다.

[CockroachDB](https://github.com/cockroachdb/cockroach)의 경우 우리가 아는 한 Go 생태계 내에서 적절한 대체물이 없었기 때문에, cgo를 사용하여 저장소 계층의 많은 부분을 [RocksDB](https://rocksdb.org/)에 위임하였습니다. 몇 차례의 시도 후, Go 래퍼 패키지를 사용하는 것이, 외부 라이브러리를 사용하는 올바른 방법(꽤 많은 경우에)이라는 것을 알게 되었습니다.

- [c-rocksdb](https://github.com/cockroachdb/c-rocksdb)
- [c-snappy](https://github.com/cockroachdb/c-snappy)
- [c-protobuf](https://github.com/cockroachdb/c-protobuf)
- [c-jemalloc](https://github.com/cockroachdb/c-jemalloc)
- [c-lz4](https://github.com/cockroachdb/c-lz4)

하지만 cgo를 사용하는 것에는 비용이 있습니다.

숙련된 cgo 사용자라면 알고 있는 내용이겠지만, cgo 사용에는 몇가지 주의사항이 있고 아래에서 알아보겠습니다.

### 호출 오버헤드

cgo 호출의 오버헤드는 Go 호출 오버헤드보다 훨씬 큽니다. 끔찍하게 들리지만 많은 애플리케이션에서 문제가 되지는 않습니다. [cgobench](https://github.com/tschottdorf/goplay/tree/master/cgobench)를 살펴봅시다.

```go
func BenchmarkCGO(b *testing.B) {
    CallCgo(b.N) // call `C.(void f() {})` b.N times
}

// BenchmarkGo must be called with `-gcflags -l` to avoid inlining.
func BenchmarkGo(b *testing.B) {
    CallGo(b.N) // call `func() {}` b.N times
}
```

```bash
$ go test -bench . -gcflags '-l'    # disable inlining for fairness
BenchmarkCGO-8  10000000              171 ns/op
BenchmarkGo-8   2000000000           1.83 ns/op
```

이 예제에는 최소한 100개 이상의 다른 고려사항이 관련되어 있습니다. 성능차이에 너무 놀라지 마십시오. 171나노세컨드는 C 코드가 상당한 작업을 수행하는 경우 이해할 만한 비용입니다. 하지만, 우리의 경우 테스트 중 십만 건 이상의 cgo 호출을 확인했기 때문에 코드 일부를 C로 넣어 반복 횟수를 줄이는 방법을 찾았습니다.

우리의 결론은 호출 오버헤드가 중요하지 않다는 것입니다(C++과 Go의 구현은 성능면에서 구분하기 어려움). 그러나 우리는 조금 더 효율적인 구현을 위해 일부 작업을 C++로 옮겼습니다.

### 수동 메모리 관리

Go는 가비지 컬렉션 런타임이지만, C는 그렇지 않습니다. 즉 C에서 Go로 또는 그 반대로 데이터를 부주의하게 전달하면 안되며, 복사본을 피할 수 없는 경우가 많습니다. 특히 높은 빈도로 바이트 문자열 교환(우리처럼)을 하면, [C.CString and C.GoBytes](https://golang.org/cmd/cgo/#hdr-Go_references_to_C)는 메모리를 많이 사용하며, CPU 사용량도 눈에 띄게 증가합니다.

때에 따라 이러한 복사 중 일부를 피할 수 있습니다. 예를 들어, 키를 반복 사용할 때 [이것](https://github.com/cockroachdb/cockroach/blob/b1bbc5c8f980c823e9ff1cd07032ce8ace35f669/storage/engine/rocksdb.go#L563)을 사용합니다.

```go
func (r *rocksDBIterator) Key() []byte {
   return C.GoBytes(unsafe.Pointer(r.key), s.len)
}

func (r *rocksDBIterator) Next() {
   // The memory referenced by r.key stays valid until the next operation
   // on the iterator.
   r.key = C.DBNext(r.iter) // cgo call
}
```

현재 키를 체크하는 것만 필요하다면, 불필요한 메모리가 계속 해제되지 않는 것을 확인할 수 있습니다. 따라서 아래의 코드에는 낭비가 있습니다.

```go
for ; iter.Valid(); iter.Next() {
    if bytes.HasPrefix(iter.Key(), someKey) { // copy!
        // ...
    }
}
```

이러한 복사를 완화하기 위해 우리는 복사없는(안전하지 않은) 버전의 `Key()`를 추가했습니다.

```go
// unsafeKey() returns the current key referenced by the iterator. The memory
// is invalid after the next operation on the iterator.
func (r *rocksDBIterator) unsafeKey() []byte {
    // Go limits arrays to a length that will fit in a (signed) 32-bit
    // integer. Fall back to copying if our slice is larger.
    const maxLen = 0x7fffffff
    if s.len > maxLen {
        return C.GoBytes(unsafe.Pointer(r.key), s.len)
    }
    return (*[maxLen]byte)(unsafe.Pointer(s.data))[:s.len:s.len]
}
```

이것은 적절히 사용될 때 안전하고 효율적이지만, 주의깊게 사용해야 합니다. 우리는 C에 의해 할당된 메모리를 사용하는 슬라이스를 생성합니다. 이를 사용하면 생성(또는 파생)된 슬라이스를 사용 중일 때 C 메모리가 해제되지 않도록 주의해야 합니다. 우리는 저수준의 코드에서 이것을 지킬 수 있지만, 공개된 API에 사용할 만한 옵션은 아닙니다. 사용자는 반환된 슬라이스가 가지는 미묘한 조건을 준수하지 않아, 무작위 널 포인터 참조 예외를 만나게 될 것입니다.

### Cgoroutines != Goroutines

이것은 심각한 문제입니다. 생각해보면 당연하지만, 그렇지 않았을 때 놀랄 수 있습니다. 아래를 살펴보십시오.

```go
func main() {
  for i := 0; i < 1000; i++ {
    go func() {
        time.Sleep(time.Second)
    }()
  }
  time.Sleep(2*time.Second)
}
```

1000개의 고루틴은 Go에서 거의 무료로 제공됩니다. 각각에 할당된 스택은 겨우 몇 킬로바이트입니다.

cgo에서는 어떨까요? 아래 코드는 [cgobench](https://github.com/tschottdorf/goplay/blob/master/cgobench/cgobench_test.go)의 예제를 단순화한 것입니다.

```go
//#include <unistd.h>
import "C"

func main() {
  for i := 0; i < 1000; i++ {
    go func() {
        C.sleep(1 /* seconds */)
    }()
  }
  time.Sleep(2*time.Second)
}
```

이것은 위와 `매우 다르게` 행동합니다. 블로킹 cgo 호출은 시스템 쓰레드를 점유합니다. Go 런타임은 고루틴처럼 스케줄을 지정할 수 없으며, 스택은 메가바이트 단위를 차지합니다.

적절하게 관리되는 동시성을 유지하며 cgo를 호출한다면 큰 문제는 아닙니다. 그러나 Go를 쓰고 있다면 고루틴에 대해 별도의 고려를 하지 않을 가능성이 높습니다. 주요 호출에서 cgo 호출이 차단되면 수만개의 쓰레드가 이 [이슈](https://groups.google.com/forum/#!topic/golang-nuts/8gszDBRZh_4)를 발생시킬 수 있습니다. 특히 `ulimit -r`나 `debug.SetMaxThreads`는 문제를 가속합니다.

[Dave Cheney](https://dave.cheney.net/),

> "과도한 cgo의 사용은 Go의 가벼운 동시성 보장을 깨뜨립니다."

### 크로스 컴파일 능력 상실

Go 1.5 이상에서도 cgo 크로스 컴파일은 쉽지 않습니다. 놀라운 일은 아니지만(C 의존성을 가진 크로스 컴파일은 반드시 C 의존성을 크로스 컴파일 해야 하기 때문에) Go 네이티브 패키지와 외부 라이브러리 중 하나를 선택해야 할 때 기준이 될 수 있습니다.

[Dave Cheney의 글](https://dave.cheney.net/2015/03/03/cross-compilation-just-got-a-whole-lot-better-in-go-1-5)은 이에 관한 가장 좋은 정보입니다.

### 정적 빌드

이것은 크로스 컴파일과 비슷한 이야기지만, 조금 더 나은 상황입니다. cgo로 정적 바이너리를 만들 수 있지만, 약간의 조정이 필요합니다. Go 1.5 이전에는 DNS 확인을 위해 glibc에 연결하지 않으려면 netgo 태그를 사용해야 했습니다. 이후 이것이 기본값으로 바뀌었지만, 몇가지 커스텀 플래그(정적이 아닌 빌드에서 캐시를 피하기 위해 `-installsuffix`, 외부 링커에서 적절한 플래그 전달을 위해 `-extldflags`, 전체 리빌드를 위해 `-a`)를 필요로 합니다.

이 모든 것이 더 이상 필요하지는 않지만 이런 생각이 듭니다. 수동 작업이 많아지고, 전체를 리빌드하며, 느려집니다. 관심 있는 분들을 위해 [저와 cgo의 첫 대결](https://tschottdorf.github.io/linking-golang-go-statically-cgo-testing/)과 우리가 추후 글에서 다룰 수 있는 [알 수 없는 버그](https://github.com/golang/go/issues/13470)를 소개합니다.

### 디버깅

디버깅이 어렵습니다. C의 구성요소는 Go의 툴링으로 접근할 수 없습니다. PProf, 런타임 통계, 줄 번호, 스택 추적 - 이 모든 것이 경계를 넘어가면 사라집니다. GoRename과 그 친구들은 가끔  날자정보를 포함한 식별자를 가진 [당신의 소스 코드를 버립니다](https://github.com/golang/tools/blob/5b9ecb9f68e2e1be33b663895c700aac9726378e/refactor/rename/rename.go#L425). 툴링을 사용할 수 없는 손실은 고통스럽지만, 다행히 gdb는 잘 동작합니다.

### 요약

cgo는 한계가 있지만 훌륭한 도구입니다. 우리는 몇몇 저수준 작업을 C++로 옮기기 시작했는데, 다른 방법으로는 해결할 수 없었던 [인상적인 속도향상](https://github.com/cockroachdb/cockroach/pull/3155)을 보여주었습니다. 멋있지 않나요?
