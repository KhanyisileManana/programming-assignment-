from abc import ABC, abstractmethod
from datetime import timedelta

class BookingPolicy(ABC):
    name = "Base"
    description = ""
    @abstractmethod
    def validate(self, start_dt, duration_minutes) -> tuple[bool, str]: ...

class StrictPolicy(BookingPolicy):
    name = "Strict (Johannesburg)"
    description = "Bookings 09:00–16:00 only. Max 60 minutes per session."
    def validate(self, start_dt, duration_minutes):
        if duration_minutes > 60: return False, "Strict policy: maximum duration is 60 minutes."
        if not (9 <= start_dt.hour < 16): return False, "Strict policy: bookings allowed only 09:00–16:00."
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        if end_dt.hour > 16 or (end_dt.hour == 16 and end_dt.minute > 0): return False, "Strict policy: booking must end by 16:00."
        return True, "OK"

class ModeratePolicy(BookingPolicy):
    name = "Moderate (Cape Town)"
    description = "Bookings 08:00–18:00. Max 120 minutes per session."
    def validate(self, start_dt, duration_minutes):
        if duration_minutes > 120: return False, "Moderate policy: maximum duration is 120 minutes."
        if not (8 <= start_dt.hour < 18): return False, "Moderate policy: bookings allowed only 08:00–18:00."
        return True, "OK"

class FlexiblePolicy(BookingPolicy):
    name = "Flexible (Durban)"
    description = "Bookings 07:00–22:00. Max 240 minutes. No bookings after 22:00."
    def validate(self, start_dt, duration_minutes):
        if duration_minutes > 240: return False, "Flexible policy: maximum duration is 240 minutes."
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        if start_dt.hour < 7 or end_dt.hour > 22: return False, "Flexible policy: bookings only between 07:00 and 22:00."
        return True, "OK"

POLICY_REGISTRY = {"strict": StrictPolicy(), "moderate": ModeratePolicy(), "flexible": FlexiblePolicy()}
def get_policy(name: str) -> BookingPolicy:
    return POLICY_REGISTRY.get(name.lower(), ModeratePolicy())