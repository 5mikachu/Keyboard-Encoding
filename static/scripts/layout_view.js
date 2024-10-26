let isUppercase = false;

// Function to render the keyboard layout
function renderKeyboard(layout) {
    const keyboard = document.getElementById("keyboard");
    keyboard.innerHTML = "";

    layout.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("keyboard-row");

        row.forEach(key => {
            if (key) {
                const keyDiv = document.createElement("div");
                keyDiv.classList.add("key");
                keyDiv.textContent = key;
                rowDiv.appendChild(keyDiv);
            }
        });

        keyboard.appendChild(rowDiv);
    });

    // Add extra keys for SHIFT, SPACE, and ENTER
    const extraKeysRow = document.createElement("div");
    extraKeysRow.classList.add("keyboard-row");

    const shiftDiv = document.createElement("div");
    shiftDiv.classList.add("key", "shift");
    shiftDiv.textContent = "SHIFT";
    shiftDiv.addEventListener("click", toggleCase);
    extraKeysRow.appendChild(shiftDiv);

    const spaceDiv = document.createElement("div");
    spaceDiv.classList.add("key", "space");
    spaceDiv.textContent = "SPACE";
    extraKeysRow.appendChild(spaceDiv);

    const enterDiv = document.createElement("div");
    enterDiv.classList.add("key", "enter");
    enterDiv.textContent = "ENTER";
    extraKeysRow.appendChild(enterDiv);

    keyboard.appendChild(extraKeysRow);
}

// Function to toggle case and render the appropriate layout
function toggleCase() {
    isUppercase = !isUppercase;
    renderKeyboard(isUppercase ? layoutUppercase : layoutLowercase);
}

// Initial render of lowercase layout
document.addEventListener("DOMContentLoaded", () => {
    renderKeyboard(layoutLowercase);
});
