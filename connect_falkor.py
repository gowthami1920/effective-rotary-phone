from falkordb import FalkorDB



from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
client = FalkorDB(
    host=FALKORDB_HOST,
    port=FALKORDB_PORT,
    username=FALKORDB_USERNAME,
    password=FALKORDB_PASSWORD
)

graph = client.select_graph("benchmark")

result = graph.query("RETURN 1 AS test")

print("FalkorDB connection successful!")
print(result.result_set)
