import os

# Database connection settings are read from environment variables.
# NEVER put real passwords or API keys in this file.

NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "")

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
FALKORDB_USERNAME = os.getenv("FALKORDB_USERNAME", "")
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", "")

COGNODB_URI = os.getenv("COGNODB_URI", "")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME", "")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD", "")

POKEC_FILE = os.getenv("POKEC_FILE", "data/pokec_sample.tsv")
