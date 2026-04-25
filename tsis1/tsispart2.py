import psycopg2

password = "12345678"
dbname = "phonebooktest"

try:
    conn = psycopg2.connect(
        host="localhost",
        database=dbname,
        user="postgres",
        password=password
    )
    cur = conn.cursor()

    name = input("Enter name: ")
    phone = input("Enter phone: ")
    
    cur.execute("SELECT id FROM groups WHERE name = 'Friends';")
    group = cur.fetchone()
    
    if not group:
        cur.execute("INSERT INTO groups (name) VALUES ('Friends') RETURNING id;")
        group_id = cur.fetchone()[0]
    else:
        group_id = group[0]

    cur.execute(
        "INSERT INTO contacts (name, group_id) VALUES (%s, %s) RETURNING id;", 
        (name, group_id)
    )
    contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, 'mobile');", 
        (contact_id, phone)
    )

    conn.commit() 
    print("Success.")

    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)