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
                DEPTNO: $DEPTNO,
                DNAME: $DNAME,
                LOC: $LOC
            })
            RETURN e
            """
        )
        params_dict: dict = {
            "DEPTNO": department.DEPTNO,
            "DNAME": department.DNAME,
            "LOC": department.LOC
        }
        result = session.run(cyp, params_dict).single()
        if result:
            department_node = result["e"]
            department_data = {
                "DEPTNO": department_node["DEPTNO"],
                "DNAME": department_node["DNAME"],
                "LOC": department_node["LOC"]
            }
            return department_data
    return None

async def destroy_department(deptno) -> bool:
    with driver.session() as session:
        cyp_check = (
            """
            MATCH (d:DEPT {DEPTNO: $DEPTNO})<-[:WORKS_IN]-(:EMP)
            RETURN COUNT(*) AS rel_count
            """
        )
        check_result = session.run(cyp_check, {"DEPTNO": deptno}).single()
        if check_result["rel_count"] > 0:
            return False

        cyp = "MATCH (e:DEPT {DEPTNO: $DEPTNO}) DELETE e"
        result = session.run(cyp, {"DEPTNO": deptno})
        return result.consume().counters.nodes_deleted > 0