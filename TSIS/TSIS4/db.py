import psycopg2
from config import load_config

def get_connection():
    # Важно: вызываем load_config()
    return psycopg2.connect(**load_config())

def save_score(username, score, level):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                    (player_id, score, level))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Save Error: {e}")

def get_top_10():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, s.score, s.level_reached 
            FROM game_sessions s JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"DB Leaderboard Error: {e}")
        return []

def get_personal_best(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(score) FROM game_sessions s 
            JOIN players p ON s.player_id = p.id WHERE p.username = %s
        """, (username,))
        res = cur.fetchone()[0]
        cur.close()
        conn.close()
        return res if res else 0
    except:
        return 0