// static/close-menu.js
document.addEventListener('DOMContentLoaded', function() {
    const menuCheckbox = document.getElementById('menu');
    const menuBackdrop = document.querySelector('.menu-backdrop');

    if (menuBackdrop && menuCheckbox) {
        menuBackdrop.addEventListener('click', function() {
            menuCheckbox.checked = false;
        });
    }

    const menuLinks = document.querySelectorAll('.nav a');
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            const menuCheckbox = document.getElementById('menu');
            if (menuCheckbox) {
                menuCheckbox.checked = false;
            }
        });
    });
});