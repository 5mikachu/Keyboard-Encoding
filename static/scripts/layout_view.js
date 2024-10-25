// Toggle between uppercase and lowercase layouts
let isUppercase = false;

// Render Keyboard Layout
function renderKeyboard(layout) {
    const keyboard = document.getElementById("keyboard");
    keyboard.innerHTML = "";  // Clear current keyboard display

    layout.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("keyboard-row");

        row.forEach(key => {
            if (key) {  // Only render non-empty keys
                const keyDiv = document.createElement("div");
                keyDiv.classList.add("key");
                keyDiv.textContent = key;
                rowDiv.appendChild(keyDiv);
            }
        });

        keyboard.appendChild(rowDiv);
    });
}

// Initial render of lowercase layout
document.addEventListener("DOMContentLoaded", () => {
    renderKeyboard(layoutLowercase);
});

// Function to toggle case and render the appropriate layout
function toggleCase() {
    isUppercase = !isUppercase;
    renderKeyboard(isUppercase ? layoutUppercase : layoutLowercase);
}

// Function to submit the layout form
async function submitLayoutForm() {
    const layoutKey = document.getElementById("layout_key").value;
    const layoutName = document.getElementById("layout_name").value;
    const layoutLowercase = document.getElementById("layout_lowercase").value;
    const layoutUppercase = document.getElementById("layout_uppercase").value;
    const messageElement = document.getElementById("addLayoutMessage");

    try {
        const response = await fetch("/add_layout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                layout_key: layoutKey,
                layout_name: layoutName,
                layout_lowercase: JSON.parse(layoutLowercase),
                layout_uppercase: JSON.parse(layoutUppercase)
            })
        });

        const result = await response.json();
        messageElement.textContent = result.message || result.error;
        messageElement.style.color = result.message ? "green" : "red";
    } catch (error) {
        messageElement.textContent = "Error adding layout.";
        messageElement.style.color = "red";
    }
}
