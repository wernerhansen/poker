// script.js

document.getElementById("add-player").addEventListener("click", () => {
    const container = document.getElementById("players-container");
    const playerDiv = document.createElement("div");
    playerDiv.classList.add("player");

    playerDiv.innerHTML = `
        <input type="text" placeholder="Player Name" class="player-name" required>
        <input type="number" placeholder="Final Chips" class="player-chips" required>
    `;

    container.appendChild(playerDiv);
});

document.getElementById("player-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const players = Array.from(document.querySelectorAll(".player"))
        .map(player => {
            const name = player.querySelector(".player-name").value;
            const chips = parseFloat(player.querySelector(".player-chips").value);
            return { name, balance: chips - 50 };
        });

    try {
        const response = await fetch("/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ players }),
        });

        const data = await response.json();

        if (data.transactions) {
            const resultsDiv = document.getElementById("results");
            const transactionsList = document.getElementById("transactions");

            transactionsList.innerHTML = ""; // Clear old results
            data.transactions.forEach(transaction => {
                const listItem = document.createElement("li");
                listItem.textContent = `${transaction.from} pays ${transaction.to}: R$${transaction.amount}`;
                transactionsList.appendChild(listItem);
            });

            resultsDiv.style.display = "block";
        } else {
            alert("Error calculating transactions. Please try again.");
        }
    } catch (error) {
        alert("An error occurred. Please check your input and try again.");
        console.error(error);
    }
});
