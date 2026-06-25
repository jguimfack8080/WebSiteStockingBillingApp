"""
Generates all billing pages for W-BIL01-06.
Run from the WebSiteStockingBillingApp root directory.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Shared fragments ──────────────────────────────────────────────────────────

def head(lang, title, desc, canonical, hreflang_fr, hreflang_en, hreflang_de, og_title=None):
    og_title = og_title or title
    lang_labels = {"fr": "fr_FR", "en": "en_US", "de": "de_DE"}
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#4361ee" />
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow" />

  <link rel="alternate" hreflang="fr" href="{hreflang_fr}" />
  <link rel="alternate" hreflang="en" href="{hreflang_en}" />
  <link rel="alternate" hreflang="de" href="{hreflang_de}" />
  <link rel="alternate" hreflang="x-default" href="{hreflang_fr}" />

  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="96x96" href="/assets/images/logo-96.png" />
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" />
  <link rel="preload" href="/assets/fonts/poppins-700.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="BizCoRa" />
  <meta property="og:locale" content="{lang_labels[lang]}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://www.jgjpaystock.com/assets/images/screenhot_app-1280.png" />

  <link rel="stylesheet" href="/assets/css/theme.css" />
  <link rel="stylesheet" href="/assets/css/components.css" />
</head>"""


def header_nav(lang, active_page):
    t = {
        "fr": {"home": "Accueil", "features": "Fonctionnalités", "pricing": "Tarifs",
               "faq": "FAQ", "about": "À propos", "cta": "Essai gratuit 14j",
               "download": "Télécharger", "lang": "Choix de la langue"},
        "en": {"home": "Home", "features": "Features", "pricing": "Pricing",
               "faq": "FAQ", "about": "About", "cta": "Free trial 14d",
               "download": "Download", "lang": "Language choice"},
        "de": {"home": "Startseite", "features": "Funktionen", "pricing": "Preise",
               "faq": "FAQ", "about": "Über uns", "cta": "Kostenlos 14 Tage",
               "download": "Download", "lang": "Sprachauswahl"},
    }[lang]
    pages = [
        ("./", t["home"], ""),
        ("features", t["features"], ""),
        ("pricing", t["pricing"], ""),
        ("download", t["download"], ""),
        ("faq", t["faq"], ""),
        ("about", t["about"], ""),
        ("register", t["cta"], " btn btn--primary btn--sm nav-cta"),
    ]
    nav_items = ""
    for href, label, cls in pages:
        active = ' class="is-active"' if href.rstrip("/") == active_page else (f' class="{cls.strip()}"' if cls else "")
        nav_items += f'\n        <a href="{href}"{active}>{label}</a>'

    lang_fr_active = ' class="is-active" aria-current="page"' if lang == "fr" else ""
    lang_en_active = ' class="is-active" aria-current="page"' if lang == "en" else ""
    lang_de_active = ' class="is-active" aria-current="page"' if lang == "de" else ""

    return f"""
  <header class="site-header">
    <div class="container">
      <a href="./" class="brand" aria-label="BizCoRa, accueil">
        <img src="/assets/images/logo-96.png" alt="" width="38" height="38" decoding="async" />
        <span>Biz<b>CoRa</b></span>
      </a>
      <nav class="nav" id="primary-nav" aria-label="Navigation principale">{nav_items}
      </nav>
      <div class="header-actions">
        <div class="lang-switch" role="group" aria-label="{t['lang']}">
          <a href="/fr/{active_page}" hreflang="fr" lang="fr"{lang_fr_active}>FR</a>
          <a href="/en/{active_page}" hreflang="en" lang="en"{lang_en_active}>EN</a>
          <a href="/de/{active_page}" hreflang="de" lang="de"{lang_de_active}>DE</a>
        </div>
        <a href="register" class="btn btn--primary btn--sm btn-desktop">{t['cta']}</a>
        <button class="nav-toggle" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="primary-nav">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
      </div>
    </div>
  </header>"""


def footer(lang):
    t = {
        "fr": {"product": "Produit", "company": "Entreprise", "contact": "Contact",
               "features": "Fonctionnalités", "pricing": "Tarifs", "security": "Sécurité",
               "about": "À propos", "faq": "FAQ", "contact_link": "Contact",
               "demo": "Demander une démo", "download": "Télécharger",
               "rights": "Tous droits réservés.", "country": "Allemagne"},
        "en": {"product": "Product", "company": "Company", "contact": "Contact",
               "features": "Features", "pricing": "Pricing", "security": "Security",
               "about": "About", "faq": "FAQ", "contact_link": "Contact",
               "demo": "Request a demo", "download": "Download",
               "rights": "All rights reserved.", "country": "Germany"},
        "de": {"product": "Produkt", "company": "Unternehmen", "contact": "Kontakt",
               "features": "Funktionen", "pricing": "Preise", "security": "Sicherheit",
               "about": "Über uns", "faq": "FAQ", "contact_link": "Kontakt",
               "demo": "Demo anfordern", "download": "Herunterladen",
               "rights": "Alle Rechte vorbehalten.", "country": "Deutschland"},
    }[lang]
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <span class="footer-brand"><img src="/assets/images/logo-96.png" alt="" width="38" height="38" decoding="async" /> BizCoRa</span>
          <p>La solution tout-en-un de gestion de stock, caisse, facturation, achats et comptabilite pour les commerces et les PME.</p>
        </div>
        <div class="footer-col">
          <h3>{t['product']}</h3>
          <ul>
            <li><a href="features">{t['features']}</a></li>
            <li><a href="pricing">{t['pricing']}</a></li>
            <li><a href="download">{t['download']}</a></li>
            <li><a href="./#securite">{t['security']}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>{t['company']}</h3>
          <ul>
            <li><a href="about">{t['about']}</a></li>
            <li><a href="faq">{t['faq']}</a></li>
            <li><a href="contact">{t['contact_link']}</a></li>
            <li><a href="contact">{t['demo']}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>{t['contact']}</h3>
          <ul class="footer-contact">
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg> <a href="mailto:contact@jgjpaystock.com">contact@jgjpaystock.com</a></li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> {t['country']}</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; <span data-year>2026</span> BizCoRa. {t['rights']}</p>
        <div class="links">
          <a href="faq">{t['faq']}</a>
          <a href="contact">{t['contact_link']}</a>
          <a href="about">{t['about']}</a>
        </div>
      </div>
    </div>
  </footer>

  <button class="to-top" aria-label="Revenir en haut de la page">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
  </button>

  <script src="/assets/js/site.js"></script>"""


# ─── W-BIL01: Download pages ────────────────────────────────────────────────────

def download_page(lang):
    t = {
        "fr": {
            "title": "Télécharger BizCoRa - Windows, macOS, Linux & Web",
            "desc": "Téléchargez BizCoRa sur Windows, macOS ou Linux. Ou accédez directement à la web app sans installation.",
            "h1": "Téléchargez <span class=\"grad\">BizCoRa</span>",
            "sub": "Disponible sur toutes les plateformes. Choisissez votre système d'exploitation ou accédez directement à la version web.",
            "win": "Télécharger pour Windows", "win_sub": "Windows 10 / 11 (.exe)",
            "mac": "Télécharger pour macOS", "mac_sub": "macOS 12+ (.dmg)",
            "linux": "Télécharger pour Linux", "linux_sub": "Ubuntu, Debian, Fedora (.AppImage)",
            "web": "Ouvrir la Web App", "web_sub": "Aucune installation requise",
            "web_desc": "Accédez à BizCoRa depuis n'importe quel navigateur : Chrome, Firefox, Safari, Edge. Toutes les fonctionnalités disponibles.",
            "mobile_title": "Application mobile", "mobile_soon": "Bientôt disponible",
            "mobile_sub": "iOS et Android - en cours de développement",
            "cta_title": "Pas encore de compte ?",
            "cta_sub": "Essai gratuit 14 jours, aucune carte bancaire requise.",
            "cta_btn": "Créer mon compte gratuitement",
            "detected": "Recommandé pour vous",
        },
        "en": {
            "title": "Download BizCoRa - Windows, macOS, Linux & Web",
            "desc": "Download BizCoRa on Windows, macOS or Linux. Or access the web app directly with no installation.",
            "h1": "Download <span class=\"grad\">BizCoRa</span>",
            "sub": "Available on all platforms. Choose your operating system or access the web version directly.",
            "win": "Download for Windows", "win_sub": "Windows 10 / 11 (.exe)",
            "mac": "Download for macOS", "mac_sub": "macOS 12+ (.dmg)",
            "linux": "Download for Linux", "linux_sub": "Ubuntu, Debian, Fedora (.AppImage)",
            "web": "Open Web App", "web_sub": "No installation required",
            "web_desc": "Access BizCoRa from any browser: Chrome, Firefox, Safari, Edge. All features available.",
            "mobile_title": "Mobile app", "mobile_soon": "Coming soon",
            "mobile_sub": "iOS and Android - under development",
            "cta_title": "No account yet?",
            "cta_sub": "14-day free trial, no credit card required.",
            "cta_btn": "Create my free account",
            "detected": "Recommended for you",
        },
        "de": {
            "title": "BizCoRa herunterladen - Windows, macOS, Linux & Web",
            "desc": "Laden Sie BizCoRa für Windows, macOS oder Linux herunter. Oder nutzen Sie die Web-App ohne Installation.",
            "h1": "BizCoRa <span class=\"grad\">herunterladen</span>",
            "sub": "Verfügbar auf allen Plattformen. Wählen Sie Ihr Betriebssystem oder nutzen Sie direkt die Webversion.",
            "win": "Für Windows herunterladen", "win_sub": "Windows 10 / 11 (.exe)",
            "mac": "Für macOS herunterladen", "mac_sub": "macOS 12+ (.dmg)",
            "linux": "Für Linux herunterladen", "linux_sub": "Ubuntu, Debian, Fedora (.AppImage)",
            "web": "Web-App öffnen", "web_sub": "Keine Installation erforderlich",
            "web_desc": "Greifen Sie von jedem Browser auf BizCoRa zu: Chrome, Firefox, Safari, Edge. Alle Funktionen verfügbar.",
            "mobile_title": "Mobile App", "mobile_soon": "Demnächst verfügbar",
            "mobile_sub": "iOS und Android - in Entwicklung",
            "cta_title": "Noch kein Konto?",
            "cta_sub": "14 Tage kostenlos testen, keine Kreditkarte erforderlich.",
            "cta_btn": "Kostenloses Konto erstellen",
            "detected": "Empfohlen für Sie",
        },
    }[lang]
    canonical = f"https://www.jgjpaystock.com/{lang}/download"
    return f"""{head(lang, t['title'], t['desc'], canonical,
        'https://www.jgjpaystock.com/fr/download',
        'https://www.jgjpaystock.com/en/download',
        'https://www.jgjpaystock.com/de/download')}
