from decimal import Decimal

from pydantic import BaseModel, Field


class OperationRequest(BaseModel):
    operation_type: str = Field(..., pattern="^(DEPOSIT|WITHDRAW)$")
    amount: Decimal = Field(..., gt=0)


class BalanceResponse(BaseModel):
    balance: Decimal
