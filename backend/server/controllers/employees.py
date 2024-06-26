from neo4j import GraphDatabase
from server.models.employee import Employee

#URI = "neo4j://neo4j:7687"
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)

async def index_employee(empno:int):
    with driver.session() as session:
        cyp = "MATCH (e:EMP {EMPNO: $EMPNO}) RETURN e"
        result = session.run(cyp, {"EMPNO": empno}).single()
        if result:
            employee_node = result["e"]
            employee_data = {
                "EMPNO": employee_node["EMPNO"],
                "ENAME": employee_node["ENAME"],
                "JOB": employee_node["JOB"],
                "MGR": employee_node.get("MGR"),
                "HIREDATE": str(employee_node["HIREDATE"]),
                "SAL": employee_node["SAL"],
                "COMM": employee_node["COMM"],
                "DEPTNO": employee_node["DEPTNO"]
            }
            return employee_data
    return None

async def list_employees():
    with driver.session() as session:
        cyp = "MATCH (e:EMP) RETURN e"
        results = session.run(cyp)
        employees = []
        for record in results:
            employee_node = record["e"]
            employee_data = {
                "EMPNO": employee_node["EMPNO"],
                "ENAME": employee_node["ENAME"],
                "JOB": employee_node["JOB"],
                "MGR": employee_node["MGR"],
                "HIREDATE": str(employee_node["HIREDATE"]),
                "SAL": employee_node["SAL"],
                "COMM": employee_node["COMM"],
                "DEPTNO": employee_node["DEPTNO"]
            }
            employees.append(employee_data)
        return employees if employees else None

async def create_employee(employee: Employee) -> dict:
    if not await is_empno_unique(employee.EMPNO):
        return None

    with driver.session() as session:
        cyp: str = (
            """
            CREATE (e:EMP {
                EMPNO: $EMPNO,
                ENAME: $ENAME,
                JOB: $JOB,
                MGR: $MGR,
                HIREDATE: date($HIREDATE),
                SAL: $SAL,
                COMM: $COMM,
                DEPTNO: $DEPTNO
            })
            RETURN e
            """
        )
        params_dict: dict = {
            "EMPNO": employee.EMPNO,
            "ENAME": employee.ENAME,
            "JOB": employee.JOB,
            "MGR": employee.MGR,
            "HIREDATE": employee.HIREDATE,
            "SAL": employee.SAL,
            "COMM": employee.COMM,
            "DEPTNO": employee.DEPTNO
        }
        result = session.run(cyp, params_dict).single()
        if result:
            employee_node = result["e"]
            #department_number = result["DEPTNO"]
            # Convert Neo4j date to string
            employee_data = {
                "EMPNO": employee_node["EMPNO"],
                "ENAME": employee_node["ENAME"],
                "JOB": employee_node["JOB"],
                "MGR": employee_node["MGR"],
                "HIREDATE": str(employee_node["HIREDATE"]),
                "SAL": employee_node["SAL"],
                "COMM": employee_node["COMM"],
                "DEPTNO": employee_node["DEPTNO"]
            }
            return employee_data
    return None

