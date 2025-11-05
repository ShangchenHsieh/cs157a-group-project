from app.db import * 

def view_profile(username):
    cypher = """
    MATCH (u:User)
    WHERE u.username = $username
    RETURN u
    """
    with session() as s:
        record = s.run(cypher, username=username).single()

        res = f"""
        --- Profile Information ___ 
        Name: {record['u']['name']}
        Username: {record['u']['username']}
        Email: {record['u']['email']}
        ---------------------------"""
        print(res)