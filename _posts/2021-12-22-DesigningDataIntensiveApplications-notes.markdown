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

# Chapter 4 Encoding and Evolution

Binary encoding: Apache Thrift, Protobuf, Apache Avro

Data outlives code

# Chapter 5 Replication 

scale up vs. scale out

- leader: first writes new data to its local storage
- follower: receive data change from leader

Synchronous vs. Asynchronous Replication

In practice, if you enable synchronous replication, it usually means one of the followers is sync, and the others are async. If the sync follower becomes unavailable or slow, one of the async followers is made sync. (also called semi-synchronous) (Azure Storage uses chain replication which is a variant of sync replication)

## Single Leader Replication

Set up new follower: take a consistent snapshot of the leader's DB, copy snapshot to the new follower, follower requests all the data changes that have happened since the snapshot was taken

Handle Node outages 
- Follower failure: catch-up recovery
- Leader failure: failover. One of the followers needs to be promoted to be the new leader. (split brain: two nodes both believe they are the leader) (Chapter 9 summary, wait for the leader to recover, or manually fail over, or use an algorithm to automatically choose a new leader. This approach requires a consensus algorithm)

Implementation of Replication logs
- Statement-based (not deterministic. call Now() or Rand(), have side effects, e.g., triggers)
- Write-ahead log shipping (the log describes that data on a very low level)
- Logical (row-based) log replication
- Trigger-based: more flexible (only replicate a subset of data), greater overheads

Eventual consistency, replication lag
- Read your own writes: always read the user's own profile from the leader, and any other user's profile from a follower.
- Monotonic Read: each user always makes their reads from the same replica
- Consistent Prefix Reads: particular problem in partitioned (sharded) DB. One solution is to make sure any writes that are causally related to each other are written to the same partition.

## Multi-leader Replication: 

allow more than one node to accept writes. Each leader simultaneously acts as a follower to the other leader (master-master or active/active replication). Used in multi-datacenter operation.

retrofitted feature, may cause other DB features (autoincreamenting keys, triggers) problematic. Should be avoided if possible.

Another situation in which multi-leader replication is appropriate is if you have an application that needs to continue to work while it is disconnected from the Internet

The biggest problem with multi-leader replication is that write conflicts can occur.

Conflict Resolutions: The simplest strategy is to avoid them: If the application can ensure that all writes for a particular record go through the same leader, then conflicts cannot occur.

Last write wins (LWW): prone to data loss

merge conflicts, let application code to resolve.

Another problem is writes may arrive in the wrong order at some replicas, similar to "Consistent Prefix Reads". Simply attaching a timestamp to every write is not sufficient, because clocks cannot be trusted to be sufficiently in sync to correctly order these events. a technique called *version vectors* can be used 

## Leaderless Replication

Read requests are also sent to several nodes in parallel. Appealing for use cases that require high availability and low latency and that can tolerate occasional stale reads, also suitable for multi-datacenter operation.

How does an unavailable node catch up on the writes that it missed?
- Read repair: This approach works well for values that are frequently read
- Anti-entropy process: a background process that constantly looks for differences in the data between replicas and copies any missing data from one replica to another

Quorum reads (r) and writes (w): r + w > n (replicas)

### What if we cannot reach a  quorum of w or r nodes?

*Sloppy quorum*: writes and reads still require w and r successful response, but those may include nodes that are not among the designated n home nodes for a value. Once the network interruption is fixed, any writes that one node temporarily accepted on behalf of another node are sent to the appropriate “home” nodes (*hinted handoff*)

Quorum Consistency cannot guarantee to get the latest value. Stronger guarantees require transactions or consensus.  

### Detect Concurrent Writes

LWW (last write wins) achieves the goal of eventual convergence, but at the cost of durability: if there are several concurrent writes to the same key, even if they were all reported as successful to the client, only one of the writes will survive and others will be silently discarded. Moreover, LWW may even drop writes that are not concurrent. 

The only safe way of using DB with LWW is to ensure a key is only written once and thereafter treated as immutable

Version vectors (vector clock): 
- The server maintains a version number for every key, increments the version number every time that key is written. 
- When a client writes a key, it must include the version number from the prior read, and it must merge together all values that it received in the prior read.
- If a client makes a write without including a version number, it is concurrent with all other writes, so it will not overwrite anything.
- An item cannot simply be deleted from DB when it is removed, instead, the system must leave a deletion marker (*tombstone*) with an appropriate version number indicating that the item has been removed when merging siblings.
- Need to use a version number per replica as well as per key.

