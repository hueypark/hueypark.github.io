---
layout: post
title: "초보다 정밀한 단위에 대한 `EXTRACT` 명령이 postgres와 다르게 동작함(CockroachDB issue #40683)"
date: 2019-10-13
tags: [cockroachdb, go, sprint]
---

## 개요

이번에는 간단하게 해결할 수 있는 이슈를 수정했습니다. 이 정도의 이슈는 처음 스프린트에 참여하는 분도 해결할 수 있을 것으로 기대합니다.

## 이슈 파악 및 수정

친절하게도 이슈를 제보하신 분께서 다음과 같이 PostgreSQL과 카크로치디비의 결과 차이를 보여주는 예를 추가해주셨습니다:

PostgreSQL:
```
=# select current_timestamp, extract(microseconds from current_timestamp);
       current_timestamp       | date_part
-------------------------------+-----------
 2019-09-11 18:03:45.553972+00 |  45553972
```

카크로치디비:
```
> select current_timestamp, extract(microseconds from current_timestamp);
         current_timestamp         | extract
+----------------------------------+---------+
  2019-09-11 18:03:35.056128+00:00 |   56128
```

해당 명령어 구현이 [builtins.go](https://github.com/cockroachdb/cockroach/pull/41069/files#diff-eab6d12f93a40b49175acbbe6ff3a354)에 있다는 것을 알았고, 코드를 살펴본 결과 초보다 정밀한 단위에 대해 `EXTRACT` 명령어를 사용했을 때 초 부분이 무시되는 것을 발견해 [PR](https://github.com/cockroachdb/cockroach/pull/41069)을 만들었습니다.

## 흥미로운 점

수정 자체는 큰 내용이 아니었지만, 릴리즈 반영에 대한 의사결정 과정이 흥미로웠습니다. 이것이 버그 수정인지, sql 변경인지에 관한 토론이 진행되었는데, [다음 댓글](https://github.com/cockroachdb/cockroach/pull/41069#issuecomment-535095601)에 의해 현재 버전(19.1) 보다 두 버전 뒤인 20.1에 반영되게 되었습니다.

> 이것은 스펙과 다르다는 점에서 버그 수정이지만, 우리가 의도한 대로 정확하게 동작합니다. `EXTRACT`에 의존하는 애플리케이션을 중단시킬 수 있는 대규모 동작 변경을 겪습니다. 이런 이유로 나는 그것을 19.1에 반영하면 안 된다고 생각합니다. 19.2는 아직 배포되지 않았기 때문에 가능할 수도 있습니다. 또 20.1까지 기다리는 것도 조금 검토 중입니다.

### 덧붙이는 말

- 이 글은 오픈소스 프로젝트의 이슈 해결에 대한 저의 접근 방법을 공유하여, 처음 스프린트에 참가하는 참가자들을 진입장벽을 낮추기 위해 작성되었습니다. 좋은 의견이 있으면 댓글로 공유 부탁드립니다.
- 카크로치 디비 이슈 해결은 [스프린트 태그](/tags/sprint/)로 연재되고 있습니다.
- 함께 기여하고 싶은 분들은 2019년 10월 26일, [스프린트서울](https://www.sprintseoul.org/)에 참가해 주십시오.
