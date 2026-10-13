# SpendWise LK

SpendWise LK is a personal finance management web application built with Python, FastAPI, SQLite, HTML, CSS, and JavaScript.

The application helps users record income and expenses, monitor monthly budgets, track savings goals, manage recurring transactions, analyze spending behaviour, export transaction data, generate smart financial insights, and estimate future expenses.

## Features

- Add income and expense transactions
- Edit and delete transactions
- View transaction history
- View total income, total expenses, and current balance
- Monthly financial analytics
- Category-wise spending analysis
- Income vs expense charts
- Multi-month financial trend visualization
- Set monthly budgets by category
- Monitor budget usage and warnings
- Create and track savings goals
- Manage recurring monthly transactions
- Export transaction history as CSV
- Smart spending insights
- Savings rate calculation
- Highest spending category detection
- Month-to-month expense comparison
- Budget alerts and recommendations
- Next-month expense forecasting
- REST API with Swagger documentation
- Responsive finance dashboard

## Smart Spending Insights

SpendWise LK analyzes monthly financial activity and generates useful insights such as:

- Monthly savings rate
- Highest spending category
- Spending changes compared with the previous month
- Budget usage warnings
- Automatic spending recommendations

## Expense Forecasting

The application includes a simple statistical forecasting feature that estimates next month's expenses using recent monthly spending history.

The forecast uses:

- Recent monthly average expenses
- Recent spending trend
- Trend adjustment
- Confidence level based on available historical data

This feature is intended as a simple financial planning estimate and not as financial advice.

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### Database

- SQLite

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### Development Tools

- Visual Studio Code
- Git
- GitHub

## Project Structure

```text
SpendWise-LK/
│
├── api.py
├── app.py
├── database.py
├── spendwise.db
├── README.md
├── requirements.txt
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── docs/

## Screenshots

### Dashboard Overview

![SpendWise LK Dashboard](docs/dashboard-overview.png)

### Smart Spending Insights

![Smart Spending Insights](docs/smart-insights.png)

### Expense Forecasting

![Expense Forecasting](docs/expense-forecast.png)

### REST API Documentation

![Swagger API Documentation](docs/swagger-api.png)
