---
layout: post
title: "用Github Copilot改了三国志9的搜索模式"
tag: 编程
date: 2026-07-26
---

以前玩三国志9的时候，每次只能选一名武将进行搜索，为了找某个宝物手都点酸了。我知道有一个plugin可以改变搜索任务的模式，把每次只能选一个人搜索变成多人搜索。但是试过之后发现并没有生效。有了大模型之后我就在想，应该可以把这个改成native support。于是今天就尝试了一下，历时一个上午，全程口述指挥，没有手写一行代码，Claude Opus 4.8, 2.9m input tokens, 30.7k output tokens。再次感慨一下程序员已是夕阳行业

[Prompt](/files/copilot-session-cb454631-a3ef-4423-bb74-e4c000bd5c1f.md), [Plan.md](/files/plan.md), [Generated scripts](/files/patch3.py), [an.py](/files/an.py), [an2.py](/files/an2.py), [an3.py](/files/an3.py)

图一 图二 图三：prompt里提到的示例(Screenshot 2026-07-25 070842.png, Screenshot 2026-07-25 070901.png, Screenshot 2026-07-25 100340.png)

图四 图五：最终效果

![img1](/img/Screenshot 2026-07-25 070842.jpg)
*图一*

![img2](/img/Screenshot 2026-07-25 070901.jpg)
*图二*

![img3](/img/Screenshot 2026-07-25 100340.jpg)
*图三*

![img4](/img/Screenshot 2026-07-26 085528.jpg)
*图四*

![img5](/img/Screenshot 2026-07-26 085553.jpg)
*图五*
