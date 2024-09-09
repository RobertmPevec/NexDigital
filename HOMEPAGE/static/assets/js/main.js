(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        //===== Preloader
        window.onload = function () {
            setTimeout(fadeout, 200);
        }

        function fadeout() {
            const preloader = document.querySelector('.preloader');
            if (preloader) {
                preloader.style.opacity = '0';
                preloader.style.display = 'none';
            }
        }

        /*=====================================
        Sticky
        ======================================= */
        window.onscroll = function () {
            var header_navbar = document.querySelector(".navbar-area");
            if (header_navbar) {
                var sticky = header_navbar.offsetTop;

                if (window.pageYOffset > sticky) {
                    header_navbar.classList.add("sticky");
                } else {
                    header_navbar.classList.remove("sticky");
                }
            }

            // Show or hide the back-top-top button
            var backToTo = document.querySelector(".scroll-top");
            if (backToTo) {
                if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
                    backToTo.style.display = "block";
                } else {
                    backToTo.style.display = "none";
                }
            }
        };

        //======== Modal Display Logic
        function displayInitialModal() {
            const modalShown = localStorage.getItem('modalShown');

            if (!modalShown) {
                const myModal = new bootstrap.Modal(document.getElementById('initialModal'));
                myModal.show();

                // Set a flag in local storage to indicate the modal has been shown
                localStorage.setItem('modalShown', 'true');
            }
        }

        // Call the function to check and display the modal
        displayInitialModal();

        //======== tiny slider
        if (document.querySelector('.client-logo-carousel')) {
            tns({
                container: '.client-logo-carousel',
                slideBy: 'page',
                autoplay: true,
                autoplayButtonOutput: false,
                mouseDrag: true,
                gutter: 15,
                nav: false,
                controls: false,
                responsive: {
                    0: { items: 1 },
                    540: { items: 2 },
                    768: { items: 3 },
                    992: { items: 4 }
                }
            });
        } else {
            console.warn("Element '.client-logo-carousel' not found, skipping Tiny Slider initialization.");
        }

        // WOW Scroll Spy
        var wow = new WOW({ mobile: false });
        wow.init();

        //====== counter up 
        var cu = new counterUp({
            start: 0,
            duration: 2000,
            intvalues: true,
            interval: 100,
        });
        cu.start();

        //============== isotope masonry js with imagesloaded
        imagesLoaded('#container', function () {
            var elem = document.querySelector('.grid');
            if (elem) {
                var iso = new Isotope(elem, {
                    itemSelector: '.grid-item',
                    masonry: { columnWidth: '.grid-item' }
                });

                let filterButtons = document.querySelectorAll('.portfolio-btn-wrapper button');
                filterButtons.forEach(e =>
                    e.addEventListener('click', (event) => {
                        let filterValue = event.target.getAttribute('data-filter');
                        iso.arrange({ filter: filterValue });
                    })
                );
            }
        });

        //======= portfolio-btn active
        var elements = document.getElementsByClassName("portfolio-btn");
        for (var i = 0; i < elements.length; i++) {
            elements[i].onclick = function () {
                var el = elements[0];
                while (el) {
                    if (el.tagName === "BUTTON") {
                        el.classList.remove("active");
                    }
                    el = el.nextSibling;
                }
                this.classList.add("active");
            };
        }

        // For menu scroll 
        var pageLink = document.querySelectorAll('.page-scroll');
        pageLink.forEach(elem => {
            elem.addEventListener('click', e => {
                e.preventDefault();
                document.querySelector(elem.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth',
                    offsetTop: 1 - 60,
                });
            });
        });

        // Section menu active
        function onScroll(event) {
            var sections = document.querySelectorAll('.page-scroll');
            var scrollPos = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

            for (var i = 0; i < sections.length; i++) {
                var currLink = sections[i];
                var val = currLink.getAttribute('href');
                var refElement = document.querySelector(val);

                // Check if the reference element exists
                if (refElement) {
                    var scrollTopMinus = scrollPos + 73;
                    if (refElement.offsetTop <= scrollTopMinus && (refElement.offsetTop + refElement.offsetHeight > scrollTopMinus)) {
                        // Remove 'active' class from other links
                        document.querySelectorAll('.page-scroll').forEach(function (link) {
                            link.classList.remove('active');
                        });
                        currLink.classList.add('active');
                    } else {
                        currLink.classList.remove('active');
                    }
                } else {
                    // Log a warning to the console if the element is not found
                    console.warn('Element not found for selector:', val);
                }
            }
        }

        window.document.addEventListener('scroll', onScroll);

        //===== close navbar-collapse when clicked
        let navbarToggler = document.querySelector(".navbar-toggler");
        var navbarCollapse = document.querySelector(".navbar-collapse");

        document.querySelectorAll(".page-scroll").forEach(e =>
            e.addEventListener("click", () => {
                navbarToggler.classList.remove("active");
                navbarCollapse.classList.remove('show');
            })
        );

        navbarToggler.addEventListener('click', function () {
            navbarToggler.classList.toggle("active");
        });

        //========= glightbox
        const myGallery = GLightbox({ 'type': 'image' });

    });
})();