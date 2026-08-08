from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, POKEC_FILE

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

with driver.session() as session:
    with open(POKEC_FILE, "r", encoding="utf-8") as file:
        count = 0

        for line in file:
            parts = line.strip().split()

            if len(parts) != 2:
                continue

            from_id = int(parts[0])
            to_id = int(parts[1])

            session.run("""
                MERGE (a:Person {id:$from_id})
                MERGE (b:Person {id:$to_id})
                MERGE (a)-[:KNOWS]->(b)
            """, from_id=from_id, to_id=to_id)

            count += 1

            if count % 500 == 0:
                print(f"Loaded {count} relationships")

print("✅ Import Completed!")

driver.close()