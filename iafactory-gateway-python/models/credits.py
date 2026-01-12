# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import datetime
class User(BaseModel):
    id: str
    email: str
    credits: int = 0
class Transaction(BaseModel):
    id: str
    user_id: str
    amount: int
    type: str
    reason: str
    balance_after: int
users_db = {}
transactions_db = []
