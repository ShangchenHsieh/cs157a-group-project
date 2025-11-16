from app.db import session


def view_friends(username: str) -> None:
    follower = username

    cypher_check = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)
    RETURN a IS NOT NULL AS has_follower, b IS NOT NULL AS friends
    """

    cypher_friends = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)
    RETURN b.username AS Friends
    """

    with session() as s:
        record = s.run(cypher_check, follower=follower).single()
        if not record:
            print("Could not verify user - user may not exist")
            return
        if not record.get('has_follower'):
            print(f"Follower user '{follower}' does not exist.")
            return
        if not record.get('friends'):
            print(f"Follower user '{follower}' does not follow anyone")
            return

        res = s.run(cypher_friends, follower=follower)
        if res:
            print("------Friends------")
            n = 0

            for rec in res.data():
                n = n + 1
                print(f"-   {n}.  {rec['Friends']}")
        else:
            print("Failed search - check logs or DB connectivity.")
