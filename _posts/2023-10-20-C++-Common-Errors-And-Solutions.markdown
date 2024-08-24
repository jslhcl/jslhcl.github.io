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

If you use CMake, the order in target\_link\_libraries matters. It seems the linker will check the symbols in each dependent library one by one, and throw the symbols away if it has no reference (To be confirmed). So make sure the dependent library using the symbol is before the dependent library defining the symbol.

Also, suppose library A depends on library B, library B depends on library C, in target\_link\_libraries, it should list all the dependencies of library A (not just direct dependency, which is B):

```cmake
target_link_libraries(libA PUBLIC ${libB}   # need to list all the dependencies B and C, and B has to be before C as B is using some symbols defined in C
                                  ${libC})
```

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

(Use a more concret example to illuastrate)

## Solution 1, wrapper solution:

```cpp
// makefile. libcustom_ep.so is the plugin of libort.so
libort.so:graph_viewer.cpp graph_viewer_ref.cpp session.cpp
	g++ -g graph_viewer.cpp graph_viewer_ref.cpp session.cpp -shared -fPIC -o libort.so

libcustom_ep.so:custom_ep.cpp
	g++ -g custom_ep.cpp -shared -fPIC -o libcustom_ep.so

test.out:test_wrapper.cpp libort.so
	g++ -g test_wrapper.cpp -L. -lort -o test.out

// graph_viewer.h
#pragma once
#include <string>

class GraphViewer {
public:
    GraphViewer() {}
    ~GraphViewer() {}
    bool IsConstantInitializer(std::string& name, bool check_outer_scope);
};

// graph_viewer.cpp
#include "graph_viewer.h"

bool GraphViewer::IsConstantInitializer(std::string& name, bool check_outer_scope) {
    if (check_outer_scope && name == "name") return true;
    return false;
}

// graph_viewer_ref.h
#pragma once
#include <string>

class GraphViewer;

class GraphViewerRef {
public:
GraphViewerRef(GraphViewer* g) : graph_(g) {}
~GraphViewerRef() = default;
bool IsConstantInitializer(std::string& name, bool check_outer_scope);
private:
GraphViewer* graph_;
};

// graph_viewer_ref.cpp
#include "graph_viewer_ref.h"
#include "graph_viewer.h"

bool GraphViewerRef::IsConstantInitializer(std::string& name, bool check_outer_scope) {
    return graph_->IsConstantInitializer(name, check_outer_scope);
}

// session.h
#pragma once
#include <string>
class EPAdapter;

class session {
public:
    session() {}
    ~session();
    void RegisterCustomEP(std::string path);
    void Run();
private:
    EPAdapter* ep_adapter_;
};

// session.cpp
#include <iostream>
#include <dlfcn.h>
#include "session.h"
#include "provider.h"
#include "graph_viewer.h"

class EPAdapter {
public:
    EPAdapter(ExecutionProvider* ep) : ep_(ep) {}
    int GetCapability(GraphViewerRef* graph) { return ep_->GetCapability(graph); }
private:
    ExecutionProvider* ep_; 
};

void session::RegisterCustomEP(std::string path) {
    void* handle = dlopen(path.c_str(), RTLD_NOW | RTLD_GLOBAL);
    ExecutionProvider* (*GetExternalProvider)();
    *(void **) (&GetExternalProvider) = dlsym(handle, "GetExternalProvider");
    ep_adapter_ = new EPAdapter((*GetExternalProvider)());
}

void session::Run() {
    std::cout << "session::Run()\n";
    GraphViewer* graph = new GraphViewer();
    GraphViewerRef graph_ref(graph);
    std::cout << "ep graph get capabiliyty: "<<ep_adapter_->GetCapability(&graph_ref)<<"\n";
    delete graph;
}

session::~session() {
    delete ep_adapter_;
}

// provider.h, API ExecutionProvider provided by libort.so. Caller needs to reimplement GetCapability() with API GraphViewerRef
#pragma once
#include "graph_viewer_ref.h"

class ExecutionProvider {
public:
    ExecutionProvider() {};
    virtual ~ExecutionProvider() = default;

    virtual int GetCapability(GraphViewerRef*) { return 0; }
};

// custom_ep.h
#pragma once
#include "provider.h"

class custom_ep : public ExecutionProvider {
public:
    custom_ep(std::string& n);
    ~custom_ep() = default;
    int GetCapability(GraphViewerRef*) override;
private:
    std::string name;
};

// custom_ep.cpp
#include "custom_ep.h"

custom_ep::custom_ep(std::string& n) { name = n; }

int custom_ep::GetCapability(GraphViewerRef* graph) {
    if (graph->IsConstantInitializer(name, true)) return 1;
    return 5;
}

#ifdef __cplusplus
extern "C" {
#endif

custom_ep* GetExternalProvider() {
    std::string name = "custom_ep";
    return new custom_ep(name);
}

#ifdef __cplusplus
}
#endif

// test_wrapper.cpp
#include "session.h"

int main() {
    session sess;
    sess.RegisterCustomEP("/home/leca/code/plugin2/libcustom_ep.so");
    sess.Run();
    return 0;
}

```

In this way, the symbol of the function GraphViewerRef::IsConstantInitializer() is in custom\_ep.so:

