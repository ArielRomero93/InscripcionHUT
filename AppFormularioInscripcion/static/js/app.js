document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const btn = document.getElementById('btn');

    // Mantenemos el sidebar abierto por defecto
    sidebar.classList.add('open');

    btn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
});
