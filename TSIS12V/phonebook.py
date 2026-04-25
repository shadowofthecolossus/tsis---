# phonebook.py
import json
import csv
from connect import get_connection, init_database

def search_ui():
    q = input("Enter search query (name/email/number): ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (q,))
    rows = cur.fetchall()
    print("\n--- Search Results ---")
    for r in rows: print(f"User: {r[0]} | Email: {r[1]} | Phone: {r[2]}")
    conn.close()

def filter_sort_ui():
    group = input("Filter by Group: ")
    sort_by = input("Sort by (name/birthday): ")
    conn = get_connection(); cur = conn.cursor()
    col = "c.birthday" if sort_by == "birthday" else "c.name"
    cur.execute(f"SELECT c.name, c.email, g.name FROM contacts c JOIN groups g ON c.group_id = g.id WHERE g.name = %s ORDER BY {col};", (group,))
    for r in cur.fetchall(): print(f"{r[0]} | {r[1]} | Group: {r[2]}")
    conn.close()

def paginate_ui():
    page = 0; limit = 5
    conn = get_connection(); cur = conn.cursor()
    while True:
        cur.execute("SELECT name, email FROM contacts ORDER BY id LIMIT %s OFFSET %s;", (limit, page * limit))
        rows = cur.fetchall()
        if not rows: print("No more data."); break
        print(f"\n--- Page {page + 1} ---")
        for r in rows: print(f"{r[0]} | {r[1]}")
        cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
        if cmd == 'n': page += 1
        elif cmd == 'p' and page > 0: page -= 1
        elif cmd == 'q': break
    conn.close()

def import_csv_ui():
    conn = get_connection(); cur = conn.cursor()
    try:
        with open('contacts.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                cur.execute("INSERT INTO contacts (name, email) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (row[0], row[1]))
        conn.commit(); print("CSV Import Successful.")
    except Exception as e: print(f"CSV Error: {e}")
    finally: conn.close()

def add_phone_ui():
    n, p, t = input("Name: "), input("Number: "), input("Type (mobile/work): ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s);", (n, p, t))
    conn.commit(); conn.close(); print("Phone added.")

def move_group_ui():
    n, g = input("Name: "), input("New Group: ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s);", (n, g))
    conn.commit(); conn.close(); print("Group updated.")

def delete_ui():
    target = input("Enter Name or Number to delete: ")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name = %s;", (target,))
    cur.execute("DELETE FROM phones WHERE phone = %s;", (target,))
    conn.commit(); conn.close(); print(f"Deleted records for '{target}'.")

def export_json_ui():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT name, email FROM contacts")
    data = [{"name": r[0], "email": r[1]} for r in cur.fetchall()]
    with open('export.json', 'w') as f: json.dump(data, f, indent=4)
    conn.close(); print("Exported to export.json")

def import_json_ui():
    try:
        with open('import.json', 'r') as f: data = json.load(f)
        conn = get_connection(); cur = conn.cursor()
        for item in data:
            name, email = item.get('name'), item.get('email')
            cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
            if cur.fetchone():
                if input(f"Update email for {name}? (y/n): ") == 'y':
                    cur.execute("UPDATE contacts SET email = %s WHERE name = %s;", (email, name))
            else:
                cur.execute("INSERT INTO contacts (name, email) VALUES (%s, %s);", (name, email))
        conn.commit(); conn.close(); print("JSON Import complete.")
    except Exception as e: print(f"JSON Error: {e}")

def main():
    init_database() # Initialize DB structure from SQL files
    while True:
        print("\n=== PHONEBOOK SYSTEM ===")
        print("1. Search")
        print("2. Filter & Sort")
        print("3. Pagination")
        print("4. Import CSV")
        print("5. Add Phone")
        print("6. Move Group")
        print("7. Delete Record")
        print("8. Export JSON")
        print("9. Import JSON")
        print("0. Exit")
        
        c = input("\nSelect Option: ")
        if c == '1': search_ui()
        elif c == '2': filter_sort_ui()
        elif c == '3': paginate_ui()
        elif c == '4': import_csv_ui()
        elif c == '5': add_phone_ui()
        elif c == '6': move_group_ui()
        elif c == '7': delete_ui()
        elif c == '8': export_json_ui()
        elif c == '9': import_json_ui()
        elif c == '0': break

if __name__ == "__main__":
    main()