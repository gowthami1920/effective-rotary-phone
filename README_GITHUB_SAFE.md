# Graph Database Benchmark

This repository contains Python scripts used for graph-database benchmarking.

## Included benchmarks
- Node count
- Point lookup
- 1-hop, 2-hop and 3-hop traversal
- Aggregation
- Indexed lookup
- Mixed read/write workload
- Ingestion benchmark

## Databases / connectors represented in the source
- FalkorDB
- Neo4j
- Neo4j-compatible connection code used for the project
- CognoDB connectivity test

## Security
Database credentials are intentionally not stored in the repository. Configure them through environment variables using `.env.example` as a template.

Do not commit `.env`, passwords, API keys, or other secrets.
