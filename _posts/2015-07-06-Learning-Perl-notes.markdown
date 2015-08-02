---
layout:	post
title:	"Learning Perl"
date:	2015-07-06
---

# Chapter 1 Introduction

```perl
#!/usr/bin/perl
print "Hello, world!\n"
```

The following program only runs under Perl 5.10 or later

```perl
#!/usr/bin/perl
use 5.010
say "Hello, world!\n"
```

Perl's internal compiler first runs through your entire source, turning it into internal bytecode

```perl
#!/usr/bin/perl

@lines = `perldoc -u -f atan2`;
foreach (@lines) {
	s/\w<([^>]+)>/\U$1/g;
	print;
}
```

# Chapter 2 Scalar Data

All numbers have the same format internally. This means that there are no integer values internal to Perl. Perl allows you to add underscores for clarity within integer literals:

61_298_040_283_768

## String

If you want to use Unicode literally in your program, you need to add the utf8 pragma:

```perl
use utf8;
```

You can concatenate, or join, string values with the . opeartor

```perl
"Hello" . "world"	# same as "Helloworld"
```

string repetition operator, consisting of the single lowercase letter x

```perl
"fred" x 3		# is "fredfredfred"
"barney" x (4+1)	# is "barney" x 5
5 x 4.8			# is really "5" x 4, which is "5555" 
```

Perl automatically converts between numbers and strings as needed. It all depends upon the operator that you apply to the scalar value. 

## Perl's Built-in Warnings

```perl
#!/usr/bin/perl
use warnings;

$perl -w my_program

#!/usr/bin/perl -w

#!/usr/bin/perl
use diagnostics;	# longer description

```

## Scalar Variables

Scalar variable names begin with a dollar sign, called the sigil. Uppercase and lowercase letters are distinct

```perl
$name
$Name
$NAME

$fred = 17;
$barney = 'hello';
$barney = $fred+3;
$barney *= 3;
```

When a string literal is double-quoted, it is subject to *variable interpolation*

```perl
$meal = "brontosaurus steak";
$barney = "fred ate a $meal";		# $barney is now "fred ate a brontosaurus steak"
$barney = 'fred ate a ' . $meal;	# another way to write that

$what = "brontosaurus steak";
$n = 3;
print "fred ate $n ${what}s. \n";	# now uses $what
print "fred ate $n $what" . "s.\n";	# another way to do it

```

## Creating Characters by Code Point

```perl
$alef = chr(0x05D0);
$alpha = chr(hex('03B1'));
$omega = chr(0x03C9);

"\x{03B1}\x{03C9}"
```

## Numeric and string comparison operation

Comparison			Numeric		String

Equal				==		eq

Not equal			!=		ne

Less than			<		lt

Greater than			> 		gt

Less than or equal to		<=		le

Greater than or equal to	>=		ge

## Boolean Values

Perl doesn't have a separate Boolean datatype. 0 and empty string ('') means false, the string '0' is the only non-empty string that is false

## Getting User Input

```perl
$line = <STDIN>;
if ($line eq "\n") {
	print "That was just a blank line!\n";
} else {
	print "that line was: $line\n";
}
```

The string value of <STDIN> typically has a newline character on the end of it. You can use chomp() to remove a trailing newline from a string in a variable. The most common use of chomp() looks like this:

```perl
chomp($text=<STDIN>);

$text=<STDIN>;
chomp($text);
```

chomp() is actually a function. It has a return value, which is the number of characters removed.

```perl
$food = <STDIN>;
$betty = chomp $food;	# get value 1. parenthese are always optional
```

If a line ends with two or more newlines, chomp() removes only one. If there's no newline, it does nothing, and return 0.

## The undef Value

Variables have the special *undef* value before they are first assigned, it acts like zero or empty string.

```perl
$n = 1;
while ($n < 10) {
	$sum += $n;
	$n += 2;
}

$string .= "more text\n";
```

## The defined Function

This function returns false for *undef* and true for everything else

```perl
$madonna = <STDIN>;
if (defined($madonna)) {
	print "The input was $madonna;
} else {
	print "No input available!\n";
}
```

# Chapter 3 Lists and Arrays

## Special Array Indices

```perl
$rocks[0] = 'bedrock';
$rocks[1] = 'slate';
$rocks[2] = 'lava';
$rocks[3] = 'crushed rock';
$rocks[99] = 'schist';

$rocks[$#rocks] = 'hard rock'; #$#rocks is the last element

$rocks[-1] = 'hard rock';	# -1 is also the last element, -2 is the second last...
```

## List Literals

```perl
(1,2,3)	# list of three values 1,2,3
("fred", 4.5)	# two values, "fred" and 4.5
(1..5)	# (1,2,3,4,5)
(1.7..5.7)	# same thing; both values are truncated
qw(fred barney betty wilma dino)	# ("fred", "barney", "betty", "wilma", "dino"). qw stands for "quoted words"
qw! fred barney betty wilma dino !	# Perl lets you choose any punctuation character as the delimiter
qw/ fred barney betty wilma dino /
qw# fred barney betty wilma dino #
qw[ fred barney betty wilma dino ]
```

## List Assignment

```perl
($fred, $barney, $dino) = ("flinstone", "rubble", undef);
($fred, $barney) = ($barney, $fred);	# swap values
@rocks = qw/ bedrock slate lava /;	# ($rocks[0], $rocks[1], $rocks[2]) = ("bedrock","slate","lava")
@tiny = ();		# the empty list
@giant = 1..1e5;	# a list with 100,000 elements
$dino = "granite";
@quarry = (@rocks, "crushed rock", @tiny, $dino) 
```

The last assignment gives @quarry the five-element list (bedrock, slate, lava, crushed rock, granite). An array name expands to the list it contains. An array doesn't become an element in the list

