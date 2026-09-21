import bcrypt
import sqlite3

from database.db import get_connection


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password."""
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    @staticmethod
    def register_user(
        username: str,
        password: str,
        full_name: str,
        email: str
    ):
        """
        Register a new learner.

        Every registered user gets the
        default role: learner.
        """

        connection = get_connection()
        cursor = connection.cursor()

        try:

            hashed_password = AuthService.hash_password(password)

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    full_name,
                    email,
                    password,
                    role
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    username.strip(),
                    full_name.strip(),
                    email.strip().lower(),
                    hashed_password,
                    "learner",
                )
            )

            connection.commit()

            return True, "Account created successfully."

        except sqlite3.IntegrityError as e:

            error = str(e).lower()

            if "username" in error:
                return False, "Username already exists."

            if "email" in error:
                return False, "Email already exists."

            return False, "User already exists."

        except Exception as e:

            return False, f"Registration failed: {str(e)}"

        finally:

            connection.close()

    @staticmethod
    def authenticate_user(
        username_or_email: str,
        password: str
    ):
        """
        Authenticate using username or email.

        Returns:

            (True, user_dict)

            (False, error_message)
        """

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
               OR email = ?
            """,
            (
                username_or_email.strip(),
                username_or_email.strip().lower(),
            )
        )

        user = cursor.fetchone()

        connection.close()

        if user is None:

            return False, "User not found."

        if not AuthService.verify_password(
            password,
            user["password"],
        ):

            return False, "Invalid password."

        user_data = {

            "id": user["id"],

            "username": user["username"],

            "full_name": user["full_name"],

            "email": user["email"],

            "role": user["role"],

            "created_at": user["created_at"],

        }

        return True, user_data

    @staticmethod
    def user_exists(
        username: str = None,
        email: str = None,
    ):
        """
        Check whether username
        or email already exists.
        """

        connection = get_connection()

        cursor = connection.cursor()

        if username:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (
                    username.strip(),
                ),
            )

            if cursor.fetchone():

                connection.close()

                return True

        if email:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = ?
                """,
                (
                    email.strip().lower(),
                ),
            )

            if cursor.fetchone():

                connection.close()

                return True

        connection.close()

        return False

    @staticmethod
    def get_user_by_id(
        user_id: int,
    ):
        """
        Fetch user details by ID.
        """

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (
                user_id,
            ),
        )

        user = cursor.fetchone()

        connection.close()

        return dict(user) if user else None

    @staticmethod
    def logout():
        """
        Placeholder for logout.

        Session cleanup is handled
        in the UI layer.
        """

        return True