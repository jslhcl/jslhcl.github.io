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

# Chapter 3 Semantic pitfalls

{%highlight C%}
int (*ap)[31];
{%endhighlight%}

we are saying here that \*ap is an array of 31 *int* elements, so *ap* is a pointer to such an array.

*Express a range by the first element of the range and the first element beyond it*. It is for that reason that we write

{%highlight C%}
int a[10], i;
for (i=0; i<10; i++)
	a[i] = 0;
{%endhighlight%}

instead of 

{%highlight C%}
int a[10], i;
for (i=0; i<=9; i++)
	a[i] = 0;
{%endhighlight%}

## Integer overflow
Suppose, for example, that *a* and *b* are two *int* variables known to be nonnegative and you want to test whether *a+b* might overflow. One obvious way to do it is:
 
{%highlight C%}
if (a + b < 0)
	complain();
{%endhighlight%}

This does not work. Once *a+b* has overflowed, all bets are off as to what the result will be. The result of an overflow is *undefined*

One correct way of doing this is to covnert *a* and *b* to unsigned:

{%highlight C%}
if ((unsigned)a + (unsigned)b > INT_MAX)
	complain();
{%endhighlight%}

Another possibility doesn't involve unsigned arithmetic at all:

{%highlight C%}
if (a > INT_MAX - b)
	complain();
{%endhighlight%}

# Chapter 4 Linkage

{%highlight C%}
extern int a;
{%endhighlight%}

It says that *a* is an external integer variable, but by including the *extern* keyword, it explicitly says that the storage for *a* is allocated somewhere else. From the linker's viewpoint, such a declaration is a *reference* to the external object *a* but does not define it.

The following function *srand* stores a copy of its integer argument in the **external** variable *random_seed*
{%highlight C%}
void srand(int n)
{
	extern int random_seed;
	random_seed = n;
}
{%endhighlight%}

## Name conflict

One useful tool for reducing conflicts of this sort is the *static* modifier.
 
{%highlight C%}
static int a;
{%endhighlight%}

means the same thing as

{%highlight C%}
int a;
{%endhighlight%}

*within a single source program file*, but *a* is hidden from other files.

This applies to functions too. If a function *f* calls a function *g*, and *only f* needs to be able to call *g*, we can put *f* and *g* in the same file and make *g* static:

{%highlight C%}
static int g(int x)
{
	/* stuff */
}

void f()
{
	/* more stuff */
	b = g(a);
}
{%endhighlight%}

We can have several files, each with its own function called *g*, as long as all of them, or all but one, are declared *static*.
