---
layout:	post
title:	"C Traps and Pitfalls notes"
tag: 笔记
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

# Chapter 5 Library Functions

## Updating a sequential file

{%highlight C%}
FILE* fp;
fp = fopen(file, "r+");
{%endhighlight%}

This example opens the file with the intention of both reading and writing it. An input operation may never directly follow an output operation or vice versa without an intervening call to **fseek**

The following program fragment appears to update selected records in a sequential file:

{%highlight C%}
FILE* fp;
struct record rec;
...
while (fread((char*)& rec, sizeof(rec), 1, fp) == 1) {
	//do something to rec
	if (rec must be rewritten) {
		fseek(fp, -(long)sizeof(rec), 1);
		fwrite((char*)&rec, sizeof(rec), 1, fp);
	}
}
{%endhighlight%}

The problem is that if a record is rewritten -- that is, if the fwrite call is executed -- the next thing done to the file is the **fread** at the beginning of the loop. This doesn't work because there is no intervening **fseek**. The solution is to rewrite it this way:

{%highlight C%}
FILE* fp;
struct record rec;
...
while (fread((char*)& rec, sizeof(rec), 1, fp) == 1) {
	//do something to rec
	if (rec must be rewritten) {
		fseek(fp, -(long)sizeof(rec), 1);
		fwrite((char*)&rec, sizeof(rec), 1, fp);
		fseek(fp, 0L, 1);
	}
}
{%endhighlight%}

The second **fseek** appears to do nothing, but it puts the file into a state where it can now be read successfully.

## Buffered output and memory allocation

{%highlight C%}
setbuf(stdout, buf);
{%endhighlight%}

tells the I/O library that all output written to *stdout* should henceforth use *buf* as an output buffer, and that output directly to *stdout* should not actually be written until *buf* becomes full or until the programmer directs it to be written by calling *fflush*. The appropriate size for such a buffer is defined as **BUFSIZE** in \<stdio.h\>

{%highlight C%}
#include <stdio.h>

main()
{
	int c;
	char buf[BUFSIZE];
	setbuf(stdout, buf);

	while ((c=getchar()) != EOF)
		putchar(c);
}
{%endhighlight%}

Unfortunately, this program is wrong. To see where the trouble lies, ask when buf is flushed for the last time. Answer: after the main program has finished, as part of the cleaning up that the library does before handing control back to the operating system. But by that time, buf has already been freed!

There are two ways to prevent this sort of trouble. First, make the buffer static

{%highlight C%}
static char buf[BUFSIZE];
{%endhighlight%}

Another possibility is to allocate the buffer dynamically and never free it:

{%highlight C%}
char* malloc();
setbuf(stdout, malloc(BUFSIZE));
{%endhighlight%}

Notice that there is no need here to check if *malloc* succeeded. If *malloc* fails, it will return a null pointer. This is acceptable second argument to *setbuf*; it requests that *stdout* be unbuffered.

## Use *errno* for error detection

The obvious way to take advantage of this is wrong:

{%highlight C%}
//call library function
if (errno)
	//complain
{%endhighlight%}

The trouble is that a library routine that sets *errno* on error is under no obligation to clear it in the absence of an error.

{%highlight C%}
errno = 0;
//call library function
if (errno)
	//complain
{%endhighlight%}

It is still wrong. Suppose that library function sets *errno* if the file isn't there. Then every time *fopen* opens a file that does not already exist, it has the side effect of setting *errno* even though no error has occured.

Thus when calling a library function, it is essential to test the value it returns for an error indication **before** examining *errno* to find the cause of the error:

{%highlight C%}
//call library function
if (error return)
	//examine errno
{%endhighlight%}

## The *signal* function

The best defense against problems is to keep signal handlers as simple as possible and group them all together. That way it will be easy to change them to suit a new system if needed.

# Chapter 6 The Preprocessor

## Spaces matter in macro definition

{%highlight C%}
#define f (x) ((x)-1)
{%endhighlight%}

means f represents 

{%highlight C%}
(x) ((x)-1)
{%endhighlight%}

To define f(x) as ((x)-1) one must write

{%highlight C%}
#define f(x) ((x)-1)
{%endhighlight%}

