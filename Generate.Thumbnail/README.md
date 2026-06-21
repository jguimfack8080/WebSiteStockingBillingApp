# Generate.Thumbnail - Generateur des vignettes (thumbnails) du site BizCoRa

Ce dossier contient TOUT ce qu'il faut pour (re)generer les vignettes produit du
site vitrine. Elles representent fidelement les ecrans reels de l'application
BizCoRa (dashboard, stock, caisse, facturation, devis, comptabilite, etc.) et
sont produites en SVG vectoriel, dans les 3 langues du site (fr / en / de).

Tu peux modifier le contenu (libelles, montants, produits, couleurs) et tout
regenerer en une commande, autant de fois que tu veux.

---

## Pourquoi ce choix technique

- **SVG vectoriel** : nettete infinie (retina / 4K), poids minime, zero perte de
  qualite, ideal pour le SEO et la stabilite de mise en page (dimensions fixes,
  donc aucun "saut" de page / CLS). C'est la version servie en production.
- **Un seul generateur** (source de verite unique) : tous les ecrans partagent
  les memes composants (AppBar, cartes, KPI, chips, icones) et les memes tokens
  du Design System Flutter. Resultat : une identite visuelle 100% coherente sur
  toutes les vignettes (regle projet "identite visuelle unique").
- **Police websafe** (`Segoe UI` / Roboto / Arial, proche d'Inter) : rendu net
  partout, sans requete reseau ni police embarquee. Jamais cassant, jamais
  problematique pour le SEO ou la performance.
- **Multilingue** : le site ET l'application ont 3 langues. Chaque vignette est
  donc produite dans les 3 langues, avec le bon **formatage des montants et des
  dates** par locale (ex : `2 450,50 €` en fr, `€2,450.50` en en, `2.450,50 €`
  en de ; dates `jj/mm` en fr, `mm/jj` en en, `jj.mm` en de).

---

## Contenu du dossier

| Fichier | Role |
|---|---|
| `generate_thumbnails.py` | Genere les 33 SVG (11 ecrans x 3 langues) dans `../assets/images/`. |
| `render_preview.py` | Rend les SVG en PNG pour inspection (QA), et regenere l'image OG raster pour le partage social. |
| `previews/` | (cree a la demande) PNG jetables de QA. Peut etre supprime. |
| `README.md` | Ce fichier. |

---

## Prerequis

- **Python 3** (aucune dependance externe, uniquement la lib standard).
- Pour le rendu PNG / OG uniquement : un navigateur Chromium (Microsoft Edge ou
  Google Chrome), present d'office sous Windows. Pas necessaire pour generer les
  SVG.

---

## Regenerer les vignettes (cas courant)

Depuis ce dossier :

```bash
python generate_thumbnails.py
```

Cela (re)ecrit dans `../assets/images/` :

```
screenhot_app.svg        screenhot_app.en.svg        screenhot_app.de.svg        (dashboard - hero)
dashboards-reports.svg   dashboards-reports.en.svg   dashboards-reports.de.svg   (tableau de bord transactions)
stock-management.svg     stock-management.en.svg     stock-management.de.svg     (gestion des produits)
pos-checkout.svg         pos-checkout.en.svg         pos-checkout.de.svg         (caisse / point de vente)
invoicing.svg            invoicing.en.svg            invoicing.de.svg            (factures)
quotes.svg               quotes.en.svg               quotes.de.svg               (devis)
document-emailing.svg    document-emailing.en.svg    document-emailing.de.svg    (envoi de document par e-mail)
loyalty.svg              loyalty.en.svg              loyalty.de.svg              (fidelite client)
accounting.svg           accounting.en.svg           accounting.de.svg           (comptabilite)
purchasing.svg           purchasing.en.svg           purchasing.de.svg           (achats / fournisseurs)
cashier-performance.svg  cashier-performance.en.svg  cashier-performance.de.svg  (performance des caissiers)
```

**Convention de nommage** : le francais garde le nom de base historique
(`<ecran>.svg`) ; l'anglais et l'allemand ajoutent un suffixe de langue
(`<ecran>.en.svg`, `<ecran>.de.svg`). Les pages `/fr` referencent les `.svg`,
les pages `/en` les `.en.svg`, les pages `/de` les `.de.svg`.

---

## Verifier le rendu (QA visuelle)

```bash
python render_preview.py preview                       # tous les SVG -> PNG
python render_preview.py preview screenhot_app.svg      # un seul
python render_preview.py preview stock-management.de.svg pos-checkout.en.svg
```

Les PNG sont ecrits dans `previews/` (jetables, non servis en production).

---

## Regenerer l'image de partage social (Open Graph)

Les balises `og:image` / `twitter:image` du site pointent vers un PNG
**raster** (`assets/images/screenhot_app-1280.png`), car les reseaux sociaux ne
savent pas afficher du SVG en apercu de lien. Si tu modifies le dashboard,
regenere ce raster :

```bash
python render_preview.py og
```

(Rendu du `screenhot_app.svg` francais en PNG 1280x676.)

---

## Personnaliser le contenu

Tout est dans `generate_thumbnails.py`, regroupe en haut du fichier pour etre
facile a editer :

- **Couleurs** : dictionnaire `C` (aligne sur `lib/theme/design_system/app_palette.dart`).
  Marque indigo `#4361EE`, accent `#6366F1`, semantiques success/warning/danger/info.
- **Libelles d'interface (i18n)** : dictionnaire `S` (cle -> `(fr, en, de)`).
  Pour changer un texte, edite le tuple correspondant.
- **Donnees de demonstration** :
  - `PRODUCTS` (gestion de stock), `CATS` (categories),
  - `POS_PRODUCTS` et `CART` (caisse),
  - `DOC_ROWS` (lignes du document e-maile).
  Les noms de clients / fournisseurs / caissiers et les montants de demo sont
  directement dans les fonctions `screen_*` (ex : `screen_invoicing`).
- **Formatage** : `money()`, `num()`, `datestr()` gerent les locales. Ne mets
  jamais un montant "en dur" deja formate : passe un nombre a `money(...)`.

### Ajouter un nouvel ecran

1. Ecris une fonction `screen_mon_ecran()` qui retourne `frame(body, appbar)`
   en reutilisant les helpers existants (`card`, `kpi_card`, `action_tile`,
   `icon`, `status_chip`, `back_appbar`, etc.).
2. Ajoute une entree dans le dictionnaire `SCREENS` :
   `"mon-ecran": screen_mon_ecran`.
3. Lance `python generate_thumbnails.py` : les 3 langues sont produites.
4. Reference `assets/images/mon-ecran.svg` (fr) / `.en.svg` / `.de.svg` dans les
   pages HTML correspondantes.

### Ajouter une langue

Ajoute le code dans `LANGS`, complete la 4e valeur de chaque tuple de `S`, des
catalogues, et adapte `money()` / `num()` / `datestr()` si la locale l'exige.

---

## Fidelite a l'application reelle (anti-hallucination)

Les ecrans ont ete recrees a partir du code Flutter reel (titres d'ecran,
libelles i18n de `assets/langs/fr.json`, structure des cartes/listes, couleurs du
Design System). Les valeurs chiffrees sont des exemples plausibles. En cas de
modification de l'app, mets a jour les libelles et structures ici pour que les
vignettes restent representatives (regle projet : doc et visuels synchronises
avec le produit).

---

## Integration dans le site

- Les SVG sont references via `<img src="/assets/images/<ecran>[.lang].svg"
  width="1280" height="676" loading="lazy" decoding="async" alt="...">`.
- Le cadre visuel (coins arrondis, ombre, fond degrade) est fourni par la classe
  CSS `.shot` du site (`assets/css/components.css`). Les SVG sont donc des ecrans
  d'app pleine surface, sans chrome de fenetre.
- Le hero de la page d'accueil precharge sa vignette (`<link rel="preload">`).
