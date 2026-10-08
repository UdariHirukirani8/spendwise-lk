from datetime import datetime
from typing import Literal

from fastapi import (
    FastAPI,
    HTTPException,
    Query
)

from fastapi.responses import (
    FileResponse
)

from fastapi.staticfiles import (
    StaticFiles
)

from pydantic import (
    BaseModel,
    Field,
    field_validator
)

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
    get_category_expense,
    get_monthly_trends,
    add_savings_goal,
    get_savings_goals,
    get_savings_goal_by_id,
    update_savings_goal,
    delete_savings_goal
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SpendWise LK API",
    description=(
        "Personal finance and "
        "expense tracking API"
    ),
    version="1.0.0"
)


# =========================================================
# FRONTEND
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="frontend"
    ),
    name="static"
)


# =========================================================
# DATABASE
# =========================================================

create_tables()


# =========================================================
# TRANSACTION MODEL
# =========================================================

class TransactionData(BaseModel):

    type: Literal[
        "income",
        "expense"
    ]

    amount: float = Field(
        gt=0
    )

    category: str = Field(
        min_length=1
    )

    description: str = ""

    transaction_date: str


    @field_validator(
        "transaction_date"
    )
    @classmethod
    def validate_date(
        cls,
        value
    ):
        try:

            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Date must use "
                "YYYY-MM-DD format"
            )

        return value


# =========================================================
# BUDGET MODEL
# =========================================================

class BudgetData(BaseModel):

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
# SAVINGS GOAL MODEL
# =========================================================

class SavingsGoalData(BaseModel):

    name: str = Field(
        min_length=1
    )

    target_amount: float = Field(
        gt=0
    )

    saved_amount: float = Field(
        ge=0
    )

    deadline: str | None = None


    @field_validator(
        "deadline"
    )
    @classmethod
    def validate_deadline(
        cls,
        value
    ):

        if (
            value is None
            or value == ""
        ):
            return None

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                "Deadline must use "
                "YYYY-MM-DD format"
            )

        return value


# =========================================================
# HELPERS
# =========================================================

def transaction_to_dict(
    transaction
):
    return {
        "id": transaction[0],
        "type": transaction[1],
        "amount": transaction[2],
        "category": transaction[3],
        "description": transaction[4],
        "transaction_date":
            transaction[5],
        "created_at":
            transaction[6]
    }


def savings_goal_to_dict(
    goal
):

    target = goal[2]
    saved = goal[3]

    remaining = max(
        target - saved,
        0
    )

    percentage = (
        (saved / target) * 100
        if target > 0
        else 0
    )

    return {
        "id": goal[0],
        "name": goal[1],
        "target_amount": target,
        "saved_amount": saved,
        "remaining_amount":
            remaining,
        "progress_percentage":
            round(
                percentage,
                2
            ),
        "completed":
            saved >= target,
        "deadline": goal[4],
        "created_at": goal[5]
    }


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "name":
            "SpendWise LK API",

        "version":
            "1.0.0",

        "message":
            "Welcome to SpendWise LK API"
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():

    return FileResponse(
        "frontend/index.html"
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "message":
            "SpendWise LK API is running"
    }


# =========================================================
# GET TRANSACTIONS
# =========================================================

@app.get("/transactions")
def read_transactions():

    transactions = (
        get_transactions()
    )

    return {
        "count":
            len(transactions),

        "transactions": [
            transaction_to_dict(
                transaction
            )
            for transaction
            in transactions
        ]
    }


# =========================================================
# GET ONE TRANSACTION
# =========================================================

@app.get(
    "/transactions/{transaction_id}"
)
def read_transaction(
    transaction_id: int
):

    transaction = (
        get_transaction_by_id(
            transaction_id
        )
    )

    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Transaction not found"
            )
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
    transaction: TransactionData
):

    transaction_id = (
        add_transaction(
            transaction.type,
            transaction.amount,
            transaction.category.strip(),
            transaction.description.strip(),
            transaction.transaction_date
        )
    )

    created = (
        get_transaction_by_id(
            transaction_id
        )
    )

    return {
        "message":
            "Transaction added successfully",

        "transaction":
            transaction_to_dict(
                created
            )
    }


# =========================================================
# UPDATE TRANSACTION
# =========================================================

@app.put(
    "/transactions/{transaction_id}"
)
def edit_transaction(
    transaction_id: int,
    transaction: TransactionData
):

    existing = (
        get_transaction_by_id(
            transaction_id
        )
    )

    if existing is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Transaction not found"
            )
        )

    update_transaction(
        transaction_id,
        transaction.type,
        transaction.amount,
        transaction.category.strip(),
        transaction.description.strip(),
        transaction.transaction_date
    )

    updated = (
        get_transaction_by_id(
            transaction_id
        )
    )

    return {
        "message":
            "Transaction updated successfully",

        "transaction":
            transaction_to_dict(
                updated
            )
    }


# =========================================================
# DELETE TRANSACTION
# =========================================================

@app.delete(
    "/transactions/{transaction_id}"
)
def remove_transaction(
    transaction_id: int
):

    if (
        get_transaction_by_id(
            transaction_id
        )
        is None
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Transaction not found"
            )
        )

    delete_transaction(
        transaction_id
    )

    return {
        "message":
            "Transaction deleted successfully",

        "deleted_id":
            transaction_id
    }


# =========================================================
# BALANCE
# =========================================================

