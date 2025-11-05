from app.db import * 

def login(username: str, password: str) -> bool:
    cypher = (
        "MATCH (u:User {username: $username, password: $password})\n"
        "RETURN u"
    )
    with session() as s:
        record = s.run(cypher, username=username, password=password).single()
        if record: 

            print(record["u"]['username'] + " — welcome back!")
            return True
        else: 
            print("Login failed: Invalid credentials.")
            return False