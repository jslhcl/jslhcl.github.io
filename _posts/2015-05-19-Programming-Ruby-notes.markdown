---
layout:	post
title:	"Programming Ruby notes"
tag: 笔记
date:	2015-05-19
---

# Chapter 1 Getting started

RVM: Ruby Version Manager, lets you have multiple independent Ruby installations on the same machine.

irb: Interactive Ruby

```Ruby
$ irb
2.0.0 :001 > def sum(n1, n2)
2.0.0 :002?>     n1+n2
2.0.0 :003?>     end
=> nil
```

Ruby Documentation: RDoc and ri

ri ClassName

```Ruby
$ ri GC
```

# Chapter 2 Ruby.new

```Ruby
puts "gin joint".length	# 9
puts "Rick".index("c")	# 2
puts 42.even?		# true

def say_goodnight(name)	# indentation is not significant; parentheses are optional
	result = "Good night, " + name	# equivalent: result = "Good night, #{name}"
	return result
end

puts say_goodnight("John-Boy")	# equivalent: puts(say_goodnight("John-Boy"))
puts say_goodnight("Mary-Ellen")
```

The value returned by a Ruby method is the value of the last expression evaluated

```Ruby
def say_goodnight(name)
	"Good night, #{name.capitalize}"
end
puts say_goodnight('ma')	# Good night, Ma
```

## Arrays and Hashes

```Ruby
a = [1, 'cat', 3.14]
puts "The first element is #{a[0]}"

a[2] = nil
puts "The array is now #{a.inspect}"	# [1, 'cat', nil]

a = %w{ant bee cat dog elk}
a[0] 	# "ant"
a[3] 	# "dog"

inst_section = {
	'cello' => 'string',
	'clarinet' => 'woodwind',
	'drum'	=> 'percussion',
	'oboe'	=> 'woodwind',
	'trumpet'	=> 'brass',
	'violin'	=> 'string'
}

p inst_section['oboe']	# "woodwind"
p inst_section['basson']	# nil

histogram = Hash.new(0)
histogram['ruby']	# 0
histogram['ruby'] = histogram['ruby']+1

```

## Symbols

Symbols are simply constant names that you don't have to predeclare and that are guaranteed to be unique. A symbol literal starts with a colon and is normally followed by some kind of name

```Ruby
inst_section = {
	:cello => 'string',
	:clarinet => 'woodwind',
	:drum	=> 'percussion',
	:oboe	=> 'woodwind',
	:trumpet	=> 'brass',
	:violin	=> 'string'
}
```

symbols are so frequently used as hash keys that Ruby has a short syntax:

```Ruby
inst_section = {
	cello:  'string',
	clarinet:  'woodwind',
	drum:	 'percussion',
	oboe:	 'woodwind',
	trumpet:	 'brass',
	violin:	 'string'
}

p inst_section[:cello]
```

## Control Structures

Most statements in Ruby return a value, which means you can use them as conditions. 

```Ruby
while line = gets	# gets returns the next line from the standard input stream or nil when the end of the file is reached.
	puts line.downcase
end
```

statement modifiers

```Ruby
if radiation > 3000
	puts "Danger, Will Robinson"
end

# equivalent:
puts "Danger, Will Robinson" if radiation > 3000

square = 4 
while square < 1000
	square = square*square
end

# equivalent:
square = square*square while square < 1000
```

## Regular Expression

```Ruby
/Perl.*Python/	# Perl, zero or more other chars, then Python
/Perl\s+Python/	# Perl, whitespace characters, then Python
```

## Blocks and Iterators

code blocks, which are chunks of code you can associate with method invocations, almost as if they were parameters.

```Ruby
def call_block
	puts "Start of method"
	yield
	yield
	puts "End of method"
end

call_block { puts "In the block" }

# produces:
# Start of method
# In the block
# In the block
# End of method

def who_says_what
	yield("Dave", "hello")
	yield("Andy", "goodbye")
end

who_says_what { |person, phrase| puts "#{person} says #{phrase}"}

# produce:
# Dave says hello
# Andy says goodbye

[ 'cat', 'dog', 'horse' ].each {|name| print name, " "}
5.times { put "*" }
3.upto(6) { |i| print i }
('a'..'e').each { |char| print char }
puts	# cat dog horse *****3456abcde
```

## Reading and Writing

```Ruby
while line = gets	# gets returns nil when it reaches the end of input
	print line
end
```

## Command-line Arguments

```Ruby
puts "You gave #{ARGV.size} arguments"
p ARGV
```

# Chapter 3 Classes, Objects, and Variables

```Ruby
class BookInStock
	attr_reader :isbn, :price	# create accessor methods
	attr_accessor :price	# if you want both a reader and a writer for a given attribute
	def initialize(isbn, price)
		@isbn = isbn	# instance variable
		@price = Float(price)
	end
	def to_s
		"ISBN: #{@isbn}, price: #{@price}"
	end

	def price_in_cents
		Integer(price*100+0.5)
	end

	def price_in_cents=(cents)	# make this "virtual attribute" writable
		@price = cents/100.0
	end

end

b2 = BookInStock.new("isbn2", 3.14)
p b2	# <BookInStock:0x007fac... @isbn="isbn2", @price=3.14>
puts b2	# ISBN: isbn2, price: 3.14

puts "Price in cents = #{b2.price_in_cents}"	# Price in cents = 314
b2.price_in_cents = 1234
puts "Price = #{b2.price}"	# Price = 12.34
puts "Price in cents = #{b2.price_in_cents}"	# Price in cents = 1234

## csv_reader.rb
require 'csv'
require_relative 'book_in_stock'

class CsvReader
	def initialize
		@books_in_stock = []
	end

	def read_in_csv_data(csv_file_name)
		CSV.foreach(csv_file_name, header:true) do |row|	# headers:true option tells the library to parse the first line of the file as teh names of the columns
			@books_in_stock << BookInStock.new(row["ISBN"], row["Price"])
		end
	end

	def total_value_in_stock
		sum = 0.0
		@book_in_stock.each {|book| sum += book.price}
		sum
	end
end

## stock_stats.rb
require_relative 'csv_reader'

reader = CsvReader.new

ARGV.each do |csv_file_name|
	STDERR.puts "Processing #{csv_file_name}"
	reader.read_in_csv_data(csv_file_name)
end

puts "Total value= #{reader.total_value_in_stock}"
```

## Specifying Access Control

