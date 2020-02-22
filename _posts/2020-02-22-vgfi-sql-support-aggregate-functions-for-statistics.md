---
layout: post
title: "(very good first issue) #41274 sql: Support aggregate functions for statistics"
date: "2020-02-20"
tags: [cockroachdb, sprint]
---

[카크로치디비 이슈 #41274](https://github.com/cockroachdb/cockroach/issues/41274) sql: Support aggregate functions for statistics

### 개요

이슈 #41274는 `PostgreSQL`에서 지원하는 [aggregate function](https://www.postgresql.org/docs/9.1/functions-aggregate.html)들의 구현을 요구하며, 대상은 아래와 같습니다.

<!--more-->

* [x] corr()
* [ ] covar_pop()
* [ ] covar_samp()
* [ ] regr_avgx()
* [ ] regr_avgy()
* [ ] regr_count()
* [ ] regr_intercept()
* [ ] regr_r2()
* [ ] regr_slope()
* [ ] regr_sxx()
* [ ] regr_syy()
* [ ] regr_sxy()

---

### 구현 가이드

1. `scalar.opt`에 함수를 추가합니다.
2. `operator.go`의 `AggregateOpReverseMap`에 추가된 함수를 등록하고, 필요에 따라 `BoolOperatorRequiresNotNullArgs`, `AggregateIgnoresNulls`, `AggregateIsNullOnEmpty`를 적절히 수정합니다.
3. `groupby.go`의 `constructAggregate` 분기에 추가된 함수를 등록합니다.
4. `aggregate_builtins.go` 에서 구현 부분을 작성합니다. PostgreSQL 구현체를 참고하면 많은 도움이 됩니다.(`corr` 같은 경우는 SQL:2003 스펙에 따라 구현되었음).
5. 분산 SQL 처리를 위해 `processors_sql.proto`의 `AggregatorSpec.Func`에 함수를 추가합니다.
6. 아래 항목에 대한 테스트를 추가합니다.
	- `pkg/sql/logictest/testdata/logic_test/aggregate`
	- `pkg/sql/logictest/testdata/logic_test/distsql_agg`
	- `pkg/sql/opt/exec/execbuilder/testdata/distsql_agg`
	- `pkg/sql/opt/exec/execbuilder/testdata/explain`
	- `pkg/sql/opt/norm/testdata/rules/agg`
	- `pkg/sql/opt/optbuilder/testdata/aggregate`
7. vim syntax를 위해 `crlogictest.vim`에 추가된 함수를 등록합니다.

---

### 팁

- `corr()` 함수를 구현한 [커밋 sql: support `corr()`](https://github.com/cockroachdb/cockroach/commit/865e011bb3d54989e4b46b046462af9d327091d1)을 참고하시기 바랍니다.
- 몇 가지 유용한 테스트 방법을 공유드립니다.
	- `make test PKG=./pkg/sql/opt/norm` 특정 패키지만 테스트합니다.
	- `make test FILES=aggregate` 특정 파일만 테스트 합니다.
	- `make test TESTFLAGS=-rewrite` 변경된 테스트 결과를 자동으로 변경합니다.
	- `make testlogic` SQL 로직만 테스트합니다.
