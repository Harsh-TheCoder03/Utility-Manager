#pass - Harshmysql01
# utility_manager.py
# Simple Utility Manager with MySQL
# Features: Documents, Files, Passwords, To-Do List, Notes, Export, Help

import mysql.connector
import getpass
import datetime

DB_NAME = "utility_manager"


# ---------- Database Setup ----------

def connect_mysql(host, user, password):
    return mysql.connector.connect(host=host, user=user, password=password)


def ensure_db(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cur.close()


def connect_db(host, user, password):
    return mysql.connector.connect(host=host, user=user, password=password, database=DB_NAME)
def ensure_tables(conn):
    cur = conn.cursor()

    # Documents
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        path TEXT,
        category VARCHAR(100),
        amount VARCHAR(50),
        due_date VARCHAR(20),
        notes TEXT
    )
    """)

    # Files
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        path TEXT,
        category VARCHAR(100),
        notes TEXT
    )
    """)

    # Passwords
    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        site VARCHAR(255),
        username VARCHAR(255),
        password VARCHAR(255),
        notes TEXT
    )
    """)

    # Tasks
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255),
        deadline VARCHAR(50),
        status VARCHAR(20),
        notes TEXT
    )
    """)

    # Notes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        content TEXT,
        created_on VARCHAR(50)
    )
    """)

    conn.commit()
    cur.close()


# ---------- Helper Functions ----------

def ask(msg):
    return input(msg).strip()


def list_table(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    if not rows:
        print("No records found.")
    else:
        for row in rows:
            print(row)
    cur.close()


def delete_row(conn, table):
    rid = ask("Enter ID to delete: ")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE id=%s", (rid,))
    conn.commit()
    if cur.rowcount:
        print("Deleted successfully.")
    else:
        print("ID not found.")
    cur.close()


# ---------- Documents Manager ----------

def menu_documents(conn):
    while True:
        print("\n--- Documents Manager ---")
        print("1) Add Document")
        print("2) View Documents")
        print("3) Delete Document")
        print("4) Back")
        ch = ask("Choice: ")
        if ch == "1":
            name = ask("Name: ")
            path = ask("Place/location: ")
            category = ask("Category: ")
            amount = ask("Amount: ")
            due_date = ask("Due Date: ")
            notes = ask("Notes: ")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO documents(name,path,category,amount,due_date,notes) VALUES (%s,%s,%s,%s,%s,%s)",
                (name, path, category, amount, due_date, notes))
            conn.commit()
            cur.close()
            print("Document saved.")
        elif ch == "2":
            list_table(conn, "documents")
        elif ch == "3":
            delete_row(conn, "documents")
        elif ch == "4":
            break


# ---------- Files Manager ----------

def menu_files(conn):
    while True:
        print("\n--- File Manager ---")
        print("1) Add File")
        print("2) View Files")
        print("3) Delete File")
        print("4) Back")
        ch = ask("Choice: ")
        if ch == "1":
            name = ask("Name: ")
            path = ask("Path: ")
            category = ask("Category: ")
            notes = ask("Notes: ")
            cur = conn.cursor()
            cur.execute("INSERT INTO files(name,path,category,notes) VALUES (%s,%s,%s,%s)",
                        (name, path, category, notes))
            conn.commit()
            cur.close()
            print("File saved.")
        elif ch == "2":
            list_table(conn, "files")
        elif ch == "3":
            delete_row(conn, "files")
        elif ch == "4":
            break


# ---------- Passwords Manager ----------

def menu_passwords(conn):
    while True:
        print("\n--- Password Manager ---")
        print("1) Add Credential")
        print("2) View Credentials")
        print("3) Delete Credential")
        print("4) Back")
        ch = ask("Choice: ")
        if ch == "1":
            site = ask("Site: ")
            uname = ask("Username: ")
            pw = getpass.getpass("Password: ")
            notes = ask("Notes: ")
            cur = conn.cursor()
            cur.execute("INSERT INTO passwords(site,username,password,notes) VALUES (%s,%s,%s,%s)",
                        (site, uname, pw, notes))
            conn.commit()
            cur.close()
            print("Credential saved.")
        elif ch == "2":
            list_table(conn, "passwords")
        elif ch == "3":
            delete_row(conn, "passwords")
        elif ch == "4":
            break


# ---------- Tasks Manager ----------

def menu_tasks(conn):
    while True:
        print("\n--- To-Do List Manager ---")
        print("1) Add Task")
        print("2) View Tasks")
        print("3) Mark Task as Done")
        print("4) Delete Task")
        print("5) Back")
        ch = ask("Choice: ")
        if ch == "1":
            task = ask("Task: ")
            deadline = ask("Deadline: ")
            notes = ask("Notes: ")
            cur = conn.cursor()
            cur.execute("INSERT INTO tasks(task,deadline,status,notes) VALUES (%s,%s,%s,%s)",
                        (task, deadline, "Pending", notes))
            conn.commit()
            cur.close()
            print("Task added.")
        elif ch == "2":
            list_table(conn, "tasks")
        elif ch == "3":
            rid = ask("Enter Task ID to mark as done: ")
            cur = conn.cursor()
            cur.execute("UPDATE tasks SET status=%s WHERE id=%s", ("Done", rid))
            conn.commit()
            if cur.rowcount:
                print("Task updated.")
            else:
                print("Task not found.")
            cur.close()
        elif ch == "4":
            delete_row(conn, "tasks")
        elif ch == "5":
            break


# ---------- Notes Manager ----------

def menu_notes(conn):
    while True:
        print("\n--- Notes Manager ---")
        print("1) Add Note")
        print("2) View Notes")
        print("3) Delete Note")
        print("4) Back")
        ch = ask("Choice: ")
        if ch == "1":
            title = ask("Title: ")
            content = ask("Content: ")
            created_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur = conn.cursor()
            cur.execute("INSERT INTO notes(title,content,created_on) VALUES (%s,%s,%s)",
                        (title, content, created_on))
            conn.commit()
            cur.close()
            print("Note added.")
        elif ch == "2":
            list_table(conn, "notes")
        elif ch == "3":
            delete_row(conn, "notes")
        elif ch == "4":
            break


# ---------- Export Function ----------

def export_data(conn):
    tables = ["documents", "files", "passwords", "tasks", "notes"]
    for table in tables:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        with open(f"{table}_backup.txt", "a") as f:
            for row in rows:
                f.append(str(row) + "\n")
        cur.close()
    print("All data exported to text files.")


# ---------- Help/About ----------

def show_help():
    print("\n--- Help / About ---")
    print("This Utility Manager lets you manage:")
    print("1) Documents: store bills and documents.")
    print("2) Files: keep track of file paths.")
    print("3) Passwords: save site logins.")
    print("4) To-Do List: manage tasks with deadlines.")
    print("5) Notes: store personal notes.")
    print("6) Export: backup all data to text files.")
    print("Simple and easy to use!\n")


# ---------- Main ----------

def main():
    print("=== Utility Manager ===")
    host = ask("MySQL host [localhost]: ") or "localhost"
    user = ask("MySQL user: ")
    pw = getpass.getpass("MySQL password: ")

    try:
        root_conn = connect_mysql(host, user, pw)
        ensure_db(root_conn)
        root_conn.close()
        conn = connect_db(host, user, pw)
        ensure_tables(conn)
    except Exception as e:
        print("Error connecting to MySQL:", e)
        return

    while True:
        print("\n=== Main Menu ===")
        print("1) Documents Manager")
        print("2) File Manager")
        print("3) Password Manager")
        print("4) To-Do List")
        print("5) Notes Manager")
        print("6) Export Data")
        print("7) Help/About")
        print("8) Exit")

        choice = ask("Choice: ")
        if choice == "1":
            menu_documents(conn)
        elif choice == "2":
            menu_files(conn)
        elif choice == "3":
            menu_passwords(conn)
        elif choice == "4":
            menu_tasks(conn)
        elif choice == "5":
            menu_notes(conn)
        elif choice == "6":
            export_data(conn)
        elif choice == "7":
            show_help()
        elif choice == "8":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
