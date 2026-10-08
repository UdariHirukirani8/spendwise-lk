const incomeCategories = [
    "Salary",
    "Freelance",
    "Business",
    "Allowance",
    "Investment",
    "Other"
];


const expenseCategories = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Health",
    "Entertainment",
    "Rent",
    "Other"
];


let editingTransactionId = null;

let categoryChart = null;
let monthlyChart = null;


// =========================================================
// CATEGORY OPTIONS
// =========================================================

function updateCategoryOptions() {

    const type =
        document.getElementById("type").value;

    const select =
        document.getElementById("category");

    const categories =
        type === "income"
            ? incomeCategories
            : expenseCategories;


    select.innerHTML =
        '<option value="">Select category</option>';


    categories.forEach(category => {

        const option =
            document.createElement("option");

        option.value = category;
        option.textContent = category;

        select.appendChild(option);
    });
}


// =========================================================
// BALANCE
// =========================================================

async function loadBalance() {

    const response =
        await fetch("/balance");

    const data =
        await response.json();


    document.getElementById(
        "totalIncome"
    ).textContent =
        `Rs. ${Number(
            data.total_income
        ).toFixed(2)}`;


    document.getElementById(
        "totalExpense"
    ).textContent =
        `Rs. ${Number(
            data.total_expense
        ).toFixed(2)}`;


    document.getElementById(
        "balance"
    ).textContent =
        `Rs. ${Number(
            data.balance
        ).toFixed(2)}`;
}


// =========================================================
// TRANSACTIONS
// =========================================================

async function loadTransactions() {

    const response =
        await fetch("/transactions");

    const data =
        await response.json();


    const body =
        document.getElementById(
            "transactionTableBody"
        );


    body.innerHTML = "";


    if (!data.transactions.length) {

        body.innerHTML = `
            <tr>
                <td colspan="7">
                    No transactions found.
                </td>
            </tr>
        `;

        return;
    }


    data.transactions.forEach(
        transaction => {

            const row =
                document.createElement("tr");


            row.innerHTML = `
                <td>${transaction.id}</td>

                <td>
                    ${transaction.transaction_date}
                </td>

                <td>
                    ${transaction.type}
                </td>

                <td>
                    ${transaction.category}
                </td>

                <td>
                    ${transaction.description || ""}
                </td>

                <td>
                    Rs. ${Number(
                        transaction.amount
                    ).toFixed(2)}
                </td>

                <td>

                    <button
                        class="secondary-button"
                        onclick="startEditTransaction(
                            ${transaction.id}
                        )"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-button"
                        onclick="deleteTransaction(
                            ${transaction.id}
                        )"
                    >
                        Delete
                    </button>

                </td>
            `;


            body.appendChild(row);
        }
    );
}


// =========================================================
// SAVE TRANSACTION
// =========================================================

async function saveTransaction(event) {

    event.preventDefault();


    const transaction = {

        type:
            document.getElementById(
                "type"
            ).value,

        amount:
            Number(
                document.getElementById(
                    "amount"
                ).value
            ),

        category:
            document.getElementById(
                "category"
            ).value,

        description:
            document.getElementById(
                "description"
            ).value.trim(),

        transaction_date:
            document.getElementById(
                "transactionDate"
            ).value
    };


    const message =
        document.getElementById(
            "formMessage"
        );


    let url = "/transactions";
    let method = "POST";


    if (editingTransactionId !== null) {

        url =
            `/transactions/${editingTransactionId}`;

        method = "PUT";
    }


    const response =
        await fetch(
            url,
            {
                method: method,

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        transaction
                    )
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        message.textContent =
            data.detail
            || "Could not save transaction.";

        return;
    }


    message.textContent =
        editingTransactionId === null
            ? "Transaction added successfully."
            : "Transaction updated successfully.";


    resetTransactionForm();

    await refreshDashboard();
}


// =========================================================
// EDIT
// =========================================================

async function startEditTransaction(
    transactionId
) {

    const response =
        await fetch(
            `/transactions/${transactionId}`
        );


    if (!response.ok) {

        alert(
            "Could not load transaction."
        );

        return;
    }


    const transaction =
        await response.json();


    editingTransactionId =
        transaction.id;


    document.getElementById(
        "type"
    ).value =
        transaction.type;


    updateCategoryOptions();


    document.getElementById(
        "category"
    ).value =
        transaction.category;


    document.getElementById(
        "amount"
    ).value =
        transaction.amount;


    document.getElementById(
        "description"
    ).value =
        transaction.description || "";


    document.getElementById(
        "transactionDate"
    ).value =
        transaction.transaction_date;


    document.getElementById(
        "submitButton"
    ).textContent =
        "Update Transaction";


    document.getElementById(
        "cancelEditButton"
    ).style.display =
        "inline-block";


    document.getElementById(
        "formMessage"
    ).textContent =
        `Editing transaction #${transaction.id}`;


    document
        .getElementById(
            "transactionForm"
        )
        .scrollIntoView({
            behavior: "smooth"
        });
}


