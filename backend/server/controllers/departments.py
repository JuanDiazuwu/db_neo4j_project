from neo4j import GraphDatabase
from server.models.department import Department

#URI = "neo4j://neo4j:7687"
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)

async def index_department(deptno:int) -> dict:
    with driver.session() as session:
        cyp = "MATCH (d:DEPT {DEPTNO: $DEPTNO}) RETURN d"
        result = session.run(cyp, {"DEPTNO": deptno}).single()
        if result:
            department_node = result["d"]
            department_data = {
                "DEPTNO": department_node["DEPTNO"],
                "DNAME": department_node["DNAME"],
                "LOC": department_node["LOC"]
            }
            return department_data
    return None

async def list_departments():
    with driver.session() as session:
        cyp = "MATCH (d:DEPT) RETURN d"
        result = session.run(cyp)
        departments = []
        for record in result:
            department_node = record["d"]
            department_data = {
                "DEPTNO": department_node["DEPTNO"],
                "DNAME": department_node["DNAME"],
                "LOC": department_node["LOC"]
            }
            departments.append(department_data)
    return departments

async def create_department(department: Department) -> dict:
    if not await is_deptno_unique(department.DEPTNO):
        return None

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

async def replace_department(deptno:id, data) -> dict:
    with driver.session() as session:
        # Create the SET clause dynamically based on provided data
        set_clauses = [f"d.{key} = ${key}" for key in data.keys()]
        set_clause = ", ".join(set_clauses)
        
        cyp: str = (
            f"""
            MATCH (d:DEPT {{DEPTNO: $DEPTNO}})
            SET {set_clause}
            RETURN d
            """
        )
        
        params_dict = {"DEPTNO": deptno}
        params_dict.update(data)
        
        result = session.run(cyp, params_dict).single()
        if result:
            department_node = result["d"]
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
    
async def is_deptno_unique(deptno:int) -> bool:
    with driver.session() as session:
        cyp = "MATCH (e:DEPT {DEPTNO: $DEPTNO}) RETURN e"
        result = session.run(cyp, {"DEPTNO": deptno}).single()
        return result is None