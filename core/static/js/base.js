document.addEventListener('DOMContentLoaded', () => {
    const posBtn = document.querySelector('.pos-banner-btn_2');
    if (posBtn) {
        posBtn.addEventListener('click', () => {
            window.open('https://pos.gosuslugi.ru/form/?op=XXXXXX&fs=false', '_blank', 'noopener');
        });
    }
});