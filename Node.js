document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    let isScrolling;
    
    document.body.classList.add('has-sticky-header');
    
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('touchmove', handleScroll);
    
    function handleScroll() {
        window.clearTimeout(isScrolling);
        isScrolling = setTimeout(function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                header.classList.add('header-hidden');
            } else {
                header.classList.remove('header-hidden');
            }
            
            // Update sticky state
            if (scrollTop > 50) {
                header.classList.add('sticky');
            } else {
                header.classList.remove('sticky');
            }
            
            lastScrollTop = scrollTop;
        }, 66);
    }
    
    // Handle accessibility
    header.addEventListener('transitionend', function() {
        header.setAttribute('aria-hidden', header.classList.contains('header-hidden'));
    });
});