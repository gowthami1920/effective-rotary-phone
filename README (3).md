# Graph Database Benchmarking

## 1. Overview

This repository contains a benchmarking study comparing graph database performance using a common graph dataset and a common set of query workloads.

The completed benchmark platforms are:

- CognoDB
- Neo4j
- Memgraph
- FalkorDB

The purpose is to evaluate graph query latency and selected workload behavior under the same benchmark dataset and client-side testing approach.

> **Scope note:** The assignment requests CognoDB plus at least four other graph databases. A fifth database was investigated but was not included because a suitable no-cost managed deployment could not be established without introducing billing or licensing risk. The four successfully tested platforms and all limitations are reported honestly below.

---

## 2. Assignment Requirements

The benchmark follows the assignment requirements as closely as possible.

The assignment requires:

- A public dataset with at least 100,000 relationships.
- The identical dataset loaded into every platform.
- 1-hop, 2-hop and 3-hop traversal latency.
- Point lookup and indexed/filtered lookup.
- Aggregation latency.
- Concurrent read/write throughput.
- Resource footprint where observable.
- P50 and P95 latency reporting.
- Equivalent resources, same dataset, same client machine/region and documented methodology.
- Honest reporting of timeouts, failed runs and other caveats.

Where a required metric was not completed on every platform, it is explicitly marked as **Not measured** rather than estimated or invented.

---

## 3. Databases Tested

| Database | Status |
|---|---|
| CognoDB | Core benchmark completed |
| Neo4j | Core benchmark completed |
| Memgraph | Core benchmark completed |
| FalkorDB | Core benchmark + additional tests completed |
| Fifth platform | Not included |

---

## 4. Dataset

The benchmark dataset contains:

- **Nodes:** 49,683
- **Relationships:** 100,000
- **Node label:** `Person`
- **Relationship type:** `KNOWS`

The same logical dataset was imported into the four tested platforms.

Database validation confirmed:

```text
Nodes: 49683
Relationships: 100000
```

The assignment requires the exact public dataset source to be stated in the README. The source name/URL was not preserved in the benchmark outputs available for this final report, so it is intentionally not guessed here.

**Before final submission, replace the following with the exact source used:**

```text
Dataset source: [INSERT EXACT PUBLIC DATASET SOURCE]
Dataset URL:    [INSERT EXACT PUBLIC DATASET URL]
```

---

## 5. Benchmark Methodology

The benchmark was executed from the same Windows client environment using Python scripts.

The workloads tested were:

1. Count Nodes
2. Point Lookup
3. 1-Hop Traversal
4. 2-Hop Traversal
5. 3-Hop Traversal
6. Aggregation

Additional FalkorDB tests were also executed:

7. Indexed / Filtered Lookup
8. Mixed Read/Write

Latency statistics reported include:

- Average
- Minimum
- Maximum
- P50
- P95

Lower latency is better.

---

## 6. Core Benchmark Results

### Average Latency (ms)

| Workload | CognoDB | Neo4j | Memgraph | FalkorDB |
|---|---:|---:|---:|---:|
| Count Nodes | 321.89 | 86.15 | 318.36 | **25.00** |
| Point Lookup | 330.80 | 105.40 | 325.83 | **28.92** |
| 1-Hop Traversal | 341.80 | 105.16 | 334.48 | **29.49** |
| 2-Hop Traversal | 393.70 | 114.04 | 478.35 | **29.92** |
| 3-Hop Traversal | 877.11 | 261.29 | 907.97 | **31.80** |
| Aggregation | 353.20 | 123.70 | 367.90 | **24.16** |

### Core benchmark conclusion

Under the benchmark configuration used in this project, FalkorDB recorded the lowest measured average latency for all six completed core workloads.

Neo4j was the second-lowest measured platform for these workloads.

This is a result of the specific benchmark environment and workload and should not be interpreted as a universal ranking of graph databases.

---

## 7. Detailed Results

### CognoDB

| Workload | Average | Minimum | Maximum | P50 | P95 |
|---|---:|---:|---:|---:|---:|
| Count Nodes | 321.89 | 286.10 | 446.50 | 319.30 | 376.94 |
| Point Lookup | 330.80 | 295.06 | 477.54 | 319.96 | 399.77 |
| 1-Hop Traversal | 341.80 | 292.08 | 1263.87 | 320.10 | 426.90 |
| 2-Hop Traversal | 393.70 | 300.83 | 772.14 | 323.84 | 694.28 |
| 3-Hop Traversal | 877.11 | 610.85 | 1356.78 | 945.91 | 1095.96 |
| Aggregation | 353.20 | 311.20 | 529.83 | 342.37 | 438.82 |

