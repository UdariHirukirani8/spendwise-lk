// =========================================================
// CATEGORY DATA
// =========================================================

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


// =========================================================
// GLOBAL STATE
// =========================================================

let editingTransactionId = null;

let editingGoalId = null;

let categoryChart = null;

let monthlyChart = null;

let trendChart = null;


// =========================================================
// TRANSACTION CATEGORY DROPDOWN
// =========================================================

function updateCategoryOptions() {

    const type =
        document.getElementById(
            "type"
        ).value;


    const categorySelect =
        document.getElementById(
            "category"
        );


    const categories =
        type === "income"
            ? incomeCategories
            : expenseCategories;


    categorySelect.innerHTML =
        '<option value="">Select category</option>';


    categories.forEach(
        category => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                category;


            option.textContent =
                category;


            categorySelect.appendChild(
                option
            );
        }
    );
}


// =========================================================
// BUDGET CATEGORY DROPDOWN
// =========================================================

function loadBudgetCategories() {

    const select =
        document.getElementById(
            "budgetCategory"
        );


    select.innerHTML =
        '<option value="">Select category</option>';


    expenseCategories.forEach(
        category => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                category;


            option.textContent =
                category;


            select.appendChild(
                option
            );
        }
    );
}


// =========================================================
// LOAD BALANCE
// =========================================================

async function loadBalance() {

    try {

        const response =
            await fetch(
                "/balance"
            );


        if (!response.ok) {

            throw new Error(
                "Could not load balance."
            );
        }


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

    catch (error) {

        console.error(
            "Balance error:",
            error
        );
    }
}


// =========================================================
// LOAD TRANSACTIONS
// =========================================================

async function loadTransactions() {

    try {

        const response =
            await fetch(
                "/transactions"
            );


        if (!response.ok) {

            throw new Error(
                "Could not load transactions."
            );
        }


        const data =
            await response.json();


        const tableBody =
            document.getElementById(
                "transactionTableBody"
            );


        tableBody.innerHTML = "";


        if (
            !data.transactions
            ||
            data.transactions.length === 0
        ) {

            tableBody.innerHTML = `
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
                    document.createElement(
                        "tr"
                    );


                row.innerHTML = `
                    <td>
                        ${transaction.id}
                    </td>

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


                tableBody.appendChild(
                    row
                );
            }
        );

    }

    catch (error) {

        console.error(
            "Transaction loading error:",
            error
        );
    }
}


// =========================================================
// SAVE TRANSACTION
// CREATE OR UPDATE
// =========================================================

async function saveTransaction(
    event
) {

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
            )
            .value
            .trim(),


        transaction_date:
            document.getElementById(
                "transactionDate"
            ).value
    };


    const message =
        document.getElementById(
            "formMessage"
        );


    if (
        !transaction.category
        ||
        transaction.amount <= 0
        ||
        !transaction.transaction_date
    ) {

        message.textContent =
            "Please complete all required fields.";

        return;
    }


    let url =
        "/transactions";


    let method =
        "POST";


    const isEditing =
        editingTransactionId !== null;


    if (isEditing) {

        url =
            `/transactions/${editingTransactionId}`;


        method =
            "PUT";
    }


    try {

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
                typeof data.detail === "string"
                    ? data.detail
                    : "Could not save transaction.";

            return;
        }


        message.textContent =
            isEditing
                ? "Transaction updated successfully."
                : "Transaction added successfully.";


        resetTransactionForm();


        await refreshDashboard();


        await loadTrendAnalytics();

    }

    catch (error) {

        console.error(
            "Transaction save error:",
            error
        );


        message.textContent =
            "Server connection failed.";
    }
}


// =========================================================
// START EDIT TRANSACTION
// =========================================================

async function startEditTransaction(
    transactionId
) {

    try {

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


        document.getElementById(
            "transactionForm"
        ).scrollIntoView({
            behavior: "smooth"
        });

    }

    catch (error) {

        console.error(
            "Edit transaction error:",
            error
        );
    }
}


// =========================================================
// DELETE TRANSACTION
// =========================================================

async function deleteTransaction(
    transactionId
) {

    const confirmed =
        confirm(
            `Delete transaction #${transactionId}?`
        );


    if (!confirmed) {

        return;
    }


    try {

        const response =
            await fetch(
                `/transactions/${transactionId}`,
                {
                    method:
                        "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Could not delete transaction."
            );

            return;
        }


        if (
            editingTransactionId
            === transactionId
        ) {

            resetTransactionForm();
        }


        await refreshDashboard();


        await loadTrendAnalytics();

    }

    catch (error) {

        console.error(
            "Delete transaction error:",
            error
        );
    }
}


