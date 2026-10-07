from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

from database import (
    create_tables,
    add_transaction,
    get_transactions,
    get_transaction_by_id,
    update_transaction,
    delete_transaction,
    get_balance_summary,
    get_monthly_summary,
    get_category_spending,
    set_budget,
    get_budgets,
    get_category_expense
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SpendWise LK API",
    description="Personal finance and expense tracking API",
    version="1.0.0"
)


create_tables()


# =========================================================
# PYDANTIC MODELS
# =========================================================

class TransactionCreate(BaseModel):
    type: Literal["income", "expense"]

    amount: float = Field(
        gt=0,
        description="Transaction amount must be greater than zero"
    )

    category: str = Field(
        min_length=1
    )

    description: str = ""

    transaction_date: str

    @field_validator("transaction_date")
    @classmethod
    def validate_date(cls, value):
        try:
            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

        except ValueError:
            raise ValueError(
                "Date must use YYYY-MM-DD format"
            )

        return value


class TransactionUpdate(BaseModel):
    type: Literal["income", "expense"]

    amount: float = Field(gt=0)

    category: str = Field(
        min_length=1
    )

    description: str = ""

    transaction_date: str

    @field_validator("transaction_date")
    @classmethod
    def validate_date(cls, value):
        try:
            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

        except ValueError:
            raise ValueError(
                "Date must use YYYY-MM-DD format"
            )

        return value


class BudgetCreate(BaseModel):
    year: int

    month: int = Field(
        ge=1,
        le=12
    )

    category: str = Field(
        min_length=1
    )

    amount: float = Field(
        gt=0
    )


# =========================================================
# HELPER
# =========================================================

def transaction_to_dict(transaction):
    return {
        "id": transaction[0],
        "type": transaction[1],
        "amount": transaction[2],
        "category": transaction[3],
        "description": transaction[4],
        "transaction_date": transaction[5],
        "created_at": transaction[6]
    }


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "name": "SpendWise LK API",
        "version": "1.0.0",
        "message": "Welcome to SpendWise LK API"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "SpendWise LK API is running"
    }


# =========================================================
# GET ALL TRANSACTIONS
# =========================================================

@app.get("/transactions")
def read_transactions():
    transactions = get_transactions()

    results = [
        transaction_to_dict(transaction)
        for transaction in transactions
    ]

    return {
        "count": len(results),
        "transactions": results
    }


# =========================================================
# GET ONE TRANSACTION
# =========================================================

@app.get("/transactions/{transaction_id}")
def read_transaction(transaction_id: int):
    transaction = get_transaction_by_id(
        transaction_id
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction_to_dict(
        transaction
    )


# =========================================================
# CREATE TRANSACTION
# =========================================================

@app.post(
    "/transactions",
    status_code=201
)
def create_transaction(
    transaction: TransactionCreate
):
    transaction_id = add_transaction(
        transaction.type,
        transaction.amount,
        transaction.category.strip(),
        transaction.description.strip(),
        transaction.transaction_date
    )

    created_transaction = (
        get_transaction_by_id(
            transaction_id
        )
    )

    return {
        "message": "Transaction added successfully",
        "transaction": transaction_to_dict(
            created_transaction
        )
    }


# =========================================================
# UPDATE TRANSACTION
# =========================================================

@app.put("/transactions/{transaction_id}")
def edit_transaction(
    transaction_id: int,
    transaction: TransactionUpdate
):
    existing = get_transaction_by_id(
        transaction_id
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    updated = update_transaction(
        transaction_id,
        transaction.type,
        transaction.amount,
        transaction.category.strip(),
        transaction.description.strip(),
        transaction.transaction_date
    )

    if not updated:
        raise HTTPException(
            status_code=500,
            detail="Transaction could not be updated"
        )

    updated_transaction = (
        get_transaction_by_id(
            transaction_id
        )
    )

    return {
        "message": "Transaction updated successfully",
        "transaction": transaction_to_dict(
            updated_transaction
        )
    }


# =========================================================
# DELETE TRANSACTION
# =========================================================

@app.delete("/transactions/{transaction_id}")
def remove_transaction(
    transaction_id: int
):
    existing = get_transaction_by_id(
        transaction_id
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    delete_transaction(
        transaction_id
    )

    return {
        "message": "Transaction deleted successfully",
        "deleted_id": transaction_id
    }


# =========================================================
# BALANCE
# =========================================================

@app.get("/balance")
def read_balance():
    total_income, total_expense, balance = (
        get_balance_summary()
    )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }


# =========================================================
# MONTHLY ANALYTICS
# =========================================================

@app.get("/analytics/monthly")
def read_monthly_analytics(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):
    total_income, total_expense, balance = (
        get_monthly_summary(
            year,
            month
        )
    )

    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }


# =========================================================
# CATEGORY ANALYTICS
# =========================================================

@app.get("/analytics/categories")
def read_category_analytics(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):
    category_spending = (
        get_category_spending(
            year,
            month
        )
    )

    total_expense = sum(
        amount
        for category, amount
        in category_spending
    )

    categories = []

    for category, amount in category_spending:

        if total_expense > 0:
            percentage = (
                amount / total_expense
            ) * 100

        else:
            percentage = 0

        categories.append({
            "category": category,
            "amount": amount,
            "percentage": round(
                percentage,
                2
            )
        })

    return {
        "year": year,
        "month": month,
        "total_expense": total_expense,
        "categories": categories
    }


# =========================================================
# CREATE / UPDATE BUDGET
# =========================================================

@app.post("/budgets")
def create_budget(
    budget: BudgetCreate
):
    set_budget(
        budget.year,
        budget.month,
        budget.category.strip(),
        budget.amount
    )

    return {
        "message": "Budget saved successfully",
        "budget": budget
    }


# =========================================================
# GET BUDGET STATUS
# =========================================================

@app.get("/budgets")
def read_budgets(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):
    budgets = get_budgets(
        year,
        month
    )

    results = []

    for category, budget_amount in budgets:

        spent = get_category_expense(
            year,
            month,
            category
        )

        remaining = (
            budget_amount - spent
        )

        percentage_used = (
            (spent / budget_amount) * 100
            if budget_amount > 0
            else 0
        )

        results.append({
            "category": category,
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "percentage_used": round(
                percentage_used,
                2
            ),
            "exceeded": spent > budget_amount
        })

    return {
        "year": year,
        "month": month,
        "budgets": results
    }