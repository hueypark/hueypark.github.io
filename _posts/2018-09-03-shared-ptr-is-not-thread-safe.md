---
layout: post
title: std::shared_ptr is not thread safe
date: 2018-09-03
tags: ["c++", "multithread"]
---

I found that std::shared_ptr is not thread-safe, and I leave that example.

<!--more-->

#### main.cpp
```cpp
#include <thread>

std::shared_ptr<int> g_ptr = nullptr;

int main() {
	std::thread t1([]() {
		int i = 0;
		while (true) {
			g_ptr = std::make_shared<int>(i);

			++i;
		}
	});

	std::thread t2([]() {
		while(true) {
			std::shared_ptr<int> ptr = g_ptr;
		}
	});

	t1.join();
	t2.join();

	return 0;
}
```
