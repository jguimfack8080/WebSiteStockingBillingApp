# Site vitrine BizCoRa

Site web officiel de **BizCoRa**, la solution tout-en-un de gestion de
stock, de caisse (point de vente) et de facturation pour les commerces et les
PME. Ce site a pour unique objectif de **presenter et vendre l'application** :
mettre en valeur toutes ses fonctionnalites et repondre directement aux
questions des clients.

Cette version est une **reconstruction complete a partir de zero**. L'ancien
site (oriente agence / portfolio, avec des dependances externes lourdes) a ete
remplace par un site vitrine produit, moderne, rapide et entierement dedie a
BizCoRa.

---

## Objectif

- Vendre l'application et creer un effet "waouh" des l'arrivee sur la page.
- Mettre en avant l'integralite des fonctionnalites (stock, caisse,
  facturation, alertes, rapports, personnalisation, roles, securite,
  plateformes).
- Repondre a toutes les questions d'un prospect (page FAQ exhaustive + FAQ sur
  la page d'accueil et la page tarifs).
- Inciter a l'action : demander une demo ou un devis.

---

## Pages

Le site est multilingue. Chaque langue contient les 6 pages suivantes :

| Page (par langue) | URL | Role |
|---|---|
| Accueil | `/<lang>/` | Landing complete : hero (probleme -> solution), valeur, solutions par probleme, modules, etapes, roles, plateformes, securite, tarifs, FAQ, recit "Notre raison d'etre", CTA |
| Fonctionnalites | `/<lang>/features.html` | Detail exhaustif de chaque module avec listes et tableau des roles |
| Tarifs | `/<lang>/pricing.html` | Offres, comparatif detaille et FAQ tarifs |
| FAQ | `/<lang>/faq.html` | Foire aux questions exhaustive, organisee par theme |
| A propos | `/<lang>/about.html` | Mission, valeurs, createur et stack technique |
| Contact | `/<lang>/contact.html` | Coordonnees et formulaire de demande de demo (mailto, sans backend) |

---

## Stack technique

- **HTML5 + CSS3 + JavaScript natif** - aucun framework, aucun bundler, aucune
  dependance externe a charger (pas de jQuery, AOS, particles ni Font Awesome).
  Les icones sont des SVG inline.
- **Aucune ressource externe** : les polices **Inter + Poppins** (sous-ensemble
  latin, woff2) sont auto-hebergees dans `assets/fonts/`. Le site ne charge donc
  aucun domaine tiers (ni Google Fonts), ce qui ameliore performance et vie privee.
- Le site est **statique** : il se deploie tel quel sur n'importe quel
  hebergement de fichiers (Nginx, Apache, Netlify, GitHub Pages, S3...).

### Structure

```
WebSiteStockingBillingApp/
├── fr/
│   ├── index.html
│   ├── features.html
│   ├── pricing.html
│   ├── faq.html
│   ├── about.html
│   └── contact.html
├── en/
│   ├── index.html
│   ├── features.html
│   ├── pricing.html
│   ├── faq.html
│   ├── about.html
│   └── contact.html
├── de/
│   ├── index.html
│   ├── features.html
│   ├── pricing.html
│   ├── faq.html
│   ├── about.html
│   └── contact.html
├── robots.txt               # Indexation + lien vers le sitemap
├── sitemap.xml              # Sitemap multilingue (URLs absolues)
├── _headers                 # En-tetes Cloudflare (cache, securite, CSP)
├── _redirects               # Redirections (fallback)
├── functions/_middleware.js # Redirection racine + detection de langue
├── .env                     # Domaine canonique (SITE_ORIGIN)
├── sync_site_origin.py      # Applique SITE_ORIGIN dans le HTML/SEO
├── sync_site_origin.sh      # Script bash: modifier .env puis executer
└── assets/
    ├── css/
    │   ├── theme.css         # Design tokens, reset, utilitaires, grilles, reveal
    │   └── components.css    # Header, hero, cartes, sections, tarifs, FAQ, footer...
    ├── js/
    │   └── site.js           # Menu mobile, header au scroll, reveal, accordeon FAQ, retour haut, annee
    ├── fonts/                # Inter + Poppins auto-hebergees (woff2, sous-ensemble latin)
    └── images/
        ├── logo-96.png           # Logo (header / footer)
        ├── favicon-32.png        # Favicon
        ├── apple-touch-icon.png  # Icone iOS (180x180)
        ├── icon-192.png          # Icone (logo schema.org / PWA)
        ├── <ecran>.svg           # Vignette produit (francais) - voir Generate.Thumbnail/
        ├── <ecran>.en.svg        # Vignette produit (anglais)
        ├── <ecran>.de.svg        # Vignette produit (allemand)
        ├── screenhot_app-1280.png# Image OG/Twitter raster (regeneree depuis le SVG dashboard)
        ├── jordanjeuna.webp      # Photo du createur (WebP, 640px)
        └── jordanjeuna-640.jpg   # Photo du createur (repli JPEG)

# Generateur des vignettes (thumbnails) produit :
Generate.Thumbnail/
├── generate_thumbnails.py   # Genere les 33 SVG (11 ecrans x 3 langues) dans assets/images/
├── render_preview.py        # Rendu PNG de QA + regeneration de l'image OG raster
└── README.md                # Comment regenerer / personnaliser
```

