from neo4j import GraphDatabase
from config import URI, USERNAME, PASSWORD

FILE_PATH = r"C:\Users\nalla\Downloads\soc-pokec-relationships.txt\soc-pokec-relationships.txt"

BATCH_SIZE = 1000
SKIP_RELATIONSHIPS = 90000
TARGET_RELATIONSHIPS = 100000

IMPORT_QUERY = """
UNWIND $rows AS row
MERGE (a:Person {id: row.source})
MERGE (b:Person {id: row.target})
MERGE (a)-[:KNOWS]->(b)
"""

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def resume_import():

    with driver.session() as session:

        print("Resuming from 90,000 relationships...")

        batch = []
        skipped = 0
        imported = 0

        with open(FILE_PATH, "r", encoding="utf-8") as file:

            for line in file:

                if line.startswith("#"):
                    continue

                parts = line.strip().split()

                if len(parts) != 2:
                    continue

                # Skip the first 90,000 already imported
                if skipped < SKIP_RELATIONSHIPS:
                    skipped += 1
                    continue

                if imported >= TARGET_RELATIONSHIPS - SKIP_RELATIONSHIPS:
                    break

                batch.append({
                    "source": parts[0],
                    "target": parts[1]
                })

                if len(batch) >= BATCH_SIZE:

                    session.run(
                        IMPORT_QUERY,
                        rows=batch
                    ).consume()

                    imported += len(batch)

                    print(
                        f"New relationships imported: "
                        f"{imported:,} "
                        f"(Total: {SKIP_RELATIONSHIPS + imported:,})"
                    )

                    batch = []

        if batch:
            session.run(
                IMPORT_QUERY,
                rows=batch
            ).consume()

            imported += len(batch)

            print(
                f"New relationships imported: "
                f"{imported:,} "
                f"(Total: {SKIP_RELATIONSHIPS + imported:,})"
            )

        print("\nIMPORT COMPLETED")
        print(f"Total relationships: {SKIP_RELATIONSHIPS + imported:,}")


if __name__ == "__main__":
    try:
        resume_import()
    finally:
        driver.close()