```perl
@array = 5..9;
$fred = pop(@array);	# $fred gets 9, @array now has (5,6,7,8)
$barney = pop @array;	# @array now has (5,6,7)

# if the array is empty, pop leaves it alone and returns undef

push(@array, 0);	# @array now has (5,6,7,0)
push @array, 8;		# @array now has (5,6,7,0,8)

# the first argument to push or the only argument for pop must be an array variable--pushing and poping would not make sense on a literal list.

@array = qw# dino fred barney #;
$m = shift(@array);	# $m gets "dino", @array now has ("fred", "barney")
$n = shift @array;	# $n gets "fred", @array now has ("barney")
unshift(@array, 5);	# @array now has (5, "barney")
unshift @array, 4;	# @array now has (4,5,"barney")

@array = qw( pebbles dino fred barney betty );
@removed = splice @array, 2;	# remove everything after fred
				# @removed is qw(fred barney betty)
				# @array is qw(pebbles dino)

@array = qw( pebbles dino fred barney betty );
@removed = splice @array, 1, 2	# remove dino, fred. 1 means index, 2 means length
				# @removed is qw(dino fred)
				# @array is qw(pebbles barney betty)

@array = qw( pebbles dino fred barney betty );
@removed = splice @array, 1, 2, qw(wilma)	# remove dino, fred
				# @removed is qw(dino fred)
				# @array is qw(pebbles wilma barney betty)

# if you specify a length of 0, you remove no elements but still insert the "replacement" list

```

## The foreach Control Structure

```perl
foreach $rock (qw/ bedrock slate lava /) {
	print "One rock is $rock.\n";
}
```

The control variable is not a copy of the list element--it actually is the list element. If you modify the control variable inside the loop, you modify the element itself.

```perl
@rocks = qw/ bedrock slate lava /;
foreach $rock (@rocks) {
	$rock = "\t$rock";
	$rock .= "\n";
}
print "The rocks are: \n", @rocks;	# each one is indented, on its own line
```

What's the value of the control variable after the loop has finished? It's the same as it was before the loop started.

```perl
$rock = 'shale';
@rocks = qw/ bedrock slate lava /;
foreach $rock (@rocks) {
	...
}
print "rock is still $rock\n";	# 'rock is still shale'
```

## Perl's Favorite Defaults: $_

```perl
foreach (1..10) {
	print "I can count to $_!\n";	# just as the control variable
}
```

Perl will automatically use $_ when you don't tell it to use some other variable or value:

```perl
$_ = "Yabba dabba doo\n";
print;	# prints $_ by default
```

## reverse

```perl
@fred = 6..10;
@barney = reverse(@fred);	//10,9,8,7,6
@wilma = reverse @fred;		//gets the same thing. reverse doesn't affect its arguments.
```

## sort

```perl
@rocks = qw/ bedrock slate rubble granite /;
@sorted = sort(@rocks);
```

## The each Operator

Starting with Perl 5.12, you can use the *each* operator on arrays. Every time that you call *each* on an array, it returns two values for the next element in the array--the index of the value and the value itself.

```perl
use 5.012;
@rocks = qw/ bedrock slate rubble granite /;
while (my($index, $value) = each @rocks) {	# my declares the listed variables to be local to the enclosing block
	say "$index: $value";
}
```

If you want to do this without *each*:

```perl
@rocks = qw/ bedrock slate rubble granite /;
foreach $index (0..$#rocks) {
	print "$index: $rocks[$index]";
}
```

## Scalar and List Context

```perl
@people = qw( fred barney betty );
@sorted = sort @people;		# list context: barney, betty, fred
$number = 42 + @people;		# number of elements, 42+3 gives 45

@list = @people;	# a list of 3 people
$n = @people;		# the number 3

@backwards = reverse qw/yabba dabba doo/;	# doo, dabba, yabba
$backwards = reverse qw/yabba dabba doo/;	# oodabbadabbay

@fred = 6*7;	# gets the one-element list (42)
@wilma = undef;	# Gets the one-element list (undef)
@betty = ();	# a correct way to empty an array
```

On occasion, you may need to force scalar context where Perl is expecting a list. In that case, you can use the fake function *scalar*

```perl
@rocks = qw(talc quartz jade obsidian);
print "I have ", @rocks, " rocks!\n";	#WRONG, prints names of rocks
print "I have ", scalar @rocks, " rocks!\n";	#Correct, gives a number
```

In list context, this operator returns all of the remaining lines up to the end-of-file. It returns each line as a separate element of the list.

```perl

# when the input is from a file, this will read the rest of the file. 
# when the input is from the keyboard, you'll normally type a Ctrl-D
@lines = <STDIN>;

@lines = <STDIN>;	# read all the lines
chomp(@lines);		# discard all the newline characters

chomp(@lines = <STDIN>);	# more common way
```

## Exercises

1. 

```perl

#!/usr/bin/perl

@lines = <STDIN>;
@lines = reverse @lines;
print @lines;
```

2. 

```perl
#!/usr/bin/perl

@names = qw/ fred betty barney dino wilma pebbles bamm-bamm/;
chomp(@index=<STDIN>);
foreach $val (@index) {
	if ($val>0 && $val<=$#names+1) {
		print "$names[$val-1]\n";
	}
}
```

# Chapter 4 Subroutines

## Define a Subroutine

You don't normally need any kind of forward declaration

```perl
sub marine {
	$n += 1;	# Global variable $n
	print "hello, sailor number $n\n";
}

&marine;	# hello, sailor number 1
&marine;	# hello, sailor number 2
&marine;	# hello, sailor number 3
&marine;	# hello, sailor number 4

```

Return value: whatever calculation is last performed in a subroutine is automatically also the return value

```perl
sub sum_of_fred_and_barney {
	print "Hey, you called the sum_of_fred_and_barney!\n";
	$fred + $barney;	# That's the return value
	# print "Hey,";	# if this line is not commented out, the return value is print statement(normally 1)
}

$fred = 3;
$barney = 4;
$wilma = $sum_of_fred_and_barney;	#wilma gets 7
```

# Arguments

