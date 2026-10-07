import sqlite3


DATABASE_NAME = "spendwise.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Transactions table
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

    # Budgets table
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

    connection.commit()
    connection.close()


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

    connection.commit()
    connection.close()


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

    transactions = cursor.fetchall()

    connection.close()

    return transactions


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

    transactions = cursor.fetchall()

    connection.close()

    return transactions


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

    return total_income, total_expense, balance


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

    return total_income, total_expense, balance


# =========================
# BUDGET FUNCTIONS
# =========================

def set_budget(year, month, category, amount):
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

    budgets = cursor.fetchall()

    connection.close()

    return budgets


def get_category_expense(year, month, category):
    connection = get_connection()
    cursor = connection.cursor()

    month_value = f"{year}-{month:02d}"

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
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