// =========================================================
// DELETE
// =========================================================

async function deleteTransaction(
    transactionId
) {

    if (
        !confirm(
            `Delete transaction #${transactionId}?`
        )
    ) {
        return;
    }


    const response =
        await fetch(
            `/transactions/${transactionId}`,
            {
                method: "DELETE"
            }
        );


    if (!response.ok) {

        alert(
            "Could not delete transaction."
        );

        return;
    }


    await refreshDashboard();
}


// =========================================================
// RESET FORM
// =========================================================

function resetTransactionForm() {

    editingTransactionId = null;


    document.getElementById(
        "transactionForm"
    ).reset();


    document.getElementById(
        "type"
    ).value =
        "expense";


    updateCategoryOptions();

    setTodayDate();


    document.getElementById(
        "submitButton"
    ).textContent =
        "Add Transaction";


    document.getElementById(
        "cancelEditButton"
    ).style.display =
        "none";
}


// =========================================================
// CANCEL EDIT
// =========================================================

function cancelEdit() {

    resetTransactionForm();


    document.getElementById(
        "formMessage"
    ).textContent =
        "Edit cancelled.";
}


// =========================================================
// ANALYTICS
// =========================================================

async function loadAnalytics() {

    const year =
        document.getElementById(
            "analyticsYear"
        ).value;


    const month =
        document.getElementById(
            "analyticsMonth"
        ).value;


    if (!year || !month) {

        alert(
            "Please enter year and month."
        );

        return;
    }


    await Promise.all([
        loadCategoryAnalytics(
            year,
            month
        ),

        loadMonthlyAnalytics(
            year,
            month
        ),

        loadBudgets(
            year,
            month
        )
    ]);
}


// =========================================================
// CATEGORY ANALYTICS
// =========================================================

async function loadCategoryAnalytics(
    year,
    month
) {

    const response =
        await fetch(
            `/analytics/categories?year=${year}&month=${month}`
        );


    const data =
        await response.json();


    const output =
        document.getElementById(
            "categoryAnalytics"
        );


    if (!data.categories.length) {

        output.innerHTML =
            "<p>No spending data found.</p>";

        if (categoryChart) {
            categoryChart.destroy();
            categoryChart = null;
        }

        return;
    }


    output.innerHTML = `
        <p>
            Total Expenses:
            <strong>
                Rs.
                ${Number(
                    data.total_expense
                ).toFixed(2)}
            </strong>
        </p>
        <br>
    `;


    data.categories.forEach(
        item => {

            output.innerHTML += `
                <div class="analytics-row">

                    <span>
                        ${item.category}
                    </span>

                    <span>
                        Rs.
                        ${Number(
                            item.amount
                        ).toFixed(2)}

                        (${item.percentage}%)
                    </span>

                </div>
            `;
        }
    );


    drawCategoryChart(
        data.categories
    );
}


// =========================================================
// CATEGORY CHART
// =========================================================

function drawCategoryChart(
    categories
) {

    const ctx =
        document.getElementById(
            "categoryChart"
        );


    if (categoryChart) {

        categoryChart.destroy();
    }


    categoryChart =
        new Chart(
            ctx,
            {
                type: "doughnut",

                data: {

                    labels:
                        categories.map(
                            item =>
                                item.category
                        ),

                    datasets: [{
                        data:
                            categories.map(
                                item =>
                                    item.amount
                            )
                    }]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false
                }
            }
        );
}


// =========================================================
// MONTHLY ANALYTICS
// =========================================================

async function loadMonthlyAnalytics(
    year,
    month
) {

    const response =
        await fetch(
            `/analytics/monthly?year=${year}&month=${month}`
        );


    const data =
        await response.json();


    drawMonthlyChart(
        data.total_income,
        data.total_expense
    );
}


// =========================================================
// MONTHLY CHART
// =========================================================

