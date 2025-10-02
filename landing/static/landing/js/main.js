document.addEventListener('DOMContentLoaded', function () {
  const burger = document.getElementById('floatingBurger');
  const mobileMenu = document.getElementById('mobileMenu');
  const overlay = document.getElementById('mobileMenuOverlay');

  let touchStartX = 0;
  let touchEndX = 0;

  function openMenu() {
    mobileMenu.classList.add('active');
    overlay.classList.add('active');
  }

  function closeMenu() {
    mobileMenu.classList.remove('active');
    overlay.classList.remove('active');
  }

  burger.addEventListener('click', () => {
    if (mobileMenu.classList.contains('active')) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  overlay.addEventListener('click', closeMenu);

  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  // Свайп вправо для закрытия меню
  mobileMenu.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  });

  mobileMenu.addEventListener('touchmove', (e) => {
    touchEndX = e.changedTouches[0].screenX;
  });

  mobileMenu.addEventListener('touchend', () => {
    // если конец свайпа больше начала + порог
    if (touchEndX - touchStartX > 50) { // порог 50px
      closeMenu();
    }
    // Сбрасываем значения
    touchStartX = 0;
    touchEndX = 0;
  });
});
