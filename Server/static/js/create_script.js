let currentEditingScript = null;

// Disable test mode when leaving the page
window.addEventListener('beforeunload', function() {
    disableTestMode();
});

// Also disable when clicking navigation links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a.nav-button, a.nav-button-active').forEach(link => {
        link.addEventListener('click', function() {
            disableTestMode();
        });
    });
});

function disableTestMode() {
    // Send sync request to disable test mode
    navigator.sendBeacon('/create_script/disable_test_mode', '');
}

function createScript() {
    const scriptName = document.getElementById('script-name-input').value;
    
    if (!scriptName) {
        console.error('Script name is required');
        return;
    }

    fetch('/create_script/create_new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            scriptName: scriptName
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Script created:', data);
        if (data.success) {
            window.location.href = window.location.href;
        }
    })
    .catch(error => {
        console.error('Error creating script:', error);
    });
}

function loadScript(scriptName) {
    fetch(`/create_script/get_script/${scriptName}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentEditingScript = scriptName;
                document.getElementById('edit-script-name').textContent = scriptName;
                document.getElementById('edit-script-delay').value = data.script.delay;
                
                // Clear and populate steps
                const stepsContainer = document.getElementById('steps-container');
                stepsContainer.innerHTML = '';
                
                data.script.values.forEach((step, index) => {
                    addStepWithValues(step.x, step.y, index);
                });
                
                // Load test state
                loadTestState();
                
                // Show edit section
                document.getElementById('edit-section').style.display = 'block';
                document.getElementById('edit-section').scrollIntoView({ behavior: 'smooth' });
            }
        })
        .catch(error => {
            console.error('Error loading script:', error);
        });
}

function loadTestState() {
    fetch('/create_script/get_test_state')
        .then(response => response.json())
        .then(data => {
            document.getElementById('test-enable-toggle').checked = data.test_enabled;
            document.getElementById('test-hipfire-toggle').checked = data.test_hipfire;
        })
        .catch(error => {
            console.error('Error loading test state:', error);
        });
}

function addStep() {
    addStepWithValues(0, 10);
}

function addStepWithValues(x = 0, y = 10, index = null) {
    const stepsContainer = document.getElementById('steps-container');
    const stepCount = stepsContainer.children.length;
    const stepIndex = index !== null ? index : stepCount;
    
    const stepDiv = document.createElement('div');
    stepDiv.className = 'input-group mb-2';
    stepDiv.innerHTML = `
        <span class="input-group-text">Step ${stepIndex + 1}</span>
        <span class="input-group-text">X:</span>
        <input type="number" class="form-control step-x" value="${x}" placeholder="0" onchange="updateTestPattern()" oninput="updateTestPattern()">
        <span class="input-group-text">Y:</span>
        <input type="number" class="form-control step-y" value="${y}" placeholder="10" onchange="updateTestPattern()" oninput="updateTestPattern()">
        <button class="btn" style="background-color: #dc3545; border-color: #dc3545; color: white;" onclick="removeStep(this)">Remove</button>
    `;
    
    stepsContainer.appendChild(stepDiv);
}

function removeStep(button) {
    button.parentElement.remove();
    updateStepLabels();
}

function updateStepLabels() {
    const stepsContainer = document.getElementById('steps-container');
    Array.from(stepsContainer.children).forEach((step, index) => {
        step.querySelector('.input-group-text').textContent = `Step ${index + 1}`;
    });
}

function saveScript() {
    if (!currentEditingScript) {
        console.error('No script is currently being edited');
        return;
    }
    
    const delay = parseInt(document.getElementById('edit-script-delay').value) || 100;
    const stepsContainer = document.getElementById('steps-container');
    const steps = [];
    
    Array.from(stepsContainer.children).forEach(stepDiv => {
        const x = parseInt(stepDiv.querySelector('.step-x').value) || 0;
        const y = parseInt(stepDiv.querySelector('.step-y').value) || 0;
        steps.push({ x, y });
    });
    
    fetch('/create_script/update_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            scriptName: currentEditingScript,
            delay: delay,
            steps: steps
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Script saved successfully!', 'success');
        } else {
            showNotification('Failed to save script', 'error');
        }
    })
    .catch(error => {
        console.error('Error updating script:', error);
        showNotification('Error saving script', 'error');
    });
}

function showNotification(message, type = 'success') {
    // Remove any existing notification
    const existing = document.getElementById('save-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.id = 'save-notification';
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px;';
    notification.innerHTML = `<i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${message}`;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function cancelEdit() {
    // Disable test mode when canceling
    document.getElementById('test-enable-toggle').checked = false;
    document.getElementById('test-hipfire-toggle').checked = false;
    toggleTestEnable(); // This will disable the test mode
    
    document.getElementById('edit-section').style.display = 'none';
    currentEditingScript = null;
}

function toggleTestEnable() {
    const enabled = document.getElementById('test-enable-toggle').checked;
    updateTestPattern();
}

function updateTestPattern() {
    const enabled = document.getElementById('test-enable-toggle').checked;
    const delay = parseInt(document.getElementById('edit-script-delay').value) || 100;
    const stepsContainer = document.getElementById('steps-container');
    const steps = [];
    
    Array.from(stepsContainer.children).forEach(stepDiv => {
        const x = parseInt(stepDiv.querySelector('.step-x').value) || 0;
        const y = parseInt(stepDiv.querySelector('.step-y').value) || 0;
        steps.push({ x, y });
    });
    
    fetch('/create_script/set_test_mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            enabled: enabled,
            delay: delay,
            steps: steps
        })
    })
    .catch(error => {
        console.error('Error toggling test mode:', error);
    });
}

function toggleTestHipfire() {
    const hipfire = document.getElementById('test-hipfire-toggle').checked;
    
    fetch('/create_script/set_test_hipfire', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            hipfire: hipfire
        })
    })
    .catch(error => {
        console.error('Error toggling hipfire:', error);
    });
}

function deleteScript() {
    if (!currentEditingScript) {
        console.error('No script is currently being edited');
        return;
    }
    
    if (!confirm(`Are you sure you want to delete "${currentEditingScript}"? This cannot be undone.`)) {
        return;
    }
    
    fetch('/create_script/delete_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            scriptName: currentEditingScript
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = window.location.href;
        }
    })
    .catch(error => {
        console.error('Error deleting script:', error);
    });
}
