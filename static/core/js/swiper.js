
$(document).ready(function (){

const swiper = new Swiper(".swiper-container", {
    // Optional parameters

    direction: "horizontal",
    loop: true,
    autoHeight: false,
    centeredSlides: false,
    spaceBetween: 10,
    slidesPerView: 1,
    // Responsive breakpoints
    breakpoints: {
        640: {
            slidesPerView: 1,
            spaceBetween: 10,
        },
        992: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
        1200:{
            slidesPerView: 3,
            spaceBetween: 10,
        }
    },

    // If we need pagination
    pagination: {
        el: ".swiper-pagination"
    },

    // Navigation arrows
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev"
    }

    // And if we need scrollbar
    /*scrollbar: {
    el: '.swiper-scrollbar',
  },*/
});
})

