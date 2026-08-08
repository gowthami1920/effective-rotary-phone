from falkordb import FalkorDB
import time


from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
from config import POKEC_FILE

FILE_PATH = POKEC_FILE

BATCH_SIZE = 200
MAX_RELATIONSHIPS = 100000

client = FalkorDB(
    host=FALKORDB_HOST,
    port=FALKORDB_PORT,
    username=FALKORDB_USERNAME,
    password=FALKORDB_PASSWORD
)

# Separate graph — does NOT touch your benchmark graph
graph = client.select_graph("ingest_test")

QUERY = """
UNWIND $rows AS row
MERGE (a:Person {id: row.source})
MERGE (b:Person {id: row.target})
MERGE (a)-[:KNOWS]->(b)
"""

# Clear only the temporary ingest graph
graph.query("""
MATCH (n)
DETACH DELETE n
""")

batch = []
total = 0

print("=" * 50)
print("FalkorDB Ingest Benchmark")
print("=" * 50)

start_time = time.perf_counter()

with open(FILE_PATH, "r", encoding="utf-8") as file:

    for line in file:

        if line.startswith("#"):
            continue

        parts = line.strip().split()

        if len(parts) != 2:
            continue

        batch.append({
            "source": parts[0],
            "target": parts[1]
        })

        if len(batch) >= BATCH_SIZE:

            graph.query(
                QUERY,
                params={"rows": batch},
                timeout=60
            )

            total += len(batch)
            batch = []

            if total % 10000 == 0:
                print(f"Imported {total:,} relationships")

            if total >= MAX_RELATIONSHIPS:
                break

if batch and total < MAX_RELATIONSHIPS:

    remaining = MAX_RELATIONSHIPS - total
    batch = batch[:remaining]

    graph.query(
        QUERY,
        params={"rows": batch},
        timeout=60
    )

    total += len(batch)

end_time = time.perf_counter()

load_time = end_time - start_time
relationships_per_sec = total / load_time

# Count actual nodes
result = graph.query("""
MATCH (n)
RETURN count(n) AS nodes
""")

nodes = result.result_set[0][0]
nodes_per_sec = nodes / load_time

print("\n" + "=" * 50)
print("FALKORDB INGEST BENCHMARK COMPLETED")
print("=" * 50)

print(f"Nodes                 : {nodes:,}")
print(f"Relationships         : {total:,}")
print(f"Load Time             : {load_time:.2f} seconds")
print(f"Relationships/sec     : {relationships_per_sec:,.2f}")
print(f"Nodes/sec             : {nodes_per_sec:,.2f}")