// =========================================================
// RESET TRANSACTION FORM
// =========================================================

function resetTransactionForm() {

    editingTransactionId =
        null;


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
// CANCEL TRANSACTION EDIT
// =========================================================

function cancelEdit() {

    resetTransactionForm();


    document.getElementById(
        "formMessage"
    ).textContent =
        "Edit cancelled.";
}


// =========================================================
// MONTHLY ANALYTICS
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


    if (
        Number(month) < 1
        ||
        Number(month) > 12
    ) {

        alert(
            "Month must be between 1 and 12."
        );

        return;
    }


    syncBudgetDate(
        year,
        month
    );


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

    const output =
        document.getElementById(
            "categoryAnalytics"
        );


    try {

        const response =
            await fetch(
                `/analytics/categories?year=${year}&month=${month}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            output.innerHTML =
                "<p>Could not load category analytics.</p>";

            return;
        }


        if (
            !data.categories
            ||
            data.categories.length === 0
        ) {

            output.innerHTML =
                "<p>No spending data found.</p>";


            if (categoryChart) {

                categoryChart.destroy();

                categoryChart =
                    null;
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

                            (${Number(
                                item.percentage
                            ).toFixed(1)}%)
                        </span>

                    </div>
                `;
            }
        );


        drawCategoryChart(
            data.categories
        );

    }

    catch (error) {

        console.error(
            "Category analytics error:",
            error
        );


        output.innerHTML =
            "<p>Server connection failed.</p>";
    }
}


// =========================================================
// CATEGORY CHART
// =========================================================

function drawCategoryChart(
    categories
) {

    const canvas =
        document.getElementById(
            "categoryChart"
        );


    if (!canvas) {

        return;
    }


    if (categoryChart) {

        categoryChart.destroy();
    }


    categoryChart =
        new Chart(
            canvas,
            {
                type:
                    "doughnut",

                data: {

                    labels:
                        categories.map(
                            item =>
                                item.category
                        ),

                    datasets: [
                        {
                            data:
                                categories.map(
                                    item =>
                                        item.amount
                                )
                        }
                    ]
                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false
                }
            }
        );
}


// =========================================================
// MONTHLY INCOME VS EXPENSE
// =========================================================

async function loadMonthlyAnalytics(
    year,
    month
) {

    try {

        const response =
            await fetch(
                `/analytics/monthly?year=${year}&month=${month}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            return;
        }


        drawMonthlyChart(
            data.total_income,
            data.total_expense
        );

    }

    catch (error) {

        console.error(
            "Monthly analytics error:",
            error
        );
    }
}


// =========================================================
// MONTHLY CHART
// =========================================================

function drawMonthlyChart(
    income,
    expense
) {

    const canvas =
        document.getElementById(
            "monthlyChart"
        );


    if (!canvas) {

        return;
    }


    if (monthlyChart) {

        monthlyChart.destroy();
    }


    monthlyChart =
        new Chart(
            canvas,
            {
                type:
                    "bar",

                data: {

                    labels: [
                        "Income",
                        "Expenses"
                    ],

                    datasets: [
                        {
                            label:
                                "Amount (Rs.)",

                            data: [
                                income,
                                expense
                            ]
                        }
                    ]
                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    scales: {

                        y: {
                            beginAtZero:
                                true
                        }
                    }
                }
            }
        );
}


// =========================================================
// FINANCIAL TREND
// =========================================================

async function loadTrendAnalytics() {

    const trendSelect =
        document.getElementById(
            "trendMonths"
        );


    if (!trendSelect) {

        return;
    }


    const months =
        trendSelect.value;


    try {

        const response =
            await fetch(
                `/analytics/trends?months=${months}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            console.error(
                "Trend endpoint error:",
                data
            );

            return;
        }


        drawTrendChart(
            data.trends
        );

    }

    catch (error) {

        console.error(
            "Trend analytics error:",
            error
        );
    }
}


// =========================================================
// TREND CHART
// =========================================================

