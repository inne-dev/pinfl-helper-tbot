"""Database configuration and models for the PINFL Helper Telegram Bot."""

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, Any


class Database:
    """Database manager for the PINFL Helper Bot."""

    db_path: str

    def __init__(self, db_path: str = "data/pinfl_bot.db"):
        """Initialize database connection and create tables."""
        self.db_path = db_path
        # Create data directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only create directory if path contains directory part
            os.makedirs(db_dir, exist_ok=True)
        self.init_db()

    def init_db(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Users table
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language_code TEXT DEFAULT 'ru',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Requests table for statistics
            _ = cursor.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    request_type TEXT, -- 'generate', 'analyze'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

            conn.commit()

    def add_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        language_code: str = "ru",
    ) -> bool:
        """Add or update user in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    INSERT OR REPLACE INTO users
                    (user_id, username, first_name, last_name, language_code, last_activity)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                    (user_id, username, first_name, last_name, language_code),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    SELECT user_id, username, first_name, last_name, language_code,
                           created_at, last_activity
                    FROM users WHERE user_id = ?
                """,
                    (user_id,),
                )
                row = cursor.fetchone()

                if row:
                    return {
                        "user_id": row[0],
                        "username": row[1],
                        "first_name": row[2],
                        "last_name": row[3],
                        "language_code": row[4],
                        "created_at": row[5],
                        "last_activity": row[6],
                    }
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def update_user_language(self, user_id: int, language_code: str) -> bool:
        """Update user's language preference."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    UPDATE users
                    SET language_code = ?, last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """,
                    (language_code, user_id),
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user language: {e}")
            return False

    def update_last_activity(self, user_id: int) -> bool:
        """Update user's last activity timestamp."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    UPDATE users
                    SET last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """,
                    (user_id,),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating last activity: {e}")
            return False

    def add_request(self, user_id: int, request_type: str) -> bool:
        """Add a request record for statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute(
                    """
                    INSERT INTO requests (user_id, request_type)
                    VALUES (?, ?)
                """,
                    (user_id, request_type),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding request: {e}")
            return False

    def get_monthly_stats(
        self, year: Optional[int] = None, month: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get monthly statistics."""
        if not year or not month:
            now = datetime.now()
            year = now.year
            month = now.month

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Start and end of the month
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1)
                else:
                    end_date = datetime(year, month + 1, 1)

                # Generate requests count
                _ = cursor.execute(
                    """
                    SELECT COUNT(*) FROM requests
                    WHERE request_type = 'generate'
                    AND created_at >= ? AND created_at < ?
                """,
                    (start_date, end_date),
                )
                generate_count = cursor.fetchone()[0]

                # Analyze requests count
                _ = cursor.execute(
                    """
                    SELECT COUNT(*) FROM requests
                    WHERE request_type = 'analyze'
                    AND created_at >= ? AND created_at < ?
                """,
                    (start_date, end_date),
                )
                analyze_count = cursor.fetchone()[0]

                # New users count
                _ = cursor.execute(
                    """
                    SELECT COUNT(*) FROM users
                    WHERE created_at >= ? AND created_at < ?
                """,
                    (start_date, end_date),
                )
                new_users_count = cursor.fetchone()[0]

                # Total users count
                _ = cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]

                return {
                    "year": year,
                    "month": month,
                    "generate_requests": generate_count,
                    "analyze_requests": analyze_count,
                    "new_users": new_users_count,
                    "total_users": total_users,
                }
        except Exception as e:
            print(f"Error getting monthly stats: {e}")
            return {
                "year": year,
                "month": month,
                "generate_requests": 0,
                "analyze_requests": 0,
                "new_users": 0,
                "total_users": 0,
            }

    def get_user_count(self) -> int:
        """Get total number of users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                _ = cursor.execute("SELECT COUNT(*) FROM users")
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting user count: {e}")
            return 0
