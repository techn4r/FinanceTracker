from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Literal

Kind = Literal["income", "expense"]


@dataclass
class Transaction:
    id: Optional[int]
    date: date
    amount: float
    kind: Kind
    category: str
    description: str
    created_at: datetime
