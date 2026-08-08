from falkordb import FalkorDB
import time
import statistics


from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
client = FalkorDB(
    host=FALKORDB_HOST,
    port=FALKORDB_PORT,
    username=FALKORDB_USERNAME,
    password=FALKORDB_PASSWORD
)

graph = client.select_graph("benchmark")

RUNS = 10

QUERIES = {
    "Count Nodes": """
        MATCH (n)
        RETURN count(n)
    """,

    "Point Lookup": """
        MATCH (n:Person {id: $id})
        RETURN n
    """,

    "1-Hop Traversal": """
        MATCH (n:Person {id: $id})-[:KNOWS]->(m)
        RETURN count(m)
    """,

    "2-Hop Traversal": """
        MATCH (n:Person {id: $id})-[:KNOWS*2]->(m)
        RETURN count(m)
    """,

    "3-Hop Traversal": """
        MATCH (n:Person {id: $id})-[:KNOWS*3]->(m)
        RETURN count(m)
    """,

    "Aggregation": """
        MATCH (n:Person)
        RETURN count(n)
    """
}


def run_benchmark(name, query, params=None):

    times = []

    # Warm-up
    for _ in range(3):
        graph.query(query, params=params or {})

    # Measurements
    for _ in range(RUNS):

        start = time.perf_counter()

        graph.query(
            query,
            params=params or {}
        )

        end = time.perf_counter()

        elapsed = (end - start) * 1000
        times.append(elapsed)

    times.sort()

    average = statistics.mean(times)
    minimum = min(times)
    maximum = max(times)

    p50 = statistics.median(times)

    p95_index = int(0.95 * len(times)) - 1
    p95 = times[max(0, p95_index)]

    print(f"\n===== {name} =====")
    print(f"Average : {average:.2f} ms")
    print(f"Minimum : {minimum:.2f} ms")
    print(f"Maximum : {maximum:.2f} ms")
    print(f"P50 : {p50:.2f} ms")
    print(f"P95 : {p95:.2f} ms")


# Use an existing node ID from the dataset
TEST_ID = "7"


print("\nFalkorDB Benchmark")
print("=" * 40)

for name, query in QUERIES.items():

    if name == "Count Nodes":
        run_benchmark(name, query)

    elif name == "Aggregation":
        run_benchmark(name, query)

    else:
        run_benchmark(
            name,
            query,
            {"id": TEST_ID}
        )

print("\nBenchmark completed successfully!")
