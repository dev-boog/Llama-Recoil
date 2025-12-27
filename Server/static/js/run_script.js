// Live check on recoil mode
const select = document.getElementById("recoil-mode-select");

// Function to update container visibility based on selected mode
function updateContainerVisibility() {
    const mode = getSelectedMode();
    const isSimple = mode.value === "simple-mode";
    
    document.getElementById("advanced-container").style.display = isSimple ? "none" : "block";
    document.getElementById("simple-container").style.display = isSimple ? "block" : "none";
}

// Load saved state from backend
function loadState() {
    fetch('/run_script/get_state')
        .then(response => response.json())
        .then(data => {
            // Set checkbox states
            document.getElementById('check1').checked = data.recoil_enabled;
            document.getElementById('simple-hipfire-checkbox').checked = data.simple_hipfire;
            document.getElementById('loop-when-complete-checkbox').checked = data.advanced_loop_on_complete;
            document.getElementById('hipfire-checkbox').checked = data.advanced_hipfire;
            
            // Set select values
            document.getElementById('recoil-mode-select').value = data.recoil_mode;
            
            const advancedScriptSelect = document.getElementById('advanced-script-select');
            if (advancedScriptSelect && data.advanced_selected_script) {
                advancedScriptSelect.value = data.advanced_selected_script;
            }
            
            // Set input values
            document.getElementById('simple-mode-x-input').value = data.simple_x || '';
            document.getElementById('simple-mode-y-input').value = data.simple_y || '';
            document.getElementById('simple-mode-delay-input').value = data.simple_delay || '';
            
            // Update visibility after loading
            updateContainerVisibility();
            
            // Update loaded script info if in advanced mode
            if (data.recoil_mode === 'advanced-mode' && data.advanced_selected_script) {
                const selectedScript = savedScriptsData.find(script => script.name === data.advanced_selected_script);
                if (selectedScript) {
                    document.getElementById('loaded-script-name').textContent = selectedScript.name;
                    document.getElementById('loaded-script-steps').textContent = selectedScript.step_count;
                    document.getElementById('loaded-script-delay').textContent = selectedScript.delay;
                }
            }
        })
        .catch(error => {
            console.error('Error loading state:', error);
        });
}

document.addEventListener("DOMContentLoaded", function() {
    loadState();
    select.addEventListener("change", updateContainerVisibility);
});

// Function to get selected mode details
function getSelectedMode() {
    return {
        value: select.value,               
        text: select.options[select.selectedIndex].text 
    };
}

// Apply settings function
function applySettings() {
    const recoilEnabled = document.getElementById('check1').checked;
    const recoilMode = document.getElementById('recoil-mode-select').value;
    const simpleX = document.getElementById('simple-mode-x-input').value;
    const simpleY = document.getElementById('simple-mode-y-input').value;
    const simpleDelay = document.getElementById('simple-mode-delay-input').value;
    const simpleHipfire = document.getElementById('simple-hipfire-checkbox').checked;

    const advancedScriptSelect = document.getElementById('advanced-script-select');
    const advancedSelectedScript = advancedScriptSelect ? advancedScriptSelect.value : '';
    const advancedLoopOnComplete = document.getElementById('loop-when-complete-checkbox').checked;
    const advancedHipfire = document.getElementById('hipfire-checkbox').checked;
    
    // Update loaded script widgets if in advanced mode
    if (recoilMode === 'advanced-mode' && advancedSelectedScript) {
        const selectedScript = savedScriptsData.find(script => script.name === advancedSelectedScript);
        if (selectedScript) {
            document.getElementById('loaded-script-name').textContent = selectedScript.name;
            document.getElementById('loaded-script-steps').textContent = selectedScript.step_count;
            document.getElementById('loaded-script-delay').textContent = selectedScript.delay;
        }
    }

    fetch('/run_script/apply_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            recoil_enabled: recoilEnabled,
            recoil_mode: recoilMode,
            simple_x: simpleX,
            simple_y: simpleY,
            simple_delay: simpleDelay,
            simple_hipfire: simpleHipfire,
            advanced_loop_on_complete: advancedLoopOnComplete,
            advanced_hipfire: advancedHipfire,


            advanced_selected_script: advancedSelectedScript
        })
    }).catch(() => {
        
    });
}
