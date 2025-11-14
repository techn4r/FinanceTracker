from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

class Transaction:
    id: Optional[int]
    date: date
    amount: float
    kind: str
    category: str
    description: str
    created_at: datetime
