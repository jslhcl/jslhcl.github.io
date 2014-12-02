---
layout:	post
title:	"C Traps and Pitfalls notes"
date:	2014-12-01
---
# Chapter 0
## Exercise 0-1
Most people would not knowingly buy a product that they expected to have significant design defects -- except if it is a software product. Most people write at least some of their programs for use by others. People expect software not to work.

## Exercise 0-3
It is easier to think of ways to make complicated tools safer than simple ones. Food processors always have interlocks to prevent their users from losing fingers. But knives don't: adding finger protection to such a simple, flexible tool would rob it of its simplicity. In fact, the result might look more like a food processor than a knife.

Making it hard to do stupid things often makes it hard t do smart ones too.

# Chapter 1 Lexical pitfalls
The way to convert a C program to tokens is to move from left to right, taking the **longest possible token each time**.

{%highlight C%}
a---b
{%endhighlight%}
means the same as 
{%highlight C%}
a-- -b
{%endhighlight%}
rather than
{%highlight C%}
a- --b
{%endhighlight%}