@app.get("/balance")
def read_balance():

    (
        total_income,
        total_expense,
        balance
    ) = get_balance_summary()

    return {
        "total_income":
            total_income,

        "total_expense":
            total_expense,

        "balance":
            balance
    }


# =========================================================
# MONTHLY ANALYTICS
# =========================================================

@app.get(
    "/analytics/monthly"
)
def monthly_analytics(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):

    (
        income,
        expense,
        balance
    ) = get_monthly_summary(
        year,
        month
    )

    return {
        "year": year,
        "month": month,
        "total_income": income,
        "total_expense": expense,
        "balance": balance
    }


# =========================================================
# CATEGORY ANALYTICS
# =========================================================

@app.get(
    "/analytics/categories"
)
def category_analytics(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):

    spending = (
        get_category_spending(
            year,
            month
        )
    )

    total_expense = sum(
        amount
        for _, amount
        in spending
    )

    categories = []

    for (
        category,
        amount
    ) in spending:

        percentage = (
            amount / total_expense * 100
            if total_expense > 0
            else 0
        )

        categories.append({
            "category": category,
            "amount": amount,
            "percentage":
                round(
                    percentage,
                    2
                )
        })

    return {
        "year": year,
        "month": month,
        "total_expense":
            total_expense,
        "categories":
            categories
    }


# =========================================================
# MONTHLY TRENDS
# =========================================================

@app.get(
    "/analytics/trends"
)
def monthly_trends(
    months: int = Query(
        default=6,
        ge=1,
        le=24
    )
):

    trends = (
        get_monthly_trends(
            months
        )
    )

    return {
        "months_requested":
            months,

        "count":
            len(trends),

        "trends":
            trends
    }


# =========================================================
# CREATE / UPDATE BUDGET
# =========================================================

@app.post("/budgets")
def create_budget(
    budget: BudgetData
):

    set_budget(
        budget.year,
        budget.month,
        budget.category.strip(),
        budget.amount
    )

    return {
        "message":
            "Budget saved successfully",

        "budget":
            budget
    }


# =========================================================
# GET BUDGETS
# =========================================================

@app.get("/budgets")
def read_budgets(
    year: int,
    month: int = Query(
        ge=1,
        le=12
    )
):

    budgets = (
        get_budgets(
            year,
            month
        )
    )

    results = []

    for (
        category,
        budget_amount
    ) in budgets:

        spent = (
            get_category_expense(
                year,
                month,
                category
            )
        )

        remaining = (
            budget_amount - spent
        )

        percentage = (
            spent
            / budget_amount
            * 100

            if budget_amount > 0
            else 0
        )

        results.append({
            "category":
                category,

            "budget":
                budget_amount,

            "spent":
                spent,

            "remaining":
                remaining,

            "percentage_used":
                round(
                    percentage,
                    2
                ),

            "exceeded":
                spent > budget_amount
        })

    return {
        "year": year,
        "month": month,
        "budgets": results
    }


# =========================================================
# CREATE SAVINGS GOAL
# =========================================================

@app.post(
    "/savings-goals",
    status_code=201
)
def create_savings_goal(
    goal: SavingsGoalData
):

    goal_id = (
        add_savings_goal(
            goal.name.strip(),
            goal.target_amount,
            goal.saved_amount,
            goal.deadline
        )
    )

    created = (
        get_savings_goal_by_id(
            goal_id
        )
    )

    return {
        "message":
            "Savings goal created successfully",

        "goal":
            savings_goal_to_dict(
                created
            )
    }


# =========================================================
# GET SAVINGS GOALS
# =========================================================

@app.get(
    "/savings-goals"
)
def read_savings_goals():

    goals = (
        get_savings_goals()
    )

    return {
        "count": len(goals),

        "goals": [
            savings_goal_to_dict(
                goal
            )
            for goal in goals
        ]
    }


# =========================================================
# GET ONE SAVINGS GOAL
# =========================================================

@app.get(
    "/savings-goals/{goal_id}"
)
def read_savings_goal(
    goal_id: int
):

    goal = (
        get_savings_goal_by_id(
            goal_id
        )
    )

    if goal is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Savings goal not found"
            )
        )

    return savings_goal_to_dict(
        goal
    )


# =========================================================
# UPDATE SAVINGS GOAL
# =========================================================

@app.put(
    "/savings-goals/{goal_id}"
)
def edit_savings_goal(
    goal_id: int,
    goal: SavingsGoalData
):

    existing = (
        get_savings_goal_by_id(
            goal_id
        )
    )

    if existing is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Savings goal not found"
            )
        )

    update_savings_goal(
        goal_id,
        goal.name.strip(),
        goal.target_amount,
        goal.saved_amount,
        goal.deadline
    )

    updated = (
        get_savings_goal_by_id(
            goal_id
        )
    )

    return {
        "message":
            "Savings goal updated successfully",

        "goal":
            savings_goal_to_dict(
                updated
            )
    }


# =========================================================
# DELETE SAVINGS GOAL
# =========================================================

@app.delete(
    "/savings-goals/{goal_id}"
)
def remove_savings_goal(
    goal_id: int
):

    existing = (
        get_savings_goal_by_id(
            goal_id
        )
    )

    if existing is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "Savings goal not found"
            )
        )

    delete_savings_goal(
        goal_id
    )

    return {
        "message":
            "Savings goal deleted successfully",

        "deleted_id":
            goal_id
    }