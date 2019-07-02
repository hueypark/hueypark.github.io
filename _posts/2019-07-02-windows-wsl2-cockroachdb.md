---
layout: post
title: "칵로치디비(CockroachDB) 윈도우(WSL2)에서 빌드"
date: 2019-07-02
tags: [cockroachdb, windows, wsl2]
---

![](/assets/post/2019-07-02-windows-wsl2-cockroachdb/cockroachdb-on-windows.png)

[스프린트서울](/2019/06/30/first-sprintseoul.html) 참가하면 가장 불편했던 일은 개발환경 설정이었다. 평소에는 집에 있는 리눅스(데스크탑) 환경에서 개발하였는데, 윈도우즈(노트북)을 사용하게 되었기 때문이다. 급한대로 VirtualBox를 사용했는데 성능 차이도 있었고, 직접 불필요하게 손봐주어야 할 부분이 많았다.

마침 WSL 2가 윈도우즈 인사이더에 [릴리즈](https://devblogs.microsoft.com/commandline/wsl-2-is-now-available-in-windows-insiders/) 되었다고 하기에 실험체가 되어보기로 했다.

18922.1000을 설치하고 얼마 후... 칵로치디비 빌드에 성공!! 앞으로 [WSL 2 태그](https://marsettler.com/tags/wsl2/)에 사용기를 꾸준히 업데이트 할 예정이니 궁금하신 분은 한 번씩 찾아와서 보시기 바랍니다.
