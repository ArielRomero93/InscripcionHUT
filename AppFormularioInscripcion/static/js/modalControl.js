function openModal(url) {
    document.getElementById('modalContainer').style.display = 'flex';
    document.getElementById('modalIframe').src = url;
}

function closeModal() {
    document.getElementById('modalContainer').style.display = 'none';
    document.getElementById('modalIframe').src = '';
}
