---
layout: default
title: Tags
permalink: /tags/
---

{% for tag in site.tags %}
* [{{ tag.title }}]({{ site.baseurl }}/tags/{{ tag.name }})
{% endfor %}