# Chapter 6 Partitioning

Consistent Hashing: a way of evenly distributing load across an internet-wide system of caches.

Cassandra achieves a compromise between two partitioning strategies (by key range and by hash of key). If the primary key is chosen to be (user\_id, update\_timestamp), the 1st key (user\_id) is hashed to determine the partition, the second key (update\_timestamp) is used as a concatenated index. Different users may be stored on different partitions, but within each user, the updates are stored ordered by timestamp on a single partition.

Hashing a key cannot avoid hot spots entirely. If one key is known to be very hot, a simple technique is to add a random number to the beginning or end of the key.

Partitioning secondary indexes by Document vs. by Term
- By Document (local index): secondary index will scatter in different partitions. Write to DB (add/remove/update a document) only need to deal with the partition that contains the document ID you are writing, but read will search all the partitions.
- By Term (global index): secondary index will be in one partition for one secondary index value. Read will only request to the partition containing the term, writes may affect multiple partitions. 
 
## Rebalancing partitions

Fixed number of partitions (partition numbers > nodes) vs. Dynamic partitioning vs. Fixed number of partitions per node

## Operations: Automatic or Manual Rebalancing

Automation can be dangerous in combination with automatic failure detection. This puts additional load on the overloaded node, other nodes and the network --making the situation worse and potentially causing a cascading failure.

Service Discovery: How does the component making the routing decision (which may be one of the nodes, or the routing tier, or the client)

Many distributed data systems rely on a separate coordination service such as ZooKeeper to keep track of this cluster metadata. Whenever a partition changes ownership, or a node is added or removed, ZooKeeper notifies the routing tier so that it can keep its routing information up to date. 

HBase, SolrCloud and Kafka also use ZooKeeper to track partition assignments.

Cassandra and Riak use a *gossip protocol* among the nodes. Requests can be sent to any node, and that node forwards them to the appropriate node.

# Chapter 7 Transactions

Systems that do not meet the ACID criteria are sometimes called *BASE*: Basically Available, Soft state, and Eventual consistency.

The idea of ACID consistency is that you have certain statements about your data (invariants) that must always be true. 

Atomicity, isolation and durability are properties of the DB, whereas consistency (in ACID sense) is a property of the application. It's the application's responsibility to define its transactions correctly, this is not something that the DB can guarantee.

The idea of ACID isolation is that concurrently running transactions shouldn't interfere with each other.  

A transaction is usually understood as a mechanism for grouping multiple operations on multiple objects into one unit of execution.

Many distributed datastores have abandoned multi-object transactions because they are difficult to implement across partitions. Datastores with leaderless replication work much more on a "best effort" basis

## Weak isolation levels (vs. serializable isolation which means the DB guarantees that transactions have the same effect as if they ran serially):

### Read Committed 

no dirty read - cannot see uncommitted data, (how to implement) use lock, or remember both the old committed value and the new value

no dirty write - cannot overwrite uncommitted data. (how to implement) use lock

### Snapshot Isolation and Repeatable Read

*read skew*, an example of nonrepeatable read. A client sees different parts of the DB at different points in time.

Each transaction reads from a consistent snapshot of the database - the transaction sees all the data that was committed in the DB at the start of the transaction. Even if the data is subsequently changed by another transaction, each transaction sees only the old data from that particular point in time. 

A key point of snapshot isolation is readers never block writes, and writes never block readers

(how to implement) DB must keep several different committed versions of an object (multi-version concurrency control, MVCC). A typical approach is that read committed uses a separate snapshot for each query, while snapshot isolation uses the same snapshot for an entire transaction. When a transaction is started, it is given a unique, always-increasing transaction ID (txid)

The reason of this naming confusion (Oracle: serializable, PostgreSQL and MySQL: repeatable read) is that the SQL standard doesn't have the concept of snapshot isolation. IBM DB2 uses "repeatable read" to refer to serializability 

#### Prevent Lost Updates

Lost update problem: read-modify-write cycle concurrently.

