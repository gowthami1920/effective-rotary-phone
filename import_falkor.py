from falkordb import FalkorDB
import time



from config import FALKORDB_HOST, FALKORDB_PORT, FALKORDB_USERNAME, FALKORDB_PASSWORD
from config import POKEC_FILE

FILE_PATH = POKEC_FILE

BATCH_SIZE = 200
START_AFTER = 27000
MAX_RELATIONSHIPS = 100000

client = FalkorDB(
    host=FALKORDB_HOST,
    port=FALKORDB_PORT,
    username=FALKORDB_USERNAME,
    password=FALKORDB_PASSWORD
)

graph = client.select_graph("benchmark")


QUERY = """
UNWIND $rows AS row
MERGE (a:Person {id: row.source})
MERGE (b:Person {id: row.target})
MERGE (a)-[:KNOWS]->(b)
"""


def import_graph():

    batch = []
    total = 0

    print("=" * 50)
    print("Starting FalkorDB import...")
    print("=" * 50)

    with open(FILE_PATH, "r", encoding="utf-8") as file:

        for line in file:

            if line.startswith("#"):
                continue

            parts = line.strip().split()

            if len(parts) != 2:
                continue

            batch.append({
                "source": parts[0],
                "target": parts[1]
            })

            if len(batch) >= BATCH_SIZE:

                graph.query(
                    QUERY,
                    params={"rows": batch}
                )

                total += len(batch)

                print(f"Imported {total:,} relationships")

                batch = []

                if total >= MAX_RELATIONSHIPS:
                    break

    if batch and total < MAX_RELATIONSHIPS:

        remaining = MAX_RELATIONSHIPS - total

        graph.query(
            QUERY,
            params={"rows": batch[:remaining]}
        )

        total += min(len(batch), remaining)

    print("\n" + "=" * 50)
    print("FALKORDB IMPORT COMPLETED")
    print("=" * 50)
    print(f"Relationships Imported: {total:,}")


if __name__ == "__main__":
    import_graph()