```Ruby
Class MyClass
	def method1	# default is 'public'
	#...
	end

	protected	# subsequent methods will be 'protected'
	def method2	
	#...
	end

	private
	def method3	# subsequent methods will be 'private'
	#...
	end

	public		# subsequent methods will be 'public'
	def method4
	#...
	end
end

# Alternatively,

Class MyClass
	def method1
	end
	def method2
	end
	def method3
	end
	def method4
	end
	#...

	public: method1, method4
	protected: method2
	private: method3
end
```

## Variables

```Ruby
person = "Tim"
puts "The object in 'person' is a #{person.class}"	# The object in 'person' is a String
puts "The object has an id of #{person.object_id}"
puts "and a value of #{person}"	# and a value of 'Tim'
```

A variable is simply a reference to an object.

```Ruby
person1 = "Tim"
person2 = person1
person1[0] = 'J'

puts "#{person1}"	# Jim
puts "#{person2}"	# Jim

person1 = "Tim"
person2 = person1.dup
person1[0] = "J"
puts "#{person1}"	# Jim
puts "#{person2}"	# Tim

person1 = "Tim"
person2 = person1
person1.freeze	# prevent modifications to the object
person2[0] = "J"	# raise a RuntimeError exception
```

# Chapter 4 Containers, Blocks and Iterators

## Arrays

```Ruby
a = [3.14, "pie", 99]
a.class # => Array
a.length # => 3
b = Array.new

a = [1,3,5,7,9]
a[1,3] # => [3, 5, 7]  ([start, count])
a[-3, 2] # => [5, 7]

a[1..3] #=> [3,5,7]
a[1...3] # => [3, 5]	([start..end] and [start...end))

a = [1,3,5,7,9]
a[3] = [9,8]	#=> [1,3,5,[9,8],7,9]
a[1,1] = [9,8,7] # => [1,9,8,7, 5,[9,8],7,9]

stack = []
stack.push "red"
stack.push "green"
stack	# => ["red", "green"]
stack.pop # => "green"

queue = []
queue.push "red"
queue.push "green"
queue.shift	# => "red"
```

## Example: Word Frenquency

```Ruby
## words_from_string.rb
def words_from_string(string)
	string.downcase.scan(/[\w']+/)	# lowercase, then matches sequences containing "word characters" and single quotes
end

## count_frequency.rb
def count_frequency(word_list)
	counts = Hash.new(0)
	for word in word_list
		counts[word] += 1
	end
	counts
end

## entry point
require_relative "words_from_string.rb"
require_relative "count_frequency.rb"

raw_text = %{the problem ...}

word_list = words_from_string(raw_text)
counts = count_frequency(word_list)
sorted = counts.sort_by{|word, count| count}
top_five = sorted.last(5)

## Unit test
require_relative 'words_from_string'
require 'test/unit'

class TestWordsFromString < Test::Unit::TestCase
	def test_single_word	# any methods whose names start with "test" are automatically run by the testing framework
		assert_equal(["cat"], words_from_string(" cat "))
	end
	def test_many_words
		assert_equal(["the","cat","sat","on","the","mat"], words_from_string("the cat sat on the mat"))
	end
end
```

## Blocks and Iterators

```Ruby
top_five.each do |word, count|	# the method "each" is an iterator that invokes a block of code repeatedly
	puts "#{word}: #{count}"
end

# Alternatively
puts top_five.map {|word, count| "#{word}: #{count}"}
```

A Block is a chunk of code enclosed between either braces or the keywords "do" and "end". You can think of a block as being somewhat like the body of an anonymous method. Just like a method, the block can take parameters

```Ruby
some_array.each {|value| puts value*3}  # parameter: value

sum = 0
other_array.each do |value|	# parameter: value
	sum += value
	puts value/sum
end
```

A Ruby iterator is simply a method that can invoke a block of code.

Within the method, the block may be invoked, almost as if it were a method itself, using the yield statement. Whenever a yield is executed, it invokes the code in the block. When the block exits, control picks back up immediately after the yield.

you can pass parameters to them and receive values from them.

```Ruby
def fib_up_to(max)
	i1, i2 = 1,1
	while i1 <= max
		yield i1
		i1, i2 = i2, i1+i2
	end
end

fib_up_to(1000) { |f| print f, " " }	# 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
```

iterator "find" returns the first corresponding element if the block returns true

```Ruby
[1,3,5,7,9].find { |v| v*v > 30 }	# 7
``` 

iterator "collect" takes each element from the collection and passes it to the block

```Ruby
["H", "A", "L"].collect{|x| x.succ}	# ["I", "B", "M"]
```

with_index: like "enumerate" in Python

```Ruby
f = File.open('testfile')
f.each.with_index do |line, index|
	puts "Line #{index} is: #{line}
end
f.close

# ouput:
# Line 0 is: xxx
# Line 1 is: xxx
```

inject

```Ruby
[1,3,5,7].inject {|sum, element| sum+element}	# 16
[1,3,5,7].inject {|product, element| product*element}	# 105

[1,3,5,7].inject(:+)	# 16
[1,3,5,7].inject(:*)	# 105
```

## Enumerators -- External Iterators

```Ruby
a = [1,3,"cat"]
h = {dog: "canine", fox: "vulpine"}

enum_a = a.to_num
enum_h = h.to_num

enum_a.next # 1
enum_h.next # [:dog, "canine"]
enum_a.next # 3
enum_h.next # [:fox, "vulpine"]

short_enum = [1,2,3].to_enum
long_enum = ('a'...'z').to_enum

loop do
	puts "#{short_enum.next} - #{long_enum.next}"
end

# output
# 1 - a
# 2 - b
# 3 - c
```

the "Enumerable" module defines each_with_index. This invokes its host class's each Method, returning successive values along with an index:

```Ruby
['a', 'b', 'c'].each_with_index {|item, index| result << [item, index]}
result	# [["a", 0], ["b", 1], ["c", 2]] 

result = []
"cat".each_char.with_index{|item, index| result << [item, index]}
result	# [["c", 0], ["a", 1], ["t", 2]]
``` 

Enumerators Are Generators and Filters, Lazy Enumerators in Ruby 2 ??

```Ruby
class File
	def self.open_and_process(*args)	# collect the actual parameters passed to the method into an array named args
		f = File.open(*args)
		yield f
		f.close()
	end
end

File.open_and_process("testfile", "r") do |file|
	while line = file.gets
		puts line
	end
end

class File
	def self.my_open(*args)
		result = file = File.new(*args)
		# If there's a block, pass in the file and close the file when it returns
		if block_given?	# returns true if a block is associated with the current method
			result = yield file
			file.close
		end
		result
	end
end 	
```

