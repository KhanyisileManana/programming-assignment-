from datetime import datetime
from database import get_connection, has_overlap, create_booking
from booking_rules import get_policy


def attempt_booking(user_id, campus_id, resource_id, date_str, start_time_str, duration_minutes):
    try:
        duration_minutes = int(duration_minutes)
        if duration_minutes <= 0: return False, "Duration must be a positive number."
        start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return False, "Invalid Date (YYYY-MM-DD) or Time (HH:MM) format."

    if start_dt < datetime.now(): return False, "Cannot book in the past."

    conn = get_connection()
    policy_name = conn.execute("SELECT policy FROM campuses WHERE id=?", (campus_id,)).fetchone()["policy"]
    conn.close()

    policy = get_policy(policy_name)
    ok, msg = policy.validate(start_dt, duration_minutes)
    if not ok: return False, msg

    if has_overlap(resource_id, date_str, start_dt, duration_minutes):
        return False, "Resource is already booked for that time slot."

    create_booking(user_id, resource_id, campus_id, date_str, start_time_str, duration_minutes)
    return True, "Booking confirmed successfully!"