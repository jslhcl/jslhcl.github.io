---
layout:	post
title:	"FSA solution to wildcardMatching in leetcode"
date:	2014-11-08
---

以前在做“[Valid Number](https://oj.leetcode.com/problems/valid-number/)”这道题的时候，各种corner case，代码又长又乱。后来上网搜了下，有大神用有限状态自动机(FSA)给了[解法](https://github.com/fuwutu/LeetCode/blob/master/Valid%20Number.cpp)。真是neat & elegant，实在佩服。后来想到这种方法也可以用来解决“[Wildcard Matching](https://oj.leetcode.com/problems/wildcard-matching/)”。具体思路如下：

首先构造FSA：假设pattern为"c*a?d"，假设初始状态为1，读取"c"之后变为状态2，状态2读取"a"变为状态3，或者读取任意多字符后留在状态2；状态3读取任意一个字符后变为状态4；状态4读取"d"之后变为状态5。状态转换图如下所示：

![](/img/wildcardMatching.png)

然后遍历字符串s，如果s[i]是某个英文字符或者"?"，就判断当前状态下能不能通过s[i]进入下一状态，如果可以，就递归下去；如果s[i]是"*"，就继续递归判断s[i+1]和当前状态。代码如下：

{% highlight C++ %}
int f[100][28];

bool isMatch2Impl(const char*s, int currentState, int finalState)
{
	if (*s==0)
		return currentState==finalState;
	
	if (f[currentState][*s-'a'])
		if (isMatch2Impl(s+1, currentState+1, finalState))
			return true;
	if (f[currentState][26])
		if (isMatch2Impl(s+1, currentState+1, finalState))
			return true;
	if (f[currentState][27])
		if (isMatch2Impl(s+1, currentState, finalState))
			return true;

	return false;
}

bool isMatch(const char* s, const char* p)
{
	int state=1;
	memset(f, 0, sizeof(f));
	//step1, construct FSA
	while (*p)
	{
		if (*p == '*')
			f[state][27] = state;
		else if (*p == '?')
		{
			f[state][26] = state+1;
			state++;
		}
		else
		{
			f[state][*p-'a'] = state+1;
			state++;
		}
		p++;
	}

	return isMatch2Impl(s, 1, state);
}
{% endhighlight %}

这个方法的问题是对于pattern里面的"*"，递归次数太多，提交的时候超时了。所以想了一些剪支方法：

1. 如果某个时刻s[i]已经是FSA里的最后一个状态，但s还没有遍历完，这时只要看pattern的最后一个元素是否是"*"即可；
2. 一般的状态（最后一个状态除外）要么有两个出口（"\*"和英文字母，或"\*"和"?"）要么有一个出口（英文字母或"?"）。对于两个出口中"\*"和英文字母的情况，要找出s[i]后面每一个和那个英文字母相等的地方，只要在那些地方遍历即可

{% highlight C++ %}
bool isMatch3Impl(const char*s, int currentState, int finalState)
{
	if (*s==0)
		return currentState==finalState;
	if (currentState==finalState)
		return f[finalState][27]==finalState;

	if (f[currentState][27])
	{
		int i=0,j;
		for (; i<27; i++)
		{
			if (f[currentState][i])
				break;
		}
		if (i<26)
		{
			for (j=0; *(s+j)!=0;j++)
			{
				if (*(s+j)==('a'+i))
				{
					if (isMatch3Impl(s+j+1, currentState+1, finalState))
						return true;
				}
			}
		}
		else if (i==26)
		{
			for (j=0; *(s+j)!=0; j++)
				if (isMatch3Impl(s+j+1, currentState+1, finalState))
					return true;
		}
	}
	else
	{
		if (f[currentState][*s-'a'])
		{
			if (isMatch3Impl(s+1, currentState+1, finalState))
				return true;
		}
		else if (f[currentState][26])
		{
			if (isMatch3Impl(s+1, currentState+1, finalState))
				return true;
		}
	}

	return false;
}
{% endhighlight %}

不过改进后还是超时。。。

