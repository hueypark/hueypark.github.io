---
layout: post
title: "sql: COMMENT ON INDEX 지원(CockroachDB issue #41316)"
date: 2019-10-20
tags: [cockroachdb, go, sprint]
---

## 개요

이슈: [sql: add support for COMMENT ON INDEX #41316](https://github.com/cockroachdb/cockroach/issues/41316)

sql: COMMENT ON INDEX 지원 작업을 했습니다. 이번에는 이슈 등록자가 저에게 먼저 연락을 하는 새로운 경험을 했습니다.

<!--more-->

## 이슈 등록

[@jordanlewis](https://github.com/jordanlewis)가 이슈를 등록하며 저에게 관심이 있냐고 [물어보았습니다](https://github.com/cockroachdb/cockroach/issues/41316#issue-502421946). 예전에 COMMENT 관련 작업 [몇 가지](https://github.com/cockroachdb/cockroach/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed+author%3Ahueypark+in%3Atitle+comment)를 주도적으로 진행한 적이 있어 그런 것 같은데 뭔가 인정받은 느낌이라 기분이 좋았습니다.

## 리뷰

이미 비슷한 작업을 여러 번 진행한 경험이 있어 구현 부분에서 특별한 수정사항은 없었습니다. 하지만 [리뷰](https://github.com/cockroachdb/cockroach/pull/41555#pullrequestreview-302936535)에서 주석에 있는 문법(동사의 단/복수 구분, 관사 `a`, `an` 의 구분)에 대한 의견을 몇 가지 공유받았습니다. 저에게 영어는 모국어가 아니지만 기본적으로 지켜야 할 부분이라고 생각했습니다.

## 덧붙이는 말

- 이 글은 오픈소스 프로젝트의 이슈 해결에 대한 저의 접근 방법을 공유하여, 처음 스프린트에 참가하는 참가자들을 진입장벽을 낮추기 위해 작성되었습니다. 좋은 의견이 있으면 댓글로 공유 부탁드립니다.
- 카크로치 디비 이슈 해결은 [스프린트 태그](/tags/sprint/)로 연재되고 있습니다.
- 함께 기여하고 싶은 분들은 [스프린트서울](https://www.sprintseoul.org/)에 참가해 주십시오.
