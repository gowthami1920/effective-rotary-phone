# -----------------------------
# Benchmark Queries
# -----------------------------

# Count all Person nodes
COUNT_NODES = """
MATCH (p:Person)
RETURN count(p) AS count
"""

# Point Lookup
POINT_LOOKUP = """
MATCH (p:Person {id: $id})
RETURN p
"""

# 1-Hop Traversal
ONE_HOP = """
MATCH (p:Person {id: $id})-[:KNOWS]->(friend)
RETURN friend
"""

# 2-Hop Traversal
TWO_HOP = """
MATCH (p:Person {id: $id})-[:KNOWS]->()-[:KNOWS]->(friend)
RETURN friend
"""

# 3-Hop Traversal
THREE_HOP = """
MATCH (p:Person {id: $id})-[:KNOWS]->()-[:KNOWS]->()-[:KNOWS]->(friend)
RETURN friend
"""

# Aggregation (Top 10 most connected persons)
AGGREGATION = """
MATCH (p:Person)-[:KNOWS]->(friend)
RETURN p.id AS Person, count(friend) AS Friends
ORDER BY Friends DESC
LIMIT 10
"""