<body>
{header_nav(lang, 'download')}

  <main>
    <section class="hero" style="padding-bottom:3rem">
      <div class="container" style="text-align:center;max-width:720px;margin:0 auto">
        <h1 style="font-size:clamp(2rem,5vw,3rem);margin-bottom:1rem">{t['h1']}</h1>
        <p class="hero-sub" style="margin-bottom:2.5rem">{t['sub']}</p>

        <!-- OS Download grid -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:2rem">
          <a href="https://github.com/jguimfack8080/BizCora-releases/releases/latest/download/BizCora-Setup.exe"
             class="btn btn--ghost btn--lg" data-os="windows" style="flex-direction:column;padding:1.5rem;gap:.5rem;height:auto">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><path d="M3 5.5L11.5 4v7.5H3zm0 13L11.5 20v-7.5H3zM12.5 4L21 3v8.5h-8.5zm0 16L21 21v-8.5h-8.5z"/></svg>
            <span style="font-weight:700">{t['win']}</span>
            <span style="font-size:.8rem;opacity:.7">{t['win_sub']}</span>
          </a>
          <a href="https://github.com/jguimfack8080/BizCora-releases/releases/latest/download/BizCora.dmg"
             class="btn btn--ghost btn--lg" data-os="mac" style="flex-direction:column;padding:1.5rem;gap:.5rem;height:auto">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98l-.09.06c-.22.15-2.19 1.28-2.17 3.81.03 3.02 2.65 4.03 2.68 4.04l-.06.27zM13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>
            <span style="font-weight:700">{t['mac']}</span>
            <span style="font-size:.8rem;opacity:.7">{t['mac_sub']}</span>
          </a>
          <a href="https://github.com/jguimfack8080/BizCora-releases/releases/latest/download/BizCora.AppImage"
             class="btn btn--ghost btn--lg" data-os="linux" style="flex-direction:column;padding:1.5rem;gap:.5rem;height:auto">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/></svg>
            <span style="font-weight:700">{t['linux']}</span>
            <span style="font-size:.8rem;opacity:.7">{t['linux_sub']}</span>
          </a>
          <a href="https://app.jgjpaystock.com" target="_blank" rel="noopener"
             class="btn btn--primary btn--lg" data-os="web" style="flex-direction:column;padding:1.5rem;gap:.5rem;height:auto">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            <span style="font-weight:700">{t['web']}</span>
            <span style="font-size:.8rem;opacity:.9">{t['web_sub']}</span>
          </a>
        </div>

        <!-- Web app note -->
        <p style="color:var(--neutral-500);font-size:.95rem;margin-bottom:2.5rem">{t['web_desc']}</p>

        <!-- Mobile coming soon -->
        <div style="background:var(--neutral-50);border:1px solid var(--neutral-100);border-radius:12px;padding:1.5rem;margin-bottom:2.5rem;text-align:center">
          <p style="font-weight:600;margin:0 0 .25rem">{t['mobile_title']}</p>
          <p style="color:var(--neutral-500);margin:0;font-size:.9rem">{t['mobile_soon']} - {t['mobile_sub']}</p>
        </div>

        <!-- CTA register -->
        <div style="background:linear-gradient(135deg,#4361ee15,#6366f115);border:1px solid #4361ee30;border-radius:16px;padding:2rem">
          <p style="font-size:1.2rem;font-weight:700;margin:0 0 .5rem">{t['cta_title']}</p>
          <p style="color:var(--neutral-500);margin:0 0 1.25rem">{t['cta_sub']}</p>
          <a href="register" class="btn btn--primary btn--lg">{t['cta_btn']}</a>
        </div>
      </div>
    </section>
  </main>

  <script>
    // OS auto-detection - highlight the right download button
    (function() {{
      const ua = navigator.userAgent;
      let detected = 'web';
      if (/Windows/.test(ua)) detected = 'windows';
      else if (/Macintosh|MacIntel/.test(ua)) detected = 'mac';
      else if (/Linux/.test(ua)) detected = 'linux';
      const btn = document.querySelector('[data-os="' + detected + '"]');
      if (btn && detected !== 'web') {{
        btn.classList.remove('btn--ghost');
        btn.classList.add('btn--primary');
        const badge = document.createElement('span');
        badge.textContent = '{t['detected']}';
        badge.style.cssText = 'font-size:.7rem;background:#4361ee;color:#fff;padding:2px 8px;border-radius:99px;display:block;margin-top:.25rem';
        btn.appendChild(badge);
      }}
    }})();
  </script>

