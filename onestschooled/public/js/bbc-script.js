// BBC School Algeria - Scripts personnalisés
document.addEventListener("DOMContentLoaded", function() {
    
    // Animation des compteurs
    function animateCounters() {
        const counters = document.querySelectorAll(".counter-number");
        const observerOptions = {
            threshold: 0.5
        };
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.getAttribute("data-target") || counter.textContent);
                    animateCounter(counter, target);
                    counterObserver.unobserve(counter);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
    
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 20);
    }
    
    // Observer pour les animations au scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("bbc-animate");
            }
        });
    }, { threshold: 0.1 });
    
    // Observer tous les éléments animables
    document.querySelectorAll(".bbc-card, .bbc-counter, .bbc-section").forEach(el => {
        observer.observe(el);
    });
    
    // Smooth scroll pour les liens internes
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }
        });
    });
    
    // Navigation sticky avec effet
    const nav = document.querySelector(".navbar");
    if (nav) {
        let lastScrollY = window.scrollY;
        
        window.addEventListener("scroll", function() {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                nav.classList.add("navbar-scrolled");
                nav.style.boxShadow = "0 2px 20px rgba(0,0,0,0.1)";
                nav.style.background = "rgba(255, 255, 255, 0.95)";
                nav.style.backdropFilter = "blur(10px)";
            } else {
                nav.classList.remove("navbar-scrolled");
                nav.style.boxShadow = "none";
                nav.style.background = "";
                nav.style.backdropFilter = "";
            }
            
            // Cacher/montrer la navigation selon le scroll
            if (currentScrollY > lastScrollY && currentScrollY > 200) {
                nav.style.transform = "translateY(-100%)";
            } else {
                nav.style.transform = "translateY(0)";
            }
            
            lastScrollY = currentScrollY;
        });
    }
    
    // Messages de bienvenue multilingues BBC School
    const welcomeMessages = {
        en: [
            "📚 Educational excellence for 15 years!",
            "🌟 Your success, our priority!",
            "🇩🇿 Quality bilingual school!",
            "🏆 Excellent BEM success rate!",
            "🚌 Secure school transport!",
            "🍽️ Balanced halal canteen!",
            "👨‍🏫 45 qualified teachers!"
        ],
        fr: [
            "📚 Excellence éducative depuis 15 ans !",
            "🌟 Votre réussite, notre priorité !",
            "🇩🇿 École bilingue de qualité !",
            "🏆 Excellent taux de réussite au BEM !",
            "🚌 Transport scolaire sécurisé !",
            "🍽️ Cantine halal équilibrée !",
            "👨‍🏫 45 enseignants qualifiés !"
        ],
        ar: [
            "📚 التميز التعليمي منذ 15 عامًا!",
            "🌟 نجاحكم، أولويتنا!",
            "🇩🇿 مدرسة ثنائية اللغة عالية الجودة!",
            "🏆 معدل نجاح 95% في البكالوريا 2024!",
            "🚌 نقل مدرسي آمن!",
            "🍽️ مطعم حلال متوازن!",
            "👨‍🏫 45 معلم مؤهل!"
        ]
    };
    
    // Fonction pour obtenir la langue actuelle
    function getCurrentLanguage() {
        const urlParams = new URLSearchParams(window.location.search);
        const langFromUrl = urlParams.get("lang");
        const langFromStorage = localStorage.getItem("bbc_language");
        return langFromUrl || langFromStorage || "fr"; // Par défaut français
    }
    
    // Fonction pour obtenir les messages dans la langue actuelle
    function getCurrentWelcomeMessages() {
        const currentLang = getCurrentLanguage();
        return welcomeMessages[currentLang] || welcomeMessages.fr;
    }
    
    // Carousel automatique des messages multilingues
    function rotateWelcomeMessage() {
        const messageElements = document.querySelectorAll(".welcome-message, .hero-subtitle");
        if (messageElements.length > 0) {
            const messages = getCurrentWelcomeMessages();
            let currentIndex = 0;
            
            setInterval(() => {
                messageElements.forEach(element => {
                    element.style.opacity = "0";
                    element.style.transform = "translateY(20px)";
                    
                    setTimeout(() => {
                        element.textContent = messages[currentIndex];
                        element.style.opacity = "1";
                        element.style.transform = "translateY(0)";
                    }, 300);
                });
                
                currentIndex = (currentIndex + 1) % messages.length;
            }, 4000);
        }
    }
    
    // Démarrer le système multilingue
    document.addEventListener("DOMContentLoaded", function() {
        // Sauvegarder la langue choisie
        const urlParams = new URLSearchParams(window.location.search);
        const langFromUrl = urlParams.get("lang");
        if (langFromUrl) {
            localStorage.setItem("bbc_language", langFromUrl);
        }
        
        // Appliquer la direction RTL pour l'arabe
        const currentLang = getCurrentLanguage();
        if (currentLang === "ar") {
            document.body.setAttribute("dir", "rtl");
            document.body.classList.add("rtl");
        } else {
            document.body.setAttribute("dir", "ltr");
            document.body.classList.remove("rtl");
        }
        
        // Démarrer les messages
        setTimeout(rotateWelcomeMessage, 2000);
    });
    
    // Effet parallax simple pour les sections
    window.addEventListener("scroll", function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll(".parallax-bg");
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
    
    // Amélioration des cartes au hover
    document.querySelectorAll(".bbc-card").forEach(card => {
        card.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-15px) scale(1.02)";
        });
        
        card.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0) scale(1)";
        });
    });
    
    // Initialisation des tooltips si Bootstrap est disponible
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Gestion des modales personnalisées
    document.querySelectorAll('.bbc-modal-trigger').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const modalId = this.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'flex';
                modal.style.animation = 'fadeIn 0.3s ease-out';
            }
        });
    });
    
    // Fermeture des modales
    document.querySelectorAll('.modal-close, .modal-overlay').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => {
                    modal.style.display = 'none';
                }, 300);
            }
        });
    });
    
    // Amélioration des formulaires avec validation en temps réel
    document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#E84393';
                this.style.boxShadow = '0 0 0 0.2rem rgba(232, 67, 147, 0.25)';
            } else {
                this.style.borderColor = '#00B894';
                this.style.boxShadow = '0 0 0 0.2rem rgba(0, 184, 148, 0.25)';
            }
        });
    });
    
    // Gestion des notifications/alertes BBC School
    function showBBCNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `bbc-notification bbc-notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Styles inline pour la notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: var(--bbc-gradient);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: all 0.3s ease;
            max-width: 300px;
        `;
        
        document.body.appendChild(notification);
        
        // Animation d'apparition
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Fermeture automatique
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, duration);
        
        // Fermeture manuelle
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        });
    }
    
    
    // BLOCAGE COMPLET DES NOTIFICATIONS AUTOMATIQUES BBC SCHOOL
    // Pour empêcher toute notification automatique de s'afficher
    const originalShowBBCNotification = window.showBBCNotification;
    window.showBBCNotification = function(message, type = "info", duration = 5000) {
        // Ne rien faire pour les notifications automatiques
        console.log("Notification automatique bloquée:", message);
        return false;
    };
    
    // Garder la fonction originale pour usage manuel si nécessaire
    window.showBBCNotificationForced = originalShowBBCNotification;
    // Fonction globale pour les notifications
    window.showBBCNotification = showBBCNotification;
    
    // Notification de bienvenue BBC School - SUPPRIMÉE POUR ÉVITER L'ENCOMBREMENT
    // setTimeout(() => {
    //     showBBCNotification('🎓 Bienvenue sur le site de BBC School Algeria !', 'success', 6000);
    // }, 3000);
    
    // Gestion de l'état de chargement
    window.addEventListener('load', function() {
        const loader = document.querySelector('.page-loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 500);
        }
        
        // Animation d'entrée pour les éléments
        document.querySelectorAll('.fade-in-on-load').forEach((element, index) => {
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });
    
    console.log("🎓 BBC School Algeria - Scripts chargés avec succès !");
    console.log("🌟 Tous les effets visuels sont actifs !");
    console.log("🤖 Chatbot IA BBC School prêt à l'emploi !");
});

// Fonction utilitaire pour formater les nombres (statistiques)
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

// Fonction pour détecter si l'élément est visible
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Fonction pour obtenir la position de scroll optimisée
function getScrollPosition() {
    return window.pageYOffset || document.documentElement.scrollTop;
}

// Debounce pour optimiser les performances
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}