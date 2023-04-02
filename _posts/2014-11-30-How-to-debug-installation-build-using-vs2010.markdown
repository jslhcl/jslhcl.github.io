---
layout:	post
title:	"How to debug installation build using vs2010"
tag: 编程
date:	2014-11-30
---

有些issue只能在installation版本里重现，这里记录一下自己在installation版本里搭建调试环境的步骤

1. 下载与installation版本匹配的代码，configuration里选择"release"，编译出相应的dll或/和exe文件，以及**对应的pdb文件**

2. 将步骤一生成的dll, exe和pdb文件拷贝到installation版本路径下，替换掉原来的dll或/和exe文件

3. 启动installation程序，在vs2010里attach上这个程序(ctrl+alt+p)，注意**选中正确的code type** (图示程序使用了CLI和C++, 所以managed code和native code都勾选了)
![](/img/vs_attach.png)

4. 然后应该就可以打断点了。

P.S., 用"append"方式打开文件(如果文件不存在会自动创建文件)也要判断文件指针是否为空，因为文件/文件夹有可能是只读的。

Update 2014-02-16

如果Installation版本打开即crash（不能attach上）：

右击Project->Properties->Configuration Properties->General，将Output Directory设成安装版本exe程序所在路径
![](/img/vs_Output_Directory.png)

感想：

1. 有调试环境很重要。与其把时间用在读代码猜测分析原因上，不如好好研究一下如何设置调试环境

2. 如果没有找到问题的原因，就一直step into进入更底层的函数


