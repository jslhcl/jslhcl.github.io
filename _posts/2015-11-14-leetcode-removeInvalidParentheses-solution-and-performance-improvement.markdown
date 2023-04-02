---
layout:	post
title:	"Solution and Improvement on removeInvalidParentheses in leetcode"
tag: 编程
date:	2015-11-14
---

[这道题](https://leetcode.com/problems/remove-invalid-parentheses/)需要列举出所有可能的组合，所以第一想法是用递归：如果当前的字符是"(", 就要考虑这个字符加入最终解和不加入最终解的情况(加入最终解的情况要先考虑这样才能产生最长的解)；如果当前的字符是")", 也分这两种情况考虑，只是")"加入最终解的时候要考虑一个限制条件，即加入后")"的数量不能大于"("的数量(这一点用变量cnt来控制)；如果当前的字符是非括号之外的其他字符，就保留该字符进行递归。代码如下：

{% highlight C++ %}
void removeInvalidParenthesesImpl(string s, int index, int cnt, string strValid, int& maxLen, vector<string>& oRet)
{
	if (index==s.length())
	{
		if (cnt==0)
		{
			if (maxLen < strValid.length())
				maxLen = strValid.length();
			if (maxLen == strValid.length())
			{
				int i=0;
				for (; i<oRet.size(); i++)
					if (oRet[i] == strValid)
						break;
				if (i==oRet.size())
					oRet.push_back(strValid);
			}
		}
		return;
	}

	if (s[index]=='(')
	{
		removeInvalidParenthesesImpl(s, index+1, cnt+1, strValid+'(', maxLen, oRet);
		removeInvalidParenthesesImpl(s, index+1, cnt, strValid, maxLen, oRet);	
	}
	else if (s[index] == ')')
	{
		if (cnt>0)
			removeInvalidParenthesesImpl(s, index+1, cnt-1, strValid+')', maxLen, oRet);
		removeInvalidParenthesesImpl(s, index+1, cnt, strValid, maxLen, oRet);
	}
	else
		removeInvalidParenthesesImpl(s, index+1, cnt, strValid+s[index], maxLen, oRet);
}

// version 1, AC, 612ms
vector<string> removeInvalidParentheses(string s)
{
	vector<string> ret;
	int maxLen = 0;
	removeInvalidParenthesesImpl(s, 0, 0, "", maxLen, ret);
	return ret;
}
{% endhighlight%}

上面的版本可以通过，但是效率低(612ms)，被鄙视了。想了一下可能的改进途径：

1. 对于字符串参数，用引用代替值传递，避免拷贝。但递归结束后要把该字符串还原。（实践证明使用引用效果很明显）

2. 对于连在一起重复出现的"("或")"，递归时只要考虑第一个出现的"("或")"即可，避免多次递归调用产生重复的结果

3. 用一个数组(rpCnt)记录从当前位置到字符串结尾右括号")"出现的次数。这主要是对当前字符为左括号"("时进行剪枝：如果当前未配对的左括号"("个数大于或等于后面的右括号")"数，就不再对该左括号"("进行递归。

4. 如果字符串开头出现")"或者结尾出现"("，这些字符肯定不会出现在最后结果中。可以在递归前把它们删掉

代码如下：

{% highlight C++ %}
void removeInvalidParenthesesImpl4(string& s, vector<int>& rpCnt, int index, int cnt, string& strValid, vector<string>& oRet)
{
	if (index==s.length())
	{
		if (oRet.size()==0 || oRet[0].length()==strValid.length())
			oRet.push_back(strValid);
		return;
	}
	if (s[index]=='(')
	{
		if (cnt<rpCnt[index])
		{
			strValid.push_back('(');
			removeInvalidParenthesesImpl4(s, rpCnt, index+1, cnt+1, strValid, oRet);
			strValid.erase(strValid.length()-1);
		}
		while (index<s.length() && s[index]=='(')
			index++;
		removeInvalidParenthesesImpl4(s, rpCnt, index, cnt, strValid, oRet);
	}
	else if (s[index]==')')
	{
		if (cnt>0)
		{
			strValid.push_back(')');
			removeInvalidParenthesesImpl4(s, rpCnt, index+1, cnt-1, strValid, oRet);
			strValid.erase(strValid.length()-1);
		}
		while (index<s.length() && s[index]==')')
			index++;
		removeInvalidParenthesesImpl4(s, rpCnt, index, cnt, strValid, oRet);
	}
	else
	{
		strValid.push_back(s[index]);
		removeInvalidParenthesesImpl4(s, rpCnt, index+1, cnt, strValid, oRet);
		strValid.erase(strValid.length()-1);
	}
}

// version 4, AC, 8ms
vector<string> removeInvalidParentheses(string s)
{
	int start=0, end=s.length()-1, i, count;
	while (start<end && s[start]==')')
		start++;
	while (start<end && s[end]=='(')
		end--;
	if (start>0 || end<s.length()-1)
		s = s.substr(start, end-start+1);
	vector<int> rpCnt(end-start+1, 0);	// number of right parentheses
	for (i=end-start; i>=0; i--)
	{
		count = (s[i]==')');
		rpCnt[i] = (i==(end-start))?(count):(rpCnt[i+1]+count);
	}
	vector<string> ret;
	string strValid;
	removeInvalidParenthesesImpl4(s, rpCnt, 0, 0, strValid, ret);
	return ret;
}
{% endhighlight %}

改进之后的提升效果明显(8ms)。

