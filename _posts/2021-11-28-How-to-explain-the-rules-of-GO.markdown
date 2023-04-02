---
layout:	post
title:	"How to explain the rules of GO (to foreigners) in one minute"
tag: 生活
date:	2021-11-28
---

**缘起**：今年感恩节被邀请去邻居家吃饭，闲聊中他问我会不会国际象棋。我答不会，只了解中国象棋和围棋(GO)。他掏出一副崭新的还未拆封的围棋，让我解释一下规则。从未料到欢快的聚会上突然有这么一个Tutorial，仓促上阵，效果不甚理想。因此想用**最简洁的语言**介绍围棋**最核心的规则**，以防再出现类似的场合。缺点是用语可能不太准确且难免挂一漏万，欢迎评论和改进意见。

**Definition 0**: a stone (black or white) can only be placed on an empty intersection 

**定义零**：棋子只能走在空白的交叉点上 

**Definition 1**: Connected Group

A group of stones (black or white) that are adjacent horizontally or vertically to each other 

**定义一**：相连的子

水平或垂直连接的子

![Fig 1](/img/fig1.png)

*Fig 1*

![Fig 2](/img/fig2.png)

*Fig 2*

Fig1 is one connected group while Fig2 is not (a single stone and one connected group of 3 stones)

Fig1 是相连的子而Fig2不是

**Definition 2**: Liberty

The empty intersection that is adjacent to a stone or a connected group horizontally or vertically

**定义二**：气

和棋子水平或垂直相连的空白交叉点

![Fig 3 black has 4 liberties 黑子有4口气](/img/fig3.png)

*Fig 3 black has 4 liberties 黑子有4口气*

![Fig 4 white has 3 liberties 白子有三口气](/img/fig4.png)

*Fig 4 white has 3 liberties 白子有三口气*

![Fig 5 black has 2 liberties 黑子有2口气](/img/fig5.png)

*Fig 5 black has 2 liberties 黑子有2口气*

![Fig 6 black has 2 liberties left 黑子还剩2口气](/img/fig6.png)

*Fig 6 black has 2 liberties left 黑子还剩2口气*

![Fig 7 black has 12 liberties 黑子有12口气](/img/fig7.png)

*Fig 7 black has 12 liberties 黑子有12口气*

![Fig 8 black has 1 liberty left 黑子还剩1口气](/img/fig8.png)

*Fig 8 black has 1 liberty left 黑子还剩1口气*

**Definition 3**: Live or Death

A stone or a connected group cannot live if it has no liberties (and should be removed from the board)

You cannot place a stone to an intersection where it has no liberties unless you can kill the opponent stones to gain liberties.

For example, you cannot place white stone on intersection 1 of Fig 7, because there is no liberty left for white, but you can do that in Fig 8, as you can kill the blacks and gain liberties by removing the blacks

Then you can figure out how to make your stones live. It is actually not a rule, but something you can derive from the above rules, which is: you must keep at least 2 separate liberties that the opponent stone cannot be placed.

Each of these separate liberties are called ‘eye’. So in short, you need to build at least 2 eyes. 

**定义三**：生死

如果没有气，棋子就不能生存(因此要从棋盘上拿掉)

你不能把一个棋子放在没有气的位置，除非你能杀掉对手并获得气

例如，你不能把白子放在Fig 7的1点，因为那里白子没有气。但你可以把白子放在Fig 8的1点，因为你可以杀死黑棋，把它们移除棋盘获得气

所以你应该明白了如何让你的棋子生存下来。这其实并不是一条规则，而是从上述规则中推导出来的，即：至少需要保存2口，对方无法进入的气。

每一个像这样的气被称为“眼”。所以简而言之，你至少需要做两个眼。

![Fig 9 black has 2 eyes so it will live forever. 黑棋有了两个眼，所以能长久的生存下去](/img/fig9.png)

*Fig 9 black has 2 eyes so it will live forever. 黑棋有了两个眼，所以能长久的生存下去*

**Definition 4**: Territory

The intersections occupied by the stones that won’t be killed (including the stones themselves and the empty liberties)

For example, in Fig 9 black has a territory with the area of 14. 

**定义四**：领土

无法被杀死的棋子所占据的交叉点被称为领土

例如，Fig 9 黑棋占有14目的领土

The goal of GO: To gain more territories. The one who owns more territories wins the game. 

围棋的目标：多占领土。围有领土越多的人获胜

后记

这其实并不能称为围棋的规则介绍，因为还有几个很重要的概念没有介绍(如：劫，双活，贴目，等等)。这只是用来帮助我厘清介绍的顺序以帮助初学者入门。了解上述的概念就可以开始下棋了。其实围棋是我见过的规则最简单，变化最复杂的棋类运动，也是我喜欢这项运动的原因。我想起了陈道蓄老师在《离散数学》课上的一句话：一个定理如果描述越简单，它的适用范围就越广，能产生的变化就越多样，比如抽屉原理；相反，如果一个定理需要很多先验知识和条件，它的适用范围就越窄。很多道理都是相通的。