Many DB provide atomic update operations, which remove the need to implement read-modify-write cycles in application code. (but it won't help if application code still uses read-modify-write cycles) Or use lock, application code needs to add lock explicitly

An alternative is to allow them to execute in parallel and, if the transaction manager detects a lost update, abort the transaction and force it to retry its read-modify-write cycle.

#### Write Skew and Phantoms

*write skew*: not dirty write nor lost update, because the two transactions are updating two different objects

*phantom*: a write in one transaction changes the result of a search query in another transaction

## Serializability

Serializable isolation is usually regarded as the strongest isolation level. It guarantees that even though transactions may execute in parallel, the end result is the same as if they had executed one at a time, serially, without any concurrency. **protect against all the concurrency issues**

### Actual Serial Execution
   
To execute only one transaction at a time, in serial order, on a single thread.

Encapsulating transactions in stored procedures. Systems with single-threaded serial transaction processing don’t allow interactive multi-statement transactions.

Cons: 
- Each DB has its own language for stored procedure; 
- Harder to debug, test and monitor; 
- Badly written stored procedure (using a lot of memory or CPU) can cause more trouble than code in application layer; 
- Cross partition is orders of magnitude below its single-partition throughput and cannot be increased by adding more machines; 
- Limited to use cases where the active dataset can fit in memory

### Two-Phase Locking (2PL)

Only one widely used algorithm for serializability for around 30 years. Used by the serializable isolation level in MySQL (InnoDB) and SQL Server, and the repeatable read isolation level in DB2.

Implementation: acquire shared lock before read; acquire exclusive lock before write; upgrade shared lock to exclusive lock if first reads then writes; hold the lock until the end of the transaction (commit or abort. This is where the name comes from: 1st phase is when the locks are acquired, 2nd phase is when all the locks are released)

Will cause deadlock. DB automatically detects deadlocks and aborts one of them. The aborted transaction needs to be retried by the application.

Unlike snapshot isolation, Reading an old version of the object is not acceptable under 2PL. 

Quite unstable latency, very slow at high percentiles.

- Predict Locks: solve phantom issue. It belongs to all objects that match some search condition. 
- Index-range lock: simplified approximation of predict locking.

### Serializable Snapshot Isolation (SSI)
    
First described in 2008.

Optimistic concurrency control. It lets transactions continue anyway, in the hope that everything will turn out all right. When a transaction wants to commit, the DB checks whether anything bad happened; if so, the transaction is aborted and has to be retried. 

Based on snapshot isolation, On top of snapshot isolation, SSI adds an algorithm for detecting serialization conflicts among writes and determining which transactions to abort. 

How to detect: 
- When the transaction wants to commit, the DB checks whether any of the ignored writes have now been committed. If so, the transaction must be aborted;  
- When the transaction writes to the DB, DB checks whether the prior read is outdated and committed. If so, the transaction must be aborted.
 
Performance: 

- Less detailed tracking is faster, but may lead to more transactions being aborted than strictly necessary.
- One transaction doesn't need to block waiting for locks held by other transaction, read-only queries can run on a consistent snapshot without requiring any locks, which is very appealing for read-heavy workloads.
- The rate of aborts significantly affects the overall performance of SSI. SSI requires that read-write transactions be fairly short (long-running read-only transactions may be OK)

# Chapter 8 The Trouble with Distributed Systems

Partial failures in a distributed system are nondeterministic. You may not even know whether something succeeded or not. 

Rather than using configured constant timeouts, systems can continually measure response times and their variability (*jitter*)

Monotonic clock is suitable for measuring a duration (time interval) as they are guaranteed to always move forward; while time-of-day clock is unsuitable due to the jumps back issue

Fundamental problems of LWW: 
- A node with a lagging clock is unable to overwrite values previously written by a node with a faster clock.
- LWW cannot distinguish between writes that occurred sequentially and writes that were truly concurrent. Additional causality tracking mechanisms, such as version vector, are needed in order to prevent violation of causality.

Physical clock (time-of-day and monotonic clock, measure actual elapsed time) vs. logical clock (based on incrementing counters, are safer for ordering events)

The truth is defined by the majority

Fencing token: a number that increases every time a lock is granted

Byzantine fault/Byzantine General Problem: nodes may "lie" (send arbitrary faulty or corrupted response)

Byzantine fault-tolerant 

# Chapter 9 Consistency and Consensus

Transaction isolation is primarily about avoiding race conditions due to concurrently executing transactions, whereas distributed consistency is mostly about coordinating the state of replicas in the face of delays and faults.

Linearizability (aka atomic consistency, strong consistency, immediate consistency, or external consistency):

The basic idea is to make a system appear as if there were only one copy of the data, and all operations on it are atomic.

Linearizability vs. Serializability
- Serializability is an isolation property of transactions, where every transaction may read and write multiple objects. It guarantees that transactions behave the same as if they had executed in some serial order.
- Linearizability is a recency guarantee on reads and writes of a register (an individual object). It doesn't group operations together into transactions, so it does not prevent problems such as write skew.

A DB may provide both serializability and linearizability, and this combination is known as *strict serializability* or *strong one-copy serializability*.
2PL or actual serial execution are linearizable, but SSI is not linearizable, as it does not include writes that are more recent than the snapshot.

Linearizability Scenarios: leader election, uniqueness constraints (username or email address must be unique)

CAP theorem: Consistency, Availability, Partition tolerance: pick 2 out of 3 (better phrasing CAP would be either Consistent (linearizability) or Availability when Partitioned, because partitions aren't something about which you have a choice: they will happen whether you like it or not). 

Applications that don't require linearizability can be more tolerant of network problems.

If you want linearizability, the response time of read and write requests is at least proportional to the uncertainty of delays in the network. A faster algorithm for linearizability does not exist, but weaker consistency models can be much faster, so this trade-off is important for latency-sensitive systems.

Linearizability has a *total order* of operations, causality defines a *partial order*. There are no concurrent operations in a linearizability datastore. Linearizability implies causality: any system that is linearizability will preserve causality correctly. In many cases, system that appear to require linearizability in fact only really require causal consistency.

## Lamport Timestamps

Generating sequence numbers that is consistent with causality.

A pair of (counter, node ID)

Every node and every client keeps track of the maximum counter value it has seen so far, and includes that maximum on every request. When a node receives a request or response with a maximum counter value greater than its own counter value, it immediately increases its own counter to that maximum.

Version vectors can distinguish whether two operations are concurrent or whether one is causally dependent on the other, whereas Lamport timestamps always enforce a total ordering, you cannot tell whether two operations are concurrent or whether they are causally dependent.

Not sufficient to solve many common problems in distributed system (for example, unique username, this approach works for determining the winner after the fact, but not sufficient when a node has just received a request from a user to create a username, and needs to decide right now)

Total Order broadcast: Knowing when your total order is finalized

Delivering a message is like appending to the log. A node is not allowed to retroactively insert a message into an earlier position in the order if subsequent messages have already been delivered. This fact makes total order broadcast stronger than timestamp ordering.

The sequence number can then serve as a fencing token, because it is monotonically increasing. In ZooKeeper, this sequence number is called zxid.

It can be proved that a linearizable compare-and-set (or increment-and-get) register and total order broadcast are both equivalent to consensus.

## Distributed Transactions and Consensus

### Two-phase Commit (2PC): implementing atomic commit (for distributed system)

- phase 1: prepare request to each nodes, asking them whether they are able to commit;
- phase 2: commit if all participants reply yes, abort if any replies no

Coordinator failure: 

The only way 2PC can complete is by waiting for the coordinator to recover (In principle, the participants could communicate among themselves to find out how each participant voted and come to some agreement, but that is not part of the 2PC protocol)

### Three-phase Commit

2PC is called a blocking atomic commit protocol due to the fact that 2PC can be stucking waiting for the coordinator to recover

Nonblocking atomic commit requires a perfect failure detector – i.e., a reliable mechanism for telling whether a node has crashed or not. In a network with unbounded delay a timeout is not a reliable failure detector.

### Distributed Transactions in Practice

Many cloud services choose not to implement distributed transactions due to the operational problems.

Distributed transactions in MySQL are reported to be over 10 times slower than single-node transactions.

Database-internal distributed transactions can often work quite well. On the other hand, transactions spanning heterogeneous technologies are a lot more challenging.

XA (extended architecture) is a standard for implementing two-phase commit across heterogeneous technologies. It's not a network protocol, merely a C/Java Transaction API for interfacing with a transaction coordinator.

### Limitations of distributed transactions

Coordinator logs are required in order to recover in-doubt transactions after a crash, which makes application server no longer stateless

Since XA needs to be compatible with a wide range of data systems, it is necessarily a lowest common denominator. (cannot detect deadlocks across different systems, does not work with SSI)

Have a tendency of amplifying failures (any part of the system is broken, the transaction fails)

### Fault-Tolerant Consensus (Paxos, Raft)

A consensus algorithm cannot simply sit around and do nothing forever, it must make progress, Even if some nodes fail, the other nodes must still reach a decision.

Any consensus algorithm requires at least a majority of nodes to be functioning correctly in order to assure termination. That majority forms a quorum

Total order broadcast is equivalent to repeated rounds of consensus

We have two rounds of voting: once to choose a leader, and a second time to vote on a leader's proposal. The key insight is that the quorums for those two votes must overlap: if a vote on a proposal succeeds, at least one of the nodes that voted for it must have also participated in the most recent lead election.

Difference between fault-tolerant consensus and 2PC:

in 2PC the coordinator is not elected, fault-tolerant consensus algorithms only require votes from a majority of nodes, whereas 2PC requires a "yes" vote from every participant. Moreover, consensus algorithms define a recovery process by which nodes can get into a consistent state after a new leader is elected.

### Membership and Coordination Service

ZooKeeper and etcd are designed to hold small amounts of data that can fit entirely in memory. 

ZooKeeper is modeled after Google's Chubby lock service, implementing not only total order broadcast (hence consensus), but also: Linearizable atomic operations, total ordering of operations, failure detection, change notification

ZooKeeper runs on a fixed number of nodes (usually three or five) and performs its majority votes among those nodes while supporting a potentially large number of clients

Normally, the kind of data managed by ZooKeeper is quite slow-changing: it represents information like "the node running on IP address 10.1.1.23 is the leader for partition 7"

ZooKeeper, etcd, and Consul are often used for service discovery – that is, to find out which IP address you need to connect to in order to reach a particular service

Causal consistency (weak consistency, as somethings can be concurrent) does not have the coordination overhead of linearizability and is much less sensitive to network problems

# Chapter 10 Batch Processing

Services (online systems) vs. Batching processing systems (offline systems) vs. Stream processing systems (near-real-time systems)

Distributed batch processing engines have a deliberately restricted programming model: 
- Treat inputs as immutable;
- Callback functions (mappers and reducers) are assumed to be stateless and to have no externally visible side effects

Sushi principle: raw data is better

## Alternatives for batching processing (besides MapReduce)

Dataflow engines: Spark (distributed batch computations), handle an entire workflow as one job, rather than breaking it up into independent subjobs. Sufficient for intermediate state between operators to be kept in memory instead of Materialization of Intermediate State (The process of writing out this intermediate state to files. like MapReduce)

MapReduce does not account for the iterative nature, it will always read the entire input dataset and produce a completely new output dataset (vs. Graph model and iterative processing)

A difference between batch processing and stream processing
- batch: input data is bounded, it has a known, fixed size
- stream: input is unbounded, its inputs are never-ending streams of data (so a job is never complete)

# Chapter 11 Stream Processing

When moving toward continual processing with low delays, polling becomes expensive if datastore is not designed for this kind of usage. It is better for consumers to be notified when new events appear (push. Messaging system).

Batch processing system provides a strong reliability guarantee (failed tasks are automatically retried, etc.), messaging system may lose messages (Direct messaging. Whether message loss is acceptable depends on the application. For example, with sensor reading, an occasional missing data is perhaps not important, since an updated value will be sent a short time later).

UDP multicast is widely used in the financial industry for streams such as stock market feeds, where low latency is important.

Message brokers (message queue) vs. Direct Messaging (UDP, etc.)

When multiple consumers read messages, two main patterns:
- Load balancing (each message is delivered to one of the consumers)
- Fan-out (each message is delivered to all of the consumers)

Log-based message brokers: producer sends a message by appending it to the end of the log. Combine the durable storage approach with low-latency notification facilities (Apache Kafka) 

# Chapter 12 The Future of Data Systems

## Lambda Architecture

Combine both batch processing and stream processing 

## Separation of application code and state

Most web applications today are deployed as stateless services, in which any user request can be routed to any application server, but the state has to go somewhere: a database

request/response interaction vs. publish/subscribe dataflow (more responsive user interfaces and better offline support): an option of subscribing to changes, not just querying the current state 

