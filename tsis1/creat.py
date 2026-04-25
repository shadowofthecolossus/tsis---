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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        birthday DATE,
        group_id INTEGER REFERENCES groups(id)
    );

    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        phone VARCHAR(20) NOT NULL,
        type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
    );
    """)

    conn.commit()
    print("Tables created.")

    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)