Perl passes the list to the subroutine. Perl automatically stores the parameter list in the @_ for the duration of the subroutine

```perl
# The @_ variable is private to the subroutine; if there's a global value in @_, Perl saves it before it invokes the next subroutine and restores its previous value upon return from that subroutine

# so @_ is always the parameter list for the current subroutine invocation

sub max {
	if ($_[0] > $_[1]) {
		$_[0];
	} else {
		$_[1];
	}
}

$n = &max(10,15);
```

## Private Variables in Subroutine

```perl
sub max {
	my($m, $n) = @_;
	if ($m>$n) {$m} else {$n} # You don't need a semicolon after the return value expression
}
```

## Variable-Length Parameter Lists

```perl
sub max {
	if (@_ != 2) {	# by examining the @_ array
		print "Warning! should get exactly two arguments\n";
	}
	# continue as before...
}

sub max {
	my($max_so_far) = shift @_;
	foreach (@_) {
		if ($_ > $max_so_far) { # remember there is no automatic connection between @_ and $_
			$max_so_far = $_;
		}
	}
	$max_so_far;
}
```

## Notes on Lexical (my) Variables

Those lexical variables can actually be used in any block, not merely in a subroutine's block. The scope of a lexical variable's name is limited to the smallest enclosing block or file.

```perl
foreach (1..10) {
	my ($square) = $_ * $_;
	print "$_ squared is $square.\n";
}
```

The *my* operator doesn't change the context of an assignment:

```perl
my($num) = @_;	# list context, $num gets the first parameter
my $num = @_;	# scalar context, $num gets the number of parameters

my $fred, $barney;	# WRONG! Fails to declare $barney
my ($fred, $barney);	# declare both

my @phone_number;	# declare private array 
```

## The use strict Pragma

```perl 
use strict;	# Enforce some good programming rules
use 5.012;	# Perl 5.12 loads strict for you

my $bamm_bamm = 3;	
$bammbamm += 1;	# No such variable: compile time fatal error
```

## The return Operator

```perl
my @names = qw/ fred barney betty wilma pebbles /;
my $result = &which_element_is("dino", @names);

sub which_element_is {
	my ($what, @array) = @_;
	foreach (0..$#array) {
		if ($what eq $array[$_]) {
			return $_;
		}
	}
	-1;
}
```

## Omitting the Ampersand

If the subroutine has the same name as a Perl built-in, you must use the ampersand to call your version. 

Until you know the names of all Perl's built-in functions, always use the ampersand on function calls.

## Non-Scalar Return Values

```perl
sub list_from_fred_to_barney {
	if ($fred < $barney) {
		$fred..$barney;
	} else {
		reverse $barney..$fred;
	}
}

$fred = 11;
$barney = 6;
@c = &list_from_fred_to_barney;	# gets (11,10,9,8,7,6)
```

## Persistent, Private Variables

With *state*, you can still have private variables scoped to the subroutine but Perl will keep their values between calls.

```perl

use 5.010;

sub marine {
	state $n = 0;
	$n += 1;
	print "hello, sailor number $n!\n";
}

The first time you call the subroutine, Perl declares and initializes $n. Perl ignores the statement on all subsequent calls. Between calls, Perl retains the value of $n for the next call to the subroutine
```

Restriction: You can't initialize them in list contexts as of Perl 5.10

```perl
state @array = qw(a b c);	# Error!
```

# Chapter 5 Input and Output

```perl
while (<STDIN>) {
	print "I saw $_";	# read a single line every time
}

foreach (<STDIN>) {
	print "I saw $_";	# read all of the input before the loop can start running
}
```

## Input from the Diamond Operator

```perl

# read each file in the command line, print their contents line by line
while (<>) {
	chomp;
	print "It was $_ that I saw!\n";
}
```

## Output to Standard Output

```perl
@array = qw/ fred barney betty /;
print @array;	# fredbarneybetty
print "@array";	# fred barney betty
```

When there are no parenthese, *print* is a list operator, printing all of the items in the following list; But when the first thing after *print* is a left parenthesis, *print* is a function call, and it will print only what's found inside the parentheses. 

```perl
print "Hello world\n";
print (2+3)*4;	# print 5 rather than 20
```

## Formatted Output with printf

```perl
printf "Hello, %s; your password expires in %d days!\n", $user, $day_to_die;

printf "%g %g %g\n", 5/2, 51/17, 51**17;	# 2.5 3 1.0683e+29

my @items = qw( wilma dino pebbles);
my $format = "The items are:\n" . ("%10s\n" x @items);
```

## Opening a Filehandle

There are six special filehandle names that Perl already uses for its own purpose: STDIN, STDOUT, STDERR, DATA, ARGV, and ARGVOUT.


```perl
open CONFIG, '<', 'dino';	# read from dino
open BEDROCK, '>', $file_name;	# write to $file_name
open LOG, '>>', &logfile_name();# append to logfile_name()
open CONFIG, '<:encoding(UTF-8)', 'dino';

close BEDROCK;	# finish with a file handle
```

You can get a list of all of the encodings that your perl understands with a Perl one-liner:

```perl
perl -MEncode -le "print for Encode->encodings(':all')"
```

dos2unix

```perl
open BEDROCK, '>:crlf', $file_name;	# ensure you get a CR-LF at the end of each line
open BEDROCK, '<:crlf', $file_name;	# do the same thing to read a file which might have DOS line endings
```

Bad FileHandles

```perl
my $success = open LOG, '>>', 'logfile';
if (!$success) {
	# the open failed
}
```

## Fatal error with die

The *die* function prints out the message you give it and make sure that your program exits with a nonzero exit status.

```perl
if (! open LOG, '>>', 'logfile') {
	die "Cannot create logfile: $!";	# $! is human-readable complaint from the system
}
```

The *warn* function works just like *die* does, except for that last step--it doesn't acutally quit the program

## Automatically die-ing

```perl
use autodie;
open LOG, '>>', 'logfile';	# When it fails, autodie invokes die on your behalf
```

