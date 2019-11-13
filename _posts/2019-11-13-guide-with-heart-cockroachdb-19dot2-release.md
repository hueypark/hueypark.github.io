---
layout: post
title: "(안내서) 카크로치디비(CockroachDB) 블로그 / 카크로치디비 19.2 출시"
date: 2019-11-13
tags: [cockroachdb, guide]
---

카크로치디비 19.2가 릴리즈되었습니다. 레이턴시, 신뢰성, 편의성 측면에서 상당한 개선을 이야기하고 있는데, 인상 깊은 내용 몇 가지를 안내해 드리겠습니다.

<!--more-->

먼저 [카크로치 유니버시티](https://university.cockroachlabs.com/catalog)가 생겼습니다. 지금은 하나의 코스(`Getting Started With CockroachDB`)가 무료로 제공되고 있습니다.

다음으로 레이턴시 감소(단일 리전, 다중 리전 모두에서)입니다. 각각 2배, 20배의 성능향상을 이루었다고 소개하고 있는데, 자세한 내용은 [Parallel Commits: 분산 트랜잭션에서 아토믹 커밋 프로토콜](https://www.cockroachlabs.com/blog/parallel-commits/)과 [벡터화된 실행 엔진을 구축한 방법](https://www.cockroachlabs.com/blog/how-we-built-a-vectorized-execution-engine/)에서 확인할 수 있습니다. 더 자세한 내용은 다음에 다른 글을 통해 안내해 드리겠습니다.

마지막으로 [19.2 버전 테크니컬 데모](https://www.cockroachlabs.com/webinars/19-2-release)가 11월 20일 새벽 3시에 계획되어 있습니다. 관심 있는 분들은 일정에 등록해 놓으시길 바랍니다.

더 자세한 내용은 [Announcing CockroachDB 19.2](https://www.cockroachlabs.com/blog/cockroachdb-19dot2-release/)에서 확인하실 수 있습니다.
