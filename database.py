import sqlite3
from aiogram.types import User


class Database:
    """Class to interact with sqlite3 database."""

    def __init__(self, file: str = "database.db") -> None:
        """Initialize database.

        Args:
            file: Path to database file.
        """
        # check if file exists
        try:
            with open(file, "r"):
                pass
            self.connect = sqlite3.connect(file)
            self.cursor = self.connect.cursor()
        except FileNotFoundError:
            self.connect = sqlite3.connect(file)
            self.cursor = self.connect.cursor()
            self.cursor.execute("""
                CREATE TABLE users(
                    id INT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    role TEXT)
            """)

            self.cursor.execute("""
                CREATE TABLE channels (id INT, type TEXT, status TEXT)
            """)
            self.save_database()

    def get_user_role(self, user_id: int) -> str:
        """
        Return role of the user ("admin", "superadmin" or "follower")

        Args:
            user_id: telegram id of the user

        Returns:
            role (str) of the user or None if user doesn't exist
        """

        self.cursor.execute(f'SELECT role FROM users WHERE id={user_id}')
        role = self.cursor.fetchone()
        if not role:
            return ""
        else:
            return role[0]

    def add_admin(self, user_id: int, role: str) -> bool:
        """Add admin to database.

        Args:
            user_id: User id.
            role: role of the admin

        Returns:
            True if user have been added, False if user is already in database.
        """
        self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}")

        if not self.cursor.fetchone():
            self.cursor.execute(
                f"""INSERT OR IGNORE INTO users VALUES (
                            {user_id},
                            "",
                            "",
                            "",
                            "{role}"
                        )"""
            )
            self.save_database()

            return True
        else:
            return self.change_user_role(user_id, role)

        return False


    def add_user(self, user: User, role: str) -> bool:
        """Add user to database.

        Args:
            user: User aiogram object
            role: role of the user ("admin"/"superadmin"/"follower")

        Returns:
            True if user have been added, False if user is already in database.
        """

        self.cursor.execute(f"SELECT * FROM users WHERE id={user.id}")

        if not self.cursor.fetchone():
            self.cursor.execute(
                f"""INSERT OR IGNORE INTO users VALUES (
                    {user.id},
                    "{user.username}",
                    "{user.first_name}",
                    "{user.last_name}",
                    "{role}"
                )"""
            )
            self.save_database()

            return True

        return False

    def get_channel_id_by_type(self, channel_type: str):

        self.cursor.execute(f'SELECT id FROM channels WHERE type="{channel_type}"')
        f = self.cursor.fetchone()
        if f is not None:
            return f[0]
        else:
            return None


    def add_channel(self, chat_id: int, channel_type: str) -> bool:
        """Add (or update) channel to database.

        Args:
            chat_id: telegram chat_id (int)
            channel_type: main or reserve (str)

        Returns:
            True if channel have been added, else False.
        """

        default_value = {
            "main": "public",
            "reserve": "private"
        }

        self.cursor.execute(f'SELECT * FROM channels WHERE type="{channel_type}"')

        if not self.cursor.fetchone():
            self.cursor.execute(
                f"""INSERT OR IGNORE INTO channels VALUES (
                    {chat_id},
                    "{channel_type}",
                    "{default_value[channel_type]}"
                )"""
            )
            self.save_database()

            return True
        else:
            try:
                self.cursor.execute(f'UPDATE channels SET id = {chat_id} WHERE type="{channel_type}"')
                self.save_database()
                return True
            except Exception as e:
                print(e)

        return False

    def change_user_role(self, user_id: int, new_role: str) -> bool:

        self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}")

        if not self.cursor.fetchone():
            return False
        else:
            try:
                self.cursor.execute(f'UPDATE users SET role = "{new_role}" WHERE id={user_id}')
                self.save_database()
                return True
            #не бейте, логгирование надо отдельно прописывать, но времени совсем в обрез было
            #может быть еще успею подключить какой-нибудь Sentry, но если вы видите это сообщение,
            #значит я не успел :)
            except Exception as e:
                print(e)
        return False

    def save_database(self) -> None:
        """Save database and close connection."""
        self.connect.commit()