{footer(lang)}
</body>
</html>"""


# ─── W-BIL02: Register pages ────────────────────────────────────────────────────

def register_page(lang):
    t = {
        "fr": {
            "title": "Inscription - Essai gratuit 14 jours - BizCoRa",
            "desc": "Créez votre compte BizCoRa gratuitement. Essai 14 jours sans carte bancaire. Gestion de stock, caisse et facturation.",
            "h1": "Commencez votre essai <span class=\"grad\">gratuit</span>",
            "sub": "14 jours gratuits, sans carte bancaire, sans engagement.",
            "step1": "Informations personnelles", "step2": "Votre entreprise", "step3": "Votre compte",
            "first": "Prénom", "last": "Nom", "email": "Email professionnel", "phone": "Téléphone (optionnel)",
            "company": "Nom de l'entreprise", "country": "Pays", "address": "Adresse (optionnel)",
            "taxid": "Numéro d'identification fiscale (optionnel)",
            "industry": "Secteur d'activité",
            "employees": "Nombre d'employés",
            "password": "Mot de passe", "password_confirm": "Confirmer le mot de passe",
            "terms": "J'accepte les <a href='../fr/faq' target='_blank'>Conditions d'utilisation</a> et la <a href='mailto:contact@jgjpaystock.com' target='_blank'>Politique de confidentialité</a>",
            "submit": "Créer mon compte",
            "next": "Suivant", "back": "Retour",
            "pw_weak": "Très faible", "pw_fair": "Faible", "pw_good": "Bon", "pw_strong": "Fort",
            "success_title": "Vérifiez votre email !",
            "success_sub": "Un email de vérification a été envoyé à",
            "success_info": "Cliquez sur le lien dans l'email pour activer votre compte. Le lien expire dans 24 heures.",
            "resend": "Renvoyer l'email",
            "resend_wait": "Renvoyer dans",
            "change_email": "Modifier mon email",
            "err_required": "Ce champ est requis",
            "err_email": "Email invalide",
            "err_pwmatch": "Les mots de passe ne correspondent pas",
            "err_terms": "Vous devez accepter les conditions",
            "err_pwlen": "Minimum 8 caractères",
            "select_country": "Sélectionner un pays",
            "select_industry": "Sélectionner un secteur",
            "select_employees": "Sélectionner",
            "industries": ["Retail / Commerce", "Restauration", "Pharmacie", "Électronique", "Mode / Textile", "Alimentation", "Services", "Autre"],
            "emp_options": ["1-5", "6-20", "21-50", "51-200", "200+"],
            "progress": "Étape",
            "of": "sur",
        },
        "en": {
            "title": "Sign Up - 14-Day Free Trial - BizCoRa",
            "desc": "Create your BizCoRa account for free. 14-day trial, no credit card required. Stock management, POS and invoicing.",
            "h1": "Start your <span class=\"grad\">free trial</span>",
            "sub": "14 days free, no credit card, no commitment.",
            "step1": "Personal information", "step2": "Your company", "step3": "Your account",
            "first": "First name", "last": "Last name", "email": "Professional email", "phone": "Phone (optional)",
            "company": "Company name", "country": "Country", "address": "Address (optional)",
            "taxid": "Tax identification number (optional)",
            "industry": "Industry",
            "employees": "Number of employees",
            "password": "Password", "password_confirm": "Confirm password",
            "terms": "I accept the <a href='../en/faq' target='_blank'>Terms of service</a> and the <a href='mailto:contact@jgjpaystock.com' target='_blank'>Privacy policy</a>",
            "submit": "Create my account",
            "next": "Next", "back": "Back",
            "pw_weak": "Very weak", "pw_fair": "Weak", "pw_good": "Good", "pw_strong": "Strong",
            "success_title": "Check your email!",
            "success_sub": "A verification email has been sent to",
            "success_info": "Click the link in the email to activate your account. The link expires in 24 hours.",
            "resend": "Resend email",
            "resend_wait": "Resend in",
            "change_email": "Change my email",
            "err_required": "This field is required",
            "err_email": "Invalid email",
            "err_pwmatch": "Passwords do not match",
            "err_terms": "You must accept the terms",
            "err_pwlen": "Minimum 8 characters",
            "select_country": "Select a country",
            "select_industry": "Select an industry",
            "select_employees": "Select",
            "industries": ["Retail", "Food & Restaurant", "Pharmacy", "Electronics", "Fashion / Textile", "Food & Grocery", "Services", "Other"],
            "emp_options": ["1-5", "6-20", "21-50", "51-200", "200+"],
            "progress": "Step",
            "of": "of",
        },
        "de": {
            "title": "Registrieren - 14 Tage kostenlos - BizCoRa",
            "desc": "Erstellen Sie Ihr BizCoRa-Konto kostenlos. 14 Tage testen, keine Kreditkarte erforderlich. Lagerverwaltung, Kasse und Rechnungsstellung.",
            "h1": "Starten Sie Ihren <span class=\"grad\">kostenlosen Test</span>",
            "sub": "14 Tage kostenlos, keine Kreditkarte, keine Bindung.",
            "step1": "Persönliche Daten", "step2": "Ihr Unternehmen", "step3": "Ihr Konto",
            "first": "Vorname", "last": "Nachname", "email": "Geschäftliche E-Mail", "phone": "Telefon (optional)",
            "company": "Firmenname", "country": "Land", "address": "Adresse (optional)",
            "taxid": "Steueridentifikationsnummer (optional)",
            "industry": "Branche",
            "employees": "Anzahl Mitarbeiter",
            "password": "Passwort", "password_confirm": "Passwort bestätigen",
            "terms": "Ich akzeptiere die <a href='../de/faq' target='_blank'>Nutzungsbedingungen</a> und die <a href='mailto:contact@jgjpaystock.com' target='_blank'>Datenschutzrichtlinie</a>",
            "submit": "Konto erstellen",
            "next": "Weiter", "back": "Zurück",
            "pw_weak": "Sehr schwach", "pw_fair": "Schwach", "pw_good": "Gut", "pw_strong": "Stark",
            "success_title": "E-Mail überprüfen!",
            "success_sub": "Eine Bestätigungs-E-Mail wurde gesendet an",
            "success_info": "Klicken Sie auf den Link in der E-Mail, um Ihr Konto zu aktivieren. Der Link läuft in 24 Stunden ab.",
            "resend": "E-Mail erneut senden",
            "resend_wait": "Erneut senden in",
            "change_email": "E-Mail ändern",
            "err_required": "Dieses Feld ist erforderlich",
            "err_email": "Ungültige E-Mail",
            "err_pwmatch": "Passwörter stimmen nicht überein",
            "err_terms": "Sie müssen die Bedingungen akzeptieren",
            "err_pwlen": "Mindestens 8 Zeichen",
            "select_country": "Land auswählen",
            "select_industry": "Branche auswählen",
            "select_employees": "Auswählen",
            "industries": ["Einzelhandel", "Gastronomie", "Apotheke", "Elektronik", "Mode / Textil", "Lebensmittel", "Dienstleistungen", "Sonstiges"],
            "emp_options": ["1-5", "6-20", "21-50", "51-200", "200+"],
            "progress": "Schritt",
            "of": "von",
        },
    }[lang]

    industry_options = "\n".join(f'            <option value="{v}">{v}</option>' for v in t["industries"])
    emp_options = "\n".join(f'            <option value="{v}">{v}</option>' for v in t["emp_options"])
    canonical = f"https://www.jgjpaystock.com/{lang}/register"

    return f"""{head(lang, t['title'], t['desc'], canonical,
        'https://www.jgjpaystock.com/fr/register',
        'https://www.jgjpaystock.com/en/register',
        'https://www.jgjpaystock.com/de/register')}
