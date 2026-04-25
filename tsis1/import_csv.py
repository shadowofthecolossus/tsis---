import psycopg2
import csv

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

    with open('contacts.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # пропускаем заголовок

        for row in reader:
            name, phone, p_type, email, birthday, group_name = row

            cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
            group = cur.fetchone()
            
            if not group:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,))
                group_id = cur.fetchone()[0]
            else:
                group_id = group[0]

            cur.execute(
                "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id;", 
                (name, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);", 
                (contact_id, phone, p_type)
            )

    conn.commit() 
    print("CSV imported.")

    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)