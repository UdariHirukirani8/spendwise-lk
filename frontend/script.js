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


let editingTransactionId = null;


// =========================================================
// UPDATE CATEGORY DROPDOWN
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
            "Could not load balance:",
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


        tableBody.innerHTML =
            "";


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
            "Could not load transactions:",
            error
        );
    }
}


// =========================================================
// CREATE OR UPDATE TRANSACTION
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
    ) {

        message.textContent =
            "Please select a category.";

        return;
    }


    if (
        !transaction.amount
        ||
        transaction.amount <= 0
    ) {

        message.textContent =
            "Please enter a valid amount.";

        return;
    }


    if (
        !transaction.transaction_date
    ) {

        message.textContent =
            "Please select a date.";

        return;
    }


    try {

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

            if (
                typeof data.detail
                === "string"
            ) {

                message.textContent =
                    data.detail;
            }

            else {

                message.textContent =
                    "Could not save transaction.";
            }

            console.error(
                data
            );

            return;
        }


        if (isEditing) {

            message.textContent =
                "Transaction updated successfully.";
        }

        else {

            message.textContent =
                "Transaction added successfully.";
        }


        resetTransactionForm();


        await refreshDashboard();

    }

    catch (error) {

        message.textContent =
            "Server connection failed.";


        console.error(
            error
        );
    }
}


// =========================================================
// START EDITING TRANSACTION
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


        document
            .getElementById(
                "transactionForm"
            )
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    }

    catch (error) {

        console.error(
            "Edit transaction failed:",
            error
        );
    }
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
// DELETE TRANSACTION
// =========================================================

async function deleteTransaction(
    transactionId
) {

    const confirmed =
        confirm(
            `Are you sure you want to delete transaction #${transactionId}?`
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


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.detail
                ||
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

    }

    catch (error) {

        console.error(
            "Delete failed:",
            error
        );


        alert(
            "Server connection failed."
        );
    }
}


// =========================================================
// CATEGORY ANALYTICS
// =========================================================

async function loadCategoryAnalytics() {

    const year =
        document.getElementById(
            "analyticsYear"
        ).value;


    const month =
        document.getElementById(
            "analyticsMonth"
        ).value;


    const output =
        document.getElementById(
            "categoryAnalytics"
        );


    if (
        !year
        ||
        !month
    ) {

        output.innerHTML =
            "<p>Please enter year and month.</p>";

        return;
    }


    if (
        Number(month) < 1
        ||
        Number(month) > 12
    ) {

        output.innerHTML =
            "<p>Month must be between 1 and 12.</p>";

        return;
    }


    try {

        const response =
            await fetch(
                `/analytics/categories?year=${year}&month=${month}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            output.innerHTML =
                "<p>Could not load analytics.</p>";

            return;
        }


        if (
            !data.categories
            ||
            data.categories.length === 0
        ) {

            output.innerHTML =
                "<p>No spending data found for this month.</p>";

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

    }

    catch (error) {

        console.error(
            "Analytics failed:",
            error
        );


        output.innerHTML =
            "<p>Server connection failed.</p>";
    }
}


// =========================================================
// REFRESH DASHBOARD
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
        loadCategoryAnalytics
    );


// =========================================================
// INITIALIZE DASHBOARD
// =========================================================

updateCategoryOptions();

setTodayDate();

setDefaultAnalyticsDate();

refreshDashboard();