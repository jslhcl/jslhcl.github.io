---
layout:	post
title:	"Designing Data-Intensive Applications notes"
date:	2021-12-22
---

# Chapter 1 Reliable, Scalable, and Maintainable Applications

Three concerns that are important in most software system: Reliability, Scalability and Maintainability

## Scalability
load parameters: numbers to describe load. e.g., (Twitter) The distribution of followers per user is a key load parameter for discussing scalability. Hybrid mode of both approaches: Most users' tweets continued to be fanned out to home timelines, small number of celebrities are fetching tweets separately and merged with that user's home timeline when it is read

use percentiles to measure performance

If you are working on a fast-growing service, you will need to rethink your architecture on every order of magnitude load increase -- or perhaps more often than that.

Keep your database on a single node (scale up) until scaling cost or high-availability requirements forced you to make it distributed.

# Chapter 2 Data Models and Query Languages
why NoSQL: greater scalability, specialized query that are not well supported by SQL, restrictiveness of relational schemas, better performance due to locality.

If data is stored in relational tables, a translation layer is required between the objects in the application code and the DB model of tables, rows and columns.

Relational model provides better support for joins, and many-to-one and many-to-many relationships.

## Document Model
 
If your application does use many-to-many relationships, the document model becomes less appealing:
- joins will be emulated in application code by making multiple requests to the DB, 
- moves complexity into the application level
- join is slower than the join performed by the specialized code inside DB

For highly interconnected data, the document model is awkward, the relational model is acceptable, and the graph models are the most natural.

If your application has mostly one-to-many relationships (tree-structured data) or no relationships between records, the document model is appropriate.

The advantage of using an ID is that because it has no meaning to humans, it never needs to change: the ID can remain the same, even if the information it identifies changes. Anything that is meaningful to humans may need to change sometime in the future.

Schema-on-read: the structure of the data is implicit, and only interpreted when the data is read. (Document DB)
Schema-on-write: the schema is explicit and the database ensures all written data conforms to it. (Relational DB) 
Schema-on-read is similar to dynamic (runtime) type checking in programming language, whereas schema-on-write is similar to static (compile-time) type checking. 

Convergence of Document and relational DB

SQL is a declarative query language. You just specify the pattern of the data you want, but not how to achieve that goal.

Many commonly used programming language are imperative

## Graph Data Model 
Facebook maintains a single graph with many types of vertices and edges: vertices represent people, locations, events, checkins and comments

Graphs are good for evolvability