function drawMonthlyChart(
    income,
    expense
) {

    const ctx =
        document.getElementById(
            "monthlyChart"
        );


    if (monthlyChart) {

        monthlyChart.destroy();
    }


    monthlyChart =
        new Chart(
            ctx,
            {
                type: "bar",

                data: {

                    labels: [
                        "Income",
                        "Expenses"
                    ],

                    datasets: [{
                        label:
                            "Amount (Rs.)",

                        data: [
                            income,
                            expense
                        ]
                    }]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );
}


// =========================================================
// BUDGETS
// =========================================================

async function loadBudgets(
    yearValue = null,
    monthValue = null
) {

    const year =
        yearValue
        ||
        document.getElementById(
            "analyticsYear"
        ).value;


    const month =
        monthValue
        ||
        document.getElementById(
            "analyticsMonth"
        ).value;


    const container =
        document.getElementById(
            "budgetContainer"
        );


    if (!year || !month) {

        container.innerHTML =
            "<p>Please enter year and month.</p>";

        return;
    }


    const response =
        await fetch(
            `/budgets?year=${year}&month=${month}`
        );


    const data =
        await response.json();


    if (!data.budgets.length) {

        container.innerHTML =
            "<p>No budgets found for this month.</p>";

        return;
    }


    container.innerHTML = "";


    data.budgets.forEach(
        budget => {

            let percentage =
                Number(
                    budget.percentage_used
                );


            const displayPercentage =
                Math.min(
                    percentage,
                    100
                );


            let warning = "";


            if (budget.exceeded) {

                warning = `
                    <p class="budget-danger">
                        Budget exceeded by
                        Rs.
                        ${Math.abs(
                            Number(
                                budget.remaining
                            )
                        ).toFixed(2)}
                    </p>
                `;
            }

            else if (
                percentage >= 80
            ) {

                warning = `
                    <p class="budget-warning">
                        Warning:
                        ${percentage.toFixed(1)}%
                        of this budget has been used.
                    </p>
                `;
            }


            container.innerHTML += `
                <div class="budget-card">

                    <div class="budget-header">

                        <strong>
                            ${budget.category}
                        </strong>

                        <span>
                            ${percentage.toFixed(1)}%
                        </span>

                    </div>


                    <p>
                        Budget:
                        Rs.
                        ${Number(
                            budget.budget
                        ).toFixed(2)}
                    </p>


                    <p>
                        Spent:
                        Rs.
                        ${Number(
                            budget.spent
                        ).toFixed(2)}
                    </p>


                    <p>
                        Remaining:
                        Rs.
                        ${Number(
                            budget.remaining
                        ).toFixed(2)}
                    </p>


                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="
                                width:
                                ${displayPercentage}%;
                            "
                        >
                        </div>

                    </div>


                    ${warning}

                </div>
            `;
        }
    );
}


// =========================================================
// REFRESH
// =========================================================

async function refreshDashboard() {

    await Promise.all([
        loadBalance(),
        loadTransactions()
    ]);
}


// =========================================================
// DEFAULT DATE
// =========================================================

function setTodayDate() {

    const today =
        new Date()
        .toISOString()
        .split("T")[0];


    document.getElementById(
        "transactionDate"
    ).value =
        today;
}


// =========================================================
// DEFAULT ANALYTICS DATE
// =========================================================

function setDefaultAnalyticsDate() {

    const now =
        new Date();


    document.getElementById(
        "analyticsYear"
    ).value =
        now.getFullYear();


    document.getElementById(
        "analyticsMonth"
    ).value =
        now.getMonth() + 1;
}


// =========================================================
// EVENT LISTENERS
// =========================================================

document
    .getElementById("type")
    .addEventListener(
        "change",
        updateCategoryOptions
    );


document
    .getElementById(
        "transactionForm"
    )
    .addEventListener(
        "submit",
        saveTransaction
    );


document
    .getElementById(
        "cancelEditButton"
    )
    .addEventListener(
        "click",
        cancelEdit
    );


document
    .getElementById(
        "refreshButton"
    )
    .addEventListener(
        "click",
        refreshDashboard
    );


document
    .getElementById(
        "analyticsButton"
    )
    .addEventListener(
        "click",
        loadAnalytics
    );


document
    .getElementById(
        "loadBudgetsButton"
    )
    .addEventListener(
        "click",
        () => loadBudgets()
    );


// =========================================================
// INITIAL LOAD
// =========================================================

updateCategoryOptions();

setTodayDate();

setDefaultAnalyticsDate();

refreshDashboard();