---
layout: post
title: "(번역) 카크로치디비(CockroachDB) 블로그 / 관리형 CockroachDB 출시: The Geo-Distributed Database as a Service"
date: 2018-10-31
tags: ["cockroachdb"]
---

원문: https://www.cockroachlabs.com/blog/launching-managed-cockroachdb

<!--more-->

Written by [Spencer Kimball](https://www.cockroachlabs.com/author/spencer-kimball/) on Oct 30, 2018

![](/assets/post/2018-10-31-launching-managed-cockroachdb/evolve-business-by-zach-meyers.jpg)

이번 주에 우리는 관리형 CockroachDB를 출시하였습니다. 이는 Cockroach 연구소에서 호스팅하고 관리되며 배포, 확장, 관리를 쉽게 할 수 있습니다. 관리형 CockroachDB는 클라우드에 구애받지 않으며 AWS, GCP를 모두 지원합니다. 목표는 단순합니다: 개발팀이 인프라 운영에 대한 걱정 없이, 확장성이 뛰어난 애플리케이션을 만드는데 집중할 수 있게 돕습니다.

**여기를 클릭하여 시작**: [CockroachDB 사용](https://www.cockroachlabs.com/get-cockroachdb)

Cockroach 연구소의 사명은 `데이터를 쉽게 만들자` 입니다. CockroachDB의 디자인은 회복력, 수평 확장성으로 빠르게 성장하는 비즈니스를 감당하고, 전 세계 어디에서나 당신의 고객 가까이 데이터를 이동시키는 업계 최고의 모델을 제공하여 이 사명을 실현합니다. 또한 [CockrochDB의 원활한 시작](https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html)을 위해서도 상당한 노력을 기울여 VM에 단일 바이너리를 내려받기만 하면, 확장성있는 분산 SQL 데이터베이스를 수 분 안에 쓸 수 있게 하였습니다. 하지만 우리는 사용자들이 CockroachDB의 관리 편이성과 무관하게, 분산 시스템의 일상적인 운영을 직접 하는 것을 선호하지 않는 것을 알게 되었습니다.

인프라를 운영하여 사용자를 만족시키는 것은 데이터를 매우 쉽게 만드는 다음 단계입니다.

### 상시 서비스

관리형 CockroachDB는 미션 크리티컬 애플리케이션을 위한 상시 서비스입니다. 한 지역 배포를 위해 세 가지 가용성 영역에 걸쳐 데이터를 자동으로 복제합니다. 비즈니스 요구사항에 맞춰 지리적으로 분산된 클러스터를 지원하는, 전 세계적으로 확장 가능한 SQL 데이터베이스입니다. CockroachDB는 클라우드 의존성이 없기 때문에, 변화하는 비즈니스 요구에 따라 한 클라우드 서비스에서 다른 서비스로 다운타임 없이 마이그레이션 할 수 있습니다.

### 우수한 운영

Cockroach 연구소가 하드웨어 프로비저닝, 설정 및 구성을 관리하므로 성능이 최적화됩니다. 최신 릴리즈로의 자동 업그레이드와 시간당 증분 백업을 보장합니다. 상시 모니터링과 엔터프라이즈급 보안 기능 또한 사용자에게 제공합니다.

### 분산 SQL 전문가

CockroachDB의 제조사로서, 우리는 CockroachDB 클러스터를 다양한 환경에서 운영하는 수년간의 경험을 축적하였으며, 사용자의 미션 크리티컬 워크로드를 서비스할 수 있습니다. 우리의 전투적인 환경에서 검증된 레퍼런스 아키텍처와 사내 SRE의 전문지식을 공유하여, CockroachDB가 제공하는 전례없이 뛰어난 매우 뛰어난 회복력과 큰 규모의 글로벌 애플리케이션으로 사용자가 시장에 빠르게 진입하기를 원합니다.

3년 전 다음 회사를 시작할 때 사용하고자 하는 데이터베이스를 당신에게 [소개했습니다](/assets/post/2018-10-15-cockroachdb-blog-hello-world). 간단하고 대담한 사명이 있었습니다. `데이터를 쉽게 만들자`. 오늘 저는 지리적으로 분산된 서비스형 데이터베이스, 관리형 CockroachDB를 통해 우리의 사명을 실현하기 위한 또 다른 중요한 단계를 발표하게 되어 기쁩니다.

**여기에서 관리형 CockroachDB를 먼저 사용해보십시**오: [CockroachDB 사용](https://www.cockroachlabs.com/get-cockroachdb)
