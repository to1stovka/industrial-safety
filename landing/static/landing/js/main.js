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
    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMenu);
    });

    // свайп вправо для закрытия меню
    mobileMenu.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    });

    mobileMenu.addEventListener('touchmove', (e) => {
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
        0: { slidesPerView: 1.1, spaceBetween: 16 },
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
const callbackForm = document.getElementById("callbackForm");
const formStep = document.getElementById("callbackFormStep");
const successStep = document.getElementById("callbackSuccessStep");

if (callbackForm) {
  callbackForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("callback_name").value.trim();
    const phone = document.getElementById("callback_phone").value.trim();
    const csrf = callbackForm.querySelector("[name='csrfmiddlewaretoken']").value;
    const postUrl = callbackForm.getAttribute("action");

    if (!name || !phone) {
      alert("Заполните оба поля.");
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("phone", phone);
    formData.append("csrfmiddlewaretoken", csrf);

    try {
      const response = await fetch(postUrl, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      const data = await response.json();

      if (response.ok && data.success) {
        formStep.style.display = "none";
        successStep.style.display = "block";
      } else {
        alert(data.error || "Ошибка при отправке. Попробуйте снова.");
      }
    } catch (error) {
      console.error("Ошибка запроса:", error);
      alert("Ошибка соединения с сервером.");
    }
  });
}

});
