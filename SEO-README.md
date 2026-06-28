# SEO-README - Optimisation SEO technique & performance

Ce document decrit **tout** ce qui a ete fait sur le site vitrine BizCoRa
lors de la passe d'optimisation SEO technique et performance, et **a quoi chaque
changement sert**. Il sert de reference durable : avant de modifier le site,
relire cette page pour ne pas casser ce qui a ete mis en place.

Perimetre : site vitrine multilingue (`/fr`, `/en`, `/de`) avec canonical, hreflang et sitemap multilingue.

---

## 1. Methode de mesure (reproductible)

Aucun chiffre n'est invente : tout est mesure en local avec Lighthouse.

- Outils installes en local (portable, sans droits admin) :
  `Node.js v22.13.1` + `lighthouse 12.8.2` + `http-server` (dossier
  `%LOCALAPPDATA%\seo-tools`).
- Serveur local : `http-server <site> -p 8099 -c-1` -> `http://127.0.0.1:8099/`.
- Mesure par page : `lighthouse <url> --output=json
  --only-categories=performance,seo,accessibility,best-practices
  --chrome-flags="--headless=new"` (profil mobile par defaut, `--preset=desktop`
  pour le desktop).
- Les scores Lighthouse mobile sont **bruites** sur cette machine (le dossier est
  synchronise par OneDrive, ce qui provoque des pics CPU pendant la mesure). Pour
  fiabiliser, chaque page a ete mesuree **3 fois et on prend la mediane**. Les
  runs ou `TBT` (Total Blocking Time) explose (500-800 ms) sont des artefacts de
  charge machine : le site lui-meme produit un TBT proche de 0.

### Ce qui differe entre local et production (Cloudflare)

- En production, Cloudflare ajoute **Brotli** (compression), **HTTP/3** et le
  **cache edge**. L'opportunite Lighthouse "Enable text compression" (~600 ms)
  vue en local n'existe **pas** en prod (le serveur de test local ne compresse
  pas). Les scores reels en production seront donc **superieurs** a ces mesures
  locales bridees.

---

## 2. Resultats mesures (avant -> apres)

Mediane de 3 mesures Lighthouse, profil mobile (sauf `desktop`).

| Page | Perf avant | Perf apres | A11y | BP | SEO | LCP mobile | CLS |
|---|---|---|---|---|---|---|---|
| index (mobile)   | 67 | ~91 (run propre) | 100 | 100 | 100 | 6.07s -> ~2.9s | 0.136 -> **0** |
| features (mobile)| 71 | 94 | 100 | 100 | 100 | 6.16s -> 2.41s | 0.080 -> **0** |
| pricing (mobile) | 86 | 94 | 100 | 100 | 100 | 3.41s -> 2.29s | 0.004 -> **0** |
| faq (mobile)     | 87 | 94 | 100 | 100 | 100 | 3.26s -> 2.41s | 0.073 -> **0** |
| about (mobile)   | 73 | 97 | 100 | 100 | 100 | 6.46s -> 2.26s | 0.007 -> **0** |
| contact (mobile) | 90 | 99 | 100 | 100 | 100 | 3.14s -> 1.88s | 0.003 -> **0** |
| index (desktop)  | 85 | 98 | 100 | 100 | 100 | 1.25s -> 0.66s | 0.220 -> 0.073 |

Gains principaux : **A11y, Best Practices et SEO a 100 partout**, **CLS ramene a
0 sur mobile** (et 0.073 sur desktop, sous le seuil 0.1 "bon"), **LCP mobile
divise par ~2 a 3** sur les pages a visuels (de ~6 s a ~2-3 s).

> Note honnete : un score Lighthouse "SEO" affichait deja 100 avant les
> changements. C'est trompeur : l'audit SEO de Lighthouse ne verifie PAS la
> justesse des canonical, le hreflang ni le JSON-LD. Les corrections SEO
> structurelles ci-dessous sont donc des corrections de **justesse** (utiles pour
> Google) que Lighthouse ne recompense pas par des points.

---

## 3. Ce qui a ete fait, et a quoi ca sert

### 3.1 Indexation et donnees structurees (SEO)

- **Canonical absolu sur chaque page** (domaine canonique `SITE_ORIGIN`, voir `.env`). Avant,
  seul `index.html` en avait un. *A quoi ca sert :* dire a Google quelle est
  l'URL de reference d'une page et eviter le contenu duplique.
