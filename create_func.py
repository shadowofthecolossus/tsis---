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
    CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
    RETURNS TABLE(contact_name VARCHAR, email VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY 
        SELECT c.name::VARCHAR, COALESCE(c.email, '')::VARCHAR, COALESCE(p.phone, '')::VARCHAR
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.name ILIKE '%' || p_query || '%'
           OR c.email ILIKE '%' || p_query || '%'
           OR p.phone ILIKE '%' || p_query || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)

    conn.commit()
    print("Function created.")

    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)