<body>
{header_nav(lang, 'register')}

  <main>
    <section style="padding:3rem 0 4rem">
      <div class="container" style="max-width:600px;margin:0 auto">
        <h1 style="text-align:center;font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:.5rem">{t['h1']}</h1>
        <p style="text-align:center;color:var(--neutral-500);margin-bottom:2rem">{t['sub']}</p>

        <!-- Progress bar -->
        <div id="progress-bar" style="display:flex;gap:.5rem;margin-bottom:2rem;justify-content:center">
          <span id="step-indicator" style="font-size:.85rem;color:var(--neutral-500)">{t['progress']} <b id="step-num">1</b> {t['of']} 3</span>
          <div style="flex:1;height:4px;background:var(--neutral-100);border-radius:99px;overflow:hidden;align-self:center">
            <div id="progress-fill" style="height:100%;background:#4361ee;border-radius:99px;transition:width .3s;width:33%"></div>
          </div>
        </div>

        <!-- FORM -->
        <form id="reg-form" novalidate>
          <!-- Honeypot -->
          <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"
            style="position:absolute;left:-9999px;opacity:0;height:0;width:0" />

          <!-- Step 1 -->
          <div id="step-1" class="step-panel" style="display:block">
            <h2 style="font-size:1.1rem;margin-bottom:1.25rem">{t['step1']}</h2>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
              <div>
                <label class="form-label" for="first_name">{t['first']} *</label>
                <input class="form-input" type="text" id="first_name" name="first_name" required minlength="2" autocomplete="given-name" />
                <span class="form-error" data-for="first_name"></span>
              </div>
              <div>
                <label class="form-label" for="last_name">{t['last']} *</label>
                <input class="form-input" type="text" id="last_name" name="last_name" required minlength="2" autocomplete="family-name" />
                <span class="form-error" data-for="last_name"></span>
              </div>
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="email">{t['email']} *</label>
              <input class="form-input" type="email" id="email" name="email" required autocomplete="email" />
              <span class="form-error" data-for="email"></span>
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="phone">{t['phone']}</label>
              <input class="form-input" type="tel" id="phone" name="phone" autocomplete="tel" />
            </div>
          </div>

          <!-- Step 2 -->
          <div id="step-2" class="step-panel" style="display:none">
            <h2 style="font-size:1.1rem;margin-bottom:1.25rem">{t['step2']}</h2>
            <div>
              <label class="form-label" for="company_name">{t['company']} *</label>
              <input class="form-input" type="text" id="company_name" name="company_name" required minlength="2" autocomplete="organization" />
              <span class="form-error" data-for="company_name"></span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
              <div>
                <label class="form-label" for="country">{t['country']} *</label>
                <select class="form-input" id="country" name="country" required>
                  <option value="">{t['select_country']}</option>
                  <option value="France">France</option>
                  <option value="Deutschland">Deutschland</option>
                  <option value="Belgique">Belgique / België</option>
                  <option value="Suisse">Suisse / Schweiz</option>
                  <option value="Luxembourg">Luxembourg</option>
                  <option value="Canada">Canada</option>
                  <option value="Maroc">Maroc</option>
                  <option value="Senegal">Sénégal</option>
                  <option value="Cote d Ivoire">Côte d'Ivoire</option>
                  <option value="Cameroun">Cameroun</option>
                  <option value="Other">Autre / Other</option>
                </select>
                <span class="form-error" data-for="country"></span>
              </div>
              <div>
                <label class="form-label" for="employee_count">{t['employees']} *</label>
                <select class="form-input" id="employee_count" name="employee_count" required>
                  <option value="">{t['select_employees']}</option>
{emp_options}
                </select>
                <span class="form-error" data-for="employee_count"></span>
              </div>
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="industry">{t['industry']}</label>
              <select class="form-input" id="industry" name="industry">
                <option value="">{t['select_industry']}</option>
{industry_options}
              </select>
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="address">{t['address']}</label>
              <input class="form-input" type="text" id="address" name="address" autocomplete="street-address" />
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="tax_id">{t['taxid']}</label>
              <input class="form-input" type="text" id="tax_id" name="tax_id" />
            </div>
          </div>

          <!-- Step 3 -->
          <div id="step-3" class="step-panel" style="display:none">
            <h2 style="font-size:1.1rem;margin-bottom:1.25rem">{t['step3']}</h2>
            <div>
              <label class="form-label" for="password">{t['password']} *</label>
              <input class="form-input" type="password" id="password" name="password" required minlength="8" autocomplete="new-password" />
              <!-- Strength indicator -->
              <div id="pw-bar" style="height:4px;border-radius:99px;background:var(--neutral-100);margin:.5rem 0;overflow:hidden">
                <div id="pw-fill" style="height:100%;width:0%;transition:width .2s,background .2s;border-radius:99px"></div>
              </div>
              <span id="pw-label" style="font-size:.78rem;color:var(--neutral-500)"></span>
              <span class="form-error" data-for="password"></span>
            </div>
            <div style="margin-top:1rem">
              <label class="form-label" for="password_confirm">{t['password_confirm']} *</label>
              <input class="form-input" type="password" id="password_confirm" name="password_confirm" required autocomplete="new-password" />
              <span class="form-error" data-for="password_confirm"></span>
            </div>
            <div style="margin-top:1.25rem;display:flex;gap:.75rem;align-items:flex-start">
              <input type="checkbox" id="accepted_terms" name="accepted_terms" style="margin-top:3px;flex-shrink:0" />
              <label for="accepted_terms" style="font-size:.9rem;color:var(--neutral-600);cursor:pointer">{t['terms']}</label>
            </div>
            <span class="form-error" data-for="accepted_terms"></span>

            <!-- Global error -->
            <div id="form-global-error" style="display:none;background:#fee2e2;color:#dc2626;border-radius:8px;padding:.75rem 1rem;margin-top:1rem;font-size:.9rem"></div>
          </div>

          <!-- Navigation buttons -->
          <div style="display:flex;gap:1rem;margin-top:1.75rem;justify-content:space-between">
            <button type="button" id="btn-back" class="btn btn--ghost btn--md" style="display:none">{t['back']}</button>
            <button type="button" id="btn-next" class="btn btn--primary btn--md" style="margin-left:auto">{t['next']}</button>
            <button type="submit" id="btn-submit" class="btn btn--primary btn--md" style="display:none;margin-left:auto">
              <span id="submit-label">{t['submit']}</span>
              <svg id="submit-spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="display:none;animation:spin 1s linear infinite"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            </button>
          </div>
        </form>

        <!-- Success screen -->
        <div id="success-screen" style="display:none;text-align:center;padding:2rem 0">
          <div style="width:72px;height:72px;background:#dcfce7;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['success_title']}</h2>
          <p id="success-email-line" style="color:var(--neutral-500);margin-bottom:1rem">{t['success_sub']} <strong id="success-email"></strong>.</p>
          <p style="color:var(--neutral-500);font-size:.9rem;margin-bottom:2rem">{t['success_info']}</p>
          <button id="btn-resend" class="btn btn--ghost btn--md" onclick="resendEmail()">{t['resend']}</button>
          <p style="margin-top:1rem"><a href="javascript:void(0)" onclick="resetForm()" style="color:#4361ee;font-size:.9rem">{t['change_email']}</a></p>
        </div>
      </div>
    </section>
  </main>

  <style>
    /* Styles de formulaire mutualises dans assets/css/components.css (systeme unifie). */
    @keyframes spin {{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
  </style>

  <script>
    const BILLING_API = 'https://api.jgjpaystock.com';
    const LANG = '{lang}';
    const MSG = {{
      required: '{t['err_required']}',
      email: '{t['err_email']}',
      pwmatch: '{t['err_pwmatch']}',
      terms: '{t['err_terms']}',
      pwlen: '{t['err_pwlen']}',
      pw: ['{t['pw_weak']}','{t['pw_fair']}','{t['pw_good']}','{t['pw_strong']}'],
      resend_wait: '{t['resend_wait']}',
    }};

    let currentStep = 1;
    let registeredEmail = '';
    let resendTimer = null;

    // ── Password strength ──────────────────────────────────────────────────────
    document.getElementById('password').addEventListener('input', function() {{
      const v = this.value;
      let score = 0;
      if (v.length >= 8) score++;
      if (v.length >= 12) score++;
      if (/[A-Z]/.test(v)) score++;
      if (/[a-z]/.test(v)) score++;
      if (/[0-9]/.test(v)) score++;
      if (/[^A-Za-z0-9]/.test(v)) score++;
      const s = Math.min(Math.floor(score * 4 / 6), 3);
      const colors = ['#dc2626','#f59e0b','#3b82f6','#16a34a'];
      const widths = ['25%','50%','75%','100%'];
      const fill = document.getElementById('pw-fill');
      fill.style.width = v ? widths[s] : '0%';
      fill.style.background = colors[s];
      document.getElementById('pw-label').textContent = v ? MSG.pw[s] : '';
    }});

    // ── Step navigation ────────────────────────────────────────────────────────
    function showStep(n) {{
      [1,2,3].forEach(i => {{
        document.getElementById('step-'+i).style.display = i === n ? 'block' : 'none';
      }});
      document.getElementById('step-num').textContent = n;
      document.getElementById('progress-fill').style.width = (n * 33.3) + '%';
      document.getElementById('btn-back').style.display = n > 1 ? 'inline-flex' : 'none';
      document.getElementById('btn-next').style.display = n < 3 ? 'inline-flex' : 'none';
      document.getElementById('btn-submit').style.display = n === 3 ? 'inline-flex' : 'none';
      currentStep = n;
    }}

    document.getElementById('btn-next').addEventListener('click', () => {{
      if (validateStep(currentStep)) showStep(currentStep + 1);
    }});
    document.getElementById('btn-back').addEventListener('click', () => showStep(currentStep - 1));

    // ── Validation ─────────────────────────────────────────────────────────────
    function setError(name, msg) {{
      const el = document.querySelector('[data-for="'+name+'"]');
      const inp = document.getElementById(name) || document.querySelector('[name="'+name+'"]');
      if (el) el.textContent = msg;
      if (inp) inp.classList.toggle('is-invalid', !!msg);
    }}
    function clearErrors() {{
      document.querySelectorAll('.form-error').forEach(e => e.textContent = '');
      document.querySelectorAll('.is-invalid').forEach(e => e.classList.remove('is-invalid'));
    }}

    function validateStep(step) {{
      clearErrors();
      let ok = true;
      if (step === 1) {{
        const fn = document.getElementById('first_name').value.trim();
        const ln = document.getElementById('last_name').value.trim();
        const em = document.getElementById('email').value.trim();
        if (fn.length < 2) {{ setError('first_name', MSG.required); ok = false; }}
        if (ln.length < 2) {{ setError('last_name', MSG.required); ok = false; }}
        if (!em || !/^[^@]+@[^@]+\.[^@]+$/.test(em)) {{ setError('email', MSG.email); ok = false; }}
      }} else if (step === 2) {{
        if (!document.getElementById('company_name').value.trim()) {{ setError('company_name', MSG.required); ok = false; }}
        if (!document.getElementById('country').value) {{ setError('country', MSG.required); ok = false; }}
        if (!document.getElementById('employee_count').value) {{ setError('employee_count', MSG.required); ok = false; }}
      }} else if (step === 3) {{
        const pw = document.getElementById('password').value;
        const pc = document.getElementById('password_confirm').value;
        const terms = document.getElementById('accepted_terms').checked;
        if (pw.length < 8) {{ setError('password', MSG.pwlen); ok = false; }}
        if (pw !== pc) {{ setError('password_confirm', MSG.pwmatch); ok = false; }}
        if (!terms) {{ setError('accepted_terms', MSG.terms); ok = false; }}
      }}
      return ok;
    }}

    // ── Submit ─────────────────────────────────────────────────────────────────
    document.getElementById('reg-form').addEventListener('submit', async (e) => {{
      e.preventDefault();
      if (!validateStep(3)) return;
      // Honeypot check
      if (document.querySelector('[name="website"]').value) return;

      const btn = document.getElementById('btn-submit');
      const lbl = document.getElementById('submit-label');
      const spinner = document.getElementById('submit-spinner');
      btn.disabled = true; lbl.style.display = 'none'; spinner.style.display = 'inline';

      const data = {{
        first_name: document.getElementById('first_name').value.trim(),
        last_name: document.getElementById('last_name').value.trim(),
        email: document.getElementById('email').value.trim().toLowerCase(),
        phone: document.getElementById('phone').value.trim() || null,
        company_name: document.getElementById('company_name').value.trim(),
        country: document.getElementById('country').value,
        address: document.getElementById('address').value.trim() || null,
        tax_id: document.getElementById('tax_id').value.trim() || null,
        industry: document.getElementById('industry').value || null,
        employee_count: document.getElementById('employee_count').value,
        password: document.getElementById('password').value,
        password_confirm: document.getElementById('password_confirm').value,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Paris',
        accepted_terms: true,
        locale: LANG,
      }};

      try {{
        const resp = await fetch(BILLING_API + '/billing/register', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify(data),
        }});
        const json = await resp.json();
        if (resp.ok) {{
          registeredEmail = data.email;
          document.getElementById('success-email').textContent = registeredEmail;
          document.getElementById('reg-form').style.display = 'none';
          document.getElementById('progress-bar').style.display = 'none';
          document.getElementById('success-screen').style.display = 'block';
          startResendTimer();
        }} else {{
          const errBox = document.getElementById('form-global-error');
          errBox.textContent = json.detail?.message || json.detail || 'Une erreur est survenue.';
          errBox.style.display = 'block';
        }}
      }} catch (err) {{
        const errBox = document.getElementById('form-global-error');
        errBox.textContent = 'Service momentanément indisponible. Réessayez dans quelques instants.';
        errBox.style.display = 'block';
      }} finally {{
        btn.disabled = false; lbl.style.display = 'inline'; spinner.style.display = 'none';
      }}
    }});

    // ── Resend ─────────────────────────────────────────────────────────────────
    function startResendTimer() {{
      const btn = document.getElementById('btn-resend');
      let sec = 60;
      btn.disabled = true;
      resendTimer = setInterval(() => {{
        sec--;
        btn.textContent = MSG.resend_wait + ' ' + sec + 's';
        if (sec <= 0) {{ clearInterval(resendTimer); btn.disabled = false; btn.textContent = '{t['resend']}'; }}
      }}, 1000);
    }}

    async function resendEmail() {{
      const btn = document.getElementById('btn-resend');
      btn.disabled = true;
      try {{
        await fetch(BILLING_API + '/billing/resend-verification', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{email: registeredEmail}}),
        }});
      }} catch(e) {{}}
      startResendTimer();
    }}

    function resetForm() {{
      document.getElementById('reg-form').style.display = 'block';
      document.getElementById('progress-bar').style.display = 'flex';
      document.getElementById('success-screen').style.display = 'none';
      showStep(1);
    }}

    showStep(1);
  </script>

