import sqlite3


def setup_database():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    cursor.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [
            ("admin", "admin123"),
            ("alice", "alice123"),
            ("bob", "bob123"),
        ],
    )

    conn.commit()
    return conn


def vulnerable_login(conn, username, password):
    cursor = conn.cursor()
    query = (
        "SELECT id, username FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    print("[Vulnerable SQL]")
    print(query)

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as exc:
        return [f"SQL error: {exc}"]


def safe_login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT id, username FROM users WHERE username = ? AND password = ?"

    print("[Safe SQL]")
    print(query)
    print("[Params]", (username, password))

    cursor.execute(query, (username, password))
    return cursor.fetchall()


def vulnerable_list_users(conn, order_by):
    cursor = conn.cursor()
    query = f"SELECT id, username FROM users ORDER BY {order_by}"

    print("[Vulnerable Sort SQL]")
    print(query)

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as exc:
        return [f"SQL error: {exc}"]


def safe_list_users(conn, order_by):
    cursor = conn.cursor()
    allowed_fields = {
        "id": "id",
        "username": "username",
    }

    safe_field = allowed_fields.get(order_by, "id")
    query = f"SELECT id, username FROM users ORDER BY {safe_field}"

    print("[Safe Sort SQL]")
    print(query)
    print("[Allowed field]", safe_field)

    cursor.execute(query)
    return cursor.fetchall()


def run_case(conn, title, username, password):
    print(f"\n=== {title} ===")
    print("Input username =", repr(username))
    print("Input password =", repr(password))
    print("Vulnerable result:", vulnerable_login(conn, username, password))
    print("Safe result:", safe_login(conn, username, password))


def run_sort_case(conn, title, order_by):
    print(f"\n=== {title} ===")
    print("Input order_by =", repr(order_by))
    print("Vulnerable sort result:", vulnerable_list_users(conn, order_by))
    print("Safe sort result:", safe_list_users(conn, order_by))


def main():
    conn = setup_database()

    run_case(conn, "Normal login", "alice", "alice123")
    run_case(conn, "Teaching-only invalid input", "alice", "' OR '1'='1")
    run_sort_case(conn, "Normal sort", "username")
    run_sort_case(conn, "Sort whitelist fallback", "username DESC, id")

    conn.close()


if __name__ == "__main__":
    main()
