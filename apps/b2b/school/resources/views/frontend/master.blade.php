@include('frontend.partials.header')

@include('frontend.partials.menu')

@yield('main')

@include('frontend.partials.footer-content')
@include('frontend.partials.footer')

{{-- BBC School Algeria - Chatbot IA Intégré --}}
@include('frontend.partials.bbc-ai-chatbot')

{{-- BBC SCHOOL - Scripts personnalisés (les scripts principaux sont dans footer.blade.php) --}}
{{-- SYSTÈME MULTILINGUE BBC SCHOOL --}}
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Détection et application de la langue
    const urlParams = new URLSearchParams(window.location.search);
    const langFromUrl = urlParams.get("lang");

    if (langFromUrl) {
        localStorage.setItem("bbc_current_language", langFromUrl);

        // Appliquer les styles RTL pour l'arabe
        if (langFromUrl === "ar") {
            document.documentElement.setAttribute("lang", "ar");
            document.documentElement.setAttribute("dir", "rtl");
            document.body.classList.add("rtl-layout");
        } else {
            document.documentElement.setAttribute("lang", langFromUrl);
            document.documentElement.setAttribute("dir", "ltr");
            document.body.classList.remove("rtl-layout");
        }

        // Mettre à jour le titre selon la langue
        const titles = {
            en: "BBC School Algeria - Educational Excellence",
            fr: "BBC School Algeria - Excellence Éducative",
            ar: "مدرسة بي بي سي الجزائر - التميز التعليمي"
        };

        if (titles[langFromUrl]) {
            document.title = titles[langFromUrl];
        }
    }
});
</script>
{{-- FIN SYSTÈME MULTILINGUE --}}

{{-- PATCH ANTI-NOTIFICATION BBC SCHOOL --}}
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Désactiver toutes les notifications automatiques
    if (typeof toastr !== "undefined") {
        const originalToastr = toastr.success;
        toastr.success = function(message, title) {
            if (message && (message.includes("Bienvenue") || message.includes("bbc") || message.includes("BBC"))) {
                console.log("Notification toastr bloquée:", message);
                return;
            }
            return originalToastr.apply(this, arguments);
        };
    }

    // Supprimer toutes les notifications existantes après 1 seconde
    setTimeout(() => {
        const allNotifications = document.querySelectorAll(
            ".bbc-notification, .toast, .alert, .notification, " +
            "[class*='notification'], [class*='toast'], [class*='alert']"
        );
        allNotifications.forEach(el => {
            if (el.textContent && el.textContent.toLowerCase().includes("bienvenue")) {
                el.remove();
            }
        });
    }, 1000);

    // Bloquer aussi les futures notifications
    setInterval(() => {
        const newNotifications = document.querySelectorAll(".bbc-notification");
        newNotifications.forEach(el => {
            if (el.textContent && el.textContent.toLowerCase().includes("bienvenue")) {
                el.remove();
            }
        });
    }, 500);
});
</script>
{{-- FIN PATCH ANTI-NOTIFICATION --}}

</body>
</html>