function drawTrendChart(
    trends
) {

    const canvas =
        document.getElementById(
            "trendChart"
        );


    if (!canvas) {

        return;
    }


    if (trendChart) {

        trendChart.destroy();
    }


    if (
        !trends
        ||
        trends.length === 0
    ) {

        return;
    }


    trendChart =
        new Chart(
            canvas,
            {
                type:
                    "line",

                data: {

                    labels:
                        trends.map(
                            item =>
                                item.month
                        ),

                    datasets: [

                        {
                            label:
                                "Income",

                            data:
                                trends.map(
                                    item =>
                                        item.income
                                ),

                            tension:
                                0.3
                        },


                        {
                            label:
                                "Expenses",

                            data:
                                trends.map(
                                    item =>
                                        item.expense
                                ),

                            tension:
                                0.3
                        },


                        {
                            label:
                                "Savings",

                            data:
                                trends.map(
                                    item =>
                                        item.savings
                                ),

                            tension:
                                0.3
                        }

                    ]
                },

                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    interaction: {

                        mode:
                            "index",

                        intersect:
                            false
                    },

                    scales: {

                        y: {
                            beginAtZero:
                                true
                        }
                    }
                }
            }
        );
}


// =========================================================
// SAVE BUDGET
// =========================================================

async function saveBudget(
    event
) {

    event.preventDefault();


    const year =
        Number(
            document.getElementById(
                "budgetYear"
            ).value
        );


    const month =
        Number(
            document.getElementById(
                "budgetMonth"
            ).value
        );


    const category =
        document.getElementById(
            "budgetCategory"
        ).value;


    const amount =
        Number(
            document.getElementById(
                "budgetAmount"
            ).value
        );


    const message =
        document.getElementById(
            "budgetMessage"
        );


    if (
        !year
        ||
        month < 1
        ||
        month > 12
        ||
        !category
        ||
        amount <= 0
    ) {

        message.textContent =
            "Please enter valid budget details.";

        return;
    }


    try {

        const response =
            await fetch(
                "/budgets",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            year:
                                year,

                            month:
                                month,

                            category:
                                category,

                            amount:
                                amount
                        })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            message.textContent =
                typeof data.detail === "string"
                    ? data.detail
                    : "Could not save budget.";

            return;
        }


        message.textContent =
            "Budget saved successfully.";


        document.getElementById(
            "budgetAmount"
        ).value =
            "";


        document.getElementById(
            "analyticsYear"
        ).value =
            year;


        document.getElementById(
            "analyticsMonth"
        ).value =
            month;


        await loadBudgets(
            year,
            month
        );

    }

    catch (error) {

        console.error(
            "Save budget error:",
            error
        );


        message.textContent =
            "Server connection failed.";
    }
}


