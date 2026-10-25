from database import init_db, create_user, get_all_campuses, add_resource


def run_seed():
    print("Initializing database...")
    init_db()

    print("Creating System Operator...")
    create_user("operator", "Khanyi123", "operator", None, "System Operator")

    campuses = get_all_campuses()
    for campus in campuses:
        admin_username = f"admin_{campus['name'].lower().replace(' ', '')}"
        print(f"Creating Admin for {campus['name']} ({admin_username})...")
        create_user(admin_username, "Khanyi123", "admin", campus['id'], f"{campus['name']} Admin")

        add_resource(campus['id'], "Lab 101", "Computer Lab")
        add_resource(campus['id'], "Projector X", "Projector")

    # Create a Default Lecturer for testing
    print("Creating Default Lecturer...")
    campus_id = campuses[0]['id']  # Assign to Johannesburg
    create_user("lecturer", "Khanyi123", "lecturer", campus_id, "John Doe")

    print("\nSeeding Complete!")
    print("Default Passwords are 'Khanyi123'")
    print("Lecturer Login -> Username: lecturer | Password: Khanyi123")


if __name__ == "__main__":
    run_seed()