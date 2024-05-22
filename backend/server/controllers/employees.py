from neo4j import GraphDatabase
from server.models.employee import Employee

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
                "MGR": employee_node["MGR"],
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
    pass

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