{footer(lang)}
</body>
</html>"""


# ─── W-BIL03: Verify-email pages ───────────────────────────────────────────────

def verify_page(lang):
    t = {
        "fr": {
            "title": "Vérification de votre email - BizCoRa",
            "desc": "Vérification de votre adresse email pour activer votre compte BizCoRa.",
            "h1": "Vérification de votre email",
            "loading": "Vérification en cours...",
            "success_title": "Compte activé !",
            "success_body": "Votre compte BizCoRa est prêt. Téléchargez l'application ou accédez à la version web.",
            "success_creds": "Vos identifiants ont été envoyés par email.",
            "expired_title": "Lien expiré",
            "expired_body": "Ce lien de vérification a expiré (valable 24h). Saisissez votre email pour recevoir un nouveau lien.",
            "expired_email": "Votre email",
            "expired_btn": "Recevoir un nouveau lien",
            "invalid_title": "Lien invalide",
            "invalid_body": "Ce lien de vérification est invalide. Utilisez le lien dans votre dernier email.",
            "invalid_btn": "Contacter le support",
            "already_title": "Email déjà vérifié",
            "already_body": "Votre compte est déjà actif. Connectez-vous à l'application.",
            "notoken_title": "Lien incomplet",
            "notoken_body": "Le lien de vérification est incomplet. Assurez-vous de cliquer sur le bouton dans l'email.",
            "download_title": "Télécharger l'application",
            "open_web": "Ouvrir la Web App",
            "open_app": "Ouvrir l'application",
        },
        "en": {
            "title": "Email Verification - BizCoRa",
            "desc": "Email address verification to activate your BizCoRa account.",
            "h1": "Email verification",
            "loading": "Verifying...",
            "success_title": "Account activated!",
            "success_body": "Your BizCoRa account is ready. Download the app or access the web version.",
            "success_creds": "Your credentials have been sent by email.",
            "expired_title": "Link expired",
            "expired_body": "This verification link has expired (valid 24h). Enter your email to receive a new link.",
            "expired_email": "Your email",
            "expired_btn": "Receive a new link",
            "invalid_title": "Invalid link",
            "invalid_body": "This verification link is invalid. Use the link in your latest email.",
            "invalid_btn": "Contact support",
            "already_title": "Email already verified",
            "already_body": "Your account is already active. Log in to the app.",
            "notoken_title": "Incomplete link",
            "notoken_body": "The verification link is incomplete. Make sure to click the button in the email.",
            "download_title": "Download the app",
            "open_web": "Open Web App",
            "open_app": "Open the app",
        },
        "de": {
            "title": "E-Mail-Verifizierung - BizCoRa",
            "desc": "E-Mail-Adressverifizierung zur Aktivierung Ihres BizCoRa-Kontos.",
            "h1": "E-Mail-Verifizierung",
            "loading": "Wird überprüft...",
            "success_title": "Konto aktiviert!",
            "success_body": "Ihr BizCoRa-Konto ist bereit. Laden Sie die App herunter oder nutzen Sie die Webversion.",
            "success_creds": "Ihre Zugangsdaten wurden per E-Mail gesendet.",
            "expired_title": "Link abgelaufen",
            "expired_body": "Dieser Verifizierungslink ist abgelaufen (24h gültig). Geben Sie Ihre E-Mail ein, um einen neuen Link zu erhalten.",
            "expired_email": "Ihre E-Mail",
            "expired_btn": "Neuen Link erhalten",
            "invalid_title": "Ungültiger Link",
            "invalid_body": "Dieser Verifizierungslink ist ungültig. Verwenden Sie den Link in Ihrer letzten E-Mail.",
            "invalid_btn": "Support kontaktieren",
            "already_title": "E-Mail bereits verifiziert",
            "already_body": "Ihr Konto ist bereits aktiv. Melden Sie sich bei der App an.",
            "notoken_title": "Unvollständiger Link",
            "notoken_body": "Der Verifizierungslink ist unvollständig. Klicken Sie auf die Schaltfläche in der E-Mail.",
            "download_title": "App herunterladen",
            "open_web": "Web-App öffnen",
            "open_app": "App öffnen",
        },
    }[lang]
    canonical = f"https://www.jgjpaystock.com/{lang}/verify-email"

    return f"""{head(lang, t['title'], t['desc'], canonical,
        'https://www.jgjpaystock.com/fr/verify-email',
        'https://www.jgjpaystock.com/en/verify-email',
        'https://www.jgjpaystock.com/de/verify-email')}
