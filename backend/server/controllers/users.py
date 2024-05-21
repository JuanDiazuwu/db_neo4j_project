from neo4j import GraphDatabase

URI = "neo4j://localhost"
AUTH = ("neo4j", "password")

driver = GraphDatabase.driver(URI, auth=AUTH)

async def create_user(user) -> dict:
    with driver.session() as session:
        cyp: str = (
            "CREATE (employee:Employee {name:$name,emp_id:$emp_id} ) "
            "RETURN employee.name AS name, employee.emp_id as emp_id;"
        )
        params_dict: dict = {"name": user.name, "emp_id": user.emp_id}
        session = driver.session()
        result: dict = session.run(cyp, params_dict).data()
    return result