### Neo4j

| Workload | Average | Minimum | Maximum | P50 | P95 |
|---|---:|---:|---:|---:|---:|
| Count Nodes | 86.15 | 70.95 | 150.29 | 81.91 | 108.73 |
| Point Lookup | 105.40 | 76.65 | 502.33 | 100.07 | 117.25 |
| 1-Hop Traversal | 105.16 | 88.86 | 242.30 | 101.11 | 130.42 |
| 2-Hop Traversal | 114.04 | 89.92 | 268.86 | 107.98 | 151.15 |
| 3-Hop Traversal | 261.29 | 184.35 | 728.71 | 243.57 | 406.17 |
| Aggregation | 123.70 | 106.54 | 198.06 | 121.31 | 148.15 |

### Memgraph

| Workload | Average | Minimum | Maximum | P50 | P95 |
|---|---:|---:|---:|---:|---:|
| Count Nodes | 318.36 | 288.62 | 456.04 | 314.82 | 359.52 |
| Point Lookup | 325.83 | 294.01 | 470.97 | 320.08 | 356.48 |
| 1-Hop Traversal | 334.48 | 295.74 | 799.97 | 319.83 | 407.64 |
| 2-Hop Traversal | 478.35 | 307.87 | 881.57 | 369.90 | 769.54 |
| 3-Hop Traversal | 907.97 | 611.35 | 3548.30 | 838.19 | 1133.32 |
| Aggregation | 367.90 | 325.83 | 463.25 | 342.82 | 448.37 |

### FalkorDB

| Workload | Average | Minimum | Maximum | P50 | P95 |
|---|---:|---:|---:|---:|---:|
| Count Nodes | 25.00 | 22.92 | 31.82 | 23.54 | 27.98 |
| Point Lookup | 28.92 | 27.66 | 32.49 | 28.64 | 28.82 |
| 1-Hop Traversal | 29.49 | 27.13 | 37.56 | 28.62 | 31.26 |
| 2-Hop Traversal | 29.92 | 27.54 | 39.31 | 28.73 | 31.93 |
| 3-Hop Traversal | 31.80 | 30.04 | 35.31 | 31.34 | 32.83 |
| Aggregation | 24.16 | 21.76 | 26.21 | 24.13 | 26.02 |

---

## 8. Additional FalkorDB Tests

### Indexed / Filtered Lookup

An index was created and verified for:

```cypher
CREATE INDEX FOR (n:Person) ON (n.id)
```

The index inspection showed the `Person.id` range index as operational.

Measured results:

- Average: **151.59 ms**
- Minimum: **121.32 ms**
- Maximum: **249.63 ms**
- P50: **129.52 ms**
- P95: **194.47 ms**

This metric was **not measured on the other three platforms**, so it must not be presented as a four-database comparison.

### Mixed Read/Write

Measured FalkorDB workload:

- Clients: **5**
- Operations: **200**
- Total time: **4.40 seconds**
- Throughput: **45.50 QPS**
- Average latency: **67.32 ms**
- P50: **57.56 ms**
- P95: **123.29 ms**

This workload was not completed on the other platforms and therefore is reported only as an additional FalkorDB result.

---

## 9. Assignment Results Coverage Matrix

| Required metric | CognoDB | Neo4j | Memgraph | FalkorDB |
|---|---|---|---|---|
| Ingest nodes/sec | Not measured | Not measured | Not measured | Not measured |
| Ingest relationships/sec | Not measured | Not measured | Not measured | Not measured |
| Total ingest wall-clock time | Not measured | Not measured | Not measured | Not measured |
| 1-Hop P50/P95 | Completed | Completed | Completed | Completed |
| 2-Hop P50/P95 | Completed | Completed | Completed | Completed |
| 3-Hop P50/P95 | Completed | Completed | Completed | Completed |
| Point lookup P50/P95 | Completed | Completed | Completed | Completed |
| Indexed/filtered lookup | Not measured | Not measured | Not measured | **Completed** |
| Aggregation P50/P95 | Completed | Completed | Completed | Completed |
| Mixed read/write QPS | Not measured | Not measured | Not measured | **Completed** |
| Resource footprint | Not documented | Not documented | Not documented | Not documented |

---

## 10. Failed and Incomplete Tests

### FalkorDB ingest

The ingest benchmark encountered Redis/socket timeout errors during long-running import attempts.

Example failure:

```text
redis.exceptions.TimeoutError: Timeout reading from socket
```

The import was subsequently completed successfully for the 100,000 relationships, but the required wall-clock ingest benchmark was not captured in a reliable form.

Therefore:

> **FalkorDB ingest throughput is not reported.**

### TigerGraph / Fifth Database

