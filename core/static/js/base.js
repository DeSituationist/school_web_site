gsap.registerPlugin(ScrollTrigger);

const dropDownItems = document.querySelectorAll(".nav-item.has-dropdown");

dropDownItems.forEach((item) => {
	const button = item.querySelector('.nav-link');

	button.addEventListener('click', (e) => {
		e.stopPropagation();
		e.preventDefault();

		dropDownItems.forEach((other) => {
			if (other !== item) other.classList.remove('open');
		});

		item.classList.toggle('open');
	});
});

document.addEventListener('click', () => {
	dropDownItems.forEach((item) => item.classList.remove('open'));
});

const posBtn = document.querySelector('.pos-banner-btn_2');
if (posBtn) {
	posBtn.addEventListener('click', () => {
		window.open('https://pos.gosuslugi.ru/form/?op=XXXXXX&fs=false', '_blank', 'noopener');
	});
}
