function validateCard() {

    const number =
        document.getElementById("validateInput").value;

    fetch("/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            number: number
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.valid) {

            document.getElementById("validateResult").innerHTML =
                "✅ Valid Card<br>" +
                "Issuer: " + data.issuer + "<br>" +
                "Category: " + data.category;

        } else {

            document.getElementById("validateResult").innerHTML =
                "❌ " + data.message;
        }

    })
    .catch(error => {
        document.getElementById("validateResult").innerHTML =
            "Server Error";
        console.error(error);
    });
}


function generateCard() {

    const cardType =
        document.getElementById("cardType").value;

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cardType: cardType
        })
    })
    .then(response => response.json())
    .then(data => {

        document.getElementById("generateResult").innerHTML =
            "Generated Card:<br>" + data.card;

    })
    .catch(error => {

        document.getElementById("generateResult").innerHTML =
            "Generation Error";

        console.error(error);
    });
}