### Vignettes produit (thumbnails)

Les vignettes qui presentent l'application (dashboard, gestion de stock, caisse,
facturation, devis, envoi de documents, fidelite, comptabilite, achats,
performance des caissiers, tableau de bord des transactions) sont des **SVG
vectoriels** generes, recrees fidelement a partir des ecrans reels de
l'application et de son Design System. Elles existent dans les **3 langues**
(`<ecran>.svg` fr, `<ecran>.en.svg` en, `<ecran>.de.svg` de), avec formatage des
montants et des dates par locale.

Pour modifier le contenu ou regenerer, voir **`Generate.Thumbnail/README.md`** :

```bash
cd WebSiteStockingBillingApp/Generate.Thumbnail
python generate_thumbnails.py     # regenere les 33 SVG
python render_preview.py og       # regenere l'image OG raster (apres modif du dashboard)
```

> SVG en production (nettete infinie, poids minime, ideal SEO/CLS). L'image
> `og:image` reste un PNG raster, car les reseaux sociaux n'affichent pas le SVG.

---

## Design

- Identite visuelle alignee sur l'application : couleur de marque indigo
  `#4361EE`, typographie Poppins (titres) + Inter (texte).
- Design SaaS moderne : hero avec mockup, cartes, sections alternees,
  animations d'apparition au scroll (sobres et performantes), section securite
  sombre, bandeau d'appel a l'action.
- **Responsive** (mobile, tablette, desktop) avec menu mobile accessible.
- **Accessibilite** : navigation au clavier, attributs ARIA sur le menu et la
  FAQ, respect de `prefers-reduced-motion`.
- **SEO** : titres et meta descriptions uniques par page, canonical absolu sur
  chaque page, Open Graph et Twitter Cards complets, donnees structurees JSON-LD
  (Organization, WebSite, SoftwareApplication, FAQPage, BreadcrumbList, Person,
  ContactPoint), `robots.txt` et `sitemap.xml` servis a la racine.
- **Performance** : images en WebP avec repli et dimensions explicites (anti-CLS),
  `loading="lazy"` hors ecran, prechargement de l'image hero (LCP), polices Google
  chargees en non bloquant.

> Domaine canonique : `https://www.jgjpaystock.com` (voir `.env`).

---

## Lancer en local

Le site etant statique, n'importe quel serveur de fichiers convient :

```bash
# Python
python -m http.server 8080

# ou Node
npx http-server -p 8080
```

Puis ouvrir `http://localhost:8080`.

---

## Deploiement

Le site est deploye sur Cloudflare (Pages / Workers Static Assets).

1. Copier l'integralite du dossier sur l'hebergement statique.
2. Les pages sont sous `/fr/`, `/en/`, `/de/`. La racine `/` est redirigee par Cloudflare Pages Functions (voir `functions/_middleware.js`).
3. HTTPS, Brotli et HTTP/3 sont fournis par Cloudflare (cote plateforme).
4. Le fichier `_headers` applique le cache et les en-tetes de securite (CSP, HSTS)
   uniquement si le deploiement utilise le gestionnaire d'assets statiques
   Cloudflare avec la prise en charge de `_headers`/`_redirects`.

Aucune etape de build n'est necessaire.

### Changer le domaine (sans modifier les pages une par une)

1. Modifier `WebSiteStockingBillingApp/.env` (variable `SITE_ORIGIN`).
2. Executer le script bash (recommande) :

```bash
cd WebSiteStockingBillingApp
bash ./sync_site_origin.sh
```

Le script met a jour automatiquement canonical, hreflang, JSON-LD, `robots.txt` et `sitemap.xml` a partir de `.env`.

---

## Personnalisation rapide

