from app.db import session

def explore_popular_users():
    """
    Finds and displays the top 10 most-followed users.
    (UC-11: Explore Popular Users)
    """
    
    # This query counts incoming :FOLLOWS relationships for each user,
    # orders by that count descending, and takes the top 10.
    query = """
    MATCH (u:User)
    OPTIONAL MATCH (follower:User)-[:FOLLOWS]->(u)
    WITH u, count(follower) AS follower_count
    WHERE follower_count > 0
    RETURN u.username AS username, u.name AS name, follower_count
    ORDER BY follower_count DESC
    LIMIT 10
    """
    
    with session() as s:
        try:
            results = s.run(query)
            users = [record.data() for record in results]
            
            if not users:
                print("\nNo users have any followers yet.\n")
            else:
                print("\n--- Top 10 Popular Users ---")
                for i, user in enumerate(users):
                    print(f"  {i+1}. {user['name']} (@{user['username']}) - {user['follower_count']} followers")
                print("------------------------------\n")

        except Exception as e:
            print(f"\nAn error occurred while finding popular users: {e}\n")