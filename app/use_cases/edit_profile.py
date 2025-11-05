from app.db import * 

def edit_profile(username):
    cypher = """
    MATCH (u:User {username: $username})
    SET u.name     = coalesce($name, u.name),
        u.email    = coalesce($email, u.email),
        u.password = coalesce($password, u.password)
    RETURN u
    """

    name = input("Enter new name: ").strip()
    email = input("Enter new email: ").strip()
    password = input("Enter new password: ").strip()


    with session() as s:
        record = s.run(cypher, username=username, name=name, email=email, password=password).single()
        res = f"""
        --- Profile Updated ___ 
        Name: {record['u']['name']}
        Username: {record['u']['username']}
        Email: {record['u']['email']}
        ---------------------------"""
        print(res)