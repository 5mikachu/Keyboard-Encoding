// Function to gather layout data from input fields
function getLayoutData(layoutId) {
    const rows = [];
    const keyboard = document.getElementById(layoutId);

    keyboard.querySelectorAll('.keyboard-row').forEach(row => {
        const rowData = [];
        row.querySelectorAll('.key-input').forEach(input => {
            rowData.push(input.value || "");  // Default to empty string for empty inputs
        });
        rows.push(rowData);
    });

    return rows;
}

// Function to submit the new layout to the backend
async function submitNewLayout() {
    const layoutKey = document.getElementById("layout_key").value;
    const layoutName = document.getElementById("layout_name").value;
    const layoutLowercase = getLayoutData("keyboard-lowercase");
    const layoutUppercase = getLayoutData("keyboard-uppercase");
    const messageElement = document.getElementById("addLayoutMessage");

    if (!layoutKey || !layoutName) {
        messageElement.textContent = "Layout key and name are required.";
        messageElement.style.color = "red";
        return;
    }

    try {
        const response = await fetch("/add_layout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                layout_key: layoutKey,
                layout_name: layoutName,
                layout_lowercase: layoutLowercase,
                layout_uppercase: layoutUppercase
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
