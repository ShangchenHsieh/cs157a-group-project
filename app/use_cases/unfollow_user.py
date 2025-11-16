from app.db import session


def unfollow_user(username: str) -> None:
    follower = username
    followee = input("Enter the username of the user you want to unfollow: ").strip()
    if not followee:
        print("No username entered — aborting.")
        return

    cypher_check = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b:User {username: $followee})
    RETURN a IS NOT NULL AS has_follower, b IS NOT NULL AS has_followee, r IS NOT NULL AS followed
    """

    cypher_unfollow = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b:User {username: $followee})
    DELETE r
    """

    with session() as s:
        record = s.run(cypher_check, follower=follower, followee=followee).single()
        if not record:
            print("Could not verify users — make sure both accounts exist.")
            return
        if not record.get('has_follower'):
            print(f"Follower user '{follower}' does not exist.")
            return
        if not record.get('has_followee'):
            print(f"Target user '{followee}' does not exist.")
            return
        if not record.get('followed'):
            print(f"Target user '{followe}' does not follow 'Follower user '{follower}")
            return

        s.run(cypher_unfollow, follower=follower, followee=followee).single()
        print("Failed to delete FOLLOW relationship — check logs or DB connectivity.")
