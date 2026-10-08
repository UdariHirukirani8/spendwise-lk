import sqlite3


DATABASE_NAME = "spendwise.db"


# =========================================================
# CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, month, category)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            saved_amount REAL NOT NULL DEFAULT 0,
            deadline TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# ADD TRANSACTION
# =========================================================

def add_transaction(
    transaction_type,
    amount,
    category,
    description,
    transaction_date
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions (
            type,
            amount,
            category,
            description,
            transaction_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_type,
        amount,
        category,
        description,
        transaction_date
    ))

    transaction_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return transaction_id


# =========================================================
# GET ALL TRANSACTIONS
# =========================================================

def get_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            type,
            amount,
            category,
            description,
            transaction_date,
            created_at
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


# =========================================================
# GET ONE TRANSACTION
# =========================================================

def get_transaction_by_id(transaction_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            type,
            amount,
            category,
            description,
            transaction_date,
            created_at
        FROM transactions
        WHERE id = ?
    """, (transaction_id,))

    result = cursor.fetchone()

    connection.close()

    return result


# =========================================================
# UPDATE TRANSACTION
# =========================================================

def update_transaction(
    transaction_id,
    transaction_type,
    amount,
    category,
    description,
    transaction_date
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET
            type = ?,
            amount = ?,
            category = ?,
            description = ?,
            transaction_date = ?
        WHERE id = ?
    """, (
        transaction_type,
        amount,
        category,
        description,
        transaction_date,
        transaction_id
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows > 0


# =========================================================
# DELETE TRANSACTION
# =========================================================

def delete_transaction(transaction_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows > 0


# =========================================================
# TRANSACTIONS BY MONTH
# =========================================================

def get_transactions_by_month(year, month):
    connection = get_connection()
    cursor = connection.cursor()

    month_value = f"{year}-{month:02d}"

    cursor.execute("""
        SELECT
            id,
            type,
            amount,
            category,
            description,
            transaction_date,
            created_at
        FROM transactions
        WHERE substr(transaction_date, 1, 7) = ?
        ORDER BY transaction_date DESC, id DESC
    """, (month_value,))

    results = cursor.fetchall()

    connection.close()

    return results


# =========================================================
# OVERALL BALANCE
# =========================================================

def get_balance_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ),
            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            )
        FROM transactions
    """)

    result = cursor.fetchone()

    connection.close()

    total_income = result[0]
    total_expense = result[1]

    balance = total_income - total_expense

    return (
        total_income,
        total_expense,
        balance
    )


# =========================================================
# MONTHLY SUMMARY
# =========================================================

def get_monthly_summary(year, month):
    connection = get_connection()
    cursor = connection.cursor()

    month_value = f"{year}-{month:02d}"

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ),
            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            )
        FROM transactions
        WHERE substr(transaction_date, 1, 7) = ?
    """, (month_value,))

    result = cursor.fetchone()

    connection.close()

    total_income = result[0]
    total_expense = result[1]

    balance = total_income - total_expense

    return (
        total_income,
        total_expense,
        balance
    )


# =========================================================
# CATEGORY SPENDING
# =========================================================

def get_category_spending(year, month):
    connection = get_connection()
    cursor = connection.cursor()

    month_value = f"{year}-{month:02d}"

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total_spent
        FROM transactions
        WHERE type = 'expense'
        AND substr(transaction_date, 1, 7) = ?
        GROUP BY category
        ORDER BY total_spent DESC
    """, (month_value,))

    results = cursor.fetchall()

    connection.close()

    return results


# =========================================================
# SET BUDGET
# =========================================================

def set_budget(
    year,
    month,
    category,
    amount
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (
            year,
            month,
            category,
            amount
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(year, month, category)
        DO UPDATE SET
            amount = excluded.amount
    """, (
        year,
        month,
        category,
        amount
    ))

    connection.commit()
    connection.close()


# =========================================================
# GET BUDGETS
# =========================================================

def get_budgets(year, month):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            amount
        FROM budgets
        WHERE year = ?
        AND month = ?
        ORDER BY category
    """, (
        year,
        month
    ))

    results = cursor.fetchall()

    connection.close()

    return results


# =========================================================
# CATEGORY EXPENSE
# =========================================================

def get_category_expense(
    year,
    month,
    category
):
    connection = get_connection()
    cursor = connection.cursor()

    month_value = f"{year}-{month:02d}"

    cursor.execute("""
        SELECT COALESCE(
            SUM(amount),
            0
        )
        FROM transactions
        WHERE type = 'expense'
        AND category = ?
        AND substr(transaction_date, 1, 7) = ?
    """, (
        category,
        month_value
    ))

    result = cursor.fetchone()

    connection.close()

    return result[0]


# =========================================================
# MONTHLY TRENDS
# =========================================================

def get_monthly_trends(months=6):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            substr(
                transaction_date,
                1,
                7
            ) AS month,

            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS income,

            COALESCE(
                SUM(
                    CASE
                        WHEN type = 'expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS expense

        FROM transactions

        GROUP BY
            substr(
                transaction_date,
                1,
                7
            )

        ORDER BY month DESC

        LIMIT ?
    """, (months,))

    rows = cursor.fetchall()

    connection.close()

    rows.reverse()

    results = []

    for (
        month_value,
        income,
        expense
    ) in rows:

        results.append({
            "month": month_value,
            "income": income,
            "expense": expense,
            "savings": (
                income - expense
            )
        })

    return results


# =========================================================
# ADD SAVINGS GOAL
# =========================================================

def add_savings_goal(
    name,
    target_amount,
    saved_amount,
    deadline
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO savings_goals (
            name,
            target_amount,
            saved_amount,
            deadline
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        target_amount,
        saved_amount,
        deadline
    ))

    goal_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return goal_id


# =========================================================
# GET SAVINGS GOALS
# =========================================================

def get_savings_goals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            target_amount,
            saved_amount,
            deadline,
            created_at
        FROM savings_goals
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


# =========================================================
# GET ONE SAVINGS GOAL
# =========================================================

def get_savings_goal_by_id(goal_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            target_amount,
            saved_amount,
            deadline,
            created_at
        FROM savings_goals
        WHERE id = ?
    """, (goal_id,))

    result = cursor.fetchone()

    connection.close()

    return result


# =========================================================
# UPDATE SAVINGS GOAL
# =========================================================

def update_savings_goal(
    goal_id,
    name,
    target_amount,
    saved_amount,
    deadline
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE savings_goals
        SET
            name = ?,
            target_amount = ?,
            saved_amount = ?,
            deadline = ?
        WHERE id = ?
    """, (
        name,
        target_amount,
        saved_amount,
        deadline,
        goal_id
    ))

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows > 0


# =========================================================
# DELETE SAVINGS GOAL
# =========================================================

def delete_savings_goal(goal_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM savings_goals
        WHERE id = ?
        """,
        (goal_id,)
    )

    connection.commit()

    deleted_rows = cursor.rowcount

    connection.close()

    return deleted_rows > 0