## Using FileHandles

```perl
if (! open PASSWD, "/etc/passwd") {
	die "How did you get logged in? ($!)";
}

while (<PASSWD>) {
	chomp;
	...
}

# You can use a filehandle open for writing or appending with print or printf
print LOG "Captain's log, stardate 3.1415926\n";	# output goes to LOG
printf STDERR "%d percent complete.\n", $done/$total * 100;
```

## Changing the Default Output Filehandle

```perl
select BEDROCK;
print "Wilma!\n";

# Setting the special $| variable to 1 will set the currently selected filehandle to always flush the buffer after each output operation

select LOG;	# change the default filehandle with the select operator
$| = 1;		# don't keep LOG entries sitting in the buffer
select STDOUT;
print LOG "This gets written to the LOG at once!\n";
```

## Filehandles in a Scalar

```perl
open my $rocks_fh, '<', 'rocks.txt'
	or die "Could not open rocks.txt: $!";

while (<$rocks_fh>) {
	chomp;
	...
}

open my $rocks_fh, '>>', 'rocks.txt'
	or die "Could not open rocks.txt: $!";
foreach my $rock (qw( slate lava granite )) {
	say $rocks_fh $rock;
}
print $rocks_fh "limstone\n";	# no comma after $rocks_fh
close $rocks_fh;
```

# Chapter 6 Hashes

## Hash element access

```perl
$family_name{'fred'} = 'flinstone';

# the Hash as a whole
%some_hash = ('foo', 35, 'bar', 12.4, 2.5, 'hello', 'wilma',  1.72e30, 'betty', "bye\n");

my %inverse_hash = reverse %any_hash;	# key in any_hash becomes value in inverse_hash

my %last_name = (
	fred => 'flinstone',
	dino => undef,
	barney => 'rubble',
	betty => 'rubble',
	);
```

## Hash functions

The *keys* function yields a list of all the keys in a hash, while the *values* function gives the corresponding values. 

```perl
my %hash = ('a'=>1, 'b'=>2, 'c'=>3);
my @k = keys %hash;	# @k contains 'a', 'b' and 'c'
my @v = values %hash;	# @v contains 1, 2 and 3

# each function
while (($key, $value) = each %hash) {
	print "$key => $value\n";
}

# exists function
if (exists $books{"dino"}) {
	print "there's a library card for dino!\n";
}

# delete function. After a delete, the key can't exist in the hash
my $person = "betty";
delete $books{$person};
```

## The %ENV hash

```perl
# Perl stores the environment in the %ENV hash
print "PATH is $ENV{PATH}\n";
```

# Chapter 7 In the World of Regular Expressions

```perl
$_ = "yabba dabba doo";
if (/abba/) {
	print "It matched!\n";
}

if (/\p{Space}/) {
	print "The string has some whitespace\n";
}

if (/\p{Digit}/) {
	print "The string has a digit\n";
}

if (/\P{Space}/) { # capital P means negating the property
	print "The string has one or more non-whitespace characters\n";
}

# . means any single character
# * means zero or more
# + means one or more
# ? means the preceding item may occur once or not at all
```

## Grouping in Patterns

The parentheses also give you a way to reuse part of the string directly in the match. 

```perl

# You denote a back reference as a backslash followed by a number.
$_ = "abba";
if (/(.)\1/) {
	print "It matches same character next to itself\n";
}

# g{N} notation is introduced in 5.10. same meaning as above
use 5.010;
$_ = "aa11bb";
if (/(.)\g{1}11/) {
	print "It matched\n";
}

# You can also use negative numbers, which is a relative back reference
# Just count from its own position and refer to the group right before it
use 5.010;
$_ = "aa11bb";
if (/(.)\g{-1}11/) {
	print "It matched\n";
}
```

## Alternatives

```perl
/fred|barney|betty/ # will match any string that mentions fred, or barney, or betty
```

## Character Class Shortcuts

```perl
# \d: any digit

use 5.014;
$_ = 'The HAL-9000 requires authorization to continue.';

if (/HAL-[\d]+/a) {	# /a tells Perl to use the old ASCII interpretation
	say 'The string mentions some model of HAL computer.';
}

# \s: match any whitespace
# \R: match any sort of linebreak, introduced in Perl 5.10
# \w: match the set of characters [a-zA-Z0-9_] 
# \D, \W, \S: [^\d], [^\w] and [^\s]
```

# Chapter 8 Matching with Regular Expressions

## Matches with m//

/fred/ is a shortcut for m/fred/, m(fred), m{fred}, etc. Just like qw// operator.

```perl
/http:\/\//	# matches "http://"
m%http://%	# same as above
```

## Match Modifiers

```perl
if (/yes/i) {	# ignore case
	print "yes";
}

$_ = "I saw Barney\ndown at the bowling alley\nwith Fred\n";
if (/Barney.*Fred/s) {	# without /s that match would fail since the two names are not on the same line.
	print "That string mentions Fred after Barney";
}

/-?[0-9]+\.?[0-9]*/	
/-? [0-9]+ \.? [0-9]* /x	# same as above. Ignore white space within the pattern

# /\w+/u: any Unicode word character
# /\w+/l: The ASCII version, and word chars from the locale
```

## Anchors

```perl
m{\Ahttps?://}i	# \A matches at the absolute beginning of a string, you can also use ^
m{\.png\z}i	# \z matches at the end of a string, you can also use $

while (<STDIN>) {	# \Z allows an optional newline after it.
	print if /\.png\Z/;
}

$_ = 'This is a wilma line
barney is on another line
but this ends in fred
and a final dino line';

/fred$/m	# match fred at the end of any line

# \b: word-boundary
/\bfred\b/	# match the word fred only (in Vim it is \<fred\>)

# \B: nonword-boundary
/\bsearch\B/	# match searches, searching, and searched, but not search or researching
```

## The Binding Operator =~

```perl
my $some_other = "I dream of betty rubble.";
if ($some_other =~ /\brub/) {	# match the string on the left instead of $_
	print "Aye, there's the rub.\n";
}
```

