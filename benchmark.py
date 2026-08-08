from neo4j import GraphDatabase
import time
import csv
import statistics

from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from queries import *

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

benchmarks = [
    ("Count Nodes", COUNT_NODES, {}),
    ("Point Lookup", POINT_LOOKUP, {"id": "1"}),
    ("1-Hop Traversal", ONE_HOP, {"id": "1"}),
    ("2-Hop Traversal", TWO_HOP, {"id": "1"}),
    ("3-Hop Traversal", THREE_HOP, {"id": "1"}),
    ("Aggregation", AGGREGATION, {})
]

WARMUP = 10
RUNS = 100

csv_file = "neo4j_results.csv"

# Create CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Query", "Run", "Time (ms)"])

with driver.session() as session:

    for query_name, query, params in benchmarks:

        print(f"\n===== {query_name} =====")

        # Warm-up runs
        for _ in range(WARMUP):
            session.run(query, **params).consume()

        times = []

        for i in range(RUNS):

            start = time.perf_counter()

            session.run(query, **params).consume()

            end = time.perf_counter()

            elapsed = (end - start) * 1000
            times.append(elapsed)

        # Save all runs at once (avoids PermissionError)
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)

            for i, t in enumerate(times):
                writer.writerow([query_name, i + 1, f"{t:.2f}"])

        avg = statistics.mean(times)
        p50 = statistics.median(times)
        sorted_times = sorted(times)
        p95 = sorted_times[int(len(sorted_times) * 0.95) - 1]

        print(f"Average : {avg:.2f} ms")
        print(f"Minimum : {min(times):.2f} ms")
        print(f"Maximum : {max(times):.2f} ms")
        print(f"P50 : {p50:.2f} ms")
        print(f"P95 : {p95:.2f} ms")

driver.close()

print("\nBenchmark completed successfully!")