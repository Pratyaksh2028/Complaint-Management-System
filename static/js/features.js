/**
 * CMS PRO - Advanced Feature Set
 * Handles real-time UX validation and interactive components.
 */

// 1. Live Table Search (Crucial for Admin/User dashboards)
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('keyup', function() {
        const filter = input.value.toLowerCase();
        const table = document.getElementById(tableId);
        const tr = table.getElementsByTagName('tr');

        for (let i = 1; i < tr.length; i++) {
            let rowText = tr[i].textContent.toLowerCase();
            tr[i].style.display = rowText.includes(filter) ? "" : "none";
        }
    });
}

// 2. Password Strength Real-time Feedback
function checkPasswordStrength() {
    const passInput = document.querySelector('input[name="password"]');
    if (!passInput || !window.location.pathname.includes('register')) return;

    // Create a small meter UI element
    const meter = document.createElement('div');
    meter.style.cssText = "height: 4px; width: 100%; background: #eee; margin-top: 5px; border-radius: 2px; overflow: hidden;";
    const fill = document.createElement('div');
    fill.style.cssText = "height: 100%; width: 0%; transition: width 0.3s, background 0.3s;";
    meter.appendChild(fill);
    passInput.parentNode.appendChild(meter);

    passInput.addEventListener('input', () => {
        const val = passInput.value;
        let strength = 0;
        if (val.length > 5) strength += 33;
        if (val.match(/[A-Z]/)) strength += 33;
        if (val.match(/[0-9]/)) strength += 34;

        fill.style.width = strength + "%";
        if (strength < 40) fill.style.background = "#ef4444";
        else if (strength < 70) fill.style.background = "#f59e0b";
        else fill.style.background = "#10b981";
    });
}

// 3. Confirm Dangerous Actions (Logout/Delete)
function setupConfirmations() {
    const logoutBtn = document.querySelector('a[href="/logout"]');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            if (!confirm("Are you sure you want to log out of CMS PRO?")) {
                e.preventDefault();
            }
        });
    }
}

// 4. Smooth Scroll for Dashboards
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    filterTable('tableSearch', 'complaintTable'); // Ensure your <table> has id="complaintTable"
    checkPasswordStrength();
    setupConfirmations();
    initSmoothScroll();
    
    console.log("🚀 Features.js Loaded: Password Meter, Table Search, and Security Hooks Active.");
});