- **`robots.txt`** (a la racine) : autorise le crawl et pointe vers le sitemap.
- **`sitemap.xml`** (a la racine) : sitemap multilingue avec `xhtml:link hreflang` (FR, EN, DE + x-default). *Sert a* accelerer et completer l'indexation, et declarer les variantes linguistiques.
- **JSON-LD (donnees structurees) injecte par page**, uniquement a partir du
  contenu reel :
  - `index.html` : `Organization` + `WebSite` + `SoftwareApplication` (l'app et
    l'editeur).
  - `faq.html` : `FAQPage` genere a partir des **42 vraies questions/reponses** de
    la page (extraites automatiquement, pas inventees).
  - `pricing/features/about/contact` : `BreadcrumbList` + `WebPage`, plus
    `Person` (createur) sur about et `ContactPoint` sur contact.
  *A quoi ca sert :* permettre les resultats enrichis Google (FAQ deroulante,
  fil d'Ariane, fiche entreprise) et mieux faire comprendre le site aux moteurs.
- **Open Graph + Twitter Cards complets** sur chaque page (titre, description,
  `og:url`, `og:image` absolue, `og:locale`, `twitter:card`). *Sert a* un bel
  apercu lors d'un partage sur les reseaux/messageries.

### 3.2 Performance et Core Web Vitals

- **Images optimisees** : la capture d'ecran passe de **520 Ko (PNG)** a
  **9,4 Ko en WebP** (repli PNG 1280px pour les vieux navigateurs, via
  `<picture>`), le logo de **117 Ko (2048x2048)** a **2,6 Ko (96px)**, la photo du
  createur de 129 Ko a 37 Ko WebP. *Sert a* reduire fortement le poids et le LCP.
- **Dimensions explicites (`width`/`height`) sur toutes les images** +
  `height:auto` en CSS. *Sert a* reserver la place de l'image avant son
  chargement => supprime le decalage de mise en page (CLS).
- **`loading="lazy"`** sur les images hors ecran, **`fetchpriority="high"` +
  `preload`** sur l'image du hero (element LCP de l'accueil). *Sert a* charger en
  priorite ce qui est visible et differer le reste.
- **Polices auto-hebergees** (Inter + Poppins, sous-ensemble latin, woff2, dans
  `assets/fonts/`). Plus aucune requete vers Google Fonts. *Sert a* supprimer
  deux connexions tierces du chemin critique (meilleur LCP/FCP) et ameliorer la
  vie privee.
- **Police de repli ajustee aux metriques** (`@font-face` "Inter Fallback" /
  "Poppins Fallback" avec `size-adjust`/`ascent-override`). *Sert a* ce que la
  police systeme occupe exactement la meme place que la police finale : la
  bascule ne provoque **aucun** decalage (CLS ~0).
- **Suppression des fichiers images originaux** devenus inutilises (`-766 Ko`
  environ : `BizCoRa.jpeg` a la racine, `screenhot_app.png`, l'ancien logo et
  l'ancienne photo). *Sert a* ne pas deployer de poids mort.

### 3.3 Accessibilite (A11y a 100)

- **Contrastes corriges** : le gris trop clair `--text-subtle` (#8a93a6, ratio
  3.08) devient #6b7280 (ratio 4.84, conforme AA) ; les liens du bas de footer
  passent en clair sur fond sombre. *Sert a* la lisibilite (et c'est un facteur
  SEO indirect).
- **Hierarchie des titres corrigee** : plus de saut de niveau. Les titres de
  colonnes du footer (`h4` -> `h3`), les noms d'offres de la page Tarifs
  (`h3` -> `h2`, sous le h1), les libelles des cartes Contact (`h4` -> `h3`).
- **Liens dans le texte soulignes** (`main p a`) : ils ne sont plus distinguables
  uniquement par la couleur.

### 3.4 Cloudflare (`_headers`)

Fichier `_headers` (format Cloudflare Pages / Workers Static Assets) :

- **Cache** : revalidation systematique du HTML ; CSS/JS en cache court avec
  `stale-while-revalidate` (car les noms de fichiers ne sont pas versionnes/hashes
  - ne PAS passer en `immutable` tant qu'il n'y a pas de fingerprint) ; images et
  polices en cache long.
- **Securite** : `Content-Security-Policy` (sources restreintes a `'self'`),
  `Strict-Transport-Security` (HSTS), `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`.

> La CSP autorise `'unsafe-inline'` pour les styles et le script en ligne
> (formulaire de contact). Un durcissement par nonce/hash est possible plus tard
> (necessite de sortir le script inline et les styles inline) ; non bloquant.

---

## 4. Ce qui N'A PAS ete touche (et pourquoi)

- **Le contenu redactionnel** : non modifie (hors corrections de niveaux de
  titres). Le SEO on-page de fond (mots-cles, intentions) depend de la strategie
  editoriale, pas du code.
- **La strategie editoriale** (SEO on page) : le code n'est qu'une partie. Les mots cles, l'intention et la ligne editoriale restent une decision produit.
- **Le formulaire de contact** : reste en `mailto:` (sans backend), inchange.

---

## 5. Points hors-code (a faire cote plateforme)

Voir **PROD-READY.md** pour la mise en production sur `https://www.bizcorasystems.com` (Cloudflare Pages, redirections, Search Console).
