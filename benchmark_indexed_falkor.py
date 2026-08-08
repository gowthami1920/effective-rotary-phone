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

TEST_ID = "7"
WARMUP_RUNS = 3
MEASURED_RUNS = 10

QUERY = """
MATCH (n:Person {id: $id})
RETURN n
"""


# -----------------------------
# Warm-up
# -----------------------------

for _ in range(WARMUP_RUNS):
    graph.query(
        QUERY,
        params={"id": TEST_ID}
    )


# -----------------------------
# Measurements
# -----------------------------

times = []

for _ in range(MEASURED_RUNS):

    start = time.perf_counter()

    graph.query(
        QUERY,
        params={"id": TEST_ID}
    )

    end = time.perf_counter()

    times.append((end - start) * 1000)


times.sort()

average = statistics.mean(times)
minimum = min(times)
maximum = max(times)
p50 = statistics.median(times)

p95_index = int(0.95 * len(times)) - 1
p95 = times[max(0, p95_index)]


print("\n===== Indexed / Filtered Lookup =====")
print(f"Average : {average:.2f} ms")
print(f"Minimum : {minimum:.2f} ms")
print(f"Maximum : {maximum:.2f} ms")
print(f"P50 : {p50:.2f} ms")
print(f"P95 : {p95:.2f} ms")

print("\nIndexed lookup benchmark completed successfully!")
