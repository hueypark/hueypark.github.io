---
title: "(번역) CockroachDB blog / Go에서 가비지 컬렉션을 최적화하는 방법"
date: 2018-10-23
tags: ["Go", "CockroachDB"]
---

원문: https://www.cockroachlabs.com/blog/how-to-optimize-garbage-collection-in-go/

Written by [Jessica Edwards](https://www.cockroachlabs.com/author/jessica-edwards/) on Nov 23, 2015

![](/post/2018-10-23-how-to-optimize-garbage-collection-in-go/gc.jpg)

<!--more-->

몇 주 전 CockroachDB에서 Go를 선택한 이유에 대한 [글](/post/2018-10-21-why-go-was-the-right-choice-for-cockroachdb/)을 공유했을 때, Go의 알려진 문제(성능, 가비지 컬렉션, 데드락)를 처리하는 방법에 대한 여러 가지 질문을 받았습니다.

이 글에서는, Go의 가비지 컬렌션과 관련된 성능 문제를 완화하는 몇 가지 강력한 최적화 방법을 설명하겠습니다. 특히, 구조체 임베딩, sync.Pool 및 배열 재사용을 통해, 메모리 할당을 최소화하고 가비지 컬렉션 오버헤드를 줄이는 방법을 공유하겠습니다.

### 메모리 할당 최소화와 가비지 컬렉션 최적화

Go가 Java와 다른 점은 Go가 메모리 레이아웃을 관리할 수 있다는 것입니다. Go를 사용하면 다른 가비지 콜렉션 언어에서는 별도의 할당이 되는 것을 하나로 결합할 수 있습니다.

디스크에서 데이터를 읽고, 디코드하는 아래 CockroachDB의 코드를 보십시오:

```go
metaKey := mvccEncodeMetaKey(key)
var meta MVCCMetadata
if err := db.GetProto(metaKey, &meta); err != nil {
    // Handle err
}
...
valueKey := makeEncodeValueKey(meta)
var value MVCCValue
if err := db.GetProto(valueKey, &value); err != nil {
    // Handle err
}
```

데이터를 읽기 위해, 4번의 할당(MVCCMetadata, MVCCValue와 두 개의 키)을 합니다. Go는 구조체를 묶고 키 공간을 미리 할당하여 단일 할당으로 줄일 수 있는 기능을 제공합니다.

```go
type getBuffer struct {
    meta  MVCCMetadata
    value MVCCValue
    key   [1024]byte
}

var buf getBuffer
metaKey := mvccEncodeKey(buf.key[:0], key)
if err := db.GetProto(metaKey, &buf.meta); err != nil {
    // Handle err
}
...
valueKey := makeEncodeValueKey(buf.key[:0], meta)
if err := db.GetProto(valueKey, &buf.value); err != nil {
    // Handle err
}
```

위에서는 MVCCMetadata, MVCCValue를 포함하는 getBuffer를 선언합니다. 세 번째 멤버는 Go에서 슬라이스에 비해 자주 보이지 않는 배열입니다.

고정 크기의 배열(1024바이트)을 가지고 있으면 추가 할당 없이 작업을 할 수 있습니다. 이것은 getBuffer 구조체에서 세 개의 오브젝트를 임베딩하여 할당을 4분의 1으로 줄일 수 있습니다. 또한, 키가 동시에 사용되지 않으므로 배열을 재사용할 수 있습니다.

### sync.Pool:

![](/post/2018-10-23-how-to-optimize-garbage-collection-in-go/syncpool.jpg)

```go
var getBufferPool = sync.Pool{
       New: func () interface{} {
              return &getBuffer{}
       },
}
```

사실, sync.Pool에 대해 알기까지 약간의 시간이 걸렸습니다. 이것은 가비지 콜렉션 사이에 오브젝트를 재활용 가능하게 하는 목록이므로 추가 오브젝트 할당을 방지합니다. 매 가비지 콜랙션 주기가 시작될 때, 풀에서 오브젝트들이 지워집니다.

sync.Pool의 사용 예:

```go
buf := getBufferPool.Get().(*getBuffer)
defer getBufferPool.Put(buf)

key := append(buf.key[0:0], …)
```

먼저 팩토리 함수를 이용해 글로벌 sync.Pool 오브젝트를 선언합니다. 위 경우 getBuffer를 새로 생성하는 대신 풀에서 가져옵니다. `Pool.Get`은 빈 인터페이스 타입을 반환하고 type assert를 이용해 우리가 원하는 타입으로 변환할 수 있습니다. 그리고 오브젝트를 다 사용한 후에는 풀에 다시 반환합니다. 결과적으로 Buffer 구조체를 얻기 위해 추가적인 할당을 할 필요가 없어집니다.

### 배열과 슬라이스

배열과 슬라이스는 Go의 타입 중 하나이며, 대부분의 경우 슬라이스가 사용됩니다. 또 [:0] 구문을 사용하여 배열에서 슬라이스를 가져올 수 있습니다.

```go
key := append(buf.key[0:0], …)
```

이러면 배열을 사용하는 슬라이스가 만들어집니다. 이 슬라이스에 이미 백업 배열이 있기 때문에 `append`는 새로운 할당을 하는 대신 배열을 사용합니다. 따라서 키를 디코딩 할 때 버퍼로 만들어진 값을 슬라이스에 넣을 수 있습니다. 따라서 키 사이즈가 1KB 이하면 아무것도 할당하지 않고 이미 할당된 배열을 재사용합니다.

만약 키 크기가 1KB 이상인 경우가 발생하더라도, 슬라이스가 새 백업 배열을 할당하므로, 코드에서 이를 고려할 필요가 없습니다.

### Gogoprotobuf vs Google protobuf

마지막으로, 우리는 디스크에 저장하기 위해 프로토콜 버퍼를 사용합니다. 하지만 우리는 구글의 [protobuf](https://github.com/protocolbuffers/protobuf) 대신 [gogoprotobuf](https://github.com/gogo/protobuf)를 강력하게 추천합니다.

Gogoprotobuf는 불필요한 할당을 피하기 위해 위에서 강조한 원칙을 따릅니다. 특히, 배열로 백업할 수 있는 슬라이스를 이용해 마샬링 할 수 있습니다. 또한, null을 허용하지 않는다면 할당없이 메시지를 저장합니다.

마지막으로 Gogoprotobuf는 자동생성된 마샬링, 언마샬링 코드를 사용합니다. 이 방법은 표준 구글 프로토콜 버퍼 라이브러리에 있는 리플렉션 기반 마샬링 및 언마샬링보다 우수한 성능을 제공합니다.

### 결론

위의 기술을 결합하여, Go의 가비지 컬렉션 오버헤드를 최소화하고, 성능을 최적화할 수 있었습니다. 베타 버전을 만들어가며, 메모리 프로파일링에 진척이 있으면, 그 결과를 후속 글로 공유하겠습니다. 만약 Go 성능 최적화에 다른 정보가 있다면, 우리에게 알려주십시오.

일러스트 제공 [Mei-Li Nieuwland](https://www.liea.nl)
