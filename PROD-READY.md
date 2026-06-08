# PROD-READY - Checklist de mise en production (jgjpaystock.com)

Ce document liste **uniquement les actions que TOI tu dois faire** pour lancer le
site en production sur le domaine final `jgjpaystock.com`. Le code, lui, est deja
pret (voir `SEO-README.md` pour le detail technique).

Aujourd'hui le site tourne sur un domaine de **test** :
`https://sitejgjpaystock.arbeitgpt1.workers.dev/`. Tout le code (canonical,
sitemap, Open Graph, JSON-LD) pointe deja vers `https://jgjpaystock.com`.

---

## A. Avant le lancement (pendant que tu testes encore)

- [ ] **Empecher l'indexation du domaine de test.** Le domaine `*.workers.dev`
      ne doit pas etre reference par Google. Un fichier statique ne peut pas
      distinguer le domaine, donc a faire **cote Cloudflare** (dashboard / regle
      de route sur le domaine de test) : ajouter l'en-tete
      `X-Robots-Tag: noindex` sur le domaine de test, OU le proteger par mot de
      passe (Cloudflare Access). **A retirer le jour du lancement.**

---

## B. Le jour du lancement sur jgjpaystock.com

1. [ ] **Brancher le domaine.** Dans le dashboard Cloudflare, ajouter
       `jgjpaystock.com` (et `www.jgjpaystock.com`) comme domaine personnalise du
       projet, et configurer le DNS (Cloudflare gere les enregistrements).
2. [ ] **Choisir www ou sans-www** et rediriger l'un vers l'autre (301). Le code
       utilise la version **sans www** (`https://jgjpaystock.com/`). Donc rediriger
       `www.jgjpaystock.com` -> `jgjpaystock.com`.
3. [ ] **Forcer HTTPS** : activer "Always Use HTTPS" (Cloudflare le fait
       automatiquement avec un certificat). Le HSTS est deja envoye par `_headers`.
4. [ ] **Retirer le `noindex`** mis a l'etape A sur l'ancien domaine de test.
5. [ ] **Verifier que `_headers` est bien applique.** Il ne fonctionne que si le
       deploiement utilise le gestionnaire d'assets statiques Cloudflare
       (Cloudflare Pages, ou Workers avec le binding `assets` et la prise en
       charge de `_headers`/`_redirects`). Si tu es sur un Worker "classique",
       il faudra rejouer ces en-tetes dans le code du Worker. A verifier en
       ouvrant les outils dev du navigateur (onglet Network -> Response Headers).

---

## C. Reglages a verifier dans le dashboard Cloudflare (cote plateforme)

Ces options ne sont pas dans le code, elles se cochent dans Cloudflare :

- [ ] **Brotli / compression** : active (gere automatiquement par Cloudflare).
- [ ] **HTTP/3 (QUIC)** : active.
- [ ] **Polish (optimisation d'images)** : optionnel. Les images sont deja
      optimisees (WebP) ; Polish n'apportera presque rien, tu peux laisser off.
- [ ] **Auto Minify** : optionnel. Le HTML/CSS/JS est deja propre ; sans effet
      majeur.
- [ ] **Early Hints** : optionnel, peut aider le LCP.
- [ ] **Ne PAS activer Rocket Loader** (il differe le JS et peut casser le menu
      mobile / l'accordeon FAQ).

---

## D. Apres le lancement (referencement)

1. [ ] **Google Search Console** : ajouter et verifier la propriete
       `jgjpaystock.com`.
2. [ ] **Soumettre le sitemap** : `https://jgjpaystock.com/sitemap.xml`.
3. [ ] **Tester les donnees structurees** avec le test des resultats enrichis
       Google (rich results test) sur l'accueil et la FAQ.
4. [ ] **Verifier l'apercu de partage** (Open Graph) sur LinkedIn / messagerie :
       l'image `og:image` doit s'afficher (elle pointe vers
       `https://jgjpaystock.com/assets/images/screenhot_app-1280.png`).

---

## E. Si un jour le domaine final change (autre que jgjpaystock.com)

Le domaine `https://jgjpaystock.com` est ecrit en absolu dans plusieurs endroits.
S'il change, faire un rechercher/remplacer de `https://jgjpaystock.com` dans :

- les 6 pages `*.html` (canonical, Open Graph, Twitter, JSON-LD) ;
- `sitemap.xml` ;
- `robots.txt` (ligne `Sitemap:`).

Puis re-tester et re-soumettre le sitemap dans Search Console.

---

## F. Plus tard (hors de cette mise en prod)

- [ ] **Multilingue FR / EN / DE** (`/fr` `/en` `/de`, hreflang reciproques,
      sitemap multilingue, selecteur de langue). Chantier dedie, non inclus ici.
- [ ] **Mettre a jour le `lastmod`** du `sitemap.xml` a chaque modification
      importante d'une page.
