/* BizCoRa Documentation - recherche instantanee, navigation, scroll-spy.
   Aucune dependance. Le contenu (pages) est statique et indexable ; ce script
   ne fait qu'ameliorer l'experience par-dessus. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------------- Recherche ---------------- */
  var input = $("#doc-search-input");
  var box = $("#doc-search-results");
  var INDEX = [];
  var active = -1;

  function norm(s) {
    return (s || "").toString().toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function esc(s) { return (s || "").replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }
  function highlight(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      try {
        var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
        out = out.replace(re, "<mark>$1</mark>");
      } catch (e) {}
    });
    return out;
  }

  function loadIndex() {
    if (!input) return;
    var url = input.getAttribute("data-index");
    if (!url) return;
    fetch(url).then(function (r) { return r.json(); }).then(function (d) {
      INDEX = (d || []).map(function (a) {
        a._h = norm([a.t, a.c, a.s, a.k, a.x].join(" "));
        a._t = norm(a.t); a._k = norm(a.k);
        return a;
      });
    }).catch(function () {});
  }

  function search(q) {
    var terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var scored = [];
    INDEX.forEach(function (a) {
      var sc = 0, ok = true;
      terms.forEach(function (t) {
        if (a._h.indexOf(t) === -1) { ok = false; return; }
        if (a._t.indexOf(t) !== -1) sc += 10;
        if (a._k.indexOf(t) !== -1) sc += 6;
        sc += 1;
      });
      if (ok) { if (a._t.indexOf(terms.join(" ")) !== -1) sc += 8; scored.push([sc, a]); }
    });
    scored.sort(function (a, b) { return b[0] - a[0]; });
    return scored.slice(0, 8).map(function (x) { return x[1]; });
  }

  function render(q) {
    if (!box) return;
    var res = search(q), terms = norm(q).split(/\s+/).filter(Boolean);
    active = -1;
    if (!q.trim()) { box.classList.remove("open"); box.innerHTML = ""; return; }
    if (!res.length) { box.innerHTML = '<div class="empty">' + (box.getAttribute("data-empty") || "Aucun resultat") + '</div>'; box.classList.add("open"); return; }
    box.innerHTML = res.map(function (a) {
      return '<a class="r" href="' + a.u + '"><span class="rc">' + esc(a.c) + '</span>' +
        '<div class="rt">' + highlight(a.t, terms) + '</div>' +
        '<div class="rs">' + highlight((a.s || "").slice(0, 140), terms) + '</div></a>';
    }).join("");
    box.classList.add("open");
  }

  if (input) {
    var t;
    input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { render(input.value); }, 90); });
    input.addEventListener("focus", function () { if (input.value.trim()) render(input.value); });
    input.addEventListener("keydown", function (e) {
      var items = $$(".r", box);
      if (e.key === "ArrowDown") { e.preventDefault(); active = Math.min(active + 1, items.length - 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); active = Math.max(active - 1, 0); }
      else if (e.key === "Enter") { if (items[active]) { e.preventDefault(); window.location = items[active].getAttribute("href"); } return; }
      else if (e.key === "Escape") { box.classList.remove("open"); input.blur(); return; }
      else return;
      items.forEach(function (el, i) { el.classList.toggle("active", i === active); });
      if (items[active]) items[active].scrollIntoView({ block: "nearest" });
    });
    document.addEventListener("click", function (e) { if (box && !box.contains(e.target) && e.target !== input) box.classList.remove("open"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== input && !/^(input|textarea)$/i.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); input.focus(); }
    });
    loadIndex();
  }

  /* ---------------- Navigation mobile ---------------- */
  var burger = $("#doc-burger"), sidebar = $("#doc-sidebar"), backdrop = $("#doc-sidebar-backdrop");
  function closeNav() { document.body.classList.remove("doc-nav-open"); if (sidebar) sidebar.classList.remove("open"); }
  if (burger) burger.addEventListener("click", function () { document.body.classList.toggle("doc-nav-open"); if (sidebar) sidebar.classList.toggle("open"); });
  if (backdrop) backdrop.addEventListener("click", closeNav);

  /* sidebar : amener l'article actif dans la vue */
  var act = $(".doc-cat .nav-link.is-active", sidebar);
  if (act && sidebar) { try { act.scrollIntoView({ block: "center" }); } catch (e) {} }

  /* ---------------- TOC scroll-spy ---------------- */
  var tocLinks = $$(".doc-toc a");
  var sections = $$(".doc-section[id]");
  if (tocLinks.length && sections.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (l) { map[l.getAttribute("href").slice(1)] = l; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (l) { l.classList.remove("is-active"); });
          var l = map[en.target.id]; if (l) l.classList.add("is-active");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    sections.forEach(function (s) { io.observe(s); });
  }
})();
