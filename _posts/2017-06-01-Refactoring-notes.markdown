---
layout:	post
title:	"Refactoring"
date:	2017-06-01
---
# Chapter 2 Principles in Refactoring

## The Rule of Three

The first time you do something, you just do it. The second time you do something similar, you wince at the duplication, but you do the duplicate thing anyway. The third time you do something similar, you refactor. 

# Chapter 3 Bad Smells in Code

## Long Method

Whenever we feel the need to comment something, we write a method instead. Such a method contains the code that was commented but is named after the intention of the code rather than how it does it.

How do you identify the clumps of code to extract? A good techique is to look for comments. A block of code with a comment that tells you what it is doing can be replaced by a method whose name is based on the comment. Even a single line is worth extracting if it needs explanation. 

## Comments

If you need a comment that explain what a block of code does, try *Extract Method*. If the method is already extracted but you still need a comment to explain what it does, use *Rename Method*. If you need to state some rules about the required state of the system, use *Introduce Assertion*. 

A good time to use a comment is when you don't know what to do. In addition to describing what is going on, comments can indicate areas in which you aren't sure. A comment is a good place to say *why* you did something.

# Chapter 4 Building Tests

When you get a bug report, start by writing a unit test that exposes the bug.

# Chapter 6 Composing Methods

## Replace Temp with Query

The problem with temps is that they are temporary and local. Because they can be seen only in the context of the method in which they are used, temps tend to encourage longer methods, because that's the only way you can reach the temp.

# Chapter 7 Moving Features Between Objects

## Extract Class

(Extract Class) A good sign is that a subset of the data and a subset of the methods seem to go together. Other good signs are subsets of data that usually change together or are particularly dependent on each other. A useful test is to ask yourself what would happen if you removed a piece of data or a method. What other fields and methods would become nonsense?

# Chapter 8 Organizing Data

## Change value to Reference

*Reference objects* are things like customer or account. Each object stands for one object in the real world, and you use the object identity to test whether they are equal. *Value objects* are things like date or money. They are defined entirely through their data values. You don't mind that copies exists; you may have hundreds of "1/1/2000" objects around your system. You do need to tell whether two of the objects are equal, so you need to override the equals method.

(P183) An important property of value objects is that they should be immutable. Any time you invoke a query on one, you should get the same result. ... If the value is mutable, you have to ensure that changing any object also updates all the other objects that represent the same thing. That's so much of a pain that the easiest thing to do is to make it a reference object.

If you have a money class with a currency and a value, ... That does not mean your salary cannot change. It means that to change your salary, you need to replace the existing money object with a new money object rather than changing the amount on an existing money object. 

## Encapsulate Collection

A method returns a collection. *Make it return a read-only view and provide add/remove methods*.

The getter should not return the collection object itself, because that allows clients to manipulate the contents of the collection without the owning class's knowing what is going on. It also reveals too much to clients about the object's internal data structures.

# Chapter 10 Making Method Calls Simpler

## Encapsulate Downcast

{% highlight Java %}
Object lastReading() {
        return readings.lastElement();
}
{% endhighlight %}

=>

{% highlight Java %}
Reading lastReading() {
        return (Reading)readings.lastElement();
}
{% endhighlight %}

If you return a value from a method, and you know the type of what is returned is more specialized than what the method signature says, you are putting unnecessary work on your clients. Rather than forcing them to do the downcasting, you should always provide them with the most specific type you can.
