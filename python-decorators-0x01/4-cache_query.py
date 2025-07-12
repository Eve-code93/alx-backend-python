#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Reuse from previous tasks
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the SQL query string
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Caching result")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