// =========================================================
// LOAD BUDGETS
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
            "<p>Please select year and month.</p>";

        return;
    }


    syncBudgetDate(
        year,
        month
    );


    try {

        const response =
            await fetch(
                `/budgets?year=${year}&month=${month}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            container.innerHTML =
                "<p>Could not load budgets.</p>";

            return;
        }


        if (
            !data.budgets
            ||
            data.budgets.length === 0
        ) {

            container.innerHTML =
                "<p>No budgets found for this month.</p>";

            return;
        }


        container.innerHTML = "";


        data.budgets.forEach(
            budget => {

                const percentage =
                    Number(
                        budget.percentage_used
                    );


                const progress =
                    Math.min(
                        percentage,
                        100
                    );


                let warning =
                    "";


                if (
                    budget.exceeded
                ) {

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


                        <div class="budget-details">

                            <p>
                                Budget:
                                <strong>
                                    Rs.
                                    ${Number(
                                        budget.budget
                                    ).toFixed(2)}
                                </strong>
                            </p>


                            <p>
                                Spent:
                                <strong>
                                    Rs.
                                    ${Number(
                                        budget.spent
                                    ).toFixed(2)}
                                </strong>
                            </p>


                            <p>
                                Remaining:
                                <strong>
                                    Rs.
                                    ${Number(
                                        budget.remaining
                                    ).toFixed(2)}
                                </strong>
                            </p>

                        </div>


                        <div class="progress-container">

                            <div
                                class="progress-bar"
                                style="
                                    width:
                                    ${progress}%;
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

    catch (error) {

        console.error(
            "Load budgets error:",
            error
        );


        container.innerHTML =
            "<p>Server connection failed.</p>";
    }
}


// =========================================================
// SYNC BUDGET DATE
// =========================================================

function syncBudgetDate(
    year,
    month
) {

    document.getElementById(
        "budgetYear"
    ).value =
        year;


    document.getElementById(
        "budgetMonth"
    ).value =
        month;
}


// =========================================================
// LOAD SAVINGS GOALS
// =========================================================

async function loadSavingsGoals() {

    const container =
        document.getElementById(
            "savingsGoalsContainer"
        );


    if (!container) {

        return;
    }


    try {

        const response =
            await fetch(
                "/savings-goals"
            );


        const data =
            await response.json();


        if (!response.ok) {

            container.innerHTML =
                "<p>Could not load savings goals.</p>";

            return;
        }


        if (
            !data.goals
            ||
            data.goals.length === 0
        ) {

            container.innerHTML =
                "<p>No savings goals yet.</p>";

            return;
        }


        container.innerHTML =
            "";


        data.goals.forEach(
            goal => {

                const percentage =
                    Number(
                        goal.progress_percentage
                    );


                const progress =
                    Math.min(
                        percentage,
                        100
                    );


                const deadline =
                    goal.deadline
                    ||
                    "No deadline";


                const completedMessage =
                    goal.completed
                    ? `
                        <p class="goal-completed">
                            Goal completed!
                        </p>
                    `
                    : "";


                container.innerHTML += `
                    <div class="savings-goal-card">

                        <div class="goal-header">

                            <h3>
                                ${goal.name}
                            </h3>

                            <span class="goal-status">
                                ${percentage.toFixed(1)}%
                            </span>

                        </div>


                        <div class="goal-details">

                            <p>
                                Target:
                                <strong>
                                    Rs.
                                    ${Number(
                                        goal.target_amount
                                    ).toFixed(2)}
                                </strong>
                            </p>


                            <p>
                                Saved:
                                <strong>
                                    Rs.
                                    ${Number(
                                        goal.saved_amount
                                    ).toFixed(2)}
                                </strong>
                            </p>


                            <p>
                                Remaining:
                                <strong>
                                    Rs.
                                    ${Number(
                                        goal.remaining_amount
                                    ).toFixed(2)}
                                </strong>
                            </p>

                        </div>


                        <p>
                            Deadline:
                            <strong>
                                ${deadline}
                            </strong>
                        </p>


                        <div class="goal-progress-container">

                            <div
                                class="goal-progress-bar"
                                style="
                                    width:
                                    ${progress}%;
                                "
                            >
                            </div>

                        </div>


                        <p class="goal-progress-text">
                            ${percentage.toFixed(1)}%
                            complete
                        </p>


                        ${completedMessage}


                        <div class="goal-actions">

                            <button
                                class="secondary-button"
                                onclick="startEditGoal(
                                    ${goal.id}
                                )"
                            >
                                Edit
                            </button>


                            <button
                                class="delete-button"
                                onclick="deleteGoal(
                                    ${goal.id}
                                )"
                            >
                                Delete
                            </button>

                        </div>

                    </div>
                `;
            }
        );

    }

    catch (error) {

        console.error(
            "Savings goals load error:",
            error
        );


        container.innerHTML =
            "<p>Server connection failed.</p>";
    }
}


// =========================================================
// SAVE SAVINGS GOAL
// =========================================================

async function saveSavingsGoal(
    event
) {

    event.preventDefault();


    const goal = {

        name:
            document.getElementById(
                "goalName"
            )
            .value
            .trim(),


        target_amount:
            Number(
                document.getElementById(
                    "goalTarget"
                ).value
            ),


        saved_amount:
            Number(
                document.getElementById(
                    "goalSaved"
                ).value
            ),


        deadline:
            document.getElementById(
                "goalDeadline"
            ).value
            ||
            null
    };


    const message =
        document.getElementById(
            "goalMessage"
        );


    if (
        !goal.name
        ||
        goal.target_amount <= 0
        ||
        goal.saved_amount < 0
    ) {

        message.textContent =
            "Please enter valid savings goal details.";

        return;
    }


    let url =
        "/savings-goals";


    let method =
        "POST";


    const isEditing =
        editingGoalId !== null;


    if (isEditing) {

        url =
            `/savings-goals/${editingGoalId}`;


        method =
            "PUT";
    }


    try {

        const response =
            await fetch(
                url,
                {
                    method:
                        method,

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            goal
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            message.textContent =
                typeof data.detail === "string"
                    ? data.detail
                    : "Could not save savings goal.";

            return;
        }


        message.textContent =
            isEditing
                ? "Savings goal updated successfully."
                : "Savings goal created successfully.";


        resetSavingsGoalForm();


        await loadSavingsGoals();

    }

    catch (error) {

        console.error(
            "Savings goal save error:",
            error
        );


        message.textContent =
            "Server connection failed.";
    }
}


// =========================================================
// EDIT SAVINGS GOAL
// =========================================================

async function startEditGoal(
    goalId
) {

    try {

        const response =
            await fetch(
                `/savings-goals/${goalId}`
            );


        if (!response.ok) {

            alert(
                "Could not load savings goal."
            );

            return;
        }


        const goal =
            await response.json();


        editingGoalId =
            goal.id;


        document.getElementById(
            "goalName"
        ).value =
            goal.name;


        document.getElementById(
            "goalTarget"
        ).value =
            goal.target_amount;


        document.getElementById(
            "goalSaved"
        ).value =
            goal.saved_amount;


        document.getElementById(
            "goalDeadline"
        ).value =
            goal.deadline || "";


        document.getElementById(
            "goalSubmitButton"
        ).textContent =
            "Update Goal";


        document.getElementById(
            "cancelGoalEditButton"
        ).style.display =
            "inline-block";


        document.getElementById(
            "goalMessage"
        ).textContent =
            `Editing savings goal #${goal.id}`;


        document.getElementById(
            "savingsGoalForm"
        ).scrollIntoView({
            behavior:
                "smooth"
        });

    }

    catch (error) {

        console.error(
            "Savings goal edit error:",
            error
        );
    }
}


