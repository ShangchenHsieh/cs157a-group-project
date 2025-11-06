from app.db import session


def follow_user(username: str) -> None:
    follower = username
    followee = input("Enter the username of the user you want to follow: ").strip()
    if not followee:
        print("No username entered — aborting.")
        return

    cypher_check = """
    MATCH (a:User {username: $follower}), (b:User {username: $followee})
    RETURN a IS NOT NULL AS has_follower, b IS NOT NULL AS has_followee
    """

    cypher_follow = """
    MATCH (a:User {username: $follower}), (b:User {username: $followee})
    MERGE (a)-[r:FOLLOW]->(b)
    RETURN a.username AS follower, b.username AS followee, type(r) AS rel
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

        res = s.run(cypher_follow, follower=follower, followee=followee).single()
        if res:
            print(f"{res['follower']} now follows {res['followee']}.")
        else:
            print("Failed to create FOLLOW relationship — check logs or DB connectivity.")