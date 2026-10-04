document.addEventListener('DOMContentLoaded', () => {
    const posBtn = document.querySelector('.pos-banner-btn_2');
    if (posBtn) {
        posBtn.addEventListener('click', () => {
            window.open('https://pos.gosuslugi.ru/form/?op=XXXXXX&fs=false', '_blank', 'noopener');
        });
    }
});

(function () {
  function initPager(root) {
    var perPage = parseInt(root.dataset.perPage, 10) || 10;
    var tags = Array.prototype.slice.call(root.querySelectorAll('[data-tag-list] .tag'));
    var pages = Math.ceil(tags.length / perPage);
    if (pages <= 1) return;

    var controls = root.querySelector('[data-tag-controls]');
    var prev = root.querySelector('[data-tag-prev]');
    var next = root.querySelector('[data-tag-next]');
    var info = root.querySelector('[data-tag-info]');

    // Открываем ту страницу, где находится выбранный тег
    var current = 0;
    for (var i = 0; i < tags.length; i++) {
      if (tags[i].classList.contains('active')) { current = Math.floor(i / perPage); break; }
    }

    function render() {
      var from = current * perPage;
      var to = Math.min(from + perPage, tags.length);
      tags.forEach(function (tag, idx) { tag.hidden = idx < from || idx >= to; });
      info.textContent = 'Теги ' + (from + 1) + '–' + to + ' из ' + tags.length;
      prev.disabled = current === 0;
      next.disabled = current === pages - 1;
    }

    prev.addEventListener('click', function () { if (current > 0) { current--; render(); } });
    next.addEventListener('click', function () { if (current < pages - 1) { current++; render(); } });

    controls.classList.replace('d-none', 'd-flex');
    render();
  }

  document.querySelectorAll('[data-tag-pager]').forEach(initPager);
})();