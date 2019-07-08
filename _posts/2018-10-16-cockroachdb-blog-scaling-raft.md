---
layout: post
title: (번역) 카크로치디비(CockroachDB) 블로그 / Raft를 스케일링하기
date: 2018-10-16
tags: ["cockroachdb"]
---

원문: https://www.cockroachlabs.com/blog/scaling-raft/

Written by [Ben Darnell](https://www.cockroachlabs.com/author/ben-darnell/) on Jun 11, 2015

![](/assets/post/2018-10-16-cockroachdb-blog-scaling-raft/multinode3.png)

<!--more-->

[CockroachDB](https://github.com/cockroachdb/cockroach)는 [Raft consensus algorithm](https://raft.github.io/)을 사용하여 장비가 고장났을 때도 데이터가 일관성을 유지하게 합니다. [etcd](https://github.com/etcd-io/etcd)나 [Consul](https://www.consul.io/)과 같이 Raft를 사용하는 대부분의 시스템에서, 전체 시스템은 하나의 Raft consensus 그룹으로 이루어집니다. 하지만 CockroachDB에서는, `Range`들로 데이터가 나늬며, 개별 Raft consensus 그룹을 가집니다. 즉, 각 노드가 수십만 개의 Raft consensus 그룹으로 나누어 질 수 있습니다. 이것은 몇가지 독특한 도전과제를 만들어내며, 우리는 [MultiRaft](https://github.com/cockroachdb/cockroach/tree/master/multiraft)라고 부르는 계층을 Raft 위에 도입하여 해결했습니다.

단일 `Range`에서 3개 또는 5개 노드 중의 하나가 리더로 선출되고, 주기적으로 팔로워에게 허트비트를 보냅니다.

<img src="/post/2018-10-16-cockroachdb-blog-scaling-raft/multinode1.png" width="300" height="216">

시스템이 커지고 더 많은 `Range`들을 가지게 되면, 허트비트를 처리하기 위한 트래픽 양도 들어납니다.

<img src="/post/2018-10-16-cockroachdb-blog-scaling-raft/multinode2.png" width="300" height="216">

`Range` 수가 노드 수보다 훨씬 많아지면(`Range`를 작게 유지하면 노드가 실패시 복구시간이 향상됩니다.), 중복되는 `Range`가 많아집니다. 이 때 `MultiRaft`가 필요합니다. 각 `Range`에서 개별적으로 Raft를 처리하는 대신, 전체 노드의 `Range`를 하나의 그룹으로 관리합니다. 아무리 많은 `Range`가 있더라도, 각 노드 쌍은 틱마다 한 번만 허트비트를 교환하면 됩니다.

<img src="/post/2018-10-16-cockroachdb-blog-scaling-raft/multinode3.png" width="300" height="216">

허트비트 네트워크 트래픽을 줄이는 것 외에도, MultiRaft는 다른 영역들에서 효율성을 향상시킵니다. 예를 들어, MultiRaft는 `Range`별 고루틴 대신 정해진 작은 수의 고루틴만(현재는 3)을 요구합니다.

Raft를 처음부터 구현하고 테스트하는 것은 어려운 일이므로, 처음부터 만드는 대신 CoreOS의 etcd 팀과 긴밀하게 협력하고 있습니다.

[etcd에서 Raft 구현](https://github.com/etcd-io/etcd/tree/master/raft)은 특별한 요구사항에 쉽게 적용할 수 있는, 깔끔한 추상화를 토대로 구축되었으며, 우리는 etcd와 커뮤니티를 개선하는 데 기여할 수 있었습니다.
