import psycopg2
import json
password = "12345678"
dbname = "phonebooktest"

def get_db():
    return psycopg2.connect(host="localhost", database=dbname, user="postgres", password=password)
def search():
    q = input("Search query: ")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s);", (q,))
    for r in cur.fetchall():
        print(f"Name: {r[0]}, Email: {r[1]}, Phone: {r[2]}")
    conn.close()

def filter_sort():
    grp = input("Filter by group (e.g. Friends): ")
    srt = input("Sort by (name/birthday): ")
    conn = get_db()
    cur = conn.cursor()
    
    order_col = "c.birthday" if srt == "birthday" else "c.name"
    cur.execute(f"""
        SELECT c.name, c.birthday, g.name 
        FROM contacts c 
        JOIN groups g ON c.group_id = g.id 
        WHERE g.name = %s 
        ORDER BY {order_col};
    """, (grp,))
    
    for r in cur.fetchall():
        print(r)
    conn.close()

def paginate():
    limit = 2
    offset = 0
    conn = get_db()
    cur = conn.cursor()
    while True:
        cur.execute("SELECT name FROM contacts ORDER BY id LIMIT %s OFFSET %s;", (limit, offset))
        rows = cur.fetchall()
        if not rows: 
            print("--- End of pages ---")
            break
        print(f"\n--- Page {(offset//limit)+1} ---")
        for r in rows: 
            print(r[0])
            
        cmd = input("Command: next (n) / prev (p) / quit (q): ")
        if cmd == 'n': offset += limit
        elif cmd == 'p' and offset >= limit: offset -= limit
        elif cmd == 'q': break
    conn.close()

def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    p_type = input("Type (home/work/mobile): ")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, p_type))
    conn.commit()
    conn.close()
    print("Phone added.")
def move_group():
    name = input("Contact name: ")
    g_name = input("New group name: ")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s);", (name, g_name))
    conn.commit()
    conn.close()
    print("Moved.")

def export_json():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, email, birthday::TEXT FROM contacts")
    data = [{"name": c[0], "email": c[1], "birthday": c[2]} for c in cur.fetchall()]
    with open('export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    conn.close()
    print("Exported to export.json")

def import_json():
    try:
        with open('import.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Create import.json first!")
        return

    conn = get_db()
    cur = conn.cursor()
    for item in data:
        name = item.get("name")
        email = item.get("email")
        
        cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
        exists = cur.fetchone()
        
        if exists:
            ans = input(f"Contact '{name}' exists. Overwrite? (y/n): ")
            if ans.lower() == 'y':
                cur.execute("UPDATE contacts SET email = %s WHERE name = %s;", (email, name))
                print(f"Updated {name}.")
            else:
                print(f"Skipped {name}.")
        else:
            cur.execute("INSERT INTO contacts (name, email) VALUES (%s, %s);", (name, email))
            print(f"Inserted {name}.")
            
    conn.commit()
    conn.close()
    print("Import finished.")

while True:
    print("\n--- MENU ---")
    print("1. Search (all fields)")
    print("2. Filter & Sort")
    print("3. Paginate Contacts")
    print("4. Add Phone to Contact")
    print("5. Move to Group")
    print("6. Export to JSON")
    print("7. Import from JSON")
    print("8. Quit")
    
    ch = input("Choose: ")
    if ch == '1': search()
    elif ch == '2': filter_sort()
    elif ch == '3': paginate()
    elif ch == '4': add_phone()
    elif ch == '5': move_group()
    elif ch == '6': export_json()
    elif ch == '7': import_json()
    elif ch == '8': break