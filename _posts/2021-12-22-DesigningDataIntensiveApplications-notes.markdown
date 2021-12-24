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
Why NoSQL: greater scalability, specialized query that are not well supported by SQL, restrictiveness of relational schemas, better performance due to locality.

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

- Schema-on-read: the structure of the data is implicit, and only interpreted when the data is read. (Document DB)
- Schema-on-write: the schema is explicit and the database ensures all written data conforms to it. (Relational DB) 

Schema-on-read is similar to dynamic (runtime) type checking in programming language, whereas schema-on-write is similar to static (compile-time) type checking. 

Convergence of Document and relational DB

SQL is a declarative query language. You just specify the pattern of the data you want, but not how to achieve that goal.

Many commonly used programming language are imperative

## Graph Data Model 
Facebook maintains a single graph with many types of vertices and edges: vertices represent people, locations, events, checkins and comments

Graphs are good for evolvability

# Chapter 3 Storage and Retrieval
Well-chosen indexes speed up read queries, but every index slows down writes
 
Append-only log is good (compared with update the file in place) for several reasons:
- Appending are sequential write operations, which are much faster than random writes;
- Concurrency and crash recovery are much simpler
- Merging old segments avoids the problem of data files getting fragmented over time 

SSTable: Sorted String Table, key-value pairs are sorted by key

LSM-Tree: Log-Structured Merge Tree: SSTable + memtable

Bloom filter: tell you if a key does not appear in the DB, saves many unnecessary disk reads for nonexistent keys

The log-structured indexes break the DB down into variable-size segments, typically several MB or more in size, and always write a segment sequentially. B-trees break the DB down into fixed-size blocks or pages, traditionally 4KB in size. Each page can be identified using an address or location, which allows one page to refer to another -- similar to a pointer, but on disk instead of in memory

WAL: write-ahead log, an append-only file to which every B-tree modification must be written before it can be applied to the pages of the tree itself (restore B-tree back after crash)

LSM-trees are faster for writes while B-trees are faster for reads. B-trees have higher write amplification. LSM-trees can be compressed better.

In MySQL's InnoDB storage engine, the primary key of a table is always a clustered index, in SQL Server, you can specify one clustered index per table. 

The performance advantage of in-memory DB is not due to the fact that they don't need to read from disk (Operating system cache will make sure a disk-based storage engine may never need to read from disk). They can be faster because they can avoid the overheads of encoding in-memory data structures in a form that can be written to disk.

## OLTP vs. OLAP
OLTP (online transaction processing): handles raw data, interactive. Records are inserted or updated based on the user’s input

OLAP (online analytic processing): aggregate raw data 

Data warehouse: a separate DB to run the analytics without affecting OLTP operations. The process of getting data into the warehouse is known as ETL (extract-transform-load)

The data model of a data warehouse is most commonly relational.

In Chapter 2, a wide range of different data models are used in transaction processing, in analytics however, there is much less diversity of data models: *star schema* (aka dimensional modeling, center: fact table). A variation of this template is known as the *snowflake*, where dimensions are further broken down into subdimensions. Snowflake schemas are more normalized than star schemas.

In a typical data warehouse, fact tables often have +100 columns. But a typical query only accesses 4 or 5 of them at one time. So column-oriented storage is a good fit.
 
Store the same data sorted in several different ways. Data needs to be replicated to multiple machines anyway. (Downside of making writes more difficult)

Data cube/OLAP cube: cache aggregates that queries use more often. One way of creating such a cache is a *materialized view*. Not often used in OLTP DB because updates make writes more expensive. In read-heavy data warehouse they can make more sense.

why OLAP workloads are so different from OLTP: when your queries require sequentially scanning across a large number of rows, indexes are much less relevant.

# Chapter 4 
Binary encoding: Apache Thrift, Protobuf, Apache Avro

Data outlives code

