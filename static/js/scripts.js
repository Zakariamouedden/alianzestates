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
                const staggeredElements = entry.target.querySelectorAll('.animate-stagger');
                staggeredElements.forEach((el, index) => {
                    el.style.transitionDelay = `${index * 0.3}s`;
                    el.classList.add('fadeInUp');
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    revealElements.forEach(element => {
        observer.observe(element);
    });


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