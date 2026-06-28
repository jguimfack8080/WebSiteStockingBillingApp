# TO-DO - Mise en ligne et visibilite de bizcorasystems.com

Plan d'action ordonne, de la mise en ligne jusqu'au referencement. A cocher au fur et a mesure.

- Domaine canonique : **https://www.bizcorasystems.com**
- Hebergement : **Cloudflare Pages** (projet `websitestockingbillingapp`) connecte a GitHub
- DNS : reste chez **STRATO** (on NE bascule PAS les nameservers, pour ne pas casser l'e-mail)
- Langues : FR / EN / DE (`/fr/ /en/ /de/`)

---

## PHASE 0 - Finir la mise en ligne (DNS)

### 0.1 CNAME www (chez STRATO) - FAIT / a verifier
- [ ] STRATO -> Domains -> Domainverwaltung -> `bizcorasystems.com` -> DNS -> **TXT- und CNAME-Records verwalten**
  - Typ : `CNAME` · Prafix : `www` · Ziel : `websitestockingbillingapp.pages.dev`
- [ ] (Si conflit) supprimer l'ancien enregistrement `www` dans **A-Record verwalten**, puis reessayer le CNAME
- [ ] NE PAS toucher : **MX-Record** (e-mail) ni les **TXT** SPF/DKIM existants

### 0.2 Activer le domaine sur Cloudflare Pages
- [ ] Cloudflare -> **Workers & Pages** -> `websitestockingbillingapp` -> **Custom domains** -> garder `www.bizcorasystems.com`
- [ ] Cliquer **Check DNS records** -> attendre l'activation + le certificat HTTPS (quelques minutes a 24 h)

### 0.3 Domaine nu bizcorasystems.com (sans www) -> redirige vers www
- [ ] STRATO -> Domainverwaltung -> `bizcorasystems.com` -> definir une **Weiterleitung (301)** vers `https://www.bizcorasystems.com`
  - Non bloquant : le site marche deja sur `www.bizcorasystems.com`. Mais a faire pour pouvoir communiquer l'adresse courte `bizcorasystems.com`.

### 0.4 Nettoyage Cloudflare (eviter la confusion)
- [ ] Supprimer la **zone DNS "Full"** `bizcorasystems.com` cote **Websites** (Overview -> Advanced Actions -> Remove Site from Cloudflare). Elle est inutile et affiche de fausses alertes e-mail.
  - Cela NE supprime PAS le projet Pages ni le Custom domain `www`.
- [ ] NE PAS changer les nameservers chez STRATO (sinon l'e-mail `contact@` / `no-reply@` casse).

---

## PHASE 1 - Verifier que tout marche (apres activation HTTPS)

- [ ] `https://www.bizcorasystems.com/` redirige vers `/fr/` (ou `/en/` `/de/` selon la langue du navigateur)
- [ ] `https://bizcorasystems.com` (sans www) renvoie vers `www` (apres la redirection 0.3)
- [ ] Une page directe charge : `https://www.bizcorasystems.com/en/features.html`
- [ ] Le selecteur de langue FR/EN/DE fonctionne sur chaque page
- [ ] `https://www.bizcorasystems.com/sitemap.xml` s'affiche
- [ ] `https://www.bizcorasystems.com/robots.txt` s'affiche
- [ ] L'e-mail fonctionne toujours : envoyer un test a `contact@bizcorasystems.com`
- [ ] Mobile : ouvrir le site sur telephone, verifier l'affichage et la vitesse

---

## PHASE 2 - Indexation (etre trouvable par Google) - PRIORITAIRE

### 2.1 Google Search Console (gratuit, indispensable)
- [ ] Aller sur search.google.com/search-console -> ajouter la propriete **`https://www.bizcorasystems.com`**
- [ ] Verifier la propriete (methode "balise HTML" ou "DNS TXT" chez STRATO)
- [ ] Menu **Sitemaps** -> soumettre : `https://www.bizcorasystems.com/sitemap.xml`
- [ ] Outil **Inspection d'URL** -> demander l'indexation de la page d'accueil

### 2.2 Bing Webmaster Tools (gratuit ; alimente Bing + ChatGPT/Copilot)
- [ ] bing.com/webmasters -> ajouter le site (import possible depuis Search Console)
- [ ] Soumettre le meme sitemap

### 2.3 Verifier les donnees structurees
- [ ] Tester l'accueil et la FAQ sur **search.google.com/test/rich-results** (doit detecter Organization / FAQPage / SoftwareApplication)
- [ ] Verifier l'apercu de partage (Open Graph) sur LinkedIn / WhatsApp : l'image doit s'afficher

---

## PHASE 3 - Visibilite RAPIDE (gratuit, fort impact)

### 3.1 App stores (tu as une vraie app = gros atout)
- [ ] Optimiser la fiche **Google Play** : titre avec mots-cles (caisse, stock, facturation), captures, description FR/EN/DE
- [ ] Idem **App Store** (iOS)
- [ ] Ajouter les **boutons de telechargement** (Play / App Store) bien visibles sur le site (me demander de les integrer)

### 3.2 Annuaires de logiciels (rankent pour toi)
- [ ] S'inscrire sur **Capterra**, **GetApp**, **G2**, **Software Advice**, **Appvizer** (FR)
- [ ] Demander **2-3 avis clients** dessus (effet enorme sur le classement et la confiance)

### 3.3 Google Business Profile (si activite/adresse locale)
- [ ] Creer une fiche Google Business (apparait sur Maps + recherches locales)

### 3.4 Reseaux
- [ ] Page **LinkedIn** entreprise (lier au profil createur deja existant) + 1er post de lancement

---

## PHASE 4 - Visibilite DURABLE (le vrai SEO, sur 3-6 mois)

### 4.1 Recherche de mots-cles (ce que les gens tapent vraiment)
- [ ] Definir le **marche prioritaire** (France ? Allemagne ? Afrique ?) et la **cible** (epiceries, grossistes, PME...)
- [ ] Lister les vraies recherches via : suggestions Google, bloc "Autres questions posees", "Recherches associees"
  - Exemples FR : "logiciel de caisse pour PME", "logiciel facturation TVA", "gestion de stock magasin"
  - Exemples DE : "Kassensystem fur kleine Geschafte", "Lagerverwaltung Software KMU"

### 4.2 Optimiser les pages existantes sur ces mots-cles
- [ ] Ajuster titres, sous-titres et textes (FR/EN/DE) pour matcher les recherches reelles (me demander : je le fais page par page)

### 4.3 Contenu / blog (capte les recherches "probleme")
- [ ] Creer une structure de **blog / guides** (FR/EN/DE) - me demander de la mettre en place
- [ ] Publier regulierement des articles utiles ("comment choisir un logiciel de caisse", etc.)

### 4.4 Pages par metier / cas d'usage
- [ ] Pages dediees (epicerie, grossiste, pharmacie, restaurant...) pour matcher des recherches precises - me demander

### 4.5 Autorite (backlinks)
- [ ] Obtenir des liens depuis des sites pertinents (annuaires, partenaires, presse specialisee, LinkedIn)
- [ ] Qualite > quantite. Jamais d'achat de liens douteux (penalise par Google).

---

## PHASE 5 - Mesure et suivi

- [ ] Installer une **analytics respectueuse de la vie privee** (Cloudflare Web Analytics - gratuit, sans cookie, ou Plausible) - me demander de l'integrer proprement (CSP a ajuster)
- [ ] Suivre dans **Search Console** : impressions, clics, requetes, pages indexees (1x/semaine)
- [ ] Ajouter le schema **AggregateRating** (etoiles dans Google) quand tu auras des avis clients - me demander

---

## (Optionnel) Visibilite IMMEDIATE payante
- [ ] **Google Ads** sur mots-cles ("logiciel caisse", etc.) pour des visiteurs tout de suite pendant que le SEO murit
- [ ] **Meta Ads** (Facebook/Instagram) selon la cible

---

## MAINTENANCE (a garder en tete)

- [ ] **Changement de domaine un jour ?** Modifier `WebSiteStockingBillingApp/.env` (`SITE_ORIGIN`) puis lancer `bash ./sync_site_origin.sh` (met a jour canonical, hreflang, sitemap, robots, middleware, redirects). Voir `PROD-READY.md`.
- [ ] **Mettre a jour `sitemap.xml`** (`<lastmod>`) a chaque modification importante d'une page.
- [ ] **Remplacer les images placeholder** (`pos-checkout`, `invoicing`, `quotes`, `document-emailing`, `loyalty`, `dashboards-reports`, `purchasing`, `stock-management`, `accounting`) par les vraies captures de l'app -> bien plus vendeur.
- [ ] **Garder le contenu synchronise** : toute nouvelle fonctionnalite de l'app = mise a jour des pages + des 3 langues.

---

### Ordre conseille pour demarrer
1. Phase 0 (DNS) -> 2. Phase 1 (verifs) -> 3. Phase 2 (Search Console + sitemap) -> 4. Phase 3 (stores + annuaires + Google Business) -> 5. Phase 4 en fond (mots-cles + contenu).

> Rappel honnete : le SEO organique prend **3 a 6 mois** pour un domaine neuf. Les gains rapides viennent des **stores, annuaires, Google Business et (si besoin) des Ads**. Le contenu + les backlinks construisent la visibilite durable.
