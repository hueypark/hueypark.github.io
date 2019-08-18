---
layout: post
title: "파이콘 한국 2019 스프린트 - 카크로치디비(CockroachDB)와 함께"
date: 2019-08-18
tags: [cockroachdb, sprint]
---

파이콘 한국 2019 스프린트에 참가했습니다.

저번과는 달리 [스프린트 참가자 안내](/sprint/), [오픈 채팅방](https://gitter.im/koreacockroachdb/community) 등을 미리 준비하였는데 [처음](/first-sprintseoul.html)보다는 참가자들에게 더 도움이 되었던 것 같습니다.

스프린트 참가자들은 카크로치디비와 오픈소스 기여에 관심이 있었는데, 짧은 기간 내에 둘 모두에서 충분한 만족을 얻기는 힘들었고, 이틀의 시간동안 하나의 PR을 만드는 것도 쉽지 않았습니다. 하지만, 이번 스프린트를 통해 어떤 분들은 생애 첫 PR을 만들기도 하였고, 카크로치디비 아키텍처와 오픈소스 기여에 전반적인 이해가 증가한 것으로 충분히 가치있다고 생각합니다.

개인적으로는 이번 스프린트를 통해 카크로치디비의 스토리지 계층을 대체하게 될 [Pebble](https://github.com/petermattis/pebble) 프로젝트를 알게되어 기쁩니다.(이게 완료되면 Windows 환경에서도 개발가능하게 되지 않을까요?)

이번 스프린트에 참가해주신 모든 분들께 감사드리고, 다음 [스프린트](https://www.sprintseoul.org/)에서 또 만나길 기원합니다!

---

### 추가된 PR 목록

- [https://github.com/cockroachdb/cockroach/pull/39681](https://github.com/cockroachdb/cockroach/pull/39681)
- [https://github.com/cockroachdb/cockroach/pull/39682](https://github.com/cockroachdb/cockroach/pull/39682)
- [https://github.com/hueypark/docs/pull/13](https://github.com/hueypark/docs/pull/13)
- [https://github.com/hueypark/docs/pull/14](https://github.com/hueypark/docs/pull/14)
- [https://github.com/hueypark/docs/pull/15](https://github.com/hueypark/docs/pull/15)

### 덧붙이는 말

- 다음에는 스프린트 시간(8시간) 내에 PR까지 만드는 것이 가능한 이슈를 별도로 분리해 보려고 합니다(그런 이슈를 충분히 확보할 수 있을까요?).
- 익숙하지 않은 상태에서 스프린트에 참가하는 분들을 위해 제가 이슈를 해결하는 과정을 [스프린트 태그](/tags/sprint/)로 연재할 예정입니다.