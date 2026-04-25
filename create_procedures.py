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
    CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
    LANGUAGE plpgsql AS $$
    DECLARE
        v_contact_id INTEGER;
    BEGIN
        SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
        IF v_contact_id IS NOT NULL THEN
            INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
        END IF;
    END;
    $$;

    CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
    LANGUAGE plpgsql AS $$
    DECLARE
        v_group_id INTEGER;
    BEGIN
        SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
        IF v_group_id IS NULL THEN
            INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        END IF;
        UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
    END;
    $$;
    """)

    conn.commit()
    print("Procedures created.")

    cur.close()
    conn.close()
    
except Exception as e:
    print("Error:", e)