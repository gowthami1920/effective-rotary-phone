
from neo4j import GraphDatabase
from config import COGNODB_URI, COGNODB_USERNAME, COGNODB_PASSWORD

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)

try:
    driver.verify_connectivity()
    print("✅ Connected to CognoDB successfully!")
finally:
    driver.close()