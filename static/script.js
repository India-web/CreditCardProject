// Format card number with spaces
function formatCardNumber(number) {
    return number.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim();
}

// Update the visual card display
function updateCardVisual(number, issuer) {
    const displayElement = document.getElementById('displayCardNumber');
    const issuerElement = document.getElementById('cardIssuer');
    
    if (number) {
        const cleanNumber = number.replace(/\s/g, '');
        const formatted = formatCardNumber(cleanNumber);
        displayElement.textContent = formatted || '•••• •••• •••• ••••';
    } else {
        displayElement.textContent = '•••• •••• •••• ••••';
    }
    
    if (issuer && issuer !== 'Unknown') {
        issuerElement.textContent = issuer;
    } else {
        issuerElement.textContent = 'Card Issuer';
    }
}

// Validate card function
async function validateCard() {
    const input = document.getElementById("validateInput");
    const number = input.value;
    const validateBtn = document.getElementById("validateBtn");
    const resultDiv = document.getElementById("validateResult");
    
    if (!number.trim()) {
        resultDiv.innerHTML = "❌ Please enter a card number";
        resultDiv.className = "result invalid";
        return;
    }
    
    // Show loading state
    validateBtn.classList.add("loading");
    validateBtn.disabled = true;
    resultDiv.innerHTML = "⏳ Validating...";
    resultDiv.className = "result";
    
    try {
        const response = await fetch("/validate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ number: number })
        });
        
        const data = await response.json();
        
        if (data.valid) {
            resultDiv.innerHTML = `
                ✅ <strong>Valid Card!</strong><br>
                🏦 Issuer: ${data.issuer}<br>
                📊 Category: ${data.category}
            `;
            resultDiv.className = "result valid";
            updateCardVisual(number, data.issuer);
        } else {
            resultDiv.innerHTML = `❌ ${data.message || "Invalid card number"}`;
            resultDiv.className = "result invalid";
            updateCardVisual(number, null);
        }
    } catch (error) {
        resultDiv.innerHTML = "❌ Server error. Please try again.";
        resultDiv.className = "result invalid";
        console.error(error);
    } finally {
        validateBtn.classList.remove("loading");
        validateBtn.disabled = false;
    }
}

// Generate card function
async function generateCard() {
    const cardType = document.getElementById("cardType").value;
    const generateBtn = document.getElementById("generateBtn");
    const resultDiv = document.getElementById("generateResult");
    
    // Show loading state
    generateBtn.classList.add("loading");
    generateBtn.disabled = true;
    resultDiv.innerHTML = "⏳ Generating card...";
    resultDiv.className = "result";
    
    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ cardType: cardType })
        });
        
        const data = await response.json();
        
        if (data.card) {
            resultDiv.innerHTML = `
                🎉 <strong>Card Generated Successfully!</strong><br>
                💳 ${data.formatted}<br>
                <button onclick="copyToClipboard('${data.card}')" style="margin-top: 10px; padding: 6px 12px; font-size: 0.85rem;">📋 Copy Number</button>
            `;
            resultDiv.className = "result success";
            
            // Update visual card
            updateCardVisual(data.formatted, cardType);
            
            // Also fill the validation input for easy testing
            document.getElementById("validateInput").value = data.formatted;
        } else {
            resultDiv.innerHTML = `❌ ${data.error || "Could not generate card"}`;
            resultDiv.className = "result invalid";
        }
    } catch (error) {
        resultDiv.innerHTML = "❌ Generation error. Please try again.";
        resultDiv.className = "result invalid";
        console.error(error);
    } finally {
        generateBtn.classList.remove("loading");
        generateBtn.disabled = false;
    }
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        const tempMsg = document.createElement('div');
        tempMsg.textContent = '✅ Copied!';
        tempMsg.style.position = 'fixed';
        tempMsg.style.bottom = '20px';
        tempMsg.style.right = '20px';
        tempMsg.style.background = '#28a745';
        tempMsg.style.color = 'white';
        tempMsg.style.padding = '10px 20px';
        tempMsg.style.borderRadius = '10px';
        tempMsg.style.zIndex = '9999';
        document.body.appendChild(tempMsg);
        setTimeout(() => tempMsg.remove(), 2000);
    });
}

// Auto-format as user types
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById("validateInput");
    if (input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            if (value.length > 0) {
                value = value.replace(/\D/g, '');
                value = value.substring(0, 19);
                const formatted = formatCardNumber(value);
                e.target.value = formatted;
            }
        });
    }
});
