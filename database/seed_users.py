from services.auth_service import AuthService


DEMO_USERS = [
    {
        "username": "ramsai",
        "full_name": "Ram Sai",
        "email": "ramsai@gmail.com",
        "password": "password123"
    },
    {
        "username": "demo",
        "full_name": "Demo User",
        "email": "demo@gmail.com",
        "password": "demo123"
    },
    {
        "username": "student",
        "full_name": "Student User",
        "email": "student@gmail.com",
        "password": "student123"
    }
]


def seed_demo_users():

    print("Seeding demo users...\n")

    for user in DEMO_USERS:

        success, message = AuthService.register_user(
            username=user["username"],
            password=user["password"],
            full_name=user["full_name"],
            email=user["email"]
        )

        print(f"{user['username']} -> {message}")

    print("\nDatabase seeding completed.")


if __name__ == "__main__":
    seed_demo_users()