from neo4j import GraphDatabase
from server.models.department import Department

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)

async def create_department(department: Department) -> dict:
    with driver.session() as session:
        cyp: str = (
            """
            CREATE (e:DEPT {
                deptno: $deptno,
                dname: $dname,
                loc: $loc
            })
            RETURN e
            """
        )
        params_dict: dict = {
            "deptno": department.deptno,
            "dname": department.dname,
            "loc": department.loc
        }
        result = session.run(cyp, params_dict).single()
        if result:
            department_node = result["e"]
            # Convert Neo4j date to string
            department_data = {
                "deptno": department_node["deptno"],
                "dname": department_node["dname"],
                "loc": department_node["loc"]
            }
            return department_data
    return None