| Element | Ou le modifier |
|---|---|
| Couleurs et typographie | `assets/css/theme.css` (variables `--brand-*`, `--font-*`) |
| Coordonnees de contact | Pied de page de chaque langue (`/fr/*.html`, `/en/*.html`, `/de/*.html`) et pages `contact.html` |
| Vignettes produit (thumbnails) | Editer puis lancer `Generate.Thumbnail/generate_thumbnails.py` (voir son README). Image OG : `Generate.Thumbnail/render_preview.py og` |
| Logo et favicons | Regenerer `logo-96.png`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png` depuis le logo source |
| Textes et offres | Directement dans les fichiers `.html` correspondants |

---

## Notes de version

**Vignettes produit en SVG vectoriel, multilingues et fideles a l'app**

- Remplacement des anciennes captures raster (PNG/WebP), partiellement dupliquees
  et a l'ancienne marque, par **11 vignettes SVG par langue** (33 au total)
  recreees fidelement a partir des ecrans reels et du Design System de
  l'application : dashboard, transactions, stock (avec illustrations produit),
  caisse, factures, devis, envoi par e-mail, fidelite, comptabilite, achats,
  performance des caissiers.
- Generateur unique et documente dans **`Generate.Thumbnail/`** (un seul fichier
  source pour une identite visuelle 100% coherente), avec formatage des montants
  et dates par locale (fr/en/de).
- Pages `index`, `features` et `about` (fr/en/de) referencent les SVG via `<img>`
  (plus de `<picture>`/WebP) ; preload du hero en SVG ; image `og:image`/`twitter`
  conservee en PNG raster (regeneree depuis le SVG dashboard).
- Anciennes vignettes raster orphelines supprimees.

**Plan selection au formulaire d'inscription (register.html fr/en/de)**

- Les pages `register.html` lisent le parametre URL `?plan=` (trial/basic/professional/enterprise)
  et affichent un badge coloré au-dessus du formulaire pour confirmer le plan choisi.
- Le champ `selected_plan` est transmis au backend billing lors de la soumission du formulaire
  (`POST /billing/register`), permettant au service de créer la subscription avec le bon plan.
- Les fonctions `resendEmail` et `resetForm` sont exposées en `window.*` pour compatibilité
  strict-mode dans les navigateurs modernes.
- Aucun changement de structure : uniquement fr/en/de register.html + ce README.

**Integration modules Comptabilite et Achats + storytelling**

- Ajout des modules **Achats et fournisseurs** et **Comptabilite** (compte de resultat, TVA collectee/deductible/due, tresorerie, valeur du stock au cout, comparaison de periodes, exports PDF/CSV et documents officiels) sur `features.html` (modules 9 et 10, renumerotation des suivants) avec ancres dediees.
- Page d'accueil : nouvelles cartes de valeur (achats, comptabilite), section **Solutions** (probleme -> reponse, tous metiers), module **Comptabilite et achats**, et section **hero** repensee pour exposer immediatement le probleme et la solution.
- Recit **"Notre raison d'etre"** (section sombre `#histoire`) racontant la genese de l'idee et les vrais problemes resolus, pour qu'un visiteur comprenne l'essentiel sans parcourir tout le site.
- FAQ : nouvelle rubrique **Comptabilite, TVA et achats**. Tarifs : comptabilite et achats positionnes sur les offres Business et Enterprise (offre + comparatif).
- Styles `.story` ajoutes dans `components.css`. Aucune dependance externe ajoutee.

**Refonte complete (branche `refonte/site-vitrine-vente`, ticket #1)**

- Reconstruction du site a partir de zero, dedie a la vente de l'application.
- 6 pages : accueil, fonctionnalites, tarifs, FAQ, a propos, contact.
- Mise en valeur de toutes les fonctionnalites de l'application, dont les
  statistiques et graphiques : courbe d'evolution des ventes, top des produits
  vendus par periode (jour / semaine / mois / trimestre / semestre / annee /
  periode libre, 5 a 50), evolution du chiffre d'affaires vs mois precedent,
  camembert de repartition par categorie, graphique des mouvements de stock
  (entrees / sorties), tableau de bord des transactions a onglets.
- Tout le texte visible est accentue correctement (UTF-8).
- Aucune reference a des outils internes (pas de lien GitHub) sur le site public.
- Aucune dependance externe lourde : HTML / CSS / JavaScript natif, sans build.

---

## Contact

- Email : contact@jgjpaystock.com
- Telephone : +49 152 585 75 909
- LinkedIn : https://www.linkedin.com/in/jordan-guimfack-jeuna-08b821211/