This rule does not apply to macro *calls*, just to macro *definitions*, Thus f(3) and f (3) both evaluate to 2.

## Side effect

The following program is not only inefficient but also wrong:

{%highlight C%}
#define max(a,b) ((a)>(b)?(a):(b))

biggest = x[0];
i = 1;
while (i<n)
	biggest = max(biggest, x[i++]);
{%endhighlight%}

It is because the operand *b* is evaluated twice in the macro definition.

Here is the typical definition of the *putc* macro:

{%highlight C%}
#define putc(x, p) \
	(--(p)->_cnt>=0?(*(p)->_ptr++=(x)):_flsbuf(x,p))
{%endhighlight%}

Notice that the first argument *x*, which could easily be bound to something like \*z++, is carefully evaluated only once: those occurrences are on opposite sides of a : operator.

In contrast, the second argument *p*, which represents the file on which to write, is always evaluated twice. Since it is unusually for the file argument to *putc* to have side effects, this rarely causes trouble. Some C implementations are less careful: it is possible to implement a *putc* that may evaluate its *first* argument more than once. If you give *putc* an argument with side effects, beware of careless implementations.

## Macros are not statements

How to define macro assert?

{%highlight C%}
#define assert(e) if (!e) assert_error(__FILE__,__LINE__)
{%endhighlight%}

This definition fails in a straightforward context (the dangling *else* problem)

{%highlight C%}
if (x>0 && y>0)
	assert (x>y);
else
	assert (y>x);
{%endhighlight%}

It is possible to avoid this problem by enclosing the body of the *assert* macro in braces:

{%highlight C%}
#define assert(e) \
	{ if (!e) assert_error(__FILE__,__LINE__); }
{%endhighlight%}

This raises a new problem. Our example now exapnds into

{%highlight C%}
if (x>0 && y>0)
	{ if (!(x>y)) assert_error("foo.c", 37); };
else
	{ if (!(y>x)) assert_error("foo.c", 39); };
{%endhighlight%}

and the semicolon before the *else* is a syntax error. One solution to this is to insist that a call to *assert* not be followed by a semicolon, but using this looks strange:

{%highlight C%}
y = distance(p, q);
assert(y > 0)
x = sqrt(y);
{%endhighlight%}

The right way to define *assert* is far from obvious: make the body of *assert* look like an expression and not a statement:

{%highlight C%}
#define assert(e) \
	((void)((e)|| assert_error(__FILE__,__LINE__)))
{%endhighlight%}

# Chapter 7 Portability Pitfalls

## Are characters signed or unsigned?

If *c* is a character variable, one can obtain the unsigned integer equivalent of *c* by writing *(unsigned) c*. This fails because when converting a *char* quantity to *unsigned*, it is converted to *int* first, with possibly unexpected results. The right way to do is *(unsigned char) c* 

## How does division truncate?

Suppose we divide *a* by *b* to give a quotient *q* and remainder *r*:

q = a/b;

r = a%b;

For the moment, suppose also that *b>0*. What relationships might we want to hold between *a*, *b*, *p* and *q*? 

1. We want q\*b+r == a

2. If we change the sign of *a*, we want that to change the sign of *q*, but not the manitude

3. When b>0, we want to ensure that r>=0 and r<b.

Unfortunately, they cannot be all be true at once.

What should be the value of (-3)/2? Property 2 suggests that it should be -1, but if that is so, the remainder must also be -1, which violates property 3. Alternatively, we can satisfy property 3 by making the remainder 1, in which case property 1 demands that the quotient be -2. This violates property 2.

Thus C, and any language that implements truncating integer division, must give up at least one of these three principles. Most programming languages give up number 3.

However, the C language definition guarantees only property 1, along with the property that |r|<|b| and that r>=0 whenever a>=0 and b>0

So for hash map, we can write:

{%highlight C%}
h = n%HASHSIZE;
if (h<0)
	h += HASHSIZE;
{%endhighlight%}

Better yet, design the program to avoid negative values of *n* in the first place and declare *n* as unsigned

## An example of portability problems

{%highlight C%}
void printnum(long n, void (*p)())
{
	if (n<0) {
		(*p)('-');
		n = -n;
	}
	if (n >= 10)
		printnum(n/10, p);
	(*p)((int)(n%10)+'0');
}
{%endhighlight%}

