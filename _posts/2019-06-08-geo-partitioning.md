---
layout: post
title: "(번역) 카크로치디비(CockroachDB) 블로그 / 지역 파티셔닝을 사용해 성능을 향상시키는 방법"
date: 2019-06-08
tags: [cockroachdb]
---

원문: [How to Improve Performance using Geo-Partitioning](https://www.cockroachlabs.com/blog/geo-partitioning/)

<!--more-->

Written by [Dan Kelly](https://www.cockroachlabs.com/blog/author/dan-kelly/) on May 2, 2019

![](/assets/post/2019-06-08-geo-partitioning/Geo-Partitioning-2-by-Lea-Heinrich.jpg)

---

분산 SQL의 가장 흥미로운 기능 중 하나는 데이터를 특정 지역에 고정시키는 기능이며 카크로치디비는 지역 파티셔닝 기능을 통해 이를 제공합니다. 만약 이 기능에 익숙하지 않다면 우리가 최근에 공개한 [비디오 데모](https://www.youtube.com/watch?time_continue=4&v=TgnQwOOk9Js)와 [튜토리얼](https://www.cockroachlabs.com/docs/v19.1/demo-geo-partitioning.html)를 통해 동작방식을 확인하실 수 있습니다. 하지만 먼저, 지역 파티셔닝에 대한 설명을 드리겠습니다:

지역 파티셔닝은 데이터(행 수준에서)를 지역에 고정할 수 있는 기능입니다. 이를 통해 수동 스키마 변경과 복잡하고 다루기 힘든 애플리케이션 로직 없이, 데이터베이스 데이터의 지역성을 보장할 수 있습니다. 지역 파티셔닝은 데이터의 값을 테이터베이스의 물리적인 구현과 결합하기 때문에 일반적인 파티셔닝과는 확연히 다릅니다. [분산 SQL 데이터베이스](https://www.cockroachlabs.com/blog/what-is-distributed-sql/)에서 각 노드는 서로 다른 물리적 장소에서 실행됩니다. 카크로치디비는 이 정보를 사용하여 데이터의 지역 파티셔닝을 적용하는 유일한 데이터베이스입니다.

지역 파티셔닝은 종종 [데이터 현지화](https://www.cockroachlabs.com/guides/data-localization/)([마크 주커버그와 유발 하라리의 대화를 통해 매우 중요한 주제가 되었음](https://techcrunch.com/2019/04/26/facebook-data-localization/))의 맥락에서 논의됩니다. 고객 데이터를 특정위치에 고정시키는 기능은 해당 지역에 데이터가 있어야 하는 국가에서 비즈니스 기준을 준수할 수 있게 도와줍니다.

위 대화에서 다루어지지 않은 것은 지역 파티셔닝이 성능을 향상시킨다는 것입니다.

## 낮은 지연을 위한 지역 파티셔닝

이 [비디오 데모](https://www.youtube.com/watch?time_continue=4&v=TgnQwOOk9Js)에서, 어떻게 지역 파티셔닝이 데이터 접근 지연을 감소시켜 애플리케이션 성능을 향상시키는지 알 수 있습니다.

비디오에는 GCE 미국 리전 3개에 9개 노드가 배포되어 있습니다. 지역 파티셔닝을 적용하기 이전 99% 쿼리의 최대 지연시간은 **수백 밀리초**입니다. 지역 파티셔닝 이후 99% 쿼리는 **4밀리초 이하** 이고, 전체 쿼리 중 90%는 **2밀리초** 이하에 실행되었습니다. 심지어 몇 종류는 **0.5밀리초** 였습니다.

<iframe width="560" height="315" src="https://www.youtube.com/embed/TgnQwOOk9Js?t=812" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

우리는 이런 종류의 성능향상이 매우 흥미롭다고 생각하며 훌륭한 문서 팀이 [튜토리얼](https://www.cockroachlabs.com/docs/v19.1/demo-geo-partitioning.html)을 작성하여 지역 파티셔닝에 세상에 참가하도록 돕고 있습니다. 우리는 이 튜토리얼을 통해 지역 파티셔닝에 익숙해지 바랍니다. 또 어떻게 이 기능으로 성능을 향상시키는가에 대한 추가 질문을 기다리고 있습니다.

지역 파티셔닝에 대한 더 자세한 정보를 알고 싶으면 다음을 확인해보십시오.

- [블로그](https://www.cockroachlabs.com/blog/geo-partitioning-one/): 글로벌 데이터는 실제로 어떻게 존재하는가?

- [웨비나](https://www.cockroachlabs.com/webinars/data-localization): 분산 SQL에서 데이터 지역화의 힘

[포럼](https://forum.cockroachlabs.com/?_ga=2.214942679.1500782602.1559970845-656481681.1550900482)을 통해 피드백을 공유해 주시기 바랍니다.
