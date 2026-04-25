
-- 1. Search Function
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(c_name VARCHAR, c_email VARCHAR, p_phone VARCHAR) AS $$
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

-- 2. Add Phone Procedure
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    SELECT id, p_phone, p_type FROM contacts WHERE name = p_contact_name;
END;
$$;

-- 3. Change Group Procedure
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_g_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_g_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_g_id WHERE name = p_contact_name;
END;
$$;