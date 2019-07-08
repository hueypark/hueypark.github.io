---
layout: post
title: "(번역) 카크로치디비(CockroachDB) 블로그 / 왜 Go가 CockroachDB에 올바른 선택인가"
date: 2018-10-21
tags: ["go", "cockroachdb"]
---

원문: https://www.cockroachlabs.com/blog/why-go-was-the-right-choice-for-cockroachdb/

Written by [Jessica Edwards](https://www.cockroachlabs.com/author/jessica-edwards/) on Nov 3, 2015

![](/assets/post/2018-10-21-why-go-was-the-right-choice-for-cockroachdb/cockroach_gopher_flag_sticker.png)

<!--more-->

많은 개발자들이 우리게게 묻는 첫 번째 질문은, 가비지 컬렉터가 있는 Go언어로 분산 데이터베이스를 작성하는 것에 대한 경험입니다. JVM 가비지 컬렉션은 꽤 비싼데, Go로 만드는 것은 CockroachDB의 성능을 위험에 처하게 할 수 있지 않은가요?

사실, 고성능 분산 시스템을 만들 때에는, C++, Java 및 Go와 같은 소수의 언어만 사용할 수 있습니다. Java는 성능 문제로 인해 매력이 없으며, 지금까지 많은 사람들이 C++로 개발해왔지만 자체 라이브러리 제작에 많은 노력이 필요하여, 작업이 훨신 복잡해집니다.

창립자를 포함한 대부분의 개발자에게 Go언어는 새로운 언어였지만, Go의 라이브러리, 인터페이스 및 툴 지원은 CockroachDB를 위해 적절한 선택이었습니다.

Go가 잘 맞다고 느끼는 이유는 언어에 대한 경험의 부족이 컨트리뷰터에게 장벽이 되지 않기 때문입니다. Go는 Java 또는 C++ 경험이 있는 모든 사람이 신속하게 사용할 수 있습니다. 지금은 프로젝트에 67명의 컨트리뷰터가 생겼고, CockroachDB는 빈 프로젝트에서 125,000줄(자동생성을 제외한)의 Go 코드로 성장했습니다. 코드 복잡성을 관리하는 것은 언어 선택에 명백한 영향을 주며, 오픈소스일 경우 특히 중요합니다.

Go가 C++ 또는 Java보다 얼마나 큰 생산성을 내는지 정량화하기는 어렵습니다. 하지만 Go는 단순성 및 직교성에 중점을 두고 대규모 코드로 확장할 수 있게 디자인되었습니다. 강제된 코딩 스타일, 간단하고 자동화된 import 관리, 다양하게 제공되는 linter, 간결하고(최소화된) 문법 등, Go가 가진 모든 특성은 깔끔하고, 이해하기 쉬운 코드를 위해 중요합니다.

Java와 비교하여 인터페이스 추가시점(초기화 시점이 아니라)이 자유롭기 때문에, 추상화보다 구현에 집중할 수 있었습니다. C++보다 좋은 점은 자동 메모리 관리와 단일화된 작업방식 제공이었습니다. 동기화를 위해 채널을 효율적으로 사용할 수 있었습니다.

물론 성능에 관한 문제가 아직 Go에 남아있습니다. 아직 CockroachDB의 핵심 기능을 구현중이기 때문에 성능 프로파일링은 대부분 나오지 않았습니다. 그러나 과거 Java에서 Go로 큰 시스템을 포팅하였을 때, 메모리 사용량과 가비지 컬렉션 오버헤드를 크게 줄일 수 있었던 경험이 있습니다.

[베타버전](https://github.com/cockroachdb/cockroach/issues/2132)이 완성되고 성능개선에 집중하게 되면, 후속 결과를 공유드리겠습니다.
