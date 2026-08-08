from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

# --------------------------------------------------
# Settings
# --------------------------------------------------

from config import POKEC_FILE

FILE_PATH = POKEC_FILE

BATCH_SIZE = 1000

# Already imported successfully
ALREADY_IMPORTED = 97000

# Total we want
MAX_RELATIONSHIPS = 100000

# --------------------------------------------------
# Query
# --------------------------------------------------

IMPORT_QUERY = """
UNWIND $rows AS row
MERGE (a:Person {id: row.source})
MERGE (b:Person {id: row.target})
MERGE (a)-[:KNOWS]->(b)
"""

# --------------------------------------------------
# Import
# --------------------------------------------------

def import_graph():

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    total_seen = 0
    imported = ALREADY_IMPORTED
    batch = []

    try:

        with driver.session() as session:

            print("=" * 50)
            print("RESUMING NEO4J IMPORT")
            print("=" * 50)
            print(f"Already imported : {ALREADY_IMPORTED:,}")
            print(f"Target           : {MAX_RELATIONSHIPS:,}")
            print("=" * 50)

            with open(FILE_PATH, "r", encoding="utf-8") as file:

                for line in file:

                    # Skip comments
                    if line.startswith("#"):
                        continue

                    parts = line.strip().split()

                    if len(parts) != 2:
                        continue

                    total_seen += 1

                    # Skip relationships already imported
                    if total_seen <= ALREADY_IMPORTED:
                        continue

                    source = parts[0]
                    target = parts[1]

                    batch.append({
                        "source": source,
                        "target": target
                    })

                    if len(batch) >= BATCH_SIZE:

                        session.run(
                            IMPORT_QUERY,
                            rows=batch
                        ).consume()

                        imported += len(batch)

                        print(f"Imported {imported:,} relationships")

                        batch = []

                        if imported >= MAX_RELATIONSHIPS:
                            break

                # Remaining batch
                if batch and imported < MAX_RELATIONSHIPS:

                    remaining = MAX_RELATIONSHIPS - imported

                    batch = batch[:remaining]

                    session.run(
                        IMPORT_QUERY,
                        rows=batch
                    ).consume()

                    imported += len(batch)

            print("\n" + "=" * 50)
            print("IMPORT COMPLETED SUCCESSFULLY")
            print("=" * 50)
            print(f"Relationships Imported : {imported:,}")

    except Exception as e:

        print("\nIMPORT STOPPED")
        print(f"Relationships safely imported so far: {imported:,}")
        print("Error:", e)

    finally:
        driver.close()


if __name__ == "__main__":
    import_graph()