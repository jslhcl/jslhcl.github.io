---
layout:	post
title:	"C/C++ - Weak Symbols"
tag: 编程
date:	2023-12-29
---

When I learned C++ at the very beginning, I was told that a function cannot be defined in multiple .cpp files as you will get the "foo already defined" error. However, the functions can be defined as inline functions in header files which can be included in multiple .cpp files. The included header files will expand their content into .cpp files, then why there won't be "multiple definition of ..." error? 

The reason is that the inline function will be compiled as weak symbol, which are allowed to have 0 or more definitions. Suppose you have the following files:

```cpp
// test2.h
void API_Func();
void non_exist_func();

inline void func() {
        non_exist_func();
}

// test2.cpp
#include "test2.h"

void API_Func() {
        func();
}
``` 

Compile these files into a shared library:

```bash
$ g++ test2.cpp -shared -o libtestInline.so
$ readelf -s libtestInline.so   # or use objdump or nm
...
    50: 0000000000001149    16 FUNC    WEAK   DEFAULT   12 _Z4funcv
    53: 0000000000000000     0 NOTYPE  GLOBAL DEFAULT  UND _Z14non_exist_funcv
    54: 0000000000001139    16 FUNC    GLOBAL DEFAULT   12 _Z8API_Funcv
```

You can see that "func", which is decorated as inline, is mangled as weak symbol , "API\_Func" is a global symbol, "non\_exist\_func" is also global but NOTYPE, as it is not defined.

The next example demonstrates "multiple definition" of weak symbol is not an issue:

```cpp
// test3.h
void non_exist_func();
void API3_func();

inline void func() {
}

// test3.cpp
#include "test3.h"

void non_exist_func() {
        int a = 3;
}

void API3_func() {
        func();
}

// main.cpp
void API_Func();
void API3_func();

int main() {
        API_Func();
        API3_func();
        return 0;
}
``` 

Build test3 as shared library and link with main:

```bash
$ g++ -g test3.cpp -shared -o libtest3.so
$ g++ -g main.cpp -L. -ltestInline -ltest3 -o testMain.out
$ readelf -s libtest3.so
...
    50: 000000000000113b    11 FUNC    WEAK   DEFAULT   12 _Z4funcv
    53: 0000000000001119    18 FUNC    GLOBAL DEFAULT   12 _Z14non_exist_funcv
    54: 000000000000112b    16 FUNC    GLOBAL DEFAULT   12 _Z9API3_funcv
$ export LD_LIBRARY_PATH=./
$ ./testMain.out    
$
```

Now we can see:
1. libtestInline.so has no dependency on libtest3.so, although there is a function definition in libtest3.so but referenced in libtestInline.so
2. the weak symbol "func" has been defined in both shared libraries, but it doesn't matter when running with main.

The next question is: which code will be built as symbol (to be continued...)
