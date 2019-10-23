---
layout: post
title: "sql: COMMENT ON INDEX 지원(CockroachDB issue #41316)"
date: 2019-10-20
tags: [cockroachdb, go, sprint]
---

이슈: [sql: add support for COMMENT ON INDEX #41316](https://github.com/cockroachdb/cockroach/issues/41316)

sql: COMMENT ON INDEX 지원 작업을 했습니다. 이번에는 이슈 등록자가 저에게 먼저 연락을 하는 새로운 경험을 했습니다.

<!--more-->

## 이슈 등록

[@jordanlewis](https://github.com/jordanlewis)가 이슈를 등록하며 저에게 관심이 있냐고 [물어보았습니다](https://github.com/cockroachdb/cockroach/issues/41316#issue-502421946). 예전에 COMMENT 관련 작업 [몇 가지](https://github.com/cockroachdb/cockroach/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+author%3Ahueypark+in%3Atitle+comment)를 주도적으로 진행한 적이 있어 할당된 것 같습니다.

## 리뷰

처음 유사한 [작업](https://github.com/cockroachdb/cockroach/pull/32442)을 했을 때는 머지에 한 달 정도의 시간이 걸렸는데, 이번 [리뷰](https://github.com/cockroachdb/cockroach/pull/41555)에서는 큰 수정사항도 없었고 머지도 빠르게 종료되었습니다.

## 덧붙이는 말

- 이 글은 오픈소스 프로젝트의 이슈 해결에 대한 저의 접근 방법을 공유하여, 처음 스프린트에 참가하는 참가자들을 진입장벽을 낮추기 위해 작성되었습니다. 좋은 의견이 있으면 댓글로 공유 부탁드립니다.
- 카크로치 디비 이슈 해결은 [스프린트 태그](/tags/sprint/)로 연재되고 있습니다.
- 함께 기여하고 싶은 분들은 [스프린트서울](https://www.sprintseoul.org/)에 참가해 주십시오.
