from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel
from datetime import date


class Expense(BaseModel):
    currency: str
    amount: Decimal


class Expenses(BaseModel):
    date: date
    by_currencies: List[Expense]


class CreateExpense(BaseModel):
    date: date
    amount: Decimal
    currency: str
    category: str


class UpdateExpense(BaseModel):
    date: Optional[date]
    amount: Optional[Decimal]
    currency: Optional[str]
    category: Optional[str]
