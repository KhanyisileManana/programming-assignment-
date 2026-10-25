import sqlite3
import hashlib
from datetime import datetime, timedelta

DB_PATH = "smart_campus.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS campuses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, policy TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL, campus_id INTEGER, full_name TEXT, FOREIGN KEY(campus_id) REFERENCES campuses(id));
        CREATE TABLE IF NOT EXISTS resources (id INTEGER PRIMARY KEY AUTOINCREMENT, campus_id INTEGER NOT NULL, name TEXT NOT NULL, resource_type TEXT NOT NULL, UNIQUE(campus_id, name, resource_type), FOREIGN KEY(campus_id) REFERENCES campuses(id));
        CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, resource_id INTEGER NOT NULL, campus_id INTEGER NOT NULL, booking_date TEXT NOT NULL, start_time TEXT NOT NULL, duration_minutes INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'active', FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(resource_id) REFERENCES resources(id), FOREIGN KEY(campus_id) REFERENCES campuses(id));
    """)
    cur.execute("SELECT COUNT(*) FROM campuses")
    if cur.fetchone()[0] == 0:
        campuses = [("Johannesburg", "strict"), ("Cape Town", "moderate"), ("Durban", "flexible")]
        cur.executemany("INSERT INTO campuses (name, policy) VALUES (?, ?)", campuses)
    conn.commit()
    conn.close()

def create_user(username, password, role, campus_id, full_name):
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (username, password_hash, role, campus_id, full_name) VALUES (?, ?, ?, ?, ?)",
            (username, hash_password(password), role, campus_id, full_name)
        )
        conn.commit()
        return True, "Account created."
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different one."
    finally:
        conn.close()
def authenticate(username, password):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hash_password(password))).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_campuses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM campuses").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_resource(campus_id, name, rtype):
    try:
        conn = get_connection()
        conn.execute("INSERT INTO resources (campus_id, name, resource_type) VALUES (?, ?, ?)", (campus_id, name, rtype))
        conn.commit()
        return True, "Resource added."
    except sqlite3.IntegrityError:
        return False, "Duplicate resource for this campus."
    finally:
        conn.close()

def list_resources(campus_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM resources WHERE campus_id=? ORDER BY name", (campus_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_resource(resource_id):
    conn = get_connection()
    conn.execute("DELETE FROM resources WHERE id=?", (resource_id,))
    conn.commit()
    conn.close()

def has_overlap(resource_id, date_str, start_dt, duration_minutes):
    conn = get_connection()
    rows = conn.execute("SELECT start_time, duration_minutes FROM bookings WHERE resource_id=? AND booking_date=? AND status='active'", (resource_id, date_str)).fetchall()
    conn.close()
    req_start = start_dt
    req_end = start_dt + timedelta(minutes=duration_minutes)
    for r in rows:
        h, m = map(int, r["start_time"].split(":"))
        existing_start = start_dt.replace(hour=h, minute=m, second=0)
        existing_end = existing_start + timedelta(minutes=r["duration_minutes"])
        if req_start < existing_end and existing_start < req_end:
            return True
    return False

def create_booking(user_id, resource_id, campus_id, date_str, start_time, duration_minutes):
    conn = get_connection()
    conn.execute("INSERT INTO bookings (user_id, resource_id, campus_id, booking_date, start_time, duration_minutes) VALUES (?, ?, ?, ?, ?, ?)", (user_id, resource_id, campus_id, date_str, start_time, duration_minutes))
    conn.commit()
    conn.close()

def cancel_booking(booking_id):
    conn = get_connection()
    conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()

def get_user_bookings(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT b.*, r.name AS resource_name FROM bookings b JOIN resources r ON r.id=b.resource_id WHERE b.user_id=? ORDER BY b.booking_date DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_campus_bookings(campus_id):
    conn = get_connection()
    rows = conn.execute("SELECT b.*, r.name AS resource_name, u.username, u.full_name FROM bookings b JOIN resources r ON r.id=b.resource_id JOIN users u ON u.id=b.user_id WHERE b.campus_id=? ORDER BY b.booking_date DESC", (campus_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def campus_report(campus_id):
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM bookings WHERE campus_id=? AND status='active'", (campus_id,)).fetchone()[0]
    avg = conn.execute("SELECT AVG(duration_minutes) FROM bookings WHERE campus_id=? AND status='active'", (campus_id,)).fetchone()[0] or 0
    top = conn.execute("SELECT r.name, COUNT(*) AS c FROM bookings b JOIN resources r ON r.id=b.resource_id WHERE b.campus_id=? AND b.status='active' GROUP BY r.id ORDER BY c DESC LIMIT 5", (campus_id,)).fetchall()
    conn.close()
    return {"total": total, "avg_duration": round(avg, 1), "top_resources": [dict(r) for r in top]}