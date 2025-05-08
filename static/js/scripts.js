document.addEventListener('DOMContentLoaded', function () {
    // Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('active');
        });
    }

    // Parallax Effect for Hero Section
    const heroVideo = document.querySelector('.hero-video');
    if (heroVideo) {
        window.addEventListener('scroll', () => {
            const scrollPosition = window.scrollY;
            heroVideo.style.transform = `translateY(${scrollPosition * 0.2}px)`;
        });
    }

    // Enhanced Scroll Reveal with Elegant Animations
    const revealElements = document.querySelectorAll('.reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
<<<<<<< HEAD
                const staggeredElements = entry.target.querySelectorAll('.animate-stagger');
                staggeredElements.forEach((el, index) => {
                    el.style.transitionDelay = `${index * 0.3}s`;
                    el.classList.add('fadeInUp');
=======
                // Remove animation logic
                const staggeredElements = entry.target.querySelectorAll('.animate-stagger');
                staggeredElements.forEach((el) => {
                    el.style.transitionDelay = '0s'; // No delay
                    el.classList.remove('fadeInUp'); // Remove animation class
>>>>>>> 9782bed (css arreglado)
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
<<<<<<< HEAD

=======
    
>>>>>>> 9782bed (css arreglado)
    revealElements.forEach(element => {
        observer.observe(element);
    });

    // Enhanced Swiper for Propiedades Destacadas
    const featuredSwiper = document.querySelector('.swiper');
    if (featuredSwiper) {
        new Swiper(featuredSwiper, {
            slidesPerView: 'auto',
            spaceBetween: 40,
            loop: true,
            centeredSlides: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                640: {
                    spaceBetween: 20,
                },
                1024: {
                    spaceBetween: 40,
                },
            },
            on: {
                slideChangeTransitionStart: function () {
                    const slides = this.slides;
                    slides.forEach(slide => {
                        slide.style.opacity = '0';
                        slide.style.transform = 'translateY(20px)';
                    });
                },
                slideChangeTransitionEnd: function () {
                    const activeSlide = this.slides[this.activeIndex];
                    const nextSlide = this.slides[this.activeIndex + 1] || this.slides[0];
                    const prevSlide = this.slides[this.activeIndex - 1] || this.slides[this.slides.length - 1];
                    [activeSlide, nextSlide, prevSlide].forEach(slide => {
                        if (slide) {
                            slide.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                            slide.style.opacity = '1';
                            slide.style.transform = 'translateY(0)';
                        }
                    });
                },
            },
        });
    }

    // Property Swiper (property_detail.html)
    const propertySwiper = document.querySelector('.swiper-container.property');
    if (propertySwiper) {
        new Swiper(propertySwiper, {
            slidesPerView: 1,
            loop: true,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }

    // Map Initialization
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        const lat = parseFloat(mapContainer.dataset.lat);
        const lng = parseFloat(mapContainer.dataset.lng);
        const title = mapContainer.dataset.title || 'Propiedad';
        if (lat && lng) {
            const map = L.map('map').setView([lat, lng], 15);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 18,
            }).addTo(map);
            L.marker([lat, lng]).addTo(map)
                .bindPopup(title)
                .openPopup();
        }
    }

    // Property Filter Form
    const propertyFilterForm = document.getElementById('property-filter');
    if (propertyFilterForm) {
        propertyFilterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(propertyFilterForm);
            const params = new URLSearchParams();
            formData.forEach((value, key) => {
                if (value) {
                    params.append(key, value);
                }
            });
            window.location.href = '/properties?' + params.toString();
        });
    }
});