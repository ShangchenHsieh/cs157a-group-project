from app.db import * 

def register(username: str, password: str, name: str, email: str) -> bool:
   # 1) Reject duplicate username
    check_cypher = """
    MATCH (u:User {username: $username})
    RETURN u.username AS username
    """
    create_cypher = """
    CREATE (u:User {
        username: $username,
        password: $password,
        name:     $name,
        email:    $email
    })
    RETURN u
    """
    with session() as s:
        existing = s.run(check_cypher, username=username).single()
        if existing:
            print(f"Registration failed: username '{username}' is already taken.")
            return False

        record = s.run(
            create_cypher,
            username=username,
            password=password,  # WARNING: plain text, for demo only
            name=name,
            email=email
        ).single()

        if record and record["u"]:
            print(record['u']["username"] + " — registered successfully!")
            return True

        print("Registration failed: unexpected error.")
        return False