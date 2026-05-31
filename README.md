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
| `index.html` | Landing complete : hero, valeur, modules (stock / caisse / facturation), etapes, roles, plateformes, securite, tarifs, FAQ, CTA |
| `features.html` | Detail exhaustif de chaque module avec listes de fonctionnalites et tableau des roles |
| `pricing.html` | Offres (Starter, Business, Enterprise), comparatif detaille et FAQ tarifs |
| `faq.html` | Foire aux questions exhaustive, organisee par theme (generalites, stock, caisse, facturation, securite, technique, mise en route et support) |
| `about.html` | Mission, valeurs, createur et stack technique |
| `contact.html` | Coordonnees et formulaire de demande de demo (ouvre la messagerie pre-remplie, sans backend) |

---

## Stack technique

- **HTML5 + CSS3 + JavaScript natif** - aucun framework, aucun bundler, aucune
  dependance externe a charger (pas de jQuery, AOS, particles ni Font Awesome).
  Les icones sont des SVG inline.
- Seule ressource externe : la police **Google Fonts** (Inter + Poppins).
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
└── assets/
    ├── css/
    │   ├── theme.css         # Design tokens, reset, utilitaires, grilles, reveal
    │   └── components.css    # Header, hero, cartes, sections, tarifs, FAQ, footer...
    ├── js/
    │   └── site.js           # Menu mobile, header au scroll, reveal, accordeon FAQ, retour haut, annee
    └── images/
        ├── JGJPayStock.jpg   # Logo
        ├── screenhot_app.png # Capture de l'application
        └── jordanjeuna.jpg   # Photo du createur
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
- **SEO** : titres et meta descriptions par page, balises Open Graph, liens
  canoniques.

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

1. Copier l'integralite du dossier sur votre hebergement statique.
2. Servir `index.html` comme page d'entree.
3. (Recommande) Activer HTTPS et la compression (gzip / brotli).

Aucune etape de build n'est necessaire.

---

## Personnalisation rapide

| Element | Ou le modifier |
|---|---|
| Couleurs et typographie | `assets/css/theme.css` (variables `--brand-*`, `--font-*`) |
| Coordonnees de contact | Pied de page de chaque `.html` et `contact.html` |
| Capture d'ecran | Remplacer `assets/images/screenhot_app.png` |
| Logo | Remplacer `assets/images/JGJPayStock.jpg` |
| Textes et offres | Directement dans les fichiers `.html` correspondants |

---

## Contact

- Email : contact@jgjpaystock.com
- Telephone : +49 152 585 75 909
- LinkedIn : https://www.linkedin.com/in/jordan-guimfack-jeuna-08b821211/
- GitHub : https://github.com/jguimfack8080
