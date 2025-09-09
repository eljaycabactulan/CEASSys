// supabase-config.js
const SUPABASE_URL = 'https://hssxqchzifnlatjvlpfi.supabase.co'
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhzc3hxY2h6aWZubGF0anZscGZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxMzc4MjgsImV4cCI6MjA2MjcxMzgyOH0.GJSU_QwoEmIkMuD5cEM0IhJbAQIVqAeMFGGqGiWpdsI'

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

function toggleMobileMenu() {
    const menu = document.querySelector('.mobile-menu');
    menu.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    const menu = document.querySelector('.mobile-menu');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    if (!menu.contains(e.target) && !menuBtn.contains(e.target)) {
        menu.classList.remove('active');
    }
});

// Add loading indicators for mobile
function showLoading() {
    const loader = document.createElement('div');
    loader.className = 'mobile-loader';
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.mobile-loader');
    if (loader) {
        loader.remove();
    }
}

// Add touch feedback
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');
    const links = document.querySelectorAll('a');
    
    buttons.forEach(button => {
        button.addEventListener('touchstart', () => {
            button.style.opacity = '0.7';
        });
        button.addEventListener('touchend', () => {
            button.style.opacity = '1';
        });
    });
    
    links.forEach(link => {
        link.addEventListener('touchstart', () => {
            link.style.opacity = '0.7';
        });
        link.addEventListener('touchend', () => {
            link.style.opacity = '1';
        });
    });
});