## Blocks Can Be Objects

If the last parameter in a method definition is prefixed with an ampersand (&action), Ruby looks for a code block whenever that method is called. That code block is converted to an object of class Proc and assigned to the parameter.

```Ruby
class ProcExample
	def pass_in_block(&action)
		@store_proc = action
	end
	def use_proc(parameter)
		@store_proc.call(parameter)
	end
end

eg = ProcExample.new
eg.pass_in_block { |param| puts "The parameter is #{param}" }
eg.use_proc(99)	# The parameter is 99
```

It's a great way of implementing callbacks, dispatch tables and so on.

## Blocks Can Be Closures

```Ruby
def n_times(thing)	# Even though that parameter is out of scope by the time the block is called, the parameter remains accessible to the block. This is called a closure
	lambda { |n| thing*n }
end

p1 = n_times(23)
p1.call(3)	# => 69
p1.call(4)	# => 92
p2 = n_times("Hello ")
p2.call(3)	# => "Hello Hello Hello "

def power_proc_generator
	value = 1
	lambda { value += value }
end

power_proc = power_proc_generator

puts power_proc.call
puts power_proc.call
puts power_proc.call

# produces:
# 2
# 4
# 8
```

## An Alternative Notation

Ruby has another way of creating Proc objects. Rather than write this:

```Ruby
lambda { |params| ... }
```

you can now write the following:

```Ruby
->params { ... }
```

```Ruby
proc1 = ->arg {puts "In proc1 with #{arg}" }
proc2 = ->arg1, arg2 {puts "In proc2 with #{arg1} and #{arg2}"}
proc3 = ->(arg1, arg2) { puts "In proc3 with #{arg1} and #{arg2}"}

proc1.call "ant"
proc2.call "bee", "cat"
proc3.call "dog", "elk"


def my_if (condition, then_clause, else_clause)
	if condition
		then_clause.call
	else
		else_clause.call
	end
end

5.times do |val|
	my_if val<2,
	      -> {puts "#{val} is small"}
	      -> {puts "#{val} is big"}
end

# produces:
# 0 is small
# 1 is small
# 2 is big
# 3 is big
# 4 is big
# 5 is big

def my_while(cond, &body)
	while cond.call
		body.call
	end
end

a = 0

my_while -> {a<3} do
	puts a
	a += 1
end

# produces:
# 0
# 1
# 2
```

## Block Parameter Lists

```Ruby
proc1 = lambda do |a, *b, &block|
	puts "a=#{a.inspect}"
	puts "b=#{b.inspect}"
	block.call
end
proc1.call(1,2,3,4) {puts "in block1"}

# produces:
# a=1
# b=[2,3,4]
# in block1

# using the new -> notation
proc2 = -> a,*b, &block do
	puts "a=#{a.inspect}"
	puts "b=#{b.inspect}"
	block.call
end
```

# Chapter 5 Sharing Functionality: Inheritance, Modules, and Mixins

```Ruby
class Parent
	def say_hello
		puts "Hello from #{self}"
	end
end

## Subclass the parent
class Child < Parent
end

Child.superclass # => Parent
Parent.superclass # => Object
Object.superclass # => BasicObject
BasicObject.superclass # => nil
```

## Mixins

A module can't have instance, because a module isn't a class. However, you can include a module within a class definition. When this happens, all the module's instance methods are suddenly available as methods in the class as well. They get *mixed in*.

```Ruby
module Debug
	def who_am_i?
		"#{self.class.name} (id:#{self.object_id}): #{self.name}"
	end
end

class Phonograph
	include Debug
	attr_reader :name
	def initialize(name)
		@name = name
	end
	#...
end

class EightTrack
	include Debug
	attr_reader :name
	def initialize(name)
		@name = name
	end
	#...
end

ph = Phonograph.new("West End Blues")
et = EightTrack.new("Surrealistic Pillow")
ph.who_am_i?
et.who_am_i?
```

The Ruby *include* statement simply makes a reference to a module. If that module is in a separate file, you must use *require* to drag that file in before using *include*. Second, a Ruby *include* does not simply copy the module's instance methods into the class. Instead, it makes a reference from the class to the included module. If multiple classes include that module, they'll all point to the same thing.

```Ruby
class Person
	include Comparable
	attr_reader :name

	def initialize(name)
		@name = name
	end
	def to_s
		"#{@name}"
	end
	def <=>(other)	# Comparable assumes that any class that uses it defines the operator <=>; get six comparison (<,<=,==,>=,>) functions for free
		self.name <=> other.name
	end
end

p1 = Person.new("Matz")
p2 = Person.new("Guido")
p3 = Person.new("Larry")

if p1 > p2
	puts "#{p1.name}'s name > #{p2.name}'s name"
end

puts "Sorted list:"
puts [p1, p2, p3].sort
```

In general, a mixin that requires its own state is not a mixin -- it should be written as a class

## Resolving Ambiguous Method Names

Ruby looks first in the immediate class of an object, then in the mixins included into that class, and then in superclass and their mixins.

# Chapter 6 Standard Types

Ruby includes support for rational and complex numbers

```Ruby
Rational(3,4) * Rational(2,3)	# => (1/2)
Rational("3/4") * Rational("2/3")	# => (1/2)

Complex(1,2) * Complex(3,4)	# => (-5+10i)
Complex("1+2i") * Complex("3+4i")	# => (-5+10i)
```

Strings that contain just digits are not automatically converted into numbers

```Ruby
3 4
5 6
7 8

some_file.each do |line|
	v1, v2 = line.split
	print v1+v2, " "
end	# 34 56 78

some_file.each do |line|
	v1, v2 = line.split
	print Integer(v1)+Integer(v2), " "
end	# 7 11 15
```

## How Numbers Interact

```Ruby
22/7	# => 3
Complex::I * Complex::I	# => (-1+0i)

require 'mathn'
22/7	# => (22/7)
Complex::I * Complex::I	#=> -1

3.times	{ print "X " }
1.upto(5)	{ |i| print i, " " }
99.downto(95)	{ |i| print i, " " }
50.step(80, 5)	{ |i| print i, " " }	# X X X 1 2 3 4 5 99 98 97 96 95 50 55 60 65 70 75 80

10.downto(7).with_index { |num, index| puts "#{index}: #{num}" }
# 0: 10
# 1: 9
# 2: 8
# 3: 7
```

## Strings

You can substitute the value of any Ruby code into a string using the sequence #{expr}