## The Match Variables

```perl
$_ = "Hello there, neighbor";
if (/\s([a-zA-Z]+),/) {
	print "the word was $1\n";	# $1 is the word captured by ([a-zA-Z]+)
```

## The Persistence of Captures

An unsuccessful match leaves the previous capture values intact, but a successful one resets them all.

You shouldn't use a match variable more than a few lines after its pattern match.

## Noncapturing Parentheses

```perl
if (/(?:bronto)?saurus (steak|burger)/) {
	print "Fred wants a $1\n";	# ?: is to group things but not trigger the capture groups
}
```

## Named Captures

```perl
use 5.010;

my $names = 'Fred or Barney';
if ($names =~ m/(?<name1>\w+) (?:and|or) (?<name2>\w+)/ ) {
	say "I saw $+{name1} and $+{name2}";
}
```

## The Automatic Match Variables

```perl

# The part of the string that actually matched the pattern is automatically stored in $&
# whatever come before the matched section is in $`
# whatever was after it is in $'
# it has performance problem
if ("hello there, neighbor" =~ /\s(\w+),/) {
	print "That was ($`)($&)($').\n";
}

# in 5.10, ${^PREMATCH}, ${^MATCH}, ${^POSTMATCH} do the same thing
use 5.010;
if ("hello there, neighbor" =~ /\s(\w+),/) {
	print "That was (${^PREMATCH})(${^MATCH})(${^POSTMATCH}).\n";
}

```

# Chapter 9 Processing Text with Regular Expressions

## Substitution

```perl
$_ = "He's out bowling with Barney tonight";
s/Barney/Fred/;	# Replace Barney with Fred
print "$_\n";

s/with (\w+)/against $1's team/;

$_ = "fred flinstone";
if (s/fred/wilma/) {
	print "Successfully replaced fred with wilma\n";
}

$_ = "home, sweet home";
s/home/cave/g;	globally, replace all the occurences

s/^\s+|\s+$//g;	# strip leading and trailing whitespace

# different Delimiters
s#^https://#http://#;
s{fred}{barney};
s[fred][barney];
s<fred>#barney#;

(my $copy=$original) =~ s/\d+ ribs?/10 ribs/;	# replace other string rather than $_

$_ = "I saw Barney with Fred";	
# \U escape forces uppercase
s/(fred|barney)/\U$1/gi;	# "I saw BARNEY with FRED"
# \L escape forces lowercase
s/(fred|barney)/\L$1/gi;	# "I saw barney with fred"
# \E turns off case shifting
s/(\w+) with (\w+)/\U$2\E with $1/i;	# "I saw FRED with barney"
# \u with \L means "capitalize the first letter"
s/(fred|barney)/\u\L$1/ig;	# "I saw Fred with Barney"

# these escape sequences are available in any double-quotish string
print "Hello, \L\u$name\E, would you like to play a game?\n";
```

## Split and join Operator

```perl
my @fields = split /:/, "abc:def:g:h";	# gives ("abc", "def", "g", "h")

my $some_input = "This  is a \t  test.\n";
my @args = split /\s+/, $some_input;	# ("This", "is", "a", "test.")

# the default for split is to break up $_ on whitespaces
my @fields = split;	# split /\s+/, $_;

my $x = join ":", 4,6,8,10,12;	# "4:6:8:10:12"

# there may be no glue at all if the list doesn't have at least two elements:
my $y = join "foo", "bar";	# gives just "bar"
my @empty;
my $empty = join "baz", @empty;	# no items so it's an empty string
```

## m// in List Context

```perl
$_ = "Hello there, neighbor!";
my($first, $second, $third) = /(\S+) (\S+), (\S+)/;

my $text = "Fred dropped a 5 ton granite block on Mr. Slate";
my @words = ($text =~ /([a-z]+)/ig);
print "Result: @words\n";	# Result: Fred dropped a ton granite block on Mr Slate

my $data = "Barney Rubble Fred Flinstone Wilma Flinstone";
my %last_name = ($data =~ /(\w+)\s+(\w+)/g); # it returns a pair of captures
```

## Updating Many Files

```perl
#!/usr/bin/perl -w

use strict;

chomp(my $date = `date`);	# system command
# when there's a string in $^I, that string is used as a backup filename's extension
$^I = ".bak";

while (<>) {
	s/^Author:.*/Author: Randel L. Schwartz/;
	s/^Phone:*\n//;
	s/^Date:.*/Date: $date/;
	print;
}
```

## In-Place Editing from the command line

```perl

# -p option always prints the contents of $_ each time around the loop
# -i.bak is the same as "$^I='.bak';"
# -w turns on warnings
# -e says "executable code follows"
$ perl -p -i.bak -w -e 's/Randall/Randal/g' fred*.dat
```

# Chapter 10 More Control Structures

```perl
unless ($fred =~ /\A[A-Z_]\w*\z/i) {	# run the block unless the condition is true
	print "The value of \$fred doesn't look like a Perl identifier name.\n";
}

# same as
if (! ($fred =~ /\A[A-Z_]\w*\z/i)) {
	print "The value of \$fred doesn't look like a Perl identifier name.\n";
}

until ($j > $i) {
	$j *= 2;
}

# same as 
while ($j <= $i) {
	$j *= 2;
}

print "$n is a negative number.\n" if $n < 0;
print " ", ($n += 2) while $n < 10;
$greet($_) foreach @person

# elsif
if (! defined $dino) {
	print "The value is undef.\n";
} elsif ($dino =~ /^-?\d+\.?$/) {
	print "The value is an integer.\n";
}

# Autoincrement and Autodecrement
my $bedrock = 42;
$bedrock++;
$bedrock--;

# for loop
for ($i=1; $i<=10; $i++) {
	print "I can count to $i\n";
}

# last Operator, immediately ends execution of the loop
# like break in C
while (<STDIN>) {
	if (/__END__/) {
		last;
	} elsif (/fred/) {
		print;
	}
}

