import sqlite3


DATABASE_NAME = "spendwise.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(transaction_type, amount, category, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions (
            type,
            amount,
            category,
            description
        )
        VALUES (?, ?, ?, ?)
    """, (
        transaction_type,
        amount,
        category,
        description
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
            created_at
        FROM transactions
        ORDER BY id DESC
    """)

    transactions = cursor.fetchall()

    connection.close()

    return transactions


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