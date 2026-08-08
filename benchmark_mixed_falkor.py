from falkordb import FalkorDB
import time
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor


from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
CLIENTS = 5
OPERATIONS_PER_CLIENT = 20

def create_client():
    return FalkorDB(
        host=FALKORDB_HOST,
        port=FALKORDB_PORT,
        username=FALKORDB_USERNAME,
        password=FALKORDB_PASSWORD
    )

def worker(client_id):
    client = create_client()
    graph = client.select_graph("mixed_test")

    times = []

    for i in range(OPERATIONS_PER_CLIENT):

        # Read
        start = time.perf_counter()

        graph.query("""
            MATCH (n:Person)
            RETURN count(n)
        """)

        times.append((time.perf_counter() - start) * 1000)

        # Write temporary node
        start = time.perf_counter()

        graph.query("""
            CREATE (:BenchmarkTemp {id: $id})
        """, params={"id": f"{client_id}_{i}"})

        times.append((time.perf_counter() - start) * 1000)

    return times


print("=" * 50)
print("FalkorDB Mixed Read/Write Benchmark")
print("=" * 50)

start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=CLIENTS) as executor:
    results = list(executor.map(worker, range(CLIENTS)))

total_time = time.perf_counter() - start_time

all_times = []

for result in results:
    all_times.extend(result)

all_times.sort()

total_operations = CLIENTS * OPERATIONS_PER_CLIENT * 2
qps = total_operations / total_time

p50 = statistics.median(all_times)

p95_index = int(0.95 * len(all_times)) - 1
p95 = all_times[max(0, p95_index)]

print("\n" + "=" * 50)
print("MIXED READ/WRITE COMPLETED")
print("=" * 50)

print(f"Clients              : {CLIENTS}")
print(f"Operations           : {total_operations}")
print(f"Total Time           : {total_time:.2f} seconds")
print(f"Throughput (QPS)     : {qps:.2f}")
print(f"Average Latency      : {statistics.mean(all_times):.2f} ms")
print(f"P50 Latency          : {p50:.2f} ms")
print(f"P95 Latency          : {p95:.2f} ms")

# Clean up temporary graph
client = create_client()
graph = client.select_graph("mixed_test")

graph.query("""
MATCH (n:BenchmarkTemp)
DELETE n
""")

print("\nTemporary benchmark data cleaned up.")
