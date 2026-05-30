/**
 * CMS PRO - Ultimate Frontend Interactions
 * This script handles UI enhancements for a premium user experience.
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Auto-hide Flash Messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(20px)';
            alert.style.transition = 'all 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // 2. Table Search Functionality (The "Ultimate" Professional Touch)
    // Add an input with id="tableSearch" to any page to use this
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const rows = document.querySelectorAll('.table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    // 3. Dynamic Sidebar Active State
    // Ensures the active link stays highlighted even if navigated manually
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // 4. Form Submission Loading State
    // Prevents double-clicking and looks professional
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const btn = form.querySelector('.btn-primary');
            if (btn) {
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                btn.style.opacity = '0.7';
                btn.style.pointerEvents = 'none';
            }
        });
    });

    // 5. Tooltip simulation or simple greeting console
    console.log("%c CMS PRO System Initialized Successfully ", 
                "background: #4f46e5; color: white; padding: 5px; border-radius: 3px;");
});