```Ruby
"Seconds/day: #{24*60*60}"	# => Seconds/day: 86400
"Safe level is #$SAFE"		# => Safe level is 0
```

## Working with Strings

```Ruby
Song = Struct.new(:title, :name, :length)

File.open("songdata") do |song_file|
	songs = []
	
	song_file.each do |line|
		file, length, name, title = line.chomp.split(/|s*|||s*/)
		songs << Song.new(title, name, length)
	end
	
	puts songs[1]
end

"2:58".split(/:/)	# => ["2", "58"]

Song = Struct.new(:title, :name, :length)

File.open("songdata") do |song_file|
	songs = []
	
	song_file.each do |line|
		file, length, name, title = line.chomp.split(/|s*|||s*/)
		name.squeeze!(" ")
		mins, secs = length.scan(/\d+/)
	end
	
	puts songs[1]
end

```

## Ranges

The two-dot form creates an inclusive range, and the three-dot form creates a range that excludes the specified high value

```Ruby
1..10
'a'..'z'
0..."cat".length
```

You can convert a range to an array using the to_a method and convert it to an Enumerator using to_enum

```Ruby
(1..10).to_a	# => [1,2,3,4,5,6,7,8,9,10]
('bar'..'bat').to_a	# => ["bar", "bas", "bat"]
enum = ('bar'..'bat').to_num
enum.next	# => "bar"
enum.next	# => "bas"
```

seeing whether some value falls within the interval represented by the range: 

```Ruby
(1..10) === 5	# => true
(1..10) === 15	# => false
(1..10) === 3.14159	# => true
('a'..'j') === 'c'	# => true
('a'..'j') === 'z'	# => false
```

# Chapter 7 Regular Expression

By far the most common is to write it between forward slashes. =~ returns the character offset into the string at which the match occured

```Ruby

/cat/ =~ "dog and cat"	# => 8
/cat/ =~ "catch"	# => 0
/cat/ =~ "Cat"		# => nil

str = "cat and dog"
if str =~ /cat/
	puts "There's a cat here somewhere"
end

File.foreach("testfile").with_index do |line, index|
	puts "#{index}: #{line}" if line !~ /on/	# !~ means does not match a string
end

# sub method replaces the matched substring with the replaced text

str = "Dog and Cat"
new_str = str.sub(/Cat/, "Gerbil")
puts "Let's go to the #{new_str} for a pint"

# To replace all matches, use gsub (the g stands for global)

str = "Dog and Cat"
new_str1 = str.gsub(/a/, "*")
puts "Using gsub: #{new_str1}"

# Both sub and gsub returns a new string. If you want to modify the original string, use the sub! and gsub! forms:

str = "now is the time"
str.sub!(/i/, "*")
puts str 
```

## Matching Against Patterns

```Ruby
# $& receives the part of the string that was matched by the pattern
# $` receives the part of the string that preceded the match 
# $' receives the string after the match

def show_regexp(string, pattern)
	match = pattern.match(string)
	if match
		"#{match.pre_match}->#{match[0]}<-#{match.post_match}"
	else
		"no match"
	end
end

show_regexp('very interesting', /t/)	# => very in->t<-eresting
show_regexp('Fats Waller', /lle/)	# => Fats Wa->lle<-r
show_regexp('Fats Waller', /z/)		# => no match
```

## Anchors

```Ruby
# ^ and $ match the beginning and the end of a line
# \A matches the beginning of a string,
# \z and \Z matches the end of a string (\Z matches the end of a string unless the string ends with \n)
# \b and \B match word boundaries and nonword boundaries, respectively

# repetition
# r* Matches zero or more occurrences of r
# r+ Matches one or more occurrences of r
# r? Matches zero or one occurrence of r
# r{m,n} Matches at least m and at most n occurrences of r
# r{m,} Matches at least m occurrences of r
# r{,n} Matches at most n occurrences of r
# r{m} Matches exactly m occurrences of r
```

# Chapter 8 More About Methods

Methods that return a boolean result are often named with a trailing ?.

Methods that modify their receiver may be named with a trailing exclamation mark (!).

Our convention is to use parentheses when a method has arguments and omit them when it doesn't 

Ruby lets you specify default values for a method's arguments

```Ruby
def cool_dude(arg1="Miles", arg2="Coltrane", arg3="Roach")
	"#{arg1}, #{arg2}, #{arg3}"
end

cool_dude	# => "Miles, Coltrane, Roach"
cool_dude("Bart")	# => "Bart, Coltrane, Roach"
```

Variable-Length Arguments List

```Ruby
def varargs(arg1, *rest)
	"arg1=#{arg1}. rest=#{rest.inspect};
end

varargs("one")	# arg1=one. rest=[]
varargs "one", "two", "three"	# arg1=one. rest=["two", "three"]

# If you care only about the first and the last parameters, you could define the method:
# def split_apart(first, *, last)
def split_apart(first, *splat, last)
	puts "First: #{first.inspect}, splat: #{splat.inspect}, last: #{last.inspect}"
end

split_apart(1,2)		# First: 1, splat: [], last: 2
split_apart(1,2,3,4)	# First: 1, splat: [2,3], last: 4 
```

if the last parameter in a method definition is prefixed with &, any associated block is converted to a Proc object, and that object is assigned to the parameter. This allows you to store the block for use later.

```Ruby
class TaxCalculator
	def initialize(name, &block)
		@name, @block = name, block
	end
	def get_tax(amount)
		"#@name on #{amount} = #{@block.call(amount)}"
	end
end

tc = TaxCalculator.new("Sales tax") { |amt| amt*0.075 }
tc.get_tax(100)		# => "Sales tax on 100 = 7.5"
tc.get_tax(250)		# => "Sales tax on 250 = 18.75"
```

Every method you call returns a value. The value of a method is the value of the last statement executed by the method.

## Splat! Expanding Collections in Method Calls

```Ruby
def five(a, b, c, d, e)
	"I was passed #{a} #{b} #{c} #{d} #{e}"
end

five(1, 2, 3, 4, 5)		# " I was passed 1 2 3 4 5"
five(*['a', 'b'], 1, 2, 3)		# "I was passed a b 1 2 3"
five(*(10..14))			# " I was passed 10 11 12 13 14
```

## Making Blocks More Dynamic

```Ruby
print "(t)imes or (p)lus: "
operator = gets
print "number: "
if operator =~ /^t/
		calc = lambda {|n| n*number}
else
		calc = lambda {|n| n+number}
end
# if the last argument to a method is preceded by an ampersand, Ruby assumes that it is a Proc object.
puts ((1..10).collect(&calc).join(", "))	 

