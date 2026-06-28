# PROD READY (www.bizcorasystems.com)

Ce fichier contient uniquement les actions essentielles pour mettre le site vitrine en production sur Cloudflare Pages, avec un domaine canonique unique et un SEO propre.

## Source de verite (domaine)

- `WebSiteStockingBillingApp/.env`
  - `SITE_ORIGIN=https://www.bizcorasystems.com`
  - `DEFAULT_LANGUAGE=fr`
- Pour propager un changement de domaine (canonical, hreflang, JSON-LD, robots, sitemap, middleware, redirects) :
  - `cd WebSiteStockingBillingApp`
  - `bash ./sync_site_origin.sh`

## Cloudflare Pages (deploiement)

1. Connecter le projet Cloudflare Pages au depot GitHub.
2. Configuration Pages (pour un site statique) :
   - Root directory : `WebSiteStockingBillingApp`
   - Framework preset : None
   - Build command : (vide)
   - Build output directory : `/`
3. Connecter `www.bizcorasystems.com` en domaine personnalise du projet Pages.
4. Ajouter aussi `bizcorasystems.com` et laisser la redirection vers `www` (301) se faire automatiquement via `functions/_middleware.js`.
5. Verifier que ces fichiers sont bien pris en compte par Cloudflare Pages :
   - `_headers` (CSP, HSTS, cache)
   - `_redirects` (fallback pour anciennes URLs)
   - `functions/_middleware.js` (redirection racine + detection de langue)

## Redirections SEO (comportement attendu)

- `https://www.bizcorasystems.com/` redirige vers `/fr/` par defaut, ou vers `/en/` et `/de/` selon `Accept-Language` (302).
- `https://bizcorasystems.com/*` redirige vers `https://www.bizcorasystems.com/*` (301).
- Les anciennes URLs racine `/about.html`, `/pricing.html`, etc redirigent vers `/fr/...` (301).

## Referencement (apres mise en ligne)

1. Google Search Console : ajouter la propriete `https://www.bizcorasystems.com`.
2. Soumettre le sitemap : `https://www.bizcorasystems.com/sitemap.xml`.
3. Verifier les donnees structurees (accueil et FAQ) avec le Rich Results Test.
4. Verifier les apercus Open Graph (LinkedIn, messageries).

## Reglages Cloudflare a verifier

- Compression (Brotli) et HTTP/3 (QUIC) actives.
- Ne pas activer Rocket Loader.
