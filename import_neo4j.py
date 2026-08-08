from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE, POKEC_FILE
import time

FILE_PATH = POKEC_FILE

BATCH_SIZE = 200
START_AFTER = 9000
MAX_RELATIONSHIPS = 100000

IMPORT_QUERY = """
UNWIND $rows AS row
MERGE (a:Person {id: row.source})
MERGE (b:Person {id: row.target})
MERGE (a)-[:KNOWS]->(b)
"""


def create_driver():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        max_connection_lifetime=300
    )


def import_graph():

    driver = create_driver()

    try:

        batch = []
        total_read = 0
        imported = START_AFTER

        with open(FILE_PATH, "r", encoding="utf-8") as file:

            for line in file:

                if line.startswith("#"):
                    continue

                parts = line.strip().split()

                if len(parts) != 2:
                    continue

                total_read += 1

                # Skip relationships already imported
                if total_read <= START_AFTER:
                    continue

                if imported >= MAX_RELATIONSHIPS:
                    break

                batch.append({
                    "source": parts[0],
                    "target": parts[1]
                })

                if len(batch) >= BATCH_SIZE:

                    success = False

                    for attempt in range(5):

                        try:

                            with driver.session(database=NEO4J_DATABASE) as session:

                                session.run(
                                    IMPORT_QUERY,
                                    rows=batch
                                ).consume()

                            success = True
                            break

                        except Exception as e:

                            print(
                                f"Connection problem. "
                                f"Retry {attempt + 1}/5..."
                            )

                            time.sleep(3)

                            driver.close()
                            driver = create_driver()

                    if not success:
                        print("\nIMPORT STOPPED")
                        print(f"Successfully imported up to approximately: {imported:,}")
                        return

                    imported += len(batch)

                    print(
                        f"Imported {imported:,} relationships"
                    )

                    batch = []

        # Remaining rows
        if batch and imported < MAX_RELATIONSHIPS:

            remaining = MAX_RELATIONSHIPS - imported
            batch = batch[:remaining]

            with driver.session(database=NEO4J_DATABASE) as session:

                session.run(
                    IMPORT_QUERY,
                    rows=batch
                ).consume()

            imported += len(batch)

        print("\n" + "=" * 50)
        print("NEO4J IMPORT COMPLETED")
        print("=" * 50)
        print(f"Relationships Imported: {imported:,}")

    finally:
        driver.close()


if __name__ == "__main__":
    import_graph()