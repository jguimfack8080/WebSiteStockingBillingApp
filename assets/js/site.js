/* ==========================================================================
   BizCoRa - Site vitrine : interactions (vanilla, sans dependance)
   - Menu mobile
   - Header au scroll
   - Reveal au scroll (IntersectionObserver)
   - Accordeon FAQ (accessible)
   - Bouton retour en haut
   - Annee dynamique dans le footer
   ========================================================================== */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initHeaderScroll();
    initReveal();
    initFaq();
    initToTop();
    initYear();
    initLightbox();
  });

  /* Menu mobile */
  function initMobileNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    // Ferme le menu apres un clic sur un lien (navigation interne)
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Ombre/bordure du header au scroll */
  function initHeaderScroll() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Reveal au scroll */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(function (el) { observer.observe(el); });
  }

  /* Accordeon FAQ */
  function initFaq() {
    var items = document.querySelectorAll(".faq-item");
    items.forEach(function (item) {
      var btn = item.querySelector(".faq-q");
      var answer = item.querySelector(".faq-a");
      if (!btn || !answer) return;

      btn.addEventListener("click", function () {
        var isOpen = item.classList.contains("is-open");

        // Ferme les autres pour un accordeon propre
        items.forEach(function (other) {
          if (other !== item) {
            other.classList.remove("is-open");
            var b = other.querySelector(".faq-q");
            var a = other.querySelector(".faq-a");
            if (b) b.setAttribute("aria-expanded", "false");
            if (a) a.style.maxHeight = null;
          }
        });

        item.classList.toggle("is-open", !isOpen);
        btn.setAttribute("aria-expanded", !isOpen ? "true" : "false");
        answer.style.maxHeight = !isOpen ? answer.scrollHeight + "px" : null;
      });
    });
  }

  /* Bouton retour en haut */
  function initToTop() {
    var btn = document.querySelector(".to-top");
    if (!btn) return;
    var onScroll = function () {
      btn.classList.toggle("is-visible", window.scrollY > 600);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* Annee dynamique */
  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  /* Lightbox : clic sur une capture (cadre tablette) pour l'agrandir.
     Le portrait (.shot--photo) est exclu : ce n'est pas une capture d'app. */
  function initLightbox() {
    var triggers = document.querySelectorAll(".device, .shot:not(.shot--photo)");
    if (!triggers.length) return;

    var lang = (document.documentElement.lang || "fr").slice(0, 2);
    var labels = {
      fr: { open: "Agrandir l'apercu", close: "Fermer l'apercu" },
      en: { open: "Enlarge preview", close: "Close preview" },
      de: { open: "Vorschau vergroessern", close: "Vorschau schliessen" }
    };
    var L = labels[lang] || labels.fr;

    // Cree l'overlay une seule fois et le reutilise
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-hidden", "true");
    lb.innerHTML =
      '<div class="lightbox__frame">' +
        '<button type="button" class="lightbox__close" aria-label="' + L.close + '">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>' +
        '</button>' +
        '<img class="lightbox__img" alt="" />' +
        '<p class="lightbox__caption"></p>' +
      '</div>';
    document.body.appendChild(lb);

    var lbImg = lb.querySelector(".lightbox__img");
    var lbCap = lb.querySelector(".lightbox__caption");
    var lbClose = lb.querySelector(".lightbox__close");
    var lastFocused = null;

    function open(img) {
      if (!img) return;
      lastFocused = document.activeElement;
      // Utilise la meilleure source disponible (srcset webp > src)
      lbImg.src = img.currentSrc || img.src;
      lbImg.alt = img.alt || "";
      lbCap.textContent = img.alt || "";
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.classList.add("lb-open");
      lbClose.focus();
    }

    function close() {
      if (!lb.classList.contains("is-open")) return;
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.classList.remove("lb-open");
      if (lastFocused && lastFocused.focus) lastFocused.focus();
    }

    triggers.forEach(function (trigger) {
      var img = trigger.querySelector("img");
      if (!img) return;
      trigger.setAttribute("role", "button");
      trigger.setAttribute("tabindex", "0");
      trigger.setAttribute("aria-label", L.open);
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        open(img);
      });
      trigger.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
          e.preventDefault();
          open(img);
        }
      });
    });

    lbClose.addEventListener("click", close);
    lb.addEventListener("click", function (e) {
      if (e.target === lb) close(); // clic sur le fond
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" || e.key === "Esc") close();
    });
  }
})();

/* Menu "Ressources" : fermer au clic exterieur ou sur Echap */
document.addEventListener('click', function (e) {
  document.querySelectorAll('details.nav-dd[open]').forEach(function (d) {
    if (!d.contains(e.target)) d.removeAttribute('open');
  });
});
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') document.querySelectorAll('details.nav-dd[open]').forEach(function (d) { d.removeAttribute('open'); });
});