# next Operator. like continue in C
while (<>) {
	foreach (split) {
		$total++;
		next if /\W/;
		$valid++;
		$count{$_}++;
	}
}

# redo Operator
# The big difference between next and redo is that next will advance to the next iteration, but redo will redo the current iteration
my @words = qw{ fred barney pebbles dino wilma betty };
my $errors = 0;

foreach (@words) {
	print "Type the word '$_': ";
	chomp(my $try = <STDIN>);
	if ($try ne $_) {
		print "Sorry - That's not right. \n\n";
		$errors++;
		redo;
	}
}
print "You've completed the test, with $errors errors.\n";

# Labeled Blocks
# work with a loop block that's not the innermost one
# recommand that they be all uppercase

LINE: while (<>) {
	foreach (split) {
		last LINE if /__END__/;
		...
	}
}

# The Conditional Operator ?:
my $location = &is_weekend($day)?"home":"work";

# Logical Operator: &&, ||, and, or
# Unlike what happens in C, the value of a short circuit logical operator is the last part evaluated, not a Boolean value

# The defined-or Operator
# if $ENV{VERBOSE} doesn't have a value, give it one
use 5.010;
my $Verbose = $ENV{VERBOSE} //1;


# The idiomatic way of opening a file
open $my $fh, '<', $filename
	or die "Can't open '$filename': $!";
```

# Chapter 11 Perl Modules

## The File::Basename Module

```perl
use File::Basename;
# or you can import that function only
# use File::Basename qw/ basename /;

my $name = "/usr/local/bin/perl";
my $basename = basename $name;	# gives 'perl', basename is the function of File::Basename module
```

or you can import nothing from that module, and call them by their full names:

```perl
use File::Basename qw/ /;

my $name = "/usr/local/bin/perl";
my $dirname = File::Basename::dirname $name;
```

## The File::Spec Module

```perl
use File::Spec

... 
my $new_name = File::Spec->catfile($dirname, $basename);
rename($old_name, $new_name)
	or warn "Can't rename '$old_name' to '$new_name': $!";
```

## CGI.pm

```perl
#!/usr/bin/perl

use CGI qw(:all)	# an export tag that specifies a group of functions rather than a single function

print header("text/plain"),
	start_html("This is the page title"),
	h1("Input parameters");

my $list_items;
foreach $param ( param() ) {
	$list_items .= li("$param: ". param($param));
}
print ul($list_items);
print end_html();
```

## Databases and DBI

```perl
use DBI;

$dbh = DBI->connect($data_source, $username, $password);

my $data_source = "dbi:Pg:dbname=name_of_database";

my $sth = $dbh->prepare("SELECT * FROM foo WHERE bla");
$sth->execute();
my @row_ary = $sth->fetchrow_array;
$sth->finish;

$dbh->disconnect();
```

## Dates and Times

```perl
# get DateTime module from CPAN

my $dt = DateTime->from_each(epoch => time);
printf '%4d%02d%02d', $dt->year, $dt->month, $dt->day;

print $dt->ymd;		#2011-04-23
print $dt->ymd('/');	#2011/04/23
print $dt->ymd('');	#20110423
```

# Chapter 12 File Tests

```perl
# -e, file exists
die "Oops! A file called '$filename' already exists\n"
	if -e $filename;	# File or directory exists

# -M modification time
warning "Config file is looking pretty old"
	if -M CONFIG > 28;	# modification time in days since the start of the program

# -s file size, -A, access time
my @original_files = qw/ fred barney betty wilma pebbles dino bamm-bamm/;
my @big_old_files;
foreach my $filename (@original_files) {
	push @big_old_files, $filename
		if -s $filename > 100_000 and -A $filename > 90;


# the virtual filehandle _ uses the information from the last file lookup that a file test operator performed
if (-r $file and -w _) {
	...
}

use 5.010;
if (-w -r -x -o -d $file) {
	print "My directory is readable, writable and executable";
}

```

## The stat and lstat Function

If you need the information about the symbolic link itself, use *lstat* rather than *stat*

```perl
my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev,
	$size, $atime, $mtime, $ctime, $blksize, $blocks)
		 = stat($filename);
```

## the localtime Function

```perl
my $timestamp = 1180630098;
my $date = localtime $timestamp;

my ($sec, $min, $hour, $day, $mon, $year, $wday, $yday, $isdst)
	 = localtime $timestamp;	# in a list context

my $now = gmtime;	# Get the current universal timestamp as a string
```

## Bitwise Operators

```perl
10 & 12;	# bitwise-and
10 | 12;	# bitwise-or
10 ^ 12;	# bitwise-xor
6 << 2;		# bitwise shift left
25 >> 2;	# bitwise shift right
~10;		# bitwise negation
```

# Chapter 13 Directory Operations

## Moving Around the Directory Tree

```perl
chdir '/etc' or die "cannot chdir to /etc: $!";
```

## Globbing

```perl
my @all_files = glob '*';
my @pm_files = glob '*.pm';

my @all_files = <*>;	# the same as my @all_files = glob '*'; 

