from app.db import session


def rec_friends(username: str) -> None:
    follower = username

    cypher_check = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)-[r1:FOLLOWS]->(common)
    RETURN a IS NOT NULL AS has_follower, b IS NOT NULL AS friends, r IS NOT NULL AS follows, r1 IS NOT NULL AS friend_follows, common AS friend_recs
    """

    cypher_friends = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)-[r1:FOLLOWS]->(common)
    RETURN common.username AS friend_rec
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
        if not record.get('friend_recs'):
            print(f"Follower user '{follower}' does not have any friend recs")
            return

        res = s.run(cypher_friends, follower=follower)
        if res:
            print("------Follower Recommendation------")
            n = 0
            for rec in res.data():
                n = n + 1
                print(f"-   {n}.  {rec['friend_rec']}")
        else:
            print("Failed search - check logs or DB connectivity.")
