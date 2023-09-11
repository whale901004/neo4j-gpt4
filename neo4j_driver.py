import os
from neo4j import GraphDatabase

host = os.environ.get('NEO4J_URL', 'bolt://localhost:7687')
user = os.environ.get('NEO4J_USER', 'neo4j')
password = os.environ.get('NEO4J_PASS', '12345678')
driver = GraphDatabase.driver(host, auth=(user, password))


def run_query(query, params={}):
    with driver.session() as session:
        result = session.run(query, params)
        response = [r.values()[0] for r in result]
        return response


if __name__ == '__main__':
    print(run_query("""
    MATCH (d:Disease {name:"肺氣腫"})-[:has_symptom]->(s)
    RETURN {Symptom:s.name} AS result;
    """))
