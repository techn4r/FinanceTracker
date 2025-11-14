import sqlite3
from os.path import curdir
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional

from .models import Transaction


class Storage:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self._ensure_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_db(self):
        conn = self._connect()
        try:
            conn.execute(
                """
                                CREATE TABLE IF NOT EXISTS transactions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date TEXT NOT NULL,
                                    amount REAL NOT NULL,
                                    kind TEXT NOT NULL CHECK (kind IN ('income', 'expense')),
                                    category TEXT NOT NULL,
                                    description TEXT,
                                    created_at TEXT NOT NULL
                                )
                                """
            )
            conn.commit()
        finally:
            conn.close()

    def add_transaction(self, tx: Transaction) -> Transaction:
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO transactions (date, amount, kind, category, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (tx.date, tx.amount, tx.kind, tx.category, tx.description, tx.created_at),
            )
            conn.commit()
            new_id = cursor.lastrowid
            return Transaction(
                id=new_id,
                date=tx.date,
                amount=tx.amount,
                kind=tx.kind,
                category=tx.category,
                description=tx.description,
                created_at=tx.created_at,
            )
        finally:
            conn.close()

    def list_transactions(
            self,
            from_date: Optional[date] = None,
            to_date: Optional[date] = None,
            category: Optional[str] = None,
    ) -> List[Transaction]:
        conn = self._connect()
        try:
            query = """
                SELECT id, date, amount, kind, category, description, created_at
                FROM transactions
            """
            conditions = []
            params: List[str] = []
            if from_date is not None:
                conditions.append("date >= ?")
                params.append(from_date.isoformat())
            if to_date is not None:
                conditions.append("date <= ?")
                params.append(to_date.isoformat())
            if category is not None:
                conditions.append("category = ?")
                params.append(category)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY date ASC, id ASC"

            rows = conn.execute(query, params).fetchall()

            result = []
            for row in rows:
                row_id, date_str, amount, kind, cat, descr, created_at_str = row
                result.append(
                    Transaction(
                        id=row_id,
                        date=date_str,
                        amount=amount,
                        kind=kind,
                        category=cat,
                        description=descr or "",
                        created_at=datetime.fromisoformat(created_at_str),
                    )
                )
            return result
        finally:
            conn.close()
