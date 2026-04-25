import psycopg2

DB_CONFIG = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "12345678", # change to your password
    "host": "localhost"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def save_result(username, score, level):
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # ensure player exists
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING RETURNING id;", (username,))
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        player_id = cur.fetchone()[0]
        
        # save session
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);", (player_id, score, level))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("db save error:", e)

def get_top_10():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at::DATE 
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC LIMIT 10;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except:
        return []

def get_personal_best(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(g.score) FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            WHERE p.username = %s;
        """, (username,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        return res[0] if res and res[0] else 0
    except:
        return 0