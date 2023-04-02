---
layout:	post
title:	"The Art Of Unix Programming notes"
tag: 笔记
date:	2016-07-17
---

# Chapter 1. Basics of the Unix philosophy

Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming.

## Rule of transparency: Design for visibility to make inspection and debugging easier.

At minimum, it implies that debugging options should not be minimal afterthoughts. Rather, they should be designed in from the beginning.

## Rule of Representation: Use smart data so program logic can be stupid and robust

Data is more tractable than program logic. It follows that where you see a choice between complexity in data structures and complexity in code, choose the former.

# Chapter 4. Modularity

## API design

there are two properties that Unix programmers have learned to think very hard about when designing APIs, command sets, protocols and other ways to computers do tricks:

### Compactness

Very few software designs are compact in an absolute sense, but many are compact in a slightly looser sense of the term. They have a compact working set, a subset of capabilities that suffices for 85% or more of what expert users normally do with them. Practically speaking, such designs normally need a reference card or a cheat sheet but not a manual.

The Unix system call API is compact but the standard C library is not. While Unix programmers easily keep a subset of the system calls sufficient for most applications programming (filesystem operations, signals, and process control) in their heads, the C library on modern Unixes includes many hundreds of entry points for, e.g. mathematical functions, that won't all fit a single programmer's cranium.

### Orthogonality

In a purely orthogonal design, operations do not have side effects; each action changes just one thing without affecting others. There is one and only one way to change each property of whatever system you are controlling.

*Perfection in design is attained not when there is nothing more to add, but when there is nothing more to remove*

## Unix and object-oriented language

The OO design concept initially proved valuable in the design of graphics systems, graphical user interfaces, and certain kinds of simulation.

It has proved hard to demonstrate significant benefits of OO outside those areas.

Unix tradition of modularity is one of thin glue, a minimalist approach with few layers of abstraction between the hardware and the top-level objects of a program.

OO languages make abstraction easy -- perhaps too easy. They encourage architectures with thick glue and elaborate layers.

All OO languages show some tendency to suck programmers into the trap of excessive layering. 

Another side-effect of OO abstraction is that opportunities for optimization tend to disappear. For example, a+a+a+a can become a\*4 and even a<<2 if a is an integer. But if one creates a class with operators, there is nothing to indicate if they are commutative, distributive, or associative. Since one isn't supposed to look inside the object.

In GUIs and graphics, for example, there is generally a rather natural mapping between manipulable visual objects and classes.

# Chapter 20. Futures

## Problems in the Design of Unix

A Unix File is Just a Big Bag of Bytes

Unix Support for GUIs Is Weak

File Deletion is Forever

Unix Assumes a Static File System

The Design of Job Control Was Badly Botched

The Unix API Doesn't Use Exceptions

ioctl(2) and fcntl(2) Are an Embarrassment

The Unix Security Model May Be Too Primitive

Unix Has Too Many Different Kinds Of Names

File Systems Might Be Considered Harmful
