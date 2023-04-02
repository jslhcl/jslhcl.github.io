---
layout:	post
title:	"CLR via C#"
tag: 笔记
date:	2016-12-27
---

# Chapter 1 The CLR's Execution Model

## parts of a Managed Module (P5, table 1-1)

PE32 or PE32+ header:   similar to the Common Object File Format(COFF) header

CLR header:             major minor version, flags, strong-name signature, etc

Metadata:               definition tables, reference tables, manifest tables

IL code

# Chapter 2 Building, Packaging, Deploying, and Administrering Applications and Types

## Assembly

Assembly contains mutiple PE file, one of the PE file contains manifest

Visual Studio doesn't support to create multifile assemblies. Have to use command line tool to create them

To build a new assembly, all of the files from a referenced assembly must be present; to run an application, all of the files from a referenced assembly do not need to be present

# Chapter 3 Shared Assemblies and Strongly Named Assemblies

## Deploy

Strong named assembly: has public and private key as signature, Can be deployed Globally (in GAC (Global Assembly Cache) folder C:\Windows\Microsoft.NET\assembly) and privately (in application's folder)

Weakly named assembly: can only be deployed privately (See P67, Table 3-1)

## GAC

gacutil.exe /i: install an assembly; /u: uninstall an assembly; /r: tells the system which application requires the assembly and then ties the application and the assembly together

MSI (Windows Installer), another tool to install assembly in GAC, just like gacutil.exe

Two copies of Microsoft's assembly files are installed when you install .Net Framework. One is installed into the compiler/CLR directory (for build your assembly), the other is installed into the GAC directory (loaded at runtime). Assemblies in the compiler/CLR directory contain only metadata in them, because IL code is not required at build time. The assemblies in the GAC can be fine-tuned for a specific CPU architecture.

When an application needs to bind to an assembly in runtime, first it will search the GAC folder, if cannot find, then CLR looks in the application's base directory, then in any of the private paths, then, if the application was installed using MSI, the CLR asks MSI to locate the assembly, then bind fails and a System.IO.FileNotFoundException is thrown.

When strongly named assembly files are loaded from a location other than the GAC, a hash of the file is performed every time an application executes and loads the assembly. Assembly in GAC won't be hashed so it will be faster. 

# Chapter 4 Type Fundamentals

Figure 4-13

Each object has a Type object Ptr, it points to the actual type of that object. 

Type object itself is also an object, its Type object Ptr points to System.Type type object.

System.Type type object's Type object Ptr points to itself.

# Chapter 5 Primitive, Reference and Value Types

Figure 5-2 Visualizing the memory as the code executes

struct allocate on stack