async def replace_employee(empno:id, data): #TODO type the data
    with driver.session() as session:
        set_clauses = [f"e.{key} = ${key}" for key in data.keys()]
        set_clause = ", ".join(set_clauses)
        
        cyp: str = (
            f"""
            MATCH (e:EMP {{EMPNO: $EMPNO}})
            SET {set_clause}
            RETURN e
            """
        )
        
        params_dict = {"EMPNO": empno}
        params_dict.update(data)
        
        result = session.run(cyp, params_dict).single()
        if result:
            employee_node = result["e"]
            employee_data = {
                "EMPNO": employee_node["EMPNO"],
                "ENAME": employee_node["ENAME"],
                "JOB": employee_node["JOB"],
                "MGR": employee_node["MGR"],
                "HIREDATE": str(employee_node["HIREDATE"]),
                "SAL": employee_node["SAL"],
                "COMM": employee_node["COMM"],
                "DEPTNO": employee_node["DEPTNO"]
            }
            if "DEPTNO" in data:
                old_deptno_cyp = (
                    """
                    MATCH (e:EMP {EMPNO: $EMPNO})-[r:WORKS_IN]->()
                    DELETE r
                    """
                )
                session.run(old_deptno_cyp, {"EMPNO": empno})
                new_deptno_cyp = (
                    """
                    MATCH (e:EMP {EMPNO: $EMPNO})
                    MATCH (d:DEPT {DEPTNO: $DEPTNO})
                    MERGE (e)-[:WORKS_IN]->(d)
                    RETURN e, d
                    """
                )
                session.run(new_deptno_cyp, {"EMPNO": empno, "DEPTNO": data["DEPTNO"]})
                employee_data["DEPTNO"] = data["DEPTNO"]

            # Handle MGR change
            if "MGR" in data:
                old_mgr_cyp = (
                    """
                    MATCH (:EMP)-[r:MANAGES]->(e:EMP {EMPNO: $EMPNO})
                    DELETE r
                    """
                )
                session.run(old_mgr_cyp, {"EMPNO": empno})
                if data["MGR"]:
                    new_mgr_cyp = (
                        """
                        MATCH (e:EMP {EMPNO: $EMPNO})
                        MATCH (m:EMP {EMPNO: $MGRNO})
                        MERGE (m)-[:MANAGES]->(e)
                        RETURN e, m
                        """
                    )
                    session.run(new_mgr_cyp, {"EMPNO": empno, "MGRNO": data["MGR"]})
                    employee_data["MGR"] = data["MGR"]
        return employee_data
    return None

async def destroy_employee(empno):
    with driver.session() as session:
        cyp = "MATCH (e:EMP {EMPNO: $EMPNO}) DELETE e"
        result = session.run(cyp, {"EMPNO": empno})
        return result.consume().counters.nodes_deleted > 0
    
# auxiliary functions
async def assign_employee_to_department(empno: int, deptno: int) -> bool:
    with driver.session() as session:
        cyp: str = (
            """
            MATCH (e:EMP {EMPNO: $EMPNO})
            MATCH (d:DEPT {DEPTNO: $DEPTNO})
            MERGE (e)-[:WORKS_IN]->(d)
            RETURN e, d
            """
        )
        params_dict: dict = {
            "EMPNO": empno,
            "DEPTNO": deptno
        }
        result = session.run(cyp, params_dict).consume()
        return result.counters.relationships_created > 0

async def delete_employee_department_relation(empno:int) -> bool:
    with driver.session() as session:
        cyp: str = (
            """
            MATCH (e:EMP {EMPNO: $EMPNO})-[r:WORKS_IN]->(d:DEPT)
            DELETE r
            RETURN e, d
            """
        )
        params_dict: dict = {"EMPNO": empno}
        result = session.run(cyp, params_dict).consume()
        return result.counters.relationships_deleted > 0
    
async def assing_manager(empno:int, mgrno:int) -> bool:
    with driver.session() as session:
        cyp: str = (
            """
            MATCH (e:EMP {EMPNO: $EMPNO})
            MATCH (m:EMP {EMPNO: $MGRNO})
            MERGE (m)-[:MANAGES]->(e)
            RETURN e, m
            """
        )
        params_dict: dict = {
            "EMPNO": empno,
            "MGRNO": mgrno
        }
        result = session.run(cyp, params_dict).consume()
        return result.counters.relationships_created > 0

async def is_empno_unique(empno:int) -> bool:
    with driver.session() as session:
        cyp = "MATCH (e:EMP {EMPNO: $EMPNO}) RETURN e"
        result = session.run(cyp, {"EMPNO": empno}).single()
        return result is None

async def delete_manager_relationship(empno:int) -> bool:
    with driver.session() as session:
        cyp = """
        MATCH (m:EMP)-[r:MANAGES]->(e:EMP {EMPNO: $EMPNO})
        DELETE r
        RETURN e
        """
        result = session.run(cyp, {"EMPNO": empno}).single()
        return result is not None
    
async def delete_subordinate_relationships(empno: int) -> bool:
    with driver.session() as session:
        cyp = """
        MATCH (m:EMP {EMPNO: $EMPNO})-[r:MANAGES]->(e:EMP)
        DELETE r
        RETURN m
        """
        result = session.run(cyp, {"EMPNO": empno}).single()
        return result is not None
