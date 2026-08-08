from falkordb import FalkorDB


from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
client = FalkorDB(
    host=FALKORDB_HOST,
    port=FALKORDB_PORT,
    username=FALKORDB_USERNAME,
    password=FALKORDB_PASSWORD
)

graph = client.select_graph("benchmark")

nodes = graph.query("""
MATCH (n)
RETURN count(n) AS nodes
""")

relationships = graph.query("""
MATCH ()-[r]->()
RETURN count(r) AS relationships
""")

print("Nodes:", nodes.result_set[0][0])
print("Relationships:", relationships.result_set[0][0])

print("FalkorDB check completed successfully!")
