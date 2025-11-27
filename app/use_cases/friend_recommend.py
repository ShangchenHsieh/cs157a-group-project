from app.db import session


def rec_friends(username: str) -> None:
    follower = username

    follow_check = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)
    RETURN a IS NOT NULL AS has_follower, b IS NOT NULL AS friends
    """

    cypher_friends = """
    MATCH (a:User {username: $follower})-[r:FOLLOWS]->(b)-[r1:FOLLOWS]->(common)
    RETURN common AS friend_rec
    """

    with session() as s:
        results = s.run(follow_check, follower=follower)

        if not results:
            print("Could not verify user - user may not exist")
            return

        users_friends = [record['friends'] for record in results]

        if not users_friends:
            print(f"Follower user '{follower}' does not have any friend recs")
            return

        res = s.run(cypher_friends, follower=follower).data()

        if res:
            print("------Follower Recommendation------")
            n = 0
            for rec in res:
                n = n + 1
                print(f"-   {n}.  {rec['friend_rec']['username']}")
        else:
            print("User's friends does have any friends")
