// Attendre que le DOM soit entièrement chargé
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des composants
    initNavbar();
    initScrollReveal();
    initBackToTop();
    initMobileMenu();
    initSmoothScroll();
    initTypingEffect();
    
    // Initialiser les animations au chargement
    animateOnLoad();
    
    // Initialiser le mode sombre si activé
    initDarkMode();
});

// ===== NAVBAR SCROLL EFFECT =====
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScroll = 0;
    const scrollThreshold = 100;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Ajouter/supprimer la classe 'scrolled' en fonction du défilement
        if (currentScroll > scrollThreshold) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Gérer l'affichage/masquage de la navbar au scroll
        if (currentScroll <= 0) {
            navbar.classList.remove('scroll-up');
            return;
        }
        
        if (currentScroll > lastScroll && !navbar.classList.contains('scroll-down')) {
            // Scroll vers le bas
            navbar.classList.remove('scroll-up');
            navbar.classList.add('scroll-down');
        } else if (currentScroll < lastScroll && navbar.classList.contains('scroll-down')) {
            // Scroll vers le haut
            navbar.classList.remove('scroll-down');
            navbar.classList.add('scroll-up');
        }
        
        lastScroll = currentScroll;
    });
}

// ===== SCROLL REVEAL ANIMATIONS =====
function initScrollReveal() {
    // Vérifier si l'API IntersectionObserver est supportée
    if (!('IntersectionObserver' in window)) {
        return;
    }
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
                // Ne plus observer une fois l'animation déclenchée
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observer tous les éléments avec l'attribut data-aos
    document.querySelectorAll('[data-aos]').forEach(element => {
        observer.observe(element);
    });
}

// ===== BACK TO TOP BUTTON =====
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;
    
    const scrollThreshold = 300;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > scrollThreshold) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===== MOBILE MENU TOGGLE =====
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const navItems = document.querySelectorAll('.nav-links li');
    
    if (!menuToggle || !navLinks) return;
    
    // Fonction pour ouvrir/fermer le menu
    const toggleMenu = (open) => {
        if (open) {
            menuToggle.classList.add('active');
            navLinks.classList.add('active');
            document.body.classList.add('menu-open');
            
            // Animer les éléments du menu un par un
            navItems.forEach((item, index) => {
                item.style.animation = `fadeInRight 0.3s ease forwards ${index * 0.1 + 0.2}s`;
            });
        } else {
            menuToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.classList.remove('menu-open');
            
            // Réinitialiser les animations
            navItems.forEach(item => {
                item.style.animation = '';
            });
        }
    };
    
    // Gestion du clic sur le bouton menu
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = this.classList.contains('active');
        toggleMenu(!isOpen);
    });
    
    // Fermer le menu en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active') && 
            !e.target.closest('.navbar') && 
            !e.target.closest('.menu-toggle')) {
            toggleMenu(false);
        }
    });
    
    // Fermer le menu lors du clic sur un lien
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Petit délai pour permettre la navigation avant de fermer le menu
            setTimeout(() => toggleMenu(false), 100);
        });
    });
    
    // Gestion du redimensionnement de la fenêtre
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (window.innerWidth > 992) {
                toggleMenu(false);
            }
        }, 250);
    });
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            // Vérifier si c'est un lien d'ancrage
            if (targetId === '#' || !document.querySelector(targetId)) {
                return;
            }
            
            e.preventDefault();
            
            const targetElement = document.querySelector(targetId);
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });
}

// ===== TYPING EFFECT =====
function initTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-text');
    if (typingElements.length === 0) return;
    
    typingElements.forEach(element => {
        const spans = element.querySelectorAll('span');
        let currentSpan = 0;
        
        function typeWriter() {
            if (currentSpan < spans.length) {
                const span = spans[currentSpan];
                const text = span.textContent;
                span.textContent = '';
                
                let charIndex = 0;
                const type = () => {
                    if (charIndex < text.length) {
                        span.textContent += text.charAt(charIndex);
                        charIndex++;
                        setTimeout(type, 100);
                    } else {
                        currentSpan++;
                        if (currentSpan < spans.length) {
                            setTimeout(typeWriter, 500);
                        }
                    }
                };
                
                type();
            }
        }
        
        // Démarrer l'animation après un court délai
        setTimeout(typeWriter, 1000);
    });
}

// ===== ANIMATIONS AU CHARGEMENT =====
function animateOnLoad() {
    // Ajouter une classe au body pour indiquer que le chargement est terminé
    document.body.classList.add('loaded');
    
    // Animation des éléments de la section hero
    const heroContent = document.querySelector('.hero-content');
    const heroImage = document.querySelector('.hero-image');
    
    if (heroContent) {
        heroContent.style.opacity = '0';
        heroContent.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            heroContent.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 300);
    }
    
    if (heroImage) {
        heroImage.style.opacity = '0';
        heroImage.style.transform = 'translateX(20px)';
        
        setTimeout(() => {
            heroImage.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            heroImage.style.opacity = '1';
            heroImage.style.transform = 'translateX(0)';
        }, 500);
    }
}

// ===== DARK MODE TOGGLE =====
function initDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (!darkModeToggle) return;
    
    // Vérifier le thème précédent
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const currentTheme = localStorage.getItem('theme');
    
    if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    
    // Gérer le changement de thème
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Mettre à jour le thème si les préférences système changent
    prefersDarkScheme.addListener(e => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                document.body.classList.add('dark-mode');
                darkModeToggle.checked = true;
            } else {
                document.body.classList.remove('dark-mode');
                darkModeToggle.checked = false;
            }
        }
    });
}

// ===== INITIALISATION DES COMPOSANTS =====
function initComponents() {
    // Initialiser les tooltips
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    tooltipTriggers.forEach(trigger => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = trigger.getAttribute('data-tooltip');
        trigger.appendChild(tooltip);
        
        trigger.addEventListener('mouseenter', () => {
            tooltip.classList.add('show');
        });
        
        trigger.addEventListener('mouseleave', () => {
            tooltip.classList.remove('show');
        });
    });
    
    // Initialiser les modales
    const modalTriggers = document.querySelectorAll('[data-modal]');
    modalTriggers.forEach(trigger => {
        const modalId = trigger.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        
        if (!modal) return;
        
        trigger.addEventListener('click', () => {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        const closeButtons = modal.querySelectorAll('.modal-close');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
        
        // Fermer la modale en cliquant en dehors
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
}

// Appeler l'initialisation des composants après le chargement du DOM
document.addEventListener('DOMContentLoaded', initComponents);
