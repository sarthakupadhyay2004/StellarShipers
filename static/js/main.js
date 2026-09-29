// STELLAR SHIPERS Client Script
document.addEventListener('DOMContentLoaded', () => {
    // 0. Theme Toggle Handler
    initThemeToggle();

    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenuDrawer = document.getElementById('mobile-menu-drawer');
    if (mobileMenuBtn && mobileMenuDrawer) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenuDrawer.classList.contains('hidden');
            if (isHidden) {
                mobileMenuDrawer.classList.remove('hidden');
            } else {
                mobileMenuDrawer.classList.add('hidden');
            }
        });
    }

    // 2. FAQ Accordion Toggle
    const faqButtons = document.querySelectorAll('.faq-toggle-btn');
    faqButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const content = btn.nextElementSibling;
            const icon = btn.querySelector('.faq-icon');
            if (content) {
                const isHidden = content.classList.contains('hidden');
                content.classList.toggle('hidden');
                if (icon) {
                    icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                }
            }
        });
    });

    // 3. Technical Spec Tab Switcher (Verified vs Provisional)
    const specTabs = document.querySelectorAll('.spec-tab-btn');
    specTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-target');
            
            // Deactivate all buttons
            specTabs.forEach(t => {
                t.classList.remove('border-slate-200', 'text-white', 'bg-slate-800');
                t.classList.add('border-transparent', 'text-slate-400');
            });
            
            // Activate clicked button
            tab.classList.remove('border-transparent', 'text-slate-400');
            tab.classList.add('border-slate-200', 'text-white', 'bg-slate-800');

            // Hide all spec panels
            document.querySelectorAll('.spec-tab-panel').forEach(panel => {
                panel.classList.add('hidden');
            });

            // Show target panel
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.remove('hidden');
            }
        });
    });

    // 4. Auto-dismiss flash messages after 6 seconds
    const flashMessages = document.querySelectorAll('.flash-alert');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        }, 6000);
    });
});

/**
 * Initializes and manages theme switching between Light (default) and Dark.
 */
function initThemeToggle() {
    const savedTheme = localStorage.getItem('stellar_theme') || 'light';
    applyTheme(savedTheme);

    const toggleButtons = document.querySelectorAll('.theme-toggle-btn');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const isDark = document.documentElement.classList.contains('dark');
            const nextTheme = isDark ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    });
}

function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('stellar_theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('stellar_theme', 'light');
    }
    updateToggleButtons(theme);
}

function updateToggleButtons(theme) {
    const isDark = theme === 'dark';
    const buttons = document.querySelectorAll('.theme-toggle-btn');
    buttons.forEach(btn => {
        const lightPill = btn.querySelector('.theme-opt-light');
        const darkPill = btn.querySelector('.theme-opt-dark');
        if (lightPill && darkPill) {
            if (isDark) {
                lightPill.classList.remove('bg-blue-600', 'text-white', 'shadow-sm');
                lightPill.classList.add('text-slate-400');
                darkPill.classList.remove('text-slate-400');
                darkPill.classList.add('bg-slate-700', 'text-white', 'shadow-sm');
            } else {
                lightPill.classList.remove('text-slate-400');
                lightPill.classList.add('bg-blue-600', 'text-white', 'shadow-sm');
                darkPill.classList.remove('bg-slate-700', 'text-white', 'shadow-sm');
                darkPill.classList.add('text-slate-400');
            }
        }
        btn.setAttribute('title', isDark ? 'Switch to Light Theme' : 'Switch to Dark Theme');
        btn.setAttribute('aria-label', isDark ? 'Switch to Light Theme' : 'Switch to Dark Theme');
    });
}
