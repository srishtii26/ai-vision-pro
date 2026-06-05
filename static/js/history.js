function savePrediction(prediction) {

    let history =
        JSON.parse(localStorage.getItem("predictionHistory")) || [];

    history.unshift(prediction);

    history = history.slice(0, 5);

    localStorage.setItem(
        "predictionHistory",
        JSON.stringify(history)
    );
}

function loadHistory() {

    const history =
        JSON.parse(localStorage.getItem("predictionHistory")) || [];

    const container =
        document.getElementById("history-list");

    if (!container) return;

    container.innerHTML = "";

    history.forEach(item => {

        const div = document.createElement("div");

        div.className = "history-item";

        div.textContent = item;

        container.appendChild(div);

    });

}

window.addEventListener("load", loadHistory);