// =========================================================
// DELETE SAVINGS GOAL
// =========================================================

async function deleteGoal(
    goalId
) {

    const confirmed =
        confirm(
            `Delete savings goal #${goalId}?`
        );


    if (!confirmed) {

        return;
    }


    try {

        const response =
            await fetch(
                `/savings-goals/${goalId}`,
                {
                    method:
                        "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Could not delete savings goal."
            );

            return;
        }


        if (
            editingGoalId
            === goalId
        ) {

            resetSavingsGoalForm();
        }


        await loadSavingsGoals();

    }

    catch (error) {

        console.error(
            "Savings goal delete error:",
            error
        );
    }
}


// =========================================================
// RESET SAVINGS GOAL FORM
// =========================================================

function resetSavingsGoalForm() {

    editingGoalId =
        null;


    document.getElementById(
        "savingsGoalForm"
    ).reset();


    document.getElementById(
        "goalSaved"
    ).value =
        "0";


    document.getElementById(
        "goalSubmitButton"
    ).textContent =
        "Create Goal";


    document.getElementById(
        "cancelGoalEditButton"
    ).style.display =
        "none";
}


// =========================================================
// CANCEL SAVINGS GOAL EDIT
// =========================================================

function cancelGoalEdit() {

    resetSavingsGoalForm();


    document.getElementById(
        "goalMessage"
    ).textContent =
        "Edit cancelled.";
}


// =========================================================
// TODAY DATE
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
// DEFAULT YEAR / MONTH
// =========================================================

function setDefaultDates() {

    const now =
        new Date();


    const year =
        now.getFullYear();


    const month =
        now.getMonth() + 1;


    document.getElementById(
        "analyticsYear"
    ).value =
        year;


    document.getElementById(
        "analyticsMonth"
    ).value =
        month;


    document.getElementById(
        "budgetYear"
    ).value =
        year;


    document.getElementById(
        "budgetMonth"
    ).value =
        month;
}


// =========================================================
// REFRESH DASHBOARD
// =========================================================

async function refreshDashboard() {

    await Promise.all([
        loadBalance(),
        loadTransactions(),
        loadSavingsGoals()
    ]);
}


// =========================================================
// EVENT LISTENERS
// =========================================================

document
    .getElementById(
        "type"
    )
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
        "budgetForm"
    )
    .addEventListener(
        "submit",
        saveBudget
    );


document
    .getElementById(
        "loadBudgetsButton"
    )
    .addEventListener(
        "click",
        () => loadBudgets()
    );


document
    .getElementById(
        "trendMonths"
    )
    .addEventListener(
        "change",
        loadTrendAnalytics
    );


document
    .getElementById(
        "savingsGoalForm"
    )
    .addEventListener(
        "submit",
        saveSavingsGoal
    );


document
    .getElementById(
        "cancelGoalEditButton"
    )
    .addEventListener(
        "click",
        cancelGoalEdit
    );


// =========================================================
// INITIALIZE DASHBOARD
// =========================================================

updateCategoryOptions();

loadBudgetCategories();

setTodayDate();

setDefaultDates();

refreshDashboard();

loadTrendAnalytics();