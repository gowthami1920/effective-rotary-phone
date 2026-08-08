from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

# Check the Neo4j-compatible graph database connection
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

# Open session WITHOUT specifying a database
with driver.session() as session:

    # Count nodes
    result = session.run("""
        MATCH (n)
        RETURN count(n) AS nodes
    """)

    print("Nodes:", result.single()["nodes"])

    # Count relationships
    result = session.run("""
        MATCH ()-[r]->()
        RETURN count(r) AS relationships
    """)

    print("Relationships:", result.single()["relationships"])

driver.close()

print("Connection and database check completed successfully!")