# produces:
(t)imes or (p)lus: t
number: 2
2, 4, 6, 8, 10, 12, 14, 16, 18, 20
```

## Keyword Argument List

```Ruby
# new in Ruby 2.0
def search(field, options)
	option = {duration: 120}.merge(options)
	if options.has_key?(:duration)
			duration = options[:duration]
			options.delete(:duration)
	end
	if options.has_key?(:genre)
			genre = options[:genre]
			options.delete(:genre)
	end
	fail "Invalid options: #{options.key.join(', ')}" unless options.empty?
end

# You can collect these extra hash arguments as a hash parameter--prefix one element of your argument list with two asterisk
def search(field, genre: nil, duration: 120, **rest)
	p [field, genre, duration, rest]
end

search(:title, duration: 432, star: 3, genre: "jazz", tempo: "slow")
# produces: [:title, "jazz", 432, {:stars=>3, :tempo=>"slow"}]
```

# Chapter 9 Expressions

## Redefine backquotes

```Ruby
alias old_backquote `
def ` (cmd)
	result = old_backquote(cmd)
	if $? != 0
			puts "*** Command #{cmd} failed: status = #{$?.exitstatus}"
	end
	result
end

print `ls -l /etc/passwd`
print `ls -l /etc/wibble`
```

## Parallel Assignment

```Ruby
a, b = 1, 2
a, b = b, a	# swap

*a, b = 1, 2, 3, 4	# a=[1,2,3], b=4
c, *d, e = 1,2,3,4	# c = 1, d = [2,3], e=4
first, *, last = 1,2,3,4,5,6	# first=1, last=6
```

## Conditional Execution

```Ruby

# and, or and not
nil && 99	# nil
false && 99	# false
"cat" && 99	# 99

nil || 99	# 99
false || 99	# 99
"cat" || 99	# "cat"

# defined? returns nil if its argument is not defined
defined? l	# "expression"
defined? Math::PI	# "constant"
defined? 42.abs		# "method"
defined? dummy		# "nil"

# if and unless

if artist == "Gillespie"	# "then" is optional if the statements are on multiple lines 
		handle = "Dizzy"
elsif artist == "Parker"
		handle = "Bird"
else
		handle = "Unknown"
end

# must separate the boolean expression from the following statements with "then"
if artist == "Gillespie" then handle = "Dizzy"
elsif artist == "Parker" then handle = "Bird"
else  handle = "Unknown"

# unless
unless duration > 180
	listen_intently
end

# C-style
cost = duration>180 ? 0.35 : 0.25

# case Expression
case line
when /title=(.*)/
	puts "Title is #$1"
when /track=(.*)/
	puts "Track is #$1"
end
```

## Loops

```Ruby
# until
until play_list.duration > 60
	play_list.add(song_list.pop)
end

a = 1
a *= 2	while a < 100
a 		# => 128
a -= 10 unless a < 100
a		# => 98

# this is perl style. gets assigns the last line read to the global variable $_
# the ~ operator does a regular expression match against $_
# This kind of code is falling out of fashion in the Ruby community and may end up being removed from the language
file = File.open("ordinal")
while file.gets
		print if ~/third/ .. ~/fifth/
end

# $. contains the current input line number
File.foreach ("ordinal") do |line|
	if (($. == 1)||line=~/eig/) .. (($. == 3)||line=~ /nin/)
			print line
	end
end

# grep
File.open("ordinal").grep(/d$/) do |line|
	puts line
end

for i in File.open("ordinal").find_all {|line| line =~ /d$/}
	print i.chomp, " "
end

# As long as your class defines a sensible each method, you can use a for loop to traverse its objects:
class Periods
	def each
		yield "Classical"
		yield "Jazz"
		yield "Rock"
	end
end

periods = Periods.new
for genre in periods
		print genre, " "
end
# produces: Classical Jazz Rock

# break, redo and next
while line = gets
		next if line =~ /^\s*#/	# like continue in C
		break if line =~ /^END/	# like break in C
		redo if line.gsub!(/`(.*?)`/) {eval ($1)}	# repeat the current iteration
end
```

## Variable Scope, Loops, and Blocks

```Ruby
x = "initial value"
y = "another value"
[1,2,3].each do |x|
	y = x+1
end
[x, y] # => ["initial value", 4]
```

# Chapter 10 Exceptions, catch, and throw

```Ruby
require 'open-uri'
page = "podcasts"
file_name = "#{page}.html"
web_page = open("http://progprog.com/#{page}")
output = File.open(file_name, "w")

begin	# raise an exception in begin/end block 
	while line = web_page.gets
			output.puts line
	end
	output.close
rescue Exception	# handle exception
	STDERR.puts "Failed to download #{page}: #{$!}"	# place a reference to the associated exception object into $!
	output.close
	File.delete(file_name)
	raise	# reraise the exception in $!, passing on those you can't handle to higher levels
else	# executed only if no exceptions are raised 
	puts "Congratulations -- no errors!"
ensure
	# ensure is similar with final in C++, always will be executed
end

# give Ruby the name of a local variable to receive the matched exception
# more readable than using $!
begin 
	eval string
rescue SyntaxError, NameError => boom
	print "String doesn't compile: " + boom
rescue StandardError => bang
	print "Error running Script: " + bang
end
```

## play it again

```Ruby
# first, connect to an SMTP server using EHLO command;
# if the connection attempt fails, sets the @esmtp to false and retries the connection
# If it fails a second time, the exception is raised up to the caller
begin 
	# First try an extended login. If it fails, fall back to a normal login
	if @esmtp then @command.ehlo(helodom)
			else   @command.helo(helodom)
	end
rescue ProtocolError
	if @esmtp then
			@esmtp = false
			retry
	else
			raise
	end
end
```

## Raising Exceptions

```Ruby
raise "Missing name" if name.nil?

if i>=names.size
		raise IndexError, "#{i} >= size (#{names.size})"
end

raise ArgumentError, "Name too big", caller
```

## Adding Information to Exeptions

```Ruby
class RetryException < RuntimeError
	attr :ok_to_retry
	def initialize(ok_to_retry)
		@ok_to_retry = ok_to_retry
	end
end

def read_data(socket)
	data = socket.read(512)
	if data.nil? 
			raise RetryException.new(true), "transient read error"
	end
	# .. normal processing
end 

begin 
	stuff = read_data(socket) 
	# .. process stuff
rescue RetryException => detail 
	retry if detail.ok_to_retry
	raise
