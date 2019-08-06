---
layout: default
title: Sprint
permalink: /sprint/
---

## 스프린트 참가자 안내

안녕하세요. 카크로치디비 스프린트에 참가하신 여러분을 환영합니다. 오픈소스 프로젝트를 함께 개발하는 과정에서 새로운 동료를 만나고, 경험과 지식을 나누길 희망합니다.

## 미리 알아야 할 내용

- 개발환경을 미리 준비해 주십시오.(당일 준비하기에는 꽤 오랜 시간이 걸립니다.)
	- [CONTRIBUTING.md](https://github.com/cockroachdb/cockroach/blob/master/CONTRIBUTING.md)와 [문서](https://marsettler.com/docs/stable/ko/contribute-to-cockroachdb.html)를 참고하십시오.
- [아키텍처 개요](https://marsettler.com/docs/stable/ko/architecture/overview.html)를 읽어보십시오.

## 첫 PR을 위해 도전할 만한 이슈

스프린트에서 해결할 카크로치디비 이슈를 정리했습니다. 이미 [good first issue](https://github.com/cockroachdb/cockroach/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22), [E-easy](https://github.com/cockroachdb/cockroach/issues?q=is%3Aopen+is%3Aissue+label%3AE-easy), [E-starter](https://github.com/cockroachdb/cockroach/issues?q=is%3Aissue+is%3Aopen+label%3AE-starter) 등의 태그가 있지만, 너무 오래되어 의미가 없어지거나, 프로젝트에 대한 이해가 적은 상태에서 해결하기 힘든 이슈를 제외한 후, 간단한 설명을 추가했습니다.

- sql: review slow tests [#37028](https://github.com/cockroachdb/cockroach/issues/37028)
	- 느린 테스트 리뷰하여 시간단축 또는 제거
- sql: only update computed columns that need updating [#23523](https://github.com/cockroachdb/cockroach/issues/23523)
	- 업데이트가 필요한 컴퓨티드 컬럼만 업데이트하게 변경
- sql: implement computed indexes [#9682](https://github.com/cockroachdb/cockroach/issues/9682)
	- 컴퓨티드 인덱스 구현