A fifth database was investigated to satisfy the assignment's "CognoDB plus at least four other graph databases" requirement.

It was not included in the final benchmark because a suitable no-cost managed deployment could not be established without creating billing/licensing concerns.

No fabricated benchmark numbers are included.

---

## 11. Resource Footprint

The assignment requires resource usage to be reported where observable.

The benchmark outputs preserved for this submission do not contain complete CPU, RAM, storage and instance specifications for all platforms.

Therefore these values are currently marked:

> **Not documented / not observable from the recorded benchmark outputs.**

They should be added before final submission if the information is available from the respective platform consoles or deployment configuration.

---

## 12. Analysis

### Query latency

FalkorDB produced the lowest measured average latency across every completed core workload.

Its average latency remained approximately between 24 ms and 32 ms for the six core workloads.

Neo4j ranged from approximately 86 ms to 261 ms.

CognoDB and Memgraph showed higher latency in the supplied measurements, particularly for deeper traversal.

### Traversal depth

The 3-hop workload produced the largest increase in latency for CognoDB, Neo4j and Memgraph.

FalkorDB showed comparatively small changes across 1-hop, 2-hop and 3-hop traversal in the recorded benchmark.

### Tail latency

P95 is important because it shows higher-latency behavior rather than only the average.

For example:

- CognoDB 3-hop P95: 1095.96 ms
- Neo4j 3-hop P95: 406.17 ms
- Memgraph 3-hop P95: 1133.32 ms
- FalkorDB 3-hop P95: 32.83 ms

These measurements show a substantial difference in the recorded tail latency for this workload.

### Important interpretation

These results demonstrate performance differences under this project's specific setup. They do not prove that one database is universally faster than another.

Differences may be influenced by:

- Deployment configuration
- Cloud/network conditions
- Query implementation
- Index configuration
- Warm-up state
- Client/server location
- Free-tier limitations
- Driver behavior

---

## 13. Limitations

The following limitations must be considered:

1. A fifth comparison database was not included.
2. Ingest throughput was not captured reliably.
3. Indexed/filtered lookup was completed only for FalkorDB.
4. Mixed read/write testing was completed only for FalkorDB.
5. Complete resource-footprint information was not preserved for every platform.
6. The exact public dataset source/URL must be inserted before final submission.
7. The recorded benchmark outputs do not independently document the exact number of warm-up iterations or ≥100 stable iterations for every workload.

These limitations are intentionally disclosed rather than hidden.

---

## 14. Reproducibility

### Create and activate the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Configure credentials

Credentials and connection information should be provided through environment variables or a local `.env` file.

Do **not** commit credentials, passwords, tokens or private connection strings.

### Database checks

Examples:

```powershell
python check_db.py
python check_falkor.py
```

### Core benchmark

```powershell
python benchmark.py
python benchmark_falkor.py
```

### Additional FalkorDB tests

```powershell
python benchmark_indexed_falkor.py
python benchmark_mixed_falkor.py
```

Do not run an ingest benchmark as a completed result unless the wall-clock load time and throughput values are captured successfully.

---

## 15. Project Structure

```text
graph-benchmark/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── benchmark.py
├── benchmark_falkor.py
├── benchmark_indexed_falkor.py
├── benchmark_mixed_falkor.py
├── benchmark_ingest_falkor.py
│
├── import_neo4j.py
├── import_memgraph.py
├── import_cognodb.py
├── import_falkor.py
│
├── check_db.py
├── check_falkor.py
│
├── results/
│   └── final_assignment_results_matrix.csv
│
└── docs/
    └── benchmark_report.pdf
```

---

## 16. Conclusion

The completed benchmark demonstrates that, under the recorded test configuration, FalkorDB achieved the lowest average latency across the six core query workloads.

Neo4j showed the next-lowest latency in the completed core comparison.

The project also demonstrates the importance of reporting P50/P95 latency and documenting failed or incomplete workloads rather than relying only on averages.

The benchmark should be considered a reproducible experimental comparison with clearly stated limitations rather than a universal ranking of graph database systems.

---

## 17. Final Submission Checklist

Before publishing the repository:

- [ ] Insert exact public dataset source and URL.
- [ ] Verify all benchmark scripts run from a clean environment.
- [ ] Verify connection credentials are not committed.
- [ ] Add `requirements.txt`.
- [ ] Add final results CSV.
- [ ] Add benchmark report.
- [ ] Document database resource specifications.
- [ ] Document region/client environment.
- [ ] Document warm-up and iteration counts if available.
- [ ] Keep failed/incomplete metrics clearly marked.
- [ ] Review README for reproducibility.
- [ ] Push repository to GitHub.