<body>
{header_nav(lang, '')}

  <main>
    <section style="padding:4rem 0;min-height:60vh;display:flex;align-items:center">
      <div class="container" style="max-width:560px;margin:0 auto;text-align:center">
        <h1 style="font-size:clamp(1.4rem,4vw,2rem);margin-bottom:2rem">{t['h1']}</h1>

        <!-- Loading state -->
        <div id="state-loading">
          <div style="width:56px;height:56px;border:3px solid #4361ee20;border-top-color:#4361ee;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 1.5rem"></div>
          <p style="color:var(--neutral-500)">{t['loading']}</p>
        </div>

        <!-- Success state -->
        <div id="state-success" style="display:none">
          <div style="width:72px;height:72px;background:#dcfce7;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['success_title']}</h2>
          <p style="color:var(--neutral-500);margin-bottom:.5rem">{t['success_body']}</p>
          <p style="color:var(--neutral-400);font-size:.875rem;margin-bottom:2rem">{t['success_creds']}</p>
          <div style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center">
            <a href="https://app.jgjpaystock.com" class="btn btn--primary btn--lg">{t['open_web']}</a>
            <a href="download" class="btn btn--ghost btn--lg">{t['download_title']}</a>
          </div>
        </div>

        <!-- Expired state -->
        <div id="state-expired" style="display:none">
          <div style="width:72px;height:72px;background:#fef3c7;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['expired_title']}</h2>
          <p style="color:var(--neutral-500);margin-bottom:1.5rem">{t['expired_body']}</p>
          <div style="display:flex;gap:.75rem;max-width:400px;margin:0 auto">
            <input class="form-input" type="email" id="resend-email" placeholder="{t['expired_email']}" style="flex:1" />
            <button class="btn btn--primary btn--md" onclick="resendVerification()">{t['expired_btn']}</button>
          </div>
          <div id="resend-msg" style="margin-top:.75rem;font-size:.875rem;color:var(--neutral-500)"></div>
        </div>

        <!-- Invalid state -->
        <div id="state-invalid" style="display:none">
          <div style="width:72px;height:72px;background:#fee2e2;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['invalid_title']}</h2>
          <p style="color:var(--neutral-500);margin-bottom:1.5rem">{t['invalid_body']}</p>
          <a href="mailto:support@jgjpaystock.com" class="btn btn--ghost btn--md">{t['invalid_btn']}</a>
        </div>

        <!-- Already verified state -->
        <div id="state-already" style="display:none">
          <div style="width:72px;height:72px;background:#dbeafe;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['already_title']}</h2>
          <p style="color:var(--neutral-500);margin-bottom:1.5rem">{t['already_body']}</p>
          <a href="https://app.jgjpaystock.com" class="btn btn--primary btn--lg">{t['open_app']}</a>
        </div>

        <!-- No token state -->
        <div id="state-notoken" style="display:none">
          <div style="width:72px;height:72px;background:#fee2e2;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.25rem">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          </div>
          <h2 style="font-size:1.5rem;margin-bottom:.5rem">{t['notoken_title']}</h2>
          <p style="color:var(--neutral-500)">{t['notoken_body']}</p>
        </div>
      </div>
    </section>
  </main>

  <style>
    /* Styles de formulaire mutualises dans assets/css/components.css (systeme unifie). */
    @keyframes spin {{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
  </style>

  <script>
    const BILLING_API = 'https://api.jgjpaystock.com';

    function show(id) {{
      ['loading','success','expired','invalid','already','notoken'].forEach(s => {{
        document.getElementById('state-'+s).style.display = s === id ? 'block' : 'none';
      }});
    }}

    async function verify() {{
      const token = new URLSearchParams(window.location.search).get('token');
      if (!token) {{ show('notoken'); return; }}

      try {{
        const resp = await fetch(BILLING_API + '/billing/verify-email', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{token}}),
        }});
        if (resp.ok) {{ show('success'); return; }}
        const data = await resp.json();
        const code = data?.detail?.code || '';
        if (code === 'TOKEN_EXPIRED') show('expired');
        else if (code === 'ALREADY_VERIFIED') show('already');
        else show('invalid');
      }} catch(e) {{
        show('invalid');
      }}
    }}

    async function resendVerification() {{
      const email = document.getElementById('resend-email').value.trim();
      if (!email) return;
      try {{
        await fetch(BILLING_API + '/billing/resend-verification', {{
          method: 'POST',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{email}}),
        }});
        document.getElementById('resend-msg').textContent = 'Email envoyé si votre adresse est connue.';
      }} catch(e) {{
        document.getElementById('resend-msg').textContent = 'Erreur. Réessayez dans un instant.';
      }}
    }}

    document.addEventListener('DOMContentLoaded', verify);
  </script>

