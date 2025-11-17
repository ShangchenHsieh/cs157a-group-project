# app/use_cases/mutual_connections.py
from app.db import session

def find_mutual_connections(username_a: str, username_b: str):
    """
    Finds and prints all users that both username_a and username_b follow.
    
    Args:
        username_a: The username of the logged-in user.
        username_b: The username of the user to compare against.
    """
    
    if username_a == username_b:
        print("\nError: You cannot find mutual connections with yourself.\n")
        return

    with session() as s:
        try:
            check_user = s.run("MATCH (u:User {username: $username}) RETURN u", username=username_b)
            if not check_user.single():
                print(f"\nError: User '{username_b}' does not exist.\n")
                return

            query = """
            MATCH (a:User {username: $username_a})-[:FOLLOWS]->(m:User)
            WITH m
            MATCH (b:User {username: $username_b})-[:FOLLOWS]->(m)
            RETURN m.username AS username, m.name AS name
            ORDER BY m.name
            """
            
            results = s.run(query, username_a=username_a, username_b=username_b)
            
            mutuals = [record.data() for record in results]
            
            if not mutuals:
                print(f"\nYou and {username_b} have no mutual connections.\n")
            else:
                print(f"\n--- Mutual Connections with {username_b} ---")
                for user in mutuals:
                    print(f"  * {user['name']} (@{user['username']})")
                print("------------------------------------------\n")

        except Exception as e:
            print(f"\nAn error occurred: {e}\n")