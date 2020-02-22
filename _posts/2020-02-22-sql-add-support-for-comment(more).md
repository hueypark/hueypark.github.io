---
layout: post
title: "(very good first issue) #44135 sql: add support for COMMENT ON VIEW, COMMENT ON SEQUENCE"
date: "2020-02-20"
tags: [cockroachdb, sprint]
---

[카크로치디비 이슈 #44135](https://github.com/cockroachdb/cockroach/issues/44135) sql: add support for COMMENT ON VIEW, COMMENT ON SEQUENCE

### 개요

이슈 #44135 `PostgreSQL`에서 지원하는 [COMMENT ON](https://www.postgresql.org/docs/9.1/functions-aggregate.html) 문법의 `VIEW`, `SEQUENCE`에 대한 지원을 요구합니다.

<!--more-->

---

### 구현 가이드

마지막으로 작업(2019년 12월 31일) 이후로 많은 것이 변경되었습니다. 그 점을 고려하고 아래 가이드를 참고해주십시오.

1. 먼저 새로운 SQL 문법 추가에 관련된 [문서](https://github.com/cockroachdb/cockroach/blob/master/docs/codelabs/01-sql-statement.md)를 읽어보시길 권장드립니다.
2. `sql.y`에서 새로운 SQL 문법을 정의합니다.
3. `constants.go`에 새로운 `COMMENT`에 관련된 타입을 정의합니다.
4. `/pkg/sql/sem/tree/comment_on_column.go`의 `CommentOnColumn`과 같은 새 `tree.Statement`를 추가합니다.
5. `/pkg/sql/comment_on_column.go`의 `commentOnColumnNode`처럼 새로운 노드를 구현합니다.
6. `event_log.go`에 로그를 정의하고 적절한 시점에 남깁니다.
7. 다음 파일의 적절한 지검에 분기처리를 해줍니다(2020년 2월 22일 기준으로 의미없는 부분이 있을 수 있음).
	- `expand_plan.go`, `opt_filters.go`, `opt_limits.go`, `opt_needed.go`, `plan.go`, `walk.go`
8. 테스트를 추가합니다. 대부분 `pkg/sql/logictest/testdata/`의 관계된 파일에 추가하고, 필요시 `comment_on_column_test.go`처럼 해당 기능에 특화된 테스트를 작성합니다.
9. 파싱관련 테스트는 `parse_test.go`에 별도로 추가합니다.

---

### 팁

- 한 PR에 하나의 문법(`VIEW` 또는 `SEQUENCE`)에 대한 작업만 하면 복잡도를 줄일 수 있습니다.
- 관련된 몇 가지 커밋을 참고하시기 바랍니다.
	- [sql: support `COMMENT ON COLUMN`](https://github.com/cockroachdb/cockroach/commit/52fa9cb3f9edc175fa953f2eb8c323fe6acafe4e)
	- [sql: print comments in SHOW CREATE TABLE](https://github.com/cockroachdb/cockroach/commit/08be7c42415af6009836da5444889eb43382103e)
