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
            transaction_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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