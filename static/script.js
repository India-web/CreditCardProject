function validateCard() {
    const number = document.getElementById("validateInput").value;

    fetch("/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ number })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("validateResult").innerText =
            JSON.stringify(data, null, 2);
    });
}

function generateCard() {
    const cardType = document.getElementById("cardType").value;

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cardType })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("generateResult").innerText =
            data.card || "Error";
    });
}
