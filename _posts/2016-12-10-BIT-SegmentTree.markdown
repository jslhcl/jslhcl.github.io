---
layout:	post
title:	"Binary Indexed Tree, Segment Tree"
date:	2016-12-10
---
# Binary Indexed Tree

Suppose there is an array, how to get the sum of some interval of the array?

Basic idea of BIT is to introduce a helper array, say, BIT[], when we update BIT[i], we also update BIT[j], where j=i+(lowerbit of i). For example, when we update BIT[3], we also need to update BIT[4] (since 4=(11)<sub>2</sub>+1), then update BIT[8] (since 8=(100)<sub>2</sub>+(100)<sub>2</sub>)

Suppose the array is {1,2,3,4,5,6,7,8} (index is 1-based), we update the BIT array step by step:

Index   |1   |2   |3  | 4   |5  | 6   |7  | 8   |
array   |1   |2   |3  | 4   |5  | 6   |7  | 8   |
BIT     |1   |1   |   | 1   |   |     |   | 1   |(update BIT[1])
        |1   |3   |   | 3   |   |     |   | 3   |(update BIT[2])
        |1   |3   |3  | 6   |   |     |   | 6   |(update BIT[3])
        |1   |3   |3  |10   |   |     |   |10   |(update BIT[4])
        |1   |3   |3  |10   |5  | 5   |   |15   |(update BIT[5])
        |1   |3   |3  |10   |5  |11   |   |21   |(update BIT[6])
        |1   |3   |3  |10   |5  |11   |7  |28   |(update BIT[7])
        |1   |3   |3  |10   |5  |11   |7  |36   |(update BIT[8])

so if we want sum(1..7), it equals BIT[7] (which is array[7]) + BIT[6] (which is array[6]+array[5]) + BIT[4] (which is array[1]+array[2]+array[3]+array[4])

## Code
{% highlight C %}
	int sum(int index)
	{
			int ret = 0;
			while (index>0 && index<nums.size())
			{
					ret += nums[index];
					index -= index&(-index);
			}
			return ret;
	}

	void update(int index, int value)
	{
			while (index<nums.size())
			{
				nums[index] += value;
				index += index&(-index);
			}
	}
{% endhighlight %}

## Reference

[topcoder](https://www.topcoder.com/community/data-science/data-science-tutorials/binary-indexed-trees/)

# Segment Tree

Usage 1: given an array, how to get the sum of some interval of the array?

Usage 2: given an array, how to get the minimum/maximum value of some interval of the array?

The basic idea of segment tree is to introduce a binary tree, where the leaves are the elements of the input array, the internal non-leave nodes represents some merging of the children nodes (sum/min/max), depending on the problem to be solve. 

We can use a helper array to represent the binary tree above (just like heap).

## Code
See the *Reference* part

## Reference

[geeksforgeeks1](http://www.geeksforgeeks.org/segment-tree-set-1-sum-of-given-range/)
[geeksforgeeks2](http://www.geeksforgeeks.org/segment-tree-set-1-range-minimum-query/)
