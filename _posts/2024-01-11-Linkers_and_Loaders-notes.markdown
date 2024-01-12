---
layout:	post
title:	"Linkers & Loaders"
tag: 笔记
date:	2024-1-11
---

# Ch1 Linking and Loading

(P5) Linkers and loaders perform several actions:

- *program loading*: copy program from secondary storage into main memory, others involves allocating storage, map virtual addresses to disk pages.
- *Relocation*: Compilers and assemblers generally create each file of object code with the program addresses starting at zero, Relocation is the process of assigning load addresses to the various parts of the program and adjusting the code and data in the program to reflect the assigned addresses.
- *Symbol resolution*: A linker resolves the symbol by noting the location of the assigned to some function in the library and patching the caller's object code

It's reasonable to define a program that does program loading as loader, and one that does symbol resolution as a linker. Either can do relocation.

(P6) Some symbols are exported - defined within the file for use in other files, other symbols are imported - used in the file but not defined.

(P8) (for Shared libraries) the linker notes in the output file the names of the (shared) libraries in which the symbols were found, so that the shared library can be bound in when the program is loaded.

# Ch2 Architectural Issues

(P23) If the value in the register is the address of a storage area, and the constant in the instruction is the offset of the desired datum in the storage area, this scheme is known as *based* addressing. If the roles are swapped and the register contains the offset, the scheme is known as *indexed* addressing.

(P40) all the code in shared libraries is usually PIC(position independent code)

# Ch3 Object Files

(P67) ELF extends this facility (shebang) to interpreters that run nontext programs.

(P82) It (Thread local storage, TLS) is usually present in EXE but not DLL files, because MS Windows doesn't allocate TLS when a program dynamically links to a DLL.

# Ch4 Storage Allocation

(P102) (Initializers and Finalizers) The usual approach is for each object file to put any startup code into an anonymous routine and to put a pointer to that routine into a segment called .init or something similar. The linker concatenates all the .init segments together, thereby creating a list of pointers to all the startup routines.

(P103) The definition of C++ states that application-level constructors are run in an unpredicatable order, but the I/O and other system library constructors need to be run before constructors in C++ applications are called. The "perfect" approach would be for each .init routine to list its dependencies explicitly and to do a topological sort.

# Ch5 Symbol Management

(P129) A strong reference must be resolved; a weak reference may be resolved if there is a definition, but it's not an error if it's not defined.

# Ch10 Dynamic Linking and Loading

(P211) The linker looks in the library cache file /etc/ld.so.conf, which contains a list of library names and paths. If the library name is present, it uses the corresponding path.

(P216) Although the ELF dynamic linker is usually called implicitly at program load time and from PLT entries, programs can also call it explicitly using **dlopen**() to load a shared library and **dlsym**() to find the address of a symbol, which is usually a procedure to call.

(P221) MS Windows also permits programs to load and unload DLLs explicitly using **LoadLibrary** and **FreeLibrary** and to find addresses of symbols using **GetProcAddress**.