end
```

## Catch and throw

```Ruby

# if any of the lines of the file doesn't contain a valid word, we want to abandon the whole process
word_list = File.open("wordlist")
word_in_error = catch(:done) do
	result = []
	while line = word_list.gets
			word = line.chomp
			# the second parameter of throw is the return value of the catch 
			# without the second parameter to throw, the catch returns nil 
			throw(:done, word) unless word =~ /^\w+$/
			result << word 
	end
	puts result.reverse
end

if word_in_error
		puts "Failed: ' #{word_in_error}' found, but a word is expected"
end

# produces: '*wow*' found, but a word is expected

# the throw does not have to appear within the static scope of the catch
def prompt_and_get(prompt)
	print prompt
	res = readline.chomp
	throw :quit_requested if res == "!"
	res
end

catch :quit_requested do
	name = prompt_and_get("Name: ")
	age = prompt_and_get("Age: ")
	sex = prompt_and_get("Sex: ")
	# ..
end
	
```

# Chapter 11 Basic Input and Output

```Ruby
# IO#each_byte invokes a block with the next 8-bit byte from the IO object
# chr converts an integer to the corresponding ASCII character
File.open("testfile") do |file|
	file.each_byte.with_index do |ch, index|
		print #{ch.chr}:#{ch} "
		break if index > 10
	end
end

# produces: T:84 h:104 i:105 s:115

# IO#each_line calls the block with each line from the file
File.open("testfile") do |file|
	file.each_line { |line| puts "Got #{line.dump}" }
end

# you can pass a parameter to each_line as the line separator
# in the following example, the line separator is "e" instead of "\n"
File.open("testfile") do |file|
	file.each_line("e") { |line| puts "Got #{line.dump}" }
end


IO.foreach("testfile") { |line| puts line }

# read into string
str = IO.read("testfile")
str.length 	# => 66
str[0,30]	# substring indexed from 0 to 30

# read into an array
arr = IO.readlines("testfile")
arr.length 	# => 4
arr[0]

# write to files
File.open("output.txt", "w") do |file|
	file.puts "Hello"
	file.puts "1+2= #{1+2}"
end

# Doing I/O with Strings
require 'stringio'

ip = StringIO.new("now is\nthe time\nto learn\nRuby!")
op = StringIO.new("", "w")
ip.each_line do |line|
	op.puts line.reverse
end
op.string	# reverse the string line by line
```

## Talking to Networks

```Ruby
require 'socket'

client = TCPSocket.open('127.0.0.1', 'www')
client.send("OPTIONS /~dave/ HTTP/1.0\n\n", 0)
puts client.readlines
client.close

# higher level
require 'net/http'
http = Net::HTTP::new('progprog.com', 80)
response = http.get('book/ruby3/programming-ruby-1-9')

if response.message == "OK"
		puts response.body.scan(/<img alt=".*?" src="(.*?)"/m).uniq[0,3]
end

# higher level
require 'open-uri'

open('http://progprog.com') do |f|
	puts f.read.scan(/<img alt=".*?" src="(.*?)"/m).uniq[0,3]
end

# Parsing HTML
require 'open-uri'
page = open('http://progprog.com/titles/ruby3/programming-ruby-1-9').read
if page =~ %r{<title>(.*?)</title>}m
		puts "Title is #{$1.inspect}"
end

# use the popular Nokogiri lib
require 'open-uri'
require 'nokogiri'

doc = Nokogiri::HTML(open("http://progprog.com"))
puts "Page title is " + doc.xpath("//title").inner_html

# output the first paragraph in the div with an id="copyright"
puts doc.css('dvi#copyright p')

# output the second hyperlink in the site-links div using xpath and css
puts "nSecond hyperlink is"
puts doc.xpath('id("site-links")//a[2]')
puts doc.css('#site-links a:nth-of-type(2)')
```

# Chapter 12 Fibers, Threads and Process

## Fibers

Ruby's fibers are just a very simple coroutine mechanism. 

In the following code, the constructor for the Fiber class takes a block and returns a fiber object

Subsequently, we can call resume on the fiber object. This causes the block to start execution
```Ruby
words = Fiber.new do
	File.foreach("testfile") do |line|
		line.scan(/\w+/) do |word|
			Fiber.yield word.downcase
		end
	end
	nil
end

counts = Hash.new(0)
while word = words.resume
		counts[word] += 1
end
counts.keys.sort.each {|k| print "#{k}: #{counts[k]}"}	
```

## Multithreading

Prior to Ruby 1.9, these were implemented as green thread--threads were switched within the interpreter. In Ruby 1.9, threading is now performed by the operating system. 

It uses native operating system threads but operates only a single thread at a time. You'll never see two threads in the same application running Ruby code truely concurrently.

```Ruby
require 'net/http'

pages = %w( www.rubycentral.org slashdot.org www.google.com)

threads = pages.map do | page_to_fetch|
	Thread.new (page_to_fetch) do |url|
		http = Net::HTTP.new(url, 80)
		print "Fetching: #{url}\n"
		resp = http.get('/')
		print "Got #{url}: {resp.message}\n"
	end
end
threads.each{|thr| thr.join}
```

## Thread Variables

```Ruby
count = 0
threads = 10.times.map do |i|
	Thread.new do 
		sleep(rand(0.1))
		Thread.current[:mycount] = count
		count += 1
	end
end

threads.each { |t| t.join; print t[:mycount], ", " }
puts "count = #{count}"
```

## Mutual Exclusion

```Ruby
sum = 0
mutex = Mutex.new
threads = 10.times.map do
	Thread.new do 
		100_000.times do
			mutex.lock	# one at a time
			new_value = sum+1
			print "#{new_value} " if new_value % 250_000 == 0
			sum = new_value
			mutex.unlock
		end
	end
end

threads.each(&:join)
puts "\nsum=#{sum}"

# Mutex#synchronize ensures that the mutex will get unlocked even if an exception is thrown while it is locked
sum = 0
mutex = Mutex.new
threads = 10.times.map do
	Thread.new do 
		100_000.times do
			mutex.synchronize do	
				new_value = sum+1
				print "#{new_value} " if new_value % 250_000 == 0
				sum = new_value
				mutex.unlock
			end
		end
	end
end

# Mutex#try_lock takes the lock if it can, but returns false if the lock is already taken.
# If you want to claim a lock if a mutex is currently unlocked, but you don't want to suspend the current thread if it isn't
rate_mutex = Mutex.new
exchange_rates = ExchangeRates.new
exchange_rates.update_from_online_feed

