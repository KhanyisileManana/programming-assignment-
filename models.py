from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, id, username, role, campus_id=None, full_name="", **kwargs):
        self.__user_id = id
        self.__username = username
        self.__role = role
        self.__campus_id = campus_id
        self.__full_name = full_name

    @property
    def user_id(self): return self.__user_id
    @property
    def username(self): return self.__username
    @property
    def role(self): return self.__role
    @property
    def campus_id(self): return self.__campus_id
    @property
    def full_name(self): return self.__full_name

    @abstractmethod
    def dashboard_permissions(self): ...

class Lecturer(User):
    def dashboard_permissions(self): return ["view_resources", "create_booking", "view_own_bookings", "cancel_booking"]

class CampusAdmin(User):
    def dashboard_permissions(self): return ["add_resource", "update_resource", "remove_resource", "view_campus_bookings", "monitor_usage"]

class SystemOperator(User):
    def dashboard_permissions(self): return ["view_all_bookings", "view_all_resources", "generate_cross_campus_report"]

def create_user_object(user_dict):
    if not user_dict: return None
    role = user_dict.get("role")
    if role == "lecturer": return Lecturer(**user_dict)
    elif role == "admin": return CampusAdmin(**user_dict)
    elif role == "operator": return SystemOperator(**user_dict)
    return User(**user_dict)