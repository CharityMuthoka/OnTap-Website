AOS.init({
    duration: 800,      
    once: true,         
    easing: 'ease-in-out',
    offset: 120         
  });
  
  var swiper = new Swiper('.partnerSwiper', {
    loop: true,
    autoplay: {
      delay: 2000,
      disableOnInteraction: false,
    },
    slidesPerView: 3,
    spaceBetween: 30,
    breakpoints: {
      640: { slidesPerView: 2 },
      768: { slidesPerView: 3 },
      1024: { slidesPerView: 4 }
    }
  });



 


  var swiper = new Swiper(".partnerSwiper", {
    loop: true,
    speed: 20000, // 20 seconds scroll duration
    autoplay: {
      delay: 0,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    spaceBetween: 50,
    allowTouchMove: false,
    freeMode: true,
    freeModeMomentum: false,

    // Pause on hover logic
    on: {
      init: function () {
        const swiperEl = document.querySelector('.partnerSwiper');
        swiperEl.addEventListener('mouseenter', () => {
          swiper.autoplay.stop();
        });
        swiperEl.addEventListener('mouseleave', () => {
          swiper.autoplay.start();
        });
      }
    }
  });



  