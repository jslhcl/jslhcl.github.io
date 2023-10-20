---
layout:	post
title:	"C/C++ - Common Errors and Solutions"
tag: 编程
date:	2023-10-20
---

Use this post to record typical C/C++ errors, reasons and solutions

# 1. C++, `unordered_map`, "attempting to reference a deleted function"

If you are using `unordered_map` and complicated class/struct as key: 

```cpp
std::unordered_map<COMPLICATED_CLASS, int> m;
```

Reason: there are some restrictions on the key for `unordered_map`, which is, it must can be hashed. As `unordered_map` is using the key's hash value when organizing the key-value pair

Solution: provide your customized hash function and comparison function when your construct `unordered_map`: 

```cpp
std::unordered_map<Key,T,Hash,KeyEqual,Allocator>::unordered_map
```

Or use std::map if you don't care about performance.

# 2. Const pointer/reference/member function

Const pointer or reference can only invoke const member function

Inside const member function, it seems to implicitly cast all referred variables to const. which means:

1. non-const variables are read only
2. can only access other const member functions (as class pointers/references are cast to const) 

# 3. Segment fault Error:

a common reason is a reference is attached to a temporary variable, or dereference an uninitialized pointer, or null pointer reference.

# 4. Undefined Symbol Error:

If library A is calling another function defined in library B, make sure library A (static or dynamic) links library B. Otherwise there will be this error for the calling function.

# 5. 

Suppose you have a shared library (lib.so), you want to expose some API (functions, classes) for 3rd party library to use:

## Solution 1:

```cpp
// public header plugin.h, which will be accessed and included in 3rd party library

class InternalClass2;
class API {
public:
    API(InternalClass2 *p) : internal_class(p) {}
    void func_API1();
private:
    InternalClass2* internal_class;
};

class API2 {    // This class is left for 3rd party developer to inherit
public:
    virtual void func_API2(API* api1) {
        // This function is left for 3rd party developer to override
    }
};

// internal file APIImpl.cpp which is invisible to 3rd party library

#include "plugin.h"

void API::func_API1() {
    internal_class->someFunc();
}

class API_Wrapper : public InternalClass {
    virtual void func(InternalClass2* p) override {
        API* api = new API (p);
        api2->func_API2(api);
    }
private:
    API2* api2;
};

```

In this way, external user cannot instantiate API class as InternalClass2 is not exposed to public (so API class instance can only be created inside lib.so), and lib.so have to expose the symbol of the function `func_API1()`

## Solution 2:

```cpp
// public header plugin.h, which will be accessed and included in 3rd party library

class APIInterface {
public:
    virtual void func_API1() = 0;
};

class API2 {    // This class is left for 3rd party developer to inherit
public:
    virtual void func_API2(APIInterface* api) {
        // This function is left for 3rd party developer to override
    }
};

// internal file APIImpl.cpp which is invisible to 3rd party library

#include "plugin.h"

class APIInterfaceImpl : public APIInterface {
private:
    const InternalClass2& internal_class;
public:
    APIInterfaceImpl(const InternalClass2& internal) : internal_class(internal) {}
    void func_API1() override {
        internal_class.someFunc();
    }
};

class API_Wrapper : public InternalClass {
    virtual void func(InternalClass2* p) override {
        APIInterfaceImpl api_impl(*p);
        api2->func_API2(&api_impl);
    }
private:
    API2* api2;
};

```

In this way, lib.so only exposes an Interface to public. External users are unaware of the implementation of the interface, lib.so does not have to expose any symbols either. 

This is the 2nd use case of interface to show base class cannot work here (the 1st use case is in Unit Test where interface is used as parameter for the test to mock/stub)