{footer(lang)}
</body>
</html>"""


# ─── W-BIL04: Pricing pages (refonte) ───────────────────────────────────────────

def pricing_page(lang):
    t = {
        "fr": {
            "title": "Tarifs BizCoRa - logiciel de caisse, stock et facturation",
            "desc": "Tarifs de BizCoRa, logiciel tout-en-un de caisse, gestion de stock et facturation. Essai gratuit 14 jours, sans carte bancaire. Plans mensuels ou annuels.",
            "h1": "Des tarifs <span class=\"grad\">simples et transparents</span>",
            "sub": "Essai gratuit 14 jours - Aucune carte bancaire - Annulez quand vous voulez",
            "monthly": "Mensuel", "yearly": "Annuel",
            "save": "Économisez 2 mois !",
            "popular": "POPULAIRE",
            "free_trial": "14 jours gratuits",
            "cta_trial": "Commencer l'essai gratuit",
            "cta_plan": "Choisir ce plan",
            "users": "utilisateurs", "products": "produits",
            "unlimited": "Illimité",
            "support_email": "Support email",
            "support_chat": "Email + Chat",
            "support_dedicated": "Support dédié",
            "compare": "Comparer toutes les fonctionnalités",
            "faq_title": "Questions fréquentes",
            "faqs": [
                ("Puis-je annuler à tout moment ?", "Oui. Vous gardez l'accès jusqu'à la fin de la période payée. Aucun frais de résiliation."),
                ("Quels moyens de paiement acceptez-vous ?", "Cartes bancaires (Visa, Mastercard), Orange Money, MTN Mobile Money, M-Pesa et virement bancaire, via Flutterwave."),
                ("Y a-t-il des frais de mise en place ?", "Non. Aucun frais caché, aucune installation payante."),
                ("Mes données sont-elles sécurisées ?", "Oui. Chiffrement TLS, isolation des données par entreprise, conforme RGPD."),
                ("Puis-je passer d'un plan à l'autre ?", "Oui, à tout moment depuis votre espace client. Le changement est instantané."),
            ],
            "plans": [
                ("Trial", 5, "1 000", "support_email"),
                ("Basic", 3, "1 000", "support_email"),
                ("Professional", 10, "10 000", "support_chat"),
                ("Enterprise", 0, "0", "support_dedicated"),
            ],
        },
        "en": {
            "title": "BizCoRa pricing - POS, inventory and invoicing software",
            "desc": "BizCoRa pricing for the all-in-one POS, inventory and invoicing software. 14-day free trial, no credit card. Simple monthly or yearly plans.",
            "h1": "Simple and <span class=\"grad\">transparent pricing</span>",
            "sub": "14-day free trial - No credit card - Cancel anytime",
            "monthly": "Monthly", "yearly": "Yearly",
            "save": "Save 2 months!",
            "popular": "POPULAR",
            "free_trial": "14 days free",
            "cta_trial": "Start free trial",
            "cta_plan": "Choose this plan",
            "users": "users", "products": "products",
            "unlimited": "Unlimited",
            "support_email": "Email support",
            "support_chat": "Email + Chat",
            "support_dedicated": "Dedicated support",
            "compare": "Compare all features",
            "faq_title": "Frequently asked questions",
            "faqs": [
                ("Can I cancel at any time?", "Yes. You keep access until the end of the paid period. No cancellation fees."),
                ("What payment methods do you accept?", "Bank cards (Visa, Mastercard), Orange Money, MTN Mobile Money, M-Pesa and bank transfer, via Flutterwave."),
                ("Are there any setup fees?", "No. No hidden fees, no paid installation."),
                ("Is my data secure?", "Yes. TLS encryption, data isolation per company, GDPR compliant."),
                ("Can I switch plans?", "Yes, at any time from your account. The change is instant."),
            ],
            "plans": [
                ("Trial", 5, "1,000", "support_email"),
                ("Basic", 3, "1,000", "support_email"),
                ("Professional", 10, "10,000", "support_chat"),
                ("Enterprise", 0, "0", "support_dedicated"),
            ],
        },
        "de": {
            "title": "BizCoRa Preise - Kassensystem und Warenwirtschaft",
            "desc": "Preise von BizCoRa, der All-in-one-Software für Kasse, Warenwirtschaft und Rechnungen. 14 Tage kostenlos, keine Kreditkarte. Monatlich oder jährlich.",
            "h1": "Einfache und <span class=\"grad\">transparente Preise</span>",
            "sub": "14 Tage kostenlos testen - Keine Kreditkarte - Jederzeit kündbar",
            "monthly": "Monatlich", "yearly": "Jährlich",
            "save": "2 Monate sparen!",
            "popular": "BELIEBT",
            "free_trial": "14 Tage kostenlos",
            "cta_trial": "Kostenlos testen",
            "cta_plan": "Diesen Plan wählen",
            "users": "Benutzer", "products": "Produkte",
            "unlimited": "Unbegrenzt",
            "support_email": "E-Mail-Support",
            "support_chat": "E-Mail + Chat",
            "support_dedicated": "Dedizierter Support",
            "compare": "Alle Funktionen vergleichen",
            "faq_title": "Häufig gestellte Fragen",
            "faqs": [
                ("Kann ich jederzeit kündigen?", "Ja. Sie behalten den Zugang bis zum Ende des bezahlten Zeitraums. Keine Kündigungsgebühren."),
                ("Welche Zahlungsmethoden akzeptieren Sie?", "Bankkarten (Visa, Mastercard), Orange Money, MTN Mobile Money, M-Pesa und Banküberweisung, über Flutterwave."),
                ("Gibt es Einrichtungsgebühren?", "Nein. Keine versteckten Gebühren, keine kostenpflichtige Installation."),
                ("Sind meine Daten sicher?", "Ja. TLS-Verschlüsselung, Datenisolierung pro Unternehmen, DSGVO-konform."),
                ("Kann ich den Plan wechseln?", "Ja, jederzeit über Ihr Kundenkonto. Die Änderung ist sofort wirksam."),
            ],
            "plans": [
                ("Trial", 5, "1.000", "support_email"),
                ("Basic", 3, "1.000", "support_email"),
                ("Professional", 10, "10.000", "support_chat"),
                ("Enterprise", 0, "0", "support_dedicated"),
            ],
        },
    }[lang]

    # Libelles dependant de la langue pour le rendu dynamique des prix (JS).
    ccy_label = {"fr": "Devise :", "en": "Currency:", "de": "Waehrung:"}[lang]
    unit_mo = {"fr": "/mois", "en": "/mo", "de": "/Monat"}[lang]
    unit_yr = {"fr": "/an", "en": "/yr", "de": "/Jahr"}[lang]

    # Build plan cards
    plan_cards = ""
    for i, (name, max_users, max_prod, support_key) in enumerate(t["plans"]):
        is_popular = name == "Professional"
        is_trial = i == 0
        is_enterprise = max_users == 0
        popular_badge = f'<span style="position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#4361ee;color:#fff;font-size:.7rem;font-weight:700;padding:3px 12px;border-radius:99px;white-space:nowrap">{t["popular"]}</span>' if is_popular else ""
        border = "border:2px solid #4361ee" if is_popular else "border:1.5px solid var(--neutral-200)"
        bg = "background:#f8f9ff" if is_popular else "background:#fff"
        users_str = t["unlimited"] if is_enterprise else f'{max_users} {t["users"]}'
        products_str = t["unlimited"] if is_enterprise else f'{max_prod} {t["products"]}'
        support_str = t[support_key]
        plan_slug = name.lower().replace(" ", "-")

        # AUCUN prix code en dur : le montant est un placeholder rempli au chargement
        # par /billing/plans (source unique = price book DB). data-plan + js-price/js-unit
        # permettent au script de cibler chaque carte. Pour l'essai, pas de prix.
        price_html_mo = f'<span class="js-price" style="font-size:2.5rem;font-weight:800">&hellip;</span> <span class="js-unit" style="font-size:.9rem;color:var(--neutral-500)">{unit_mo}</span>' if not is_trial else f'<span style="font-size:2.5rem;font-weight:800">{t["free_trial"]}</span>'
        price_html_yr = f'<span class="js-price" style="font-size:2.5rem;font-weight:800">&hellip;</span> <span class="js-unit" style="font-size:.9rem;color:var(--neutral-500)">{unit_yr}</span>' if not is_trial else f'<span style="font-size:2.5rem;font-weight:800">{t["free_trial"]}</span>'

        cta_href = f"register?plan={plan_slug}" if not is_trial else "register"
        cta_label = t["cta_trial"] if is_trial else t["cta_plan"]
        cta_class = "btn--primary" if (is_popular or is_trial) else "btn--ghost"

        plan_cards += f"""
          <div class="price-card" style="position:relative;{border};{bg};border-radius:16px;padding:2rem;display:flex;flex-direction:column">
            {popular_badge}
            <h3 style="font-size:1.1rem;font-weight:700;margin:0 0 1rem">{name}</h3>
            <div class="price-monthly" data-plan="{plan_slug}" data-period="monthly" style="margin-bottom:1rem">{price_html_mo}</div>
            <div class="price-yearly" data-plan="{plan_slug}" data-period="yearly" style="margin-bottom:1rem;display:none">{price_html_yr}</div>
            <ul style="list-style:none;padding:0;margin:0 0 1.5rem;flex:1;display:flex;flex-direction:column;gap:.5rem">
              <li style="display:flex;gap:.5rem;align-items:center;font-size:.9rem"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>{users_str}</li>
              <li style="display:flex;gap:.5rem;align-items:center;font-size:.9rem"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>{products_str}</li>
              <li style="display:flex;gap:.5rem;align-items:center;font-size:.9rem"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>{support_str}</li>
            </ul>
            <a href="{cta_href}" class="btn {cta_class} btn--md" style="text-align:center">{cta_label}</a>
          </div>"""

    # Build FAQ items
    faq_html = ""
    for q, a in t["faqs"]:
        faq_html += f"""
          <details style="border-bottom:1px solid var(--neutral-100);padding:.75rem 0">
            <summary style="font-weight:600;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center">{q}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
            </summary>
            <p style="color:var(--neutral-500);margin:.5rem 0 0;font-size:.95rem">{a}</p>
          </details>"""

    canonical = f"https://www.jgjpaystock.com/{lang}/pricing"
    return f"""{head(lang, t['title'], t['desc'], canonical,
        'https://www.jgjpaystock.com/fr/pricing',
        'https://www.jgjpaystock.com/en/pricing',
        'https://www.jgjpaystock.com/de/pricing')}
