document.addEventListener('DOMContentLoaded', function () {
  // Мобильное меню
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

  if (burger) {
    burger.addEventListener('click', () => {
      if (mobileMenu.classList.contains('active')) {
        closeMenu();
      } else {
        openMenu();
      }
    });
  }

  if (overlay) overlay.addEventListener('click', closeMenu);

  if (mobileMenu) {
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', event => {
        if (link.classList.contains('dropdown-toggle') || link.closest('.dropdown-menu')) {
          event.stopPropagation();
          return;
        }
        closeMenu();
      });
    });

    // свайп вправо для закрытия меню
    mobileMenu.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    });

    mobileMenu.addEventListener('touchmove', e => {
      touchEndX = e.changedTouches[0].screenX;
    });

    mobileMenu.addEventListener('touchend', () => {
      if (touchEndX - touchStartX > 50) closeMenu(); // порог 50px
      touchStartX = 0;
      touchEndX = 0;
    });
  }

  // Swiper (Отзывы)
  if (document.querySelector('.reviews-swiper')) {
    new Swiper('.reviews-swiper', {
      slidesPerView: 3,
      spaceBetween: 30,
      loop: true,
      centeredSlides: false,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      autoplay: {
        delay: 8000,
        disableOnInteraction: false,
      },
      speed: 600,
      breakpoints: {
        0: { slidesPerView: 1, spaceBetween: 16 },
        768: { slidesPerView: 2, spaceBetween: 20 },
        1024: { slidesPerView: 3, spaceBetween: 20 },
      },
    });
  }

  // Swiper (Наши клиенты)
  if (document.querySelector('.clients-swiper')) {
    new Swiper('.clients-swiper', {
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      navigation: {
        nextEl: '.clients-button-next',
        prevEl: '.client-button-prev',
      },
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      speed: 700,
    });
  }

  // Модалка обратного звонка
  const callbackForm = document.getElementById('callbackForm');
  const formStep = document.getElementById('callbackFormStep');
  const successStep = document.getElementById('callbackSuccessStep');

  if (callbackForm) {
    callbackForm.addEventListener('submit', async e => {
      e.preventDefault();

      const name = document.getElementById('callback_name').value.trim();
      const phone = document.getElementById('callback_phone').value.trim();
      const csrf = callbackForm.querySelector("[name='csrfmiddlewaretoken']").value;
      const postUrl = callbackForm.getAttribute('action');

      if (!name || !phone) {
        alert('Заполните оба поля.');
        return;
      }

      const formData = new FormData();
      formData.append('name', name);
      formData.append('phone', phone);
      formData.append('csrfmiddlewaretoken', csrf);

      try {
        const response = await fetch(postUrl, {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });

        const data = await response.json();

        if (response.ok && data.success) {
          formStep.style.display = 'none';
          successStep.style.display = 'block';
        } else {
          alert(data.error || 'Ошибка при отправке. Попробуйте снова.');
        }
      } catch (error) {
        console.error('Ошибка запроса:', error);
        alert('Ошибка соединения с сервером.');
      }
    });
  }

  // Форма"Оставить заявку"
  const nokForm = document.querySelector('.nok-form');
  const successBlock = document.querySelector('.form-success');

  if (nokForm) {
    // Обрезка имени файла
    const fileInput = nokForm.querySelector("input[type='file']");
    const fileNameSpan = nokForm.querySelector('.file-name');

    if (fileInput && fileNameSpan) {
      fileInput.addEventListener('change', function () {
        const file = this.files && this.files[0];
        if (file) {
          let name = file.name;
          if (name.length > 25) name = name.substring(0, 25) + '...';
          fileNameSpan.textContent = name;
          fileNameSpan.classList.add('active');
        } else {
          fileNameSpan.textContent = 'Прикрепите заявление';
          fileNameSpan.classList.remove('active');
        }
      });
    }

    // Отправка формы AJAX
    nokForm.addEventListener('submit', async function (e) {
      e.preventDefault();

      nokForm.querySelectorAll('.form-item').forEach(i => i.classList.remove('has-error'));

      let valid = true;
      const name = nokForm.querySelector('#id_name');
      const email = nokForm.querySelector('#id_email');
      const message = nokForm.querySelector('#id_message');
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (name && name.value.trim().length < 2) {
        name.closest('.form-item').classList.add('has-error');
        valid = false;
      }
      if (email && !emailRegex.test(email.value.trim())) {
        email.closest('.form-item').classList.add('has-error');
        valid = false;
      }
      if (message && message.value.trim().length < 5) {
        message.closest('.form-item').classList.add('has-error');
        valid = false;
      }
      if (!valid) return;

      const formData = new FormData(nokForm);
      const postUrl = nokForm.getAttribute('action') || '/nok/';

      try {
        const response = await fetch(postUrl, {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });

        if (response.ok) {
          const wrapper = nokForm.closest('.form-wrapper');
          if (wrapper) {
            wrapper.classList.add('is-success');
          }
        } else {
          console.error('Ошибка при отправке формы');
        }
      } catch (error) {
        console.error('Ошибка сети:', error);
      }
    });

    // Убираем ошибку при вводе
    nokForm.querySelectorAll('input, textarea').forEach(input => {
      input.addEventListener('input', () => {
        const wrapper = input.closest('.form-item');
        if (wrapper) wrapper.classList.remove('has-error');
      });
    });
  }

  // Аккордеоны с серым фоном (карточки)
  const toggles = document.querySelectorAll('.accordion-toggle');
  toggles.forEach(toggle => {
    const content = toggle.nextElementSibling;

    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
      content.classList.toggle('open');
    });
  });
});
