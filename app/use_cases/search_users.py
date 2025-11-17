from app.db import session

def search_users(search_term: str):
    """
    Finds users by a search term, matching against username or name.
    (UC-10: Search Users)
    
    Args:
        search_term: The string to search for.
    """
    
    # Using CONTAINS for partial, case-insensitive matching
    query = """
    MATCH (u:User)
    WHERE toLower(u.username) CONTAINS toLower($term)
       OR toLower(u.name) CONTAINS toLower($term)
    RETURN u.username AS username, u.name AS name
    ORDER BY u.name
    """
    
    with session() as s:
        try:
            results = s.run(query, term=search_term)
            users = [record.data() for record in results]
            
            if not users:
                print(f"\nNo users found matching '{search_term}'.\n")
            else:
                print(f"\n--- Search Results for '{search_term}' ---")
                for user in users:
                    print(f"  * {user['name']} (@{user['username']})")
                print("-------------------------------------------\n")

        except Exception as e:
            print(f"\nAn error occurred during search: {e}\n")