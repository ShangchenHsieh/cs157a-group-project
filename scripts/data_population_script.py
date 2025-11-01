"""Populate Neo4j with users from CSV and synthetic users to reach targets.

Creates User nodes (fields: username, name, email, password) and FOLLOWS
relationships between them. Designed to be idempotent (uses MERGE).

Run:
    python scripts/data_population_script.py --csv data/farmaciavernile.it.csv

"""
from __future__ import annotations

import csv
import os
import random
import argparse
from typing import List, Dict, Set, Tuple
from math import ceil
from app.db import *


TARGET_NODES = 1000
TARGET_RELATIONSHIPS = 5000
BATCH_SIZE = 200


def load_users_from_csv(csv_path: str) -> List[Dict[str, str]]:
    users: List[Dict[str, str]] = []
    seen: Set[str] = set()
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            username = (row.get('username') or row.get('user') or '').strip()
            if not username:
                continue
            if username in seen:
                continue
            seen.add(username)
            users.append({
                'username': username,
                'name': (row.get('name') or '').strip(),
                'email': (row.get('email') or '').strip(),
                'password': (row.get('password') or '').strip(),
            })
    return users


def synthesize_users(existing_usernames: Set[str], needed: int, start_index: int = 1) -> List[Dict[str, str]]:
    users = []
    i = start_index
    while len(users) < needed:
        username = f"synthetic_user_{i}"
        if username in existing_usernames:
            i += 1
            continue
        users.append({
            'username': username,
            'name': f'Synthetic User {i}',
            'email': f'{username}@example.com',
            'password': 'changeme'
        })
        existing_usernames.add(username)
        i += 1
    return users


def create_constraint():
    # Create uniqueness constraint on username if not exists
    cypher = (
        "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE (u.username) IS UNIQUE"
    )
    with session() as s:
        s.run(cypher)


def chunked_iter(items: List, size: int):
    for i in range(0, len(items), size):
        yield items[i:i+size]


def insert_users(users: List[Dict[str, str]]):
    print(f"Inserting {len(users)} users in batches of {BATCH_SIZE}...")
    cypher = (
        "UNWIND $batch AS u\n"
        "MERGE (n:User {username: u.username})\n"
        "SET n.name = u.name, n.email = u.email, n.password = u.password"
    )
    with session() as s:
        for batch in chunked_iter(users, BATCH_SIZE):
            s.run(cypher, batch=batch)


def insert_relationships(pairs: List[Tuple[str, str]]):
    print(f"Inserting {len(pairs)} FOLLOWS relationships in batches of {BATCH_SIZE}...")
    cypher = (
        "UNWIND $batch AS r\n"
        "MATCH (a:User {username: r.follower}), (b:User {username: r.followee})\n"
        "WHERE a.username <> b.username\n"
        "MERGE (a)-[:FOLLOWS]->(b)"
    )
    # transform to dict list
    dicts = [{'follower': f, 'followee': t} for f, t in pairs]
    with session() as s:
        for batch in chunked_iter(dicts, BATCH_SIZE):
            s.run(cypher, batch=batch)


def build_relationship_pairs(usernames: List[str], target: int) -> List[Tuple[str, str]]:
    pairs: Set[Tuple[str, str]] = set()
    n = len(usernames)
    if n < 2:
        return []
    # create relationships until target reached; random selection
    attempts = 0
    max_attempts = target * 10
    while len(pairs) < target and attempts < max_attempts:
        a = random.randrange(n)
        b = random.randrange(n)
        if a == b:
            attempts += 1
            continue
        pair = (usernames[a], usernames[b])
        if pair in pairs:
            attempts += 1
            continue
        pairs.add(pair)
    if len(pairs) < target:
        # fallback: deterministic fill by cycling
        i = 0
        while len(pairs) < target:
            a = i % n
            b = (i+1) % n
            if a != b:
                pairs.add((usernames[a], usernames[b]))
            i += 1
    return list(pairs)


def main(csv_path: str, target_nodes: int, target_rels: int):
    print("Loading users from CSV...", csv_path)
    existing = load_users_from_csv(csv_path)
    existing_usernames = {u['username'] for u in existing}
    print(f"Found {len(existing)} unique users in CSV")

    if len(existing) >= target_nodes:
        users_to_insert = existing[:target_nodes]
    else:
        needed = target_nodes - len(existing)
        synth = synthesize_users(existing_usernames, needed, start_index=1)
        users_to_insert = existing + synth
        print(f"Synthesized {len(synth)} users to reach {target_nodes} total")

    # create constraint
    print("Creating uniqueness constraint for :User(username)")
    create_constraint()

    # insert users
    insert_users(users_to_insert)

    usernames = [u['username'] for u in users_to_insert]

    # build random relationships
    print(f"Generating {target_rels} relationship pairs...")
    pairs = build_relationship_pairs(usernames, target_rels)
    insert_relationships(pairs)

    close_driver()
    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='data/farmaciavernile.it.csv', help='Path to CSV file')
    parser.add_argument('--nodes', type=int, default=TARGET_NODES, help='Target number of nodes')
    parser.add_argument('--rels', type=int, default=TARGET_RELATIONSHIPS, help='Target number of relationships')
    args = parser.parse_args()
    main(args.csv, args.nodes, args.rels)
