// Function to get selected layout and check it's set
function getSelectedLayout() {
    const layoutSelector = document.getElementById("layoutSelector");
    if (layoutSelector.value) return layoutSelector.value;
    alert("Please select a layout before encoding or decoding.");
    return null;
}

// Function to handle form submission with layout
async function submitForm(event, formId, resultId, route) {
    event.preventDefault();

    const layout = getSelectedLayout();
    if (!layout) return;

    const form = document.getElementById(formId);
    const formData = new FormData(form);
    formData.append("layout_name", layout);  // Attach layout

    const resultElement = document.getElementById(resultId);

    try {
        const response = await fetch(route, {
            method: "POST",
            body: new URLSearchParams(formData),
        });

        const result = await response.json();
        if (response.ok) {
            resultElement.innerHTML = `<p>${result.encoded_text || result.decoded_text || result.message}</p>`;
            resultElement.style.color = "green";
        } else {
            resultElement.innerHTML = `<p>Error: ${result.error}</p>`;
            resultElement.style.color = "red";
        }
    } catch (error) {
        resultElement.innerHTML = `<p>Error: ${error.message}</p>`;
        resultElement.style.color = "red";
    }
}

// Event listeners for encode and decode forms
document.getElementById("encodeForm").addEventListener("submit", (event) => {
    submitForm(event, "encodeForm", "encodeResult", "/encode");
});

document.getElementById("decodeForm").addEventListener("submit", (event) => {
    submitForm(event, "decodeForm", "decodeResult", "/decode");
});