problems:

1. '0'+5 might not be '5' in some machines (do not use ASCII character set or any ANSI-conforming implementation)

2. set a negative value to positive value might overflow

3. the division truncate problem mentioned above

the final program:

{%highlight C%}

void printneg(long n, void (*p)())
{
	long q;
	int r;

	q = n/10;
	r = n%10;
	if (r>0) {
		r -= 10;
		q++;
	}
	if (n<=-10)
		printneg(q, p);
	(*p)("0123456789"[-r]);
}

void printnum(long n, void (*p)())
{
	if (n<0) {
		(*p)('-');
		printneg(n, p);
	} else
		printneg(-n, p);
}
{%endhighlight%}

# Chapter 8 Advice and Answers

Understanding how the pieces are going to fit before actually fitting them is one of the keys to a reliable result. Such understanding is particularly important under time pressure. Near the end of a long debugging session, it becomes tempting to try things almost at random and stop as something seems to work. That way lies disaster.

# Appendix: printf, varargs, and stdarg

## printf:

%g: It causes the corresponding value (float or double) to be printed, with trailing zeroes removed, to six significant digits. If the magnitude is greater than 999999, %g format prints such a value in scientific notation (still 6 siginificant digits)

%e: insists on writing floating-point values with an explicit exponent. pi written under %e format is 3.141593e+00. The %e format item prints six digits *after the decimal point*, rather than six siginificant digits.

%f: forces the value to be printed without an explicit exponent. %f format item prints six digits after the decimal point. Thus a very small value may appear as zero even if it is not, and a very large value appears with a lot of digits

The width modifier never causes truncation of a field. When using the width modifier to line up columns of figures, a value that is too large for its column will displace subsequent values on that row to the right:

{%highlight C%}
int i;
for (i=0; i<=10; i++)
	printf("%2d %2d *\n", i, i*i);
{%endhighlight%}

The width modifier is effective for all format codes, even %%. Thus

{%highlight C%}
printf("%8%\n");
{%endhighlight%}

prints seven spaces followed by a %.

## precision modifier:

It consists of a decimal point followed by a string of digits and appears before the format code and length modifier and after the % and width modifier.

+ for the integer format items %d, %o, %x and %u, it specifies the minimum number of digits to print. If the value doesn't need that many digits, leading 0s will be supplied.

{%highlight C%}
printf("%.2d/%.2d/%.4d",7,14,1789);
{%endhighlight%}

prints 

07/14/1789

+ for %e,%E and %f, the precision specifies the number of digits after the decimal point.

+ for %g and %G, the precision specifies the number of significant digits to print

+ the precision is ignored for c and % format items.

## Flags:

+ the - flag is meaningful only if a width is present. In that case, any padding blanks will appear on the right rather than on the left

+ the + flag specifies that every numberic value printed should have a sign as its first character. It bears no relationship to the - flag.

+ when a blank is used as a flag, it means that a single blank is to appear before a numberic value if its first character is not a sign.

+ the # flag causes the decimal point always to be printed; and it stops the %g and %G formats from suppressing trailing 0s. %#0 cause the value to be preceded by 0 (%#o is not the same as 0%o because 0%o prints zeros as 00), %#x and %#X format items cause the value to be preceded by 0x and 0X respectively.

## Variable field width and precision:

{%highlight C%}
printf("%*.*s\n", 12, 5, str);
{%endhighlight%}

has the same effect as 

{%highlight C%}
printf("%12.5s\n", str);
{%endhighlight%}

which prints the first five characters of str (or fewer, if strlen(str)<5), preceded by enough blanks to bring the total number of characters printed to 12.

{%highlight C%}
printf("%*%\n", n);
{%endhighlight%}

prints n-1 spaces followed by a %.

If * is used for the field width, and the corresponding value is negative, the effect is as if the - flag were also present. Thus, in the example immediately above, if n is negative, the output will be a % followed by 1-n spaces.

## Neologisms:

After executing

{%highlight C%}
int n;
printf("hello\n%n", &n);
{%endhighlight%}

n has the value 6
