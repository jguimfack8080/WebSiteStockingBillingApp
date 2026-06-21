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
})();
