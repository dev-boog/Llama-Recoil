// Log to console
function logToConsole(message) {
    const consoleEl = document.getElementById("console-output");

    consoleEl.value += "[Llama-Recoil] " + message + "\n";
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

// Run Command
function runCommand(cmd = null) {
    let command = cmd;

    if (!command) {
        const input = document.querySelector(".console-cmd-input");
        command = input.value.trim();
        input.value = "";
    }

    if (command === "") return;
    logToConsole("> " + command);
}

// Clear Console
function clearConsole() {
    const consoleEl = document.getElementById("console-output");
    consoleEl.value = "";
}

// Copy Console
function copyConsole() {
    const consoleEl = document.getElementById("console-output");
    navigator.clipboard.writeText(consoleEl.value)
}

