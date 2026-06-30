import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS purchases (
                    user_id INTEGER,
                    product_id TEXT,
                    charge_id TEXT UNIQUE,
                    created_at TIMESTAMP,
                    PRIMARY KEY (user_id, product_id)
                )
            """)
            conn.commit()

    def record_purchase(self, user_id, product_id, charge_id):
        """Records a purchase. Returns True if new, False if already exists (idempotency)."""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO purchases (user_id, product_id, charge_id, created_at) VALUES (?, ?, ?, ?)",
                    (user_id, product_id, charge_id, datetime.now())
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # unique constraint failed (charge_id or primary key)
            return False

    def get_user_purchases(self, user_id):
        """Returns a list of product IDs purchased by the user."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT product_id FROM purchases WHERE user_id = ?", (user_id,))
            return [row[0] for row in cursor.fetchall()]

    def check_access(self, user_id, product_id):
        """Returns True if the user has purchased the product."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM purchases WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )
            return cursor.fetchone() is not None
