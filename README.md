# Site vitrine JGJPayStock

Site web officiel de **JGJPayStock**, la solution tout-en-un de gestion de
stock, de caisse (point de vente) et de facturation pour les commerces et les
PME. Ce site a pour unique objectif de **presenter et vendre l'application** :
mettre en valeur toutes ses fonctionnalites et repondre directement aux
questions des clients.

Cette version est une **reconstruction complete a partir de zero**. L'ancien
site (oriente agence / portfolio, avec des dependances externes lourdes) a ete
remplace par un site vitrine produit, moderne, rapide et entierement dedie a
JGJPayStock.

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

| Page | Role |
|---|---|
| `index.html` | Landing complete : hero (probleme -> solution), valeur, solutions par probleme, modules (stock / caisse / facturation / comptabilite et achats), etapes, roles, plateformes, securite, tarifs, FAQ, recit "Notre raison d'etre", CTA |
| `features.html` | Detail exhaustif de chaque module (stock, caisse, facturation, devis, e-mailing, fidelite, alertes, rapports, achats et fournisseurs, comptabilite, personnalisation, roles, securite) avec listes de fonctionnalites et tableau des roles |
| `pricing.html` | Offres (Starter, Business, Enterprise), comparatif detaille et FAQ tarifs |
| `faq.html` | Foire aux questions exhaustive, organisee par theme (generalites, stock, caisse, facturation, securite, technique, mise en route et support) |
| `about.html` | Mission, valeurs, createur et stack technique |
| `contact.html` | Coordonnees et formulaire de demande de demo (ouvre la messagerie pre-remplie, sans backend) |

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
├── index.html
├── features.html
├── pricing.html
├── faq.html
├── about.html
├── contact.html
├── robots.txt               # Indexation + lien vers le sitemap
├── sitemap.xml              # Sitemap (URLs absolues jgjpaystock.com)
├── _headers                 # En-tetes Cloudflare (cache, securite, CSP)
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
        ├── screenhot_app.webp    # Capture de l'application (WebP, 1280px)
        ├── screenhot_app-1280.png# Capture (repli PNG pour navigateurs sans WebP)
        ├── jordanjeuna.webp      # Photo du createur (WebP, 640px)
        └── jordanjeuna-640.jpg   # Photo du createur (repli JPEG)
```

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

> Le domaine canonique de reference est `https://jgjpaystock.com`. Tant que le
> site est servi depuis un domaine de test (`*.workers.dev`), ce domaine de test
> ne doit pas etre indexe (voir la section Deploiement).

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
2. Servir `index.html` comme page d'entree.
3. HTTPS, Brotli et HTTP/3 sont fournis par Cloudflare (cote plateforme).
4. Le fichier `_headers` applique le cache et les en-tetes de securite (CSP, HSTS)
   uniquement si le deploiement utilise le gestionnaire d'assets statiques
   Cloudflare avec la prise en charge de `_headers`/`_redirects`.

Aucune etape de build n'est necessaire.

### Domaine de test vs production

- Le domaine canonique est `https://jgjpaystock.com` (canonical, hreflang futurs,
  sitemap et Open Graph y pointent).
- Tant que le site est servi depuis un domaine de test (`*.workers.dev`), il ne
  faut PAS laisser ce domaine s'indexer. Un fichier statique ne peut pas
  distinguer l'hote : pour bloquer l'indexation du test, ajouter cote plateforme
  (dashboard / route Cloudflare) un en-tete `X-Robots-Tag: noindex` sur le
  domaine de test, ou le proteger par mot de passe. A retirer au passage en
  production sur le domaine final.

---

## Personnalisation rapide

| Element | Ou le modifier |
|---|---|
| Couleurs et typographie | `assets/css/theme.css` (variables `--brand-*`, `--font-*`) |
| Coordonnees de contact | Pied de page de chaque `.html` et `contact.html` |
| Capture d'ecran | Regenerer `assets/images/screenhot_app.webp` et `screenhot_app-1280.png` (memes dimensions 1280x676) |
| Logo et favicons | Regenerer `logo-96.png`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png` depuis le logo source |
| Textes et offres | Directement dans les fichiers `.html` correspondants |

---

## Notes de version

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
