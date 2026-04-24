#!/usr/bin/env bash
set -euo pipefail

# Wait for Neo4j Bolt to be reachable from this one-shot seeder container.
until cypher-shell -a bolt://neo4j:7687 -u neo4j -p password "RETURN 1" >/dev/null 2>&1; do
  sleep 2
done

# Neo4j community supports one user database; seed the default neo4j database.
cypher-shell -a bolt://neo4j:7687 -u neo4j -p password -d neo4j < /seed/appdbprojNeo4j.json

echo "Neo4j seed completed."