Thread.new do
	loop do
		sleep 3600
		rate_mutex.synchronize do 
			exchange_rates.update_from_online_feed
		end
	end
end

loop do
	print "Enter currency code and amount: "
	line = gets
	if rate_mutex.try_lock
			puts(exchange_rates.convert(line)) ensure rate_mutex.unlock
	else
			puts "Sorry, rates being updated. Try again in a minute"
	end
end

# If you are holding the lock on a mutex and you want to temporarily unlock it, allowing others to use it, 
# you can use Mutex#sleep
rate_mutex = Mutex.new
exchange_rates = ExchangeRates.new
exchange_rates.update_from_online_feed

Thread.new do
	rate_mutex.lock
	loop do
		rate_mutex.sleep 3600
		rate_mutex.synchronize do 
			exchange_rates.update_from_online_feed
		end
	end
end

loop do
	print "Enter currency code and amount: "
	line = gets
	if rate_mutex.try_lock
			puts(exchange_rates.convert(line)) ensure rate_mutex.unlock
	else
			puts "Sorry, rates being updated. Try again in a minute"
	end
end

```

## Running Multiple Processes

```Ruby
# Spawn new Process, invoke system API, executes the command in a subprocess
system("tar xzf test.tgz")
`date`

# the popen method runs a command as a subprocess and connects that subprocess's standard input and 
# standard output to a Ruby IO object
pig = IO.popen("local/util/pig", "w+")
pig.puts "ice cream after they go to bed"
pig.close_write
puts pig.gets 

# Blocks and Subprocesses
IO.popen("date") {|f| puts "Date is #{f.gets}"}
```

# Chapter 13 Unit Testing

```Ruby
require_relative 'romanbug'
require 'test/unit'

class TestRoman < Test::Unit::TestCase
	def test_simple
		assert_equal("i", Roman.new(1).to_s)
		assert_equal("ix", Roman.new(9).to_s)
	end
end
```

# Chapter 14 When Trouble Strikes

## Ruby Debugger

```Ruby
# command: ruby -r debug <debug-options> <programfile> <program-arguments>
$ ruby -r debug t.rb
```

## Benchmark, time section of code

```Ruby
require 'benchmark'
include Benchmark

LOOP_COUNT = 1_000_000

bmbm(12) do |test|
	test.report("inline:") do
		LOOP_COUNT.times do |x|
			#nothing
		end
	end
	test.report("method":) do
		def method
			#nothing
		end
		LOOP_COUNT.times do |x|
			method
		end
	end
end
```

## The profiler

You can add profiling to your code using the command-line option *-r profile*

# Chapter 15 Ruby and Its World

## Command-Line Arguments

If no filename is present on the command line or if the filename is a single hyphen (-), Ruby reads the program source from the standard input 

```Ruby
# test.rb
ARGV.each {|arg| p arg}

# command line
$ ruby -w test.rb "Hello World" a1 1.6180

# output: "Hello World" "a1" "1.6180"

# ARGV[0] is the first argument to the program, not the program name
# program name is available in the global variable $0, which is aliased to $PROGRAM_NAME 

# ARGF
while line = gets
	printf "%d: %10s[%d] %s", ARGF.lineno, ARGF.filename, ARGF.file.lineno, line
end

$ ruby copy.rb testfile otherfile
1:  testfile[1] This is line one
2:  testfile[2] This is line two
3: otherfile[1] ANOTHER LINE ONE
```

## In-place Editing

```Ruby
# reverse.rb
while line = gets
		puts line.chomp.reverse
end

# command line, testfile and otherfile would now have reversed lines,
# and that the original files would be available in testfile.bak and otherfile.bak
$ ruby -i.bak reverse.rb testfile otherfile
```

## Environment Variables

You can access operating system environment variables using the predefined variable ENV

```Ruby
ENV['SHELL']
ENV['HOME']
ENV.keys.size
```

## The Rake Build Tool

Ruby version of Make

```Ruby
# put the following code into a file called Rakefile
desc "Remove files whose names end with a tilde"
task :delete_unix_backups do
	files = Dir['*~']
	rm(files, verbose: true) unless files.empty?
end

# we can invoke this task from the command line
$ rake delete_unix_backups

# we can also compose tasks
desc "Remove Unix and Windows backup files"
task :delete_backups => [:delete_unix_backups, :delete_windows_backups] do
	puts "All backups deleted"
end
```

# Chapter 17 Character Encoding

If the first line of the file is a comment (or the second line if the first line is a #! shebang line), Ruby scans it looking for the string *coding:*. Thus, to specify that a source file is in UTF-8 encoding, you can write this:

```Ruby
# coding: utf-8
```

As Ruby is just scanning for *coding:*, you could also write the following

```Ruby
# encoding: ascii
```

The String#bytes method is a convenient way to inspect the bytes in a string object. Notice that in the following code, the 16-bit codepoint is converted to a two-byte UTF-8 encoding:

```Ruby
# encoding: utf-8
"pi: \u03c0".bytes"	# => [112, 105, 58, 32, 207, 128]
``` 

You can force the external encoding associated with an I/O object when you open it

```Ruby
f = File.open("/etc/passwd", "r:ascii")
puts "File encoding is #{f.external_encoding"}"
line = f.gets
puts "Data encoding is #{line.encoding}"

# produces:
# File encoding is US-ASCII
# Data encoding is US-ASCII
```

If all your files are written with ISO-8859-1 encoding but you want your program to have to deal with their content as if it were UTF-8, you can use this:

```Ruby
ruby -E iso-8859-1:utf-8

# or you can specify just an internal encoding
ruby -E :utf-8
```

# Chapter 18 Interactive Ruby Shell

load a file into irb

```Ruby
ruby 2.0 > load 'code/irb/fibonacci_sequence.rb'
```

# Chapter 20 Ruby and the Web

## CGI

```Ruby
require 'cgi'
puts CGI.escape("Nicholas Payton/Trumpet & Flugel Horn") # Nicholas+Payton%2FTrumpet+%26+Flugel+Horn

puts CGI.escapeHTML("a<100 && b>200")	# a&lt;100 &amp;&amp; b&gt;200

# escape only certain HTML elements within a string:
CGI.escapeElement('<hr><a href="/mp3">Click Here</a></hr>', 'A')
# (only <a...> is escaped)<hr>&lt;a href=&quot;/mp3&quot;&gt;Click Here&lt;/a&gt;<br>  

# unescape html:
# CGI.unescapeHTML(...)
```

## Query Parameters

```Ruby
<html>
	<head>
		<title>Test Form</title>
	</head>
	<body>
		<p>I like Ruby because:</p>
		<form action="cgi-bin/survey.rb">
			<p>
				<input type="checkbox" name="reason" value="flexible" />
				It's flexible
			</p>
			<p>
				<input type="checkbox" name="reason" value="transparent" />
				It's transparent
			</p>
			<p>
				<input type="checkbox" name="reason" value="perlish" />
				It's like Perl
			</p>
			<p>
				<input type="checkbox" name="reason" value="fun" />
				It's fun
			</p>
			<p>
				Your name: <input type="text" name="name" />
			</p>
			<input type="submit" />
		</form>
	</body>
</html>

require 'cgi'
cgi = CGI.params # {"name"=>["Dave Thomas"], reason=["flexible", ..., "transparent", "fun"]
cgi.params['name']
cgi.params['reason']
```

## erb and eruby

embed Ruby in an HTML document

## Cookies

```Ruby
#!/usr/bin/ruby
require 'cgi'

COOKIE_NAME = 'chocolate chip'

cgi = CGI.new
values = cgi.cookies[COOKIE_NAME]

if values.empty?
	msg = "It looks as if you haven't visited recently"
else
	msg = "You last visited #{values[0]}"
end

cookie = CGI::Cookie.new(COOKIE_NAME, Time.now.to_s)
cookie.expires = Time.now + 30*24*3600	# 30 days
cgi.out("cookie" => cookie) {msg}
```

## Sessions

```Ruby
require 'cgi'
require 'cgi/session'

cgi = CGI.new("html4")
sess = CGI::Session.new(cgi, "session_key" => "rubyweb", "prefix" => "web-session.")

if sess['lastaccess']
	msg = "<p>You were last here #{sess['lastaccess']}.</p>"
else
	msg = "<p>Looks like you haven't been here for a while</p>"
end

count = (sess["accesscount"] || 0).to_i
count += 1

msg << "<p>Number of visits: #{count}</p>"

sess["accesscount"] = count
sess["lastaccess"] = Time.now.to_s
sess.close

cgi.out {
		cgi.html {
				cgi.body {
						msg
				}
		}
}
```

## web server

```Ruby
#!/usr/bin/ruby

require 'webrick'
include WEBrick

# set the document root to be the html/ subdirectory of the current directory
# s = HTTPServer.new(Port: 2000, DocumentRoot: File.join(Dir.pwd, "/html")
s = HTTPServer.new(Port: 2000)

class HelloServlet < HTTPServlet::AbstractServlet
	def do_GET(req, res)
		res['Content-Type'] = "text/html"
		res.body = %{
				<html><body>
					<p>Hello. You're calling from a #{req['User-Agent']}</p>
					<p>I see paremeters: #{req.query.keys.join(', ')}</p>
				</body></html>}
	end
end

# mount a simple servlet at the location /hello
s.mount("/hello", HelloServlet)
# shut down on interrupts
trap("INT"){s.shutdown}
s.start	
```

# Chapter 21 Ruby and Microsoft Windows

```Ruby
# create a new WIN32OLE client that launches a fresh copy of IE and visit its home page
# and navigate to a new page
require 'win32ole'
ie = WIN32OLE.new('InternetExplorer.Application')
ie.visible = true
ie.gohome
ie.navigate("http://www.pragprog.com")
# properties
ie.Height = 300
```

## build into OpenOffice suite to create a spreadsheet and populate some cells

```Ruby
class OOSpreadsheet
	def initialize
		mgr = WIN32OLE.new('com.sun.star.ServiceManager')
		desktop = mgr.createInstance("com.sun.star.ServiceManager")
		@doc = desktop.LoadComponentFromUrl("private:factory/scalc", "_blank", 0, [])
		@sheet = @doc.sheets[0]
	end

	def get_cell(row, col)
		@sheet.getCellByPosition(col, row, 0)
	end

	def get_cell_range(tl_row, tl_col, br_row, br_col)
		@sheet.getCellRangeByPosition(tl_row, tl_col, br_row, br_col, 0)
	end
end

spreadsheet = OOSpreadsheet.new
cell = spreadsheet.get_cell(1, 0)
cell.Value = 1234

cells = spreadsheet.get_cell_range(1,2,5,3)
cols = cells.Columns.count
rows = cells.Rows.count

cols.times do |col_no|
	rows.times do |row_no|
		cell = cells.getCellByPosition(col_no, row_no)
		cell.Value = (col_no+1)*(row_no+1)
	end
end
```

## Events

```Ruby
require 'win32ole'

urls_visited = []
running = true

def default_handler(event, *args)
	case event
	when "BeforeNavigate"
		puts "Now Navigating to #{args[0]}..."
	end
end

ie = WIN32OLE.new('InternetExplorer.Application')
ie.visible = TRUE
ie.gohome
ev = WIN32OLE_EVENT.new(ie, 'DWebBrowserEvents')

ev.on_event {|*args| default_handler(*args)}
ev.on_event ("NavigateComplete") {|url| urls_visited << url}
ev.on_event ("Quit") do |*args|
	puts "IE has quit"
	puts "You Navigated to the following URLs: "
	urls_visited.each_with_index do |url, i|
		puts "(#{i+1}) #{url}"
	end
	running = false
end

# hang around processing messages
WIN32OLE_EVENT.message_loop while running
```

# Chapter 22 The Ruby language

## General Delimited Input (New in 2.0)

```Ruby
%i{ one digit#{1+1} three } #=> [:one, :"digit\#{1+1}", :three], array of symbols
%I{ one digit#{1+1} three } #=> [:one, :"digit2", :three]
%q{ one digit#{1+1} three } #=> " one digit\#{1+1} three "
%Q{ one digit#{1+1} three } #=> " one digit2 three "
%w{ one digit#{1+1} three } #=> [ "one", "digit\#{1+1}", "three"]
%W{ one digit#{1+1} three } #=> [ "one", "digit2", "three"]

# Just like Perl!!
%q/this is a string/
%q-string-
%q(a (nested) string)
```

## String

```Ruby
# Adjacent single- and double-quoted strings are concatenated to form a single String object
'Con' "cat" 'en' "ate"	#=> "Concatenate"
```

## Name

```Ruby
# an instance variable name starts with an @
# @name  @_  @size

# a class variable name starts with two @
# @@name  @@_  @@size
# Class variables are inherited by children but propagated upward if first defined in a child 

# global variables, and some special system variables, start with a $
# $params  $PROGRAM  $!  $_
```