my @files = <FRED/*>;	# a glob
my @lines = <FRED>;	# a filehandle read
```

## Directory Handles

```perl
my $dir_to_process = '/etc';
opendir my $dh, $dir_to_process or die "Cannot open $dir_to_process: $!";
foreach $file (readdir $dh) {	# read the names of the files in a directory
	print "one file in $dir_to_process is $file\n";
}
closedir $dh;


use File::Sepc::Functions;
opendir my $somedir, $dirname or dir "Cannot open $dirname:$!";
while (my $name = readdir $somedir) {
	next if $name =~ /^\./;			#skip over dot files
	$name = catfile($dirname, $name);
	next unless -f $name and -r $name;	#only readable files
	...
}
```

## Recursive Directory Listing

```perl
$ find2perl . -name '*.pm'
#!/usr/bin/perl -w 
	eval 'exec /usr/bin/perl -S $0 ${1+"$@"}'
		if 0;	#$running_under_some_shell

use strict;
use File::Find ();

use vars qw/*name *dir *prune/;
*name = *File::Find::name;
*dir = *File::Find::dir;
*prune = *File::Find::prune;

sub wanted;

Fild::Find::find({wanted => \&wanted}, '.');
exit;

sub wanted {
	/^.*\.pm\z/s
	&& print ("$name\n");
}
```

## Manipulating Files and Directories

```perl

# unlink -- remove files
unlink 'slate', 'bedrock', 'lava';	# same as `rm slate bedrock lava` in shell
unlink glob '*.o';

foreach my $file (qw(slate bedrock lava)) {
	unlink $file or warn "Failed on $file: $!\n";
}

# Renaming Files
rename 'old', 'new';
rename 'over_there/some/place/some_file' => 'some_file';	
```

## Links and Files

Each file is stored in a numbered *inode*. A directory is a table of filenames and their inode numbers. Each inode holds a number called its *link count*. The link count is always 0 if the inode isn't listed in any directory

Use the Perl *link* function to create a new link:

```perl
# the same as `ln chicken egg` in shell
link 'chicken', 'egg' or warn "Can't link chicken to egg: $!";
```

Another restriction is that you can't add links to directories. There is a way to get around these restrictions on links, by using a new and different kind of link: **symbolic link**:

```perl
# the same as `ln -s dodgson carroll` in shell
symlink 'dodgson', 'carroll'
	or warn "can't symlink dodgson to carroll: $!";

my $where = readlink 'carroll';	# gives "dodgson"
```

## Making and Removing Directories

```perl
mkdir 'fred', 0755 or warn "Cannot make fred directory: $!";

my ($name, $perm) = @ARGV;
mkdir $name, oct($perm) or die "Cannot create $name: $!";	# use a number instead of a string

# the rmdir operator fails for nonempty directories
# for a more robust solution, check out the rmtree function provided by 
# the File::Path module of the standard distribution
foreach my $dir (qw(fred barney betty)) {
	rmdir $dir or warn "Cannot rmdir $dir: $!\n";
}
```

## Permissions, Ownership, and Timestamps

```perl
chmod 0755, 'fred', 'barney';

my $user = 1004;
my $group = 100;
chown $user, $group, glob '*.o';

defined(my $user = getpwnam 'merlyn') or die 'bad user';
defined(my $group = getpwnam 'users') or die 'bad group';
chown $user, $group, glob '/home/merely/*';

my $now = time;
my $ago = $now- 24*60*60;	# seconds per day
utime $now, $ago, glob '*';	# set access to now, mod to a day ago
```

# Chapter 14 Strings and Sorting

```perl
my $stuff = "Howdy world!";
my $where = index($stuff, "wor");	# find a substring with index, 0-base
my $where2 = index($stuff, "w", $where+1);	

my $last_slash = rindex("/etc/passwd", "/");	# search from the end of the string

my $part = substr($string, $initia_position, $length);
my $pebble = substr "Fred j. Flinstone", 13;	# gets "stone"
my $out = substr("some very long string", -3, 2);	# count from the end of the string
```

## Formatting Data with sprintf

```perl
my $data_tag = sprintf "%4d/%02d/%02d %2d:%02d:%02d", $yr, $mo, $da, $h, $m, $s;
```

## Advanced Sort

```perl
# You don't have to do anything in the sort subroutine to declare $a and $b
sub by_number {
	if ($a < $b) {-1} elsif ($a > $b) {1} else {0}
}

my @result = sort by_number @some_numbers;

# a simpler way
sub by_number { $a <=> $b }

# a corresponding three-way string comparison operator: cmp
sub by_code_point { $a cmp $b }

my @strings = sort by_code_point @any_strings;

# case-insensitive sort:
sub case_insensitive { "\L$a" cmp "\L$b" }

# dealing with Unicode string
use Unicode::Normalize;

sub equivalents { NFKD($a) cmp NFKD($b) }

# $a and $b aren't copies of the data items. They're actually new, temporary aliases
# for elements of the original list. Don't change them
# a simpler way:
my @numbers = sort { $a <=> $b } @some_numbers;
```

## Sorting a Hash by value

```perl

# You can't sort a hash, but when you used sort with hashes, you sorted the keys of the hash.
my %score = ("barney"=>195, "fred"=>205, "dino"=>30);
sub by_score { $score{$b} <=> $score{$a} }
my @winners = sort by_score keys %score;

# first compare value then if the values are equal then compare the keys
sub by_score_and_name {
	$score{$b} <=> $score{$a}
		or
	$a cmp $b
}
```

# Smart Matching and given-when

## The Smart Match Operator

```perl

# the smart match operator ~~: If the operands look like numbers, it does a numeric comparison
# If they look like strings, it does a string comparison
# If one of the operands is a regular expression, it does a pattern match

use 5.010001;	# at least 5.10.1
# at least one key in the hash matches the regular expression
say "I found a key matching 'Fred'" if %names ~~ /Fred/;


# two arrays are equal
use 5.010001;

say "The arrays have the same elements!"
	if @name1 ~~ @names2;


# a scalar is in an array 
use 5.010001;
my @nums = qw(1 2 3 27 42);
my $result = max(@nums);
say "The result [$result] is one of the input values (@nums)"
	if @nums ~~ $result;
```

## The given Statement

```perl

# the same as C's switch. There is an implicit break at the end of each when block
use 5.010001;

given ($ARGV[0]) {
	when ('Fred') { say 'Name is Fred'; continue }	# the same as when ($_ ~~ 'Fred'), smart match 
	when (/fred/i) { say 'Name has fred in it'; continue }
	when (/\AFred/) { say 'Name starts with Fred' }
	default		{ say "I don't see a Fred" }
}

# You can also use dumb match

use 5.010001;

given ($ARGV[0]) {
	when ( $_ eq 'Fred') { say 'Name is Fred'; continue }	# the same as when ($_ ~~ 'Fred'), smart match 
	when ( $_ =~ /fred/i) { say 'Name has fred in it'; continue }
	when ( $_ =~ /\AFred/) { say 'Name starts with Fred' }
	default		{ say "I don't see a Fred" }
}
```

## Using when with Many Items

```perl

# to go through many elements, you don't need the given
use 5.010001;

foreach (@names) {
	when ('Fred') { say 'Name is Fred'; continue }	# the same as when ($_ ~~ 'Fred'), smart match 
	when (/fred/i) { say 'Name has fred in it'; continue }
	when (/\AFred/) { say 'Name starts with Fred' }
	default		{ say "I don't see a Fred" }
}
```

# Chapter 16 Process Management

## The system Function

```perl

# When the command is simple enough, no shell gets involved.
# But if there's anything weird in the string, Perl invokes the standard Bourne Shell to work through the complicated stuff.
# In that case, the shell is the child process, and the requested commands are grandchildren

system 'date';
system 'ls -l $HOME';
```

## The Environment Variables

```perl
# The environment variables are available via the special %ENV hash

$ENV{'PATH'} = "/home/rootbeer/bin:$ENV{'PATH'}";
delete $ENV{'IFS'};
my $make_result = system 'make';
```

## The exec Function

```perl

# suppose you wanted to run the bedrock command in the /tmp directory,
# passing it arguments of -o args1 followed by whatever arguments your own program was invoked with
# When you reach the exec operation, Perl locates bedrock and 'jump into it', at that point, there is no Perl process any more
chdir '/tmp' or die "Cannot chdir /tmp: $!";
exec 'bedrock', '-o' 'args1', @ARGV;
```

## Using Backquotes to capture output

```perl

# avoid using backquotes if you don't need return value. Just use system instead
my $now = `date`;
print "The time is now $now";

# Instead of the backquotes, you can also use the generalized quoting operator, qx()
foreach (@functions) {
	$about{$_} = qx(perldoc -t -f $_);
}

# Backquotes in a list context
my $who_text = `who`;
my @who_lines = split /\n/,

my @who_lines = `who`;	# same as above

foreach (`who`) {
	my ($user, $tty, $date) = /(\S+)\s+(\S+)\s+(.*)/;
	$ttys{$user} .= "$tty at $date\n";
}
```

## Getting Down and Dirty with Fork

```perl
# the same as system `date`
defined (my $pid = fork) or die "Cannot fork: $!";
unless ($pid) {
	# Child process is here
	exec 'date';
	die "Cannot exec date: $!";
}
# parent process is here
waitpid($pid, 0);
```

## Sending and Receiving Signals

```perl
my $temp_directory = "/tmp/myprog.$$";
mkdir $temp_directory, 0700 or die "Cannot create $temp_directory: $!";

sub clean_up {
	unlink glob "$temp_directory/*";
	rmdir $temp_directory;
}

sub my_int_handler {
	&clean_up();
	die "interrupted, exiting...\n";
}

$SIG{'INT'} = 'my_int_handler';	#signal handler

&clean_up();
```

# Chapter 17 Some Advanced Perl Techniques

```perl
# suppose the input file looks like this:
# fred flinstone:2168:301 Cobblestone Way:555-1212:555-2121:3
# barney rubble:709913:3128 Granite Blvd:555-3333:555-3438:0

while (<$fh>) {
	chomp;
	my @items = split /:/;
	my ($card_num, $count) = ($items[1], $items[5]);
}

my ($name, $card_num, $addr, $home, $work, $count) = split /:/;	# you don't need the array @items

my (undef, $card_num, undef, undef, undef, $count) = split /:/;	

my $card_name = (split /:/)[1];
my $count = (split /:/)[5];
my (card_num, $count) = (split /:/)[1,5];

my ($first, $last) = (sort @names)[0, -1];	# -1 means the last element

# Array slice

my @names = qw{ zero one two three four five six seven eight nine };
print "Bedrock @names[9,0,2,1,0]\n";	# get the 9th, 0th, ... element 

# Hash Slice 

my @three_scores = ($score{"barney"}, $score{"fred"}, $score{"dino"});
my @three_scores = @score{ qw/ barney fred dino /};
```

## Trapping Errors

```perl
# eval won't crash the program.
use 5.010;
my $barney = eval {$fred/$dino};	//'NaN' if $dino is 0
print "I couldn't divide by \$dino: $@" if $@;	//put the error message in the $@ variable

# Try::Tiny module, not included in the Standard Library, you can get it from CPAN

use Try::Tiny;

try {
	$fred/$dino;	
}
catch {
	say "Error was $_";	# not $@
}
finally {
	# the finally block runs in either case: if there is an error or not. 
	# If it has arguments in @_, there was an error 
	say @_ ? 'There was an error': 'Everything worked';
}

# autodie

use autodie;

open my $fh, '>', $filename;	# If this fails, you get the error message.

# You can specify which operators you apply autodie in the import list
use autodie qw( open system :socket);
```

## Picking Items from a list with grep

```perl
my @odd_numbers = grep { $_ % 2 } 1..1000;	# get odd numbers
my @matching_lines = grep { /\bfred\b/i } <$fh>;
my $line_count = grep /\bfred\b/i, <$fh>;	# get line count
```

## Transforming Items from a list with map

```perl
my @data = (4.75, 1.5, 2, 1234, 6.9456, 12345678.9, 29.95);
my @formatted_data = map { $big_money($_) } @data;
```

## List Utilities

```perl

use List::Util qw(first);
my $first_match = first { /\bPebbles\b/i } @characters;	# get first match

use List::Util qw(sum);
my $total = sum(1..1000);	# 500500

use List::Util qw(max);
my $max = max(3,5,10,4,6);

use List::Util qw(maxstr);
my $max = maxstr(@strings);

use List::Util qw(shuffle);
my @shuffled = shuffle(1..1000);	# randomized order of elements
```
