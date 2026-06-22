// resizer.js - Handles responsive preview toggling for the generated website

document.addEventListener('DOMContentLoaded', () => {
    // Assuming you add an iframe with id 'preview-frame' and buttons to your frontend later
    const previewFrame = document.getElementById('preview-frame');
    const btnDesktop = document.getElementById('view-desktop');
    const btnTablet = document.getElementById('view-tablet');
    const btnMobile = document.getElementById('view-mobile');

    if (!previewFrame) return; // Exit if preview frame isn't built into the UI yet

    function setPreviewSize(width) {
        previewFrame.style.width = width;
        previewFrame.style.margin = '0 auto';
        previewFrame.style.display = 'block';
        previewFrame.style.transition = 'width 0.3s ease-in-out';
    }

    if (btnDesktop) {
        btnDesktop.addEventListener('click', () => setPreviewSize('100%'));
    }
    
    if (btnTablet) {
        btnTablet.addEventListener('click', () => setPreviewSize('768px'));
    }
    
    if (btnMobile) {
        btnMobile.addEventListener('click', () => setPreviewSize('375px'));
    }
});