<body>
{header_nav(lang, 'pricing')}

  <main>
    <!-- Hero -->
    <section style="padding:3rem 0 1.5rem;text-align:center">
      <div class="container" style="max-width:720px;margin:0 auto">
        <p style="background:#4361ee15;color:#4361ee;font-weight:600;font-size:.875rem;border-radius:99px;display:inline-block;padding:.375rem 1rem;margin-bottom:1rem">{t['sub']}</p>
        <h1 style="font-size:clamp(1.8rem,5vw,3rem);margin-bottom:1.5rem">{t['h1']}</h1>

        <!-- Toggle -->
        <div style="display:inline-flex;background:var(--neutral-100);border-radius:99px;padding:4px;gap:4px;margin-bottom:2.5rem">
          <button id="toggle-monthly" onclick="setInterval('monthly')" class="btn btn--primary btn--sm" style="border-radius:99px">{t['monthly']}</button>
          <button id="toggle-yearly" onclick="setInterval('yearly')" class="btn btn--ghost btn--sm" style="border-radius:99px">
            {t['yearly']} <span style="background:#dc2626;color:#fff;font-size:.65rem;padding:2px 6px;border-radius:99px;margin-left:.25rem">{t['save']}</span>
          </button>
        </div>

        <!-- Selecteur de devise (international) : pilote les prix affiches via /billing/plans -->
        <div style="margin-bottom:2rem">
          <label for="ccy-select" style="font-size:.85rem;color:var(--neutral-500);margin-right:.5rem">{ccy_label}</label>
          <select id="ccy-select" aria-label="{ccy_label}" style="padding:.4rem .9rem;border:1.5px solid var(--neutral-200);border-radius:99px;font-size:.9rem;background:#fff;cursor:pointer">
            <option value="EUR">EUR</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Plans grid -->
    <section style="padding:0 0 3rem">
      <div class="container">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;max-width:960px;margin:0 auto">
{plan_cards}
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section style="padding:3rem 0">
      <div class="container" style="max-width:640px;margin:0 auto">
        <h2 style="text-align:center;margin-bottom:2rem">{t['faq_title']}</h2>
        <div>
{faq_html}
        </div>
      </div>
    </section>
  </main>

  <script>
    function setInterval(mode) {{
      const isYearly = mode === 'yearly';
      document.querySelectorAll('.price-monthly').forEach(e => e.style.display = isYearly ? 'none' : 'block');
      document.querySelectorAll('.price-yearly').forEach(e => e.style.display = isYearly ? 'block' : 'none');
      document.getElementById('toggle-monthly').className = isYearly ? 'btn btn--ghost btn--sm' : 'btn btn--primary btn--sm';
      document.getElementById('toggle-yearly').className = isYearly ? 'btn btn--primary btn--sm' : 'btn btn--ghost btn--sm';
      document.getElementById('toggle-monthly').style.borderRadius = '99px';
      document.getElementById('toggle-yearly').style.borderRadius = '99px';
    }}

    // ── Prix dynamiques : source UNIQUE = price book DB via /billing/plans ──
    // AUCUN prix code en dur dans le site : les montants sont des placeholders charges via /billing/plans
    // remplis ici par l'API. Une modif de prix cote back-office est donc refletee
    // immediatement (sans regeneration), pour toutes les devises. Si l'API est
    // indisponible, le placeholder reste affiche (jamais un faux prix).
    const BILLING_API = (window.__ENV__ && window.__ENV__.BILLING_API) || 'https://api.jgjpaystock.com';
    const LANG = '{lang}';
    const UNIT = {{ monthly: '{unit_mo}', yearly: '{unit_yr}' }};
    let CCY = localStorage.getItem('jgj_ccy') || 'EUR';

    function fmtAmount(n) {{
      try {{ return new Intl.NumberFormat(LANG).format(n); }} catch (e) {{ return String(n); }}
    }}
    function fillPrices(data) {{
      const cur = (data.currency || CCY).toUpperCase();
      const byCode = {{}};
      (data.plans || []).forEach(p => {{ byCode[p.code] = p; }});
      document.querySelectorAll('[data-plan]').forEach(el => {{
        const p = byCode[el.getAttribute('data-plan')];
        const amtEl = el.querySelector('.js-price');
        if (!p || !amtEl) return; // trial / sans prix -> inchange
        const amount = el.getAttribute('data-period') === 'yearly' ? p.price_yearly : p.price_monthly;
        if (amount == null) return;
        amtEl.textContent = fmtAmount(amount);
        const unitEl = el.querySelector('.js-unit');
        if (unitEl) unitEl.textContent = cur + ' ' + UNIT[el.getAttribute('data-period')];
      }});
    }}
    function fillCurrencySelector(data) {{
      const sel = document.getElementById('ccy-select');
      const list = (data.available_currencies || []).map(c => c.code);
      if (!sel || !list.length) return;
      const cur = (data.currency || CCY).toUpperCase();
      sel.innerHTML = '';
      list.forEach(code => {{
        const o = document.createElement('option');
        o.value = code; o.textContent = code;
        if (code === cur) o.selected = true;
        sel.appendChild(o);
      }});
    }}
    async function loadPrices() {{
      try {{
        const r = await fetch(BILLING_API + '/billing/plans?currency=' + encodeURIComponent(CCY), {{ headers: {{ 'Accept-Language': LANG }} }});
        if (!r.ok) return; // fallback = prix EUR bakes
        const data = await r.json();
        fillCurrencySelector(data);
        fillPrices(data);
        CCY = (data.currency || CCY).toUpperCase();
        localStorage.setItem('jgj_ccy', CCY);
      }} catch (e) {{ /* API indisponible -> on garde le fallback */ }}
    }}
    document.addEventListener('DOMContentLoaded', function () {{
      const sel = document.getElementById('ccy-select');
      if (sel) sel.addEventListener('change', function () {{ CCY = this.value; loadPrices(); }});
      loadPrices();
    }});

    // Preselect plan from URL param
    const plan = new URLSearchParams(window.location.search).get('plan');
    if (plan) {{
      const btn = document.querySelector('[href*="register?plan=' + plan + '"]');
      if (btn) btn.scrollIntoView({{behavior:'smooth',block:'center'}});
    }}
  </script>

{footer(lang)}
</body>
</html>"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {os.path.relpath(path, BASE)}")


if __name__ == "__main__":
    print("Generating W-BIL01: download pages...")
    for lang in ["fr", "en", "de"]:
        write(os.path.join(BASE, lang, "download.html"), download_page(lang))

    print("Generating W-BIL02: register pages...")
    for lang in ["fr", "en", "de"]:
        write(os.path.join(BASE, lang, "register.html"), register_page(lang))

    print("Generating W-BIL03: verify-email pages...")
    for lang in ["fr", "en", "de"]:
        write(os.path.join(BASE, lang, "verify-email.html"), verify_page(lang))

    print("Generating W-BIL04: pricing pages (refonte)...")
    for lang in ["fr", "en", "de"]:
        write(os.path.join(BASE, lang, "pricing.html"), pricing_page(lang))

    print("\nDone. Run W-BIL05 (nav update) and W-BIL06 (headers) manually.")