```bash
leca@host [ ~/code/plugin2 ]$ readelf -s --wide libcustom_ep.so | grep -i 'IsConstantInitializer'
    28: 0000000000000000     0 NOTYPE  GLOBAL DEFAULT  UND _ZN14GraphViewerRef21IsConstantInitializerERNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEb
    76: 0000000000000000     0 NOTYPE  GLOBAL DEFAULT  UND _ZN14GraphViewerRef21IsConstantInitializerERNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEb
```

## Solution 2, pure virtual class solution:

```cpp
// makefile
libort.so:graph_view_api_impl.cpp session.cpp
	g++ -g graph_view_api_impl.cpp session.cpp -shared -fPIC -o libort.so

libcustom_ep.so:custom_ep.cpp
	g++ -g custom_ep.cpp -shared -fPIC -o libcustom_ep.so

test.out:test_pure_virtual.cpp libort.so
	g++ -g test_pure_virtual.cpp -L. -lort -o test.out

// graph_viewer_ref.h. This is the API provided by libort.so
#pragma once
#include <string>

class GraphViewerRef {
public:
    virtual bool IsConstantInitializer(std::string& name, bool check_outer_scope) = 0;
};

// graph_view_api_impl.h
#pragma once
#include "graph_viewer_ref.h"

class ApiGraphView : public GraphViewerRef {
    bool IsConstantInitializer(std::string& name, bool check_outer_scope) override;
};

// graph_view_api_impl.cpp
#include "graph_view_api_impl.h"

bool ApiGraphView::IsConstantInitializer(std::string& name, bool check_outer_scope) {
    if (check_outer_scope && name == "name") return true;
    return false;
}

// session.h is the same as Solution 1's

// session.cpp
#include <iostream>
#include <dlfcn.h>
#include "session.h"
#include "provider.h"
#include "graph_view_api_impl.h"

class EPAdapter {
public:
    EPAdapter(ExecutionProvider* ep) : ep_(ep) {}
    int GetCapability(GraphViewerRef* graph) { return ep_->GetCapability(graph); }
private:
    ExecutionProvider* ep_; 
};

void session::RegisterCustomEP(std::string path) {
    void* handle = dlopen(path.c_str(), RTLD_NOW | RTLD_GLOBAL);
    ExecutionProvider* (*GetExternalProvider)();
    *(void **) (&GetExternalProvider) = dlsym(handle, "GetExternalProvider");
    ep_adapter_ = new EPAdapter((*GetExternalProvider)());
}

void session::Run() {
    std::cout << "session::Run()\n";
    ApiGraphView* api_graph_view = new ApiGraphView();
    std::cout << "ep graph get capabiliyty: "<<ep_adapter_->GetCapability(api_graph_view)<<"\n";
}

session::~session() {
    delete ep_adapter_;
}

// provider.h is the same as Solution 1's
#pragma once
#include "graph_viewer_ref.h"

class ExecutionProvider {
public:
    ExecutionProvider() {};
    virtual ~ExecutionProvider() = default;

    virtual int GetCapability(GraphViewerRef*) { return 0; }
};

// custom_ep.h is the same as Solution 1's
#pragma once
#include "provider.h"

class custom_ep : public ExecutionProvider {
public:
    custom_ep(std::string& n);
    ~custom_ep() = default;
    int GetCapability(GraphViewerRef*) override;
private:
    std::string name;
};

// custom_ep.cpp is the same as Solution 1's
#include "custom_ep.h"

custom_ep::custom_ep(std::string& n) { name = n; }

int custom_ep::GetCapability(GraphViewerRef* graph) {
    if (graph->IsConstantInitializer(name, true)) return 1;
    return 2;
}

#ifdef __cplusplus
extern "C" {
#endif

custom_ep* GetExternalProvider() {
    std::string name = "custom_ep";
    return new custom_ep(name);
}

#ifdef __cplusplus
}
#endif

// test_pure_virtual.cpp is the same as Solution 1's test_wrapper.cpp
#include "session.h"

int main() {
    session sess;
    sess.RegisterCustomEP("/home/leca/code/plugin_pure_virtual/libcustom_ep.so");
    sess.Run();
    return 0;
}
```

In this way, there is no such symbol of the function GraphViewerRef::IsConstantInitializer() in custom\_ep.so:

```bash
leca@host [ ~/code/plugin_pure_virtual ]$ readelf -s --wide libcustom_ep.so | grep -i 'IsConstantInitializer'
leca@host [ ~/code/plugin_pure_virtual ]$ 
```

# 6. static_cast vs. reinterpret_cast

reinterpret_cast can only perform pointer-to-pointer conversions and reference-to-reference conversions (plus pointer-to-integer and integer-to-pointer conversions). So the following case, there will be an build error:

```cpp
float f = 3;
int i = reinterpret_cast<int>(f);   // build error! You can use static_cast instead
```

For the opaque pointer case you can only use reinterpret_cast where you want to cast a pointer to an unimplemented class:

```cpp
struct StructNoImplementaion;
    
struct StructWithImplementation {
    StructWithImplementation(int m) : member1(m) {}
    int member1;
};
    
int main()
{
    StructWithImplementation s(3);
    // no error
    StructNoImplementaion* p = reinterpret_cast<StructNoImplementaion*>(&s);

    // error: cannot convert from 'StructWithImplemetation' to 'StructNoImplementation'
    //StructNoImplementaion* p = static_cast<StructNoImplementaion*>(&s);
}
```