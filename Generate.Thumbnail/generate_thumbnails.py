#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur de thumbnails SVG du site vitrine BizCoRa (multilingue fr / en / de).

Source de verite UNIQUE pour les vignettes produit : chaque ecran est recree
fidelement a partir des memes composants mutualises (AppBar, cartes, KPI, chips,
icones), avec les tokens exacts du Design System de l'application Flutter
(lib/theme/design_system/app_palette.dart, app_typography.dart).

Pourquoi SVG : vectoriel (nettete infinie retina/4K), poids minime, zero perte,
ideal SEO/CLS (dimensions fixes). Pourquoi un generateur : DRY + identite
visuelle 100% coherente sur tous les ecrans (regle projet "identite unique").

Multilingue : le site ET l'application ont 3 langues. Chaque vignette est donc
produite dans les 3 langues (texte, formatage des montants et des dates par
locale), pour que chaque version du site montre l'app dans SA langue.

Police : pile websafe ("Segoe UI"/Roboto/Arial) proche d'Inter, robuste partout
sans dependance reseau ni embarquement (best practice SEO/perf, jamais cassante).

Sortie (assets/images/) :
    <ecran>.svg       -> francais (reference historique du site)
    <ecran>.en.svg    -> anglais
    <ecran>.de.svg    -> allemand

Usage : python generate_thumbnails.py
"""

import os

# Ce script vit dans <site>/Generate.Thumbnail/ ; la sortie va dans <site>/assets/images.
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SITE_ROOT, "assets", "images")
LANGS = ("fr", "en", "de")
LANG = "fr"  # langue courante (positionnee par main)

W, H = 1280, 676

# --- Palette (alignee sur AppPalette du Design System Flutter) ----------------
C = {
    "brand": "#4361EE", "brandDark": "#303FB0", "accent": "#6366F1",
    "brand50": "#EEF2FF", "brand100": "#E0E7FF", "brand300": "#A5B4FC",
    "n0": "#FFFFFF", "n50": "#F8FAFC", "n100": "#F1F5F9", "n200": "#E2E8F0",
    "n300": "#CBD5E1", "n400": "#94A3B8", "n500": "#64748B", "n600": "#475569",
    "n700": "#334155", "n800": "#1E293B", "n900": "#0F172A",
    "success": "#16A34A", "successBg": "#DCFCE7",
    "warning": "#D97706", "warningBg": "#FEF3C7",
    "danger": "#DC2626", "dangerBg": "#FEE2E2", "dangerDark": "#B91C1C",
    "info": "#2563EB", "infoBg": "#DBEAFE", "infoDark": "#1D4ED8",
    "teal": "#0D9488", "tealBg": "#CCFBF1",
    "gold": "#EAB308", "silver": "#94A3B8", "bronze": "#B45309",
}

FONT = "'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
NBSP = " "

# =============================================================================
# i18n - libelles d'interface (cle -> fr / en / de)
# =============================================================================
S = {
    # chrome dashboard
    "greeting": ("Bonjour, Alexis", "Hello, Alexis", "Hallo, Alexis"),
    "business_time": ("Heure de l'entreprise", "Business time", "Geschäftszeit"),
    "today_overview": ("Aperçu du jour", "Today's overview", "Tagesüberblick"),
    "total_sales": ("Total des ventes", "Total sales", "Gesamtumsatz"),
    "transactions": ("Transactions", "Transactions", "Transaktionen"),
    "out_of_stock": ("Rupture", "Out of stock", "Nicht vorrätig"),
    "low_stock": ("Faible stock", "Low stock", "Niedriger Bestand"),
    "sec_sales_customers": ("Ventes & clients", "Sales & customers", "Verkauf & Kunden"),
    "sec_stock_finance": ("Stock & finances", "Stock & finance", "Bestand & Finanzen"),
    "tile_sales": ("Ventes", "Sales", "Verkauf"),
    "tile_sales_history": ("Historique des ventes", "Sales history", "Verkaufsverlauf"),
    "tile_quotes": ("Devis", "Quotes", "Angebote"),
    "tile_invoices": ("Factures", "Invoices", "Rechnungen"),
    "tile_stock_mgmt": ("Gestion du stock", "Stock management", "Bestandsverwaltung"),
    "tile_transactions": ("Transactions", "Transactions", "Transaktionen"),
    "tile_accounting": ("Comptabilité", "Accounting", "Buchhaltung"),
    "tile_cashier_perf": ("Performance caissiers", "Cashier performance", "Kassenleistung"),
    # transactions dashboard
    "tx_dashboard": ("Tableau de bord des transactions", "Transactions dashboard", "Transaktions-Dashboard"),
    "tab_overview": ("Vue d'ensemble", "Overview", "Übersicht"),
    "tab_tx_list": ("Liste des transactions", "Transactions list", "Transaktionsliste"),
    "tab_reports": ("Rapports", "Reports", "Berichte"),
    "total_revenue": ("Chiffre d'affaires total", "Total revenue", "Gesamtumsatz"),
    "avg_per_tx": ("Montant moyen / transaction", "Average per transaction", "Ø pro Transaktion"),
    "payment_methods": ("Moyens de paiement", "Payment methods", "Zahlungsmethoden"),
    "types_3": ("3 types", "3 types", "3 Arten"),
    "payment_distribution": ("RÉPARTITION DES PAIEMENTS", "PAYMENT DISTRIBUTION", "ZAHLUNGSVERTEILUNG"),
    "payment_distribution_sub": ("Répartition des ventes par méthode de paiement",
                                 "Sales distribution by payment method",
                                 "Umsatzverteilung nach Zahlungsmethode"),
    "total": ("Total", "Total", "Gesamt"),
    "cash": ("Espèces", "Cash", "Bargeld"),
    "transfer": ("Virement", "Transfer", "Überweisung"),
    "credit_card": ("Carte bancaire", "Credit card", "Kreditkarte"),
    # stock
    "product_mgmt": ("Gestion des produits", "Product management", "Produktverwaltung"),
    "total_products": ("Total des produits", "Total products", "Produkte gesamt"),
    "total_value": ("Valeur totale", "Total value", "Gesamtwert"),
    "search_product": ("Rechercher un produit", "Search a product", "Produkt suchen"),
    "sort": ("Trier", "Sort", "Sortieren"),
    "filters": ("Filtres", "Filters", "Filter"),
    "left_qty": ("{n} restant", "{n} left", "{n} übrig"),
    "stock_n": ("Stock {n}", "Stock {n}", "Bestand {n}"),
    # pos
    "new_sale": ("Nouvelle vente", "New sale", "Neuer Verkauf"),
    "search_product_dots": ("Rechercher un produit…", "Search a product…", "Produkt suchen…"),
    "cart": ("Panier", "Cart", "Warenkorb"),
    "subtotal_ht": ("Sous-total HT", "Subtotal (net)", "Zwischensumme (netto)"),
    "vat": ("TVA", "VAT", "MwSt."),
    "total_ttc": ("Total TTC", "Total (gross)", "Gesamt (brutto)"),
    "proceed_payment": ("Procéder au paiement", "Proceed to payment", "Zur Zahlung"),
    # listes (factures / devis / achats)
    "search_dots": ("Rechercher…", "Search…", "Suchen…"),
    "all_f": ("Toutes", "All", "Alle"),
    "all_m": ("Tous", "All", "Alle"),
    "col_num": ("N°", "No.", "Nr."),
    "col_customer": ("Client", "Customer", "Kunde"),
    "col_date": ("Date", "Date", "Datum"),
    "col_amount_ttc": ("Montant TTC", "Amount (gross)", "Betrag (brutto)"),
    "col_amount": ("Montant", "Amount", "Betrag"),
    "col_status": ("Statut", "Status", "Status"),
    "col_items": ("Articles", "Items", "Artikel"),
    "col_order_no": ("N° commande", "Order no.", "Bestell-Nr."),
    "col_supplier": ("Fournisseur", "Supplier", "Lieferant"),
    "n_items": ("{n} articles", "{n} items", "{n} Artikel"),
    "n_item": ("{n} article", "{n} item", "{n} Artikel"),
    "invoices": ("Factures", "Invoices", "Rechnungen"),
    "quotes": ("Devis", "Quotes", "Angebote"),
    "purchases": ("Achats", "Purchases", "Einkäufe"),
    # statuts factures
    "st_paid": ("Payée", "Paid", "Bezahlt"),
    "st_sent": ("Envoyée", "Sent", "Gesendet"),
    "st_draft": ("Brouillon", "Draft", "Entwurf"),
    "st_cancelled": ("Annulée", "Cancelled", "Storniert"),
    # statuts devis
    "qs_converted": ("Converti", "Converted", "Umgewandelt"),
    "qs_sent": ("Envoyé", "Sent", "Gesendet"),
    "qs_accepted": ("Accepté", "Accepted", "Angenommen"),
    "qs_draft": ("Brouillon", "Draft", "Entwurf"),
    "qs_expired": ("Expiré", "Expired", "Abgelaufen"),
    # statuts achats
    "ps_received": ("Réceptionné", "Received", "Empfangen"),
    "ps_draft": ("Brouillon", "Draft", "Entwurf"),
    "ps_cancelled": ("Annulé", "Cancelled", "Storniert"),
    # document emailing
    "invoice_word": ("FACTURE", "INVOICE", "RECHNUNG"),
    "from": ("Émetteur", "From", "Aussteller"),
    "to_customer": ("Client", "Customer", "Kunde"),
    "demo_company": ("BizCoRa Démo SARL", "BizCoRa Demo Ltd", "BizCoRa Demo GmbH"),
    "demo_address": ("12 rue du Commerce, Paris", "12 Commerce St, Paris", "Handelsstraße 12, Paris"),
    "col_designation": ("Désignation", "Description", "Bezeichnung"),
    "col_qty": ("Qté", "Qty", "Menge"),
    "send_by_email": ("Envoyer par e-mail", "Send by e-mail", "Per E-Mail senden"),
    "pdf_auto": ("Le PDF est joint automatiquement", "The PDF is attached automatically",
                 "Das PDF wird automatisch angehängt"),
    "recipient": ("Destinataire", "Recipient", "Empfänger"),
    "subject": ("Objet", "Subject", "Betreff"),
    "subject_val": ("Votre facture FAC-001", "Your invoice INV-001", "Ihre Rechnung RE-001"),
    "message": ("Message", "Message", "Nachricht"),
    "msg_l1": ("Bonjour, veuillez trouver ci-joint", "Hello, please find attached",
               "Hallo, anbei finden Sie"),
    "msg_l2": ("votre facture. Cordialement.", "your invoice. Best regards.",
               "Ihre Rechnung. Mit freundlichen Grüßen."),
    "send": ("Envoyer", "Send", "Senden"),
    "invoice_no": ("Facture FAC-001", "Invoice INV-001", "Rechnung RE-001"),
    "invoice_ref": ("N° FAC-001  -  15/01/2026", "No. INV-001  -  01/15/2026", "Nr. RE-001  -  15.01.2026"),
    "pdf_name": ("facture-FAC-001.pdf", "invoice-INV-001.pdf", "rechnung-RE-001.pdf"),
    # loyalty
    "customer_loyalty": ("Fidélité client", "Customer loyalty", "Kundentreue"),
    "points": ("points", "points", "Punkte"),
    "redeemable": ("Valeur rachetable : {v}", "Redeemable value: {v}", "Einlösbarer Wert: {v}"),
    "points_earned": ("Points gagnés", "Points earned", "Punkte gesammelt"),
    "points_used": ("Points utilisés", "Points used", "Punkte eingelöst"),
    "gold_tier": ("Palier Or", "Gold tier", "Gold-Stufe"),
    "tier_progress": ("1 250 / 1 500 pts", "1,250 / 1,500 pts", "1.250 / 1.500 Pkt."),
    "to_platinum": ("Plus que 250 points avant le palier Platine",
                    "250 points to the Platinum tier", "Noch 250 Punkte bis Platin"),
    "points_history": ("Historique des points", "Points history", "Punkteverlauf"),
    "pts": ("pts", "pts", "Pkt."),
    "loy_purchase": ("Achat n° {r}", "Purchase no. {r}", "Kauf Nr. {r}"),
    "loy_discount": ("Remise fidélité - {r}", "Loyalty discount - {r}", "Treuerabatt - {r}"),
    "loy_adjust": ("Ajustement - correction de saisie", "Adjustment - entry correction",
                   "Anpassung - Korrektur"),
    # accounting
    "accounting": ("Comptabilité", "Accounting", "Buchhaltung"),
    "net_revenue_ht": ("Chiffre d'affaires net HT", "Net revenue (excl. tax)", "Nettoumsatz"),
    "gross_margin": ("Marge brute", "Gross margin", "Bruttomarge"),
    "cogs": ("Coût des marchandises (COGS)", "Cost of goods (COGS)", "Wareneinsatz (COGS)"),
    "vat_payable": ("TVA à payer", "VAT payable", "Zahllast (MwSt.)"),
    "net_cash": ("Trésorerie nette", "Net cash", "Nettoliquidität"),
    "stock_value_cost": ("Valeur du stock (coût)", "Stock value (cost)", "Bestandswert (Kosten)"),
    "vat_summary": ("Synthèse de la TVA", "VAT summary", "MwSt.-Übersicht"),
    "vat_collected": ("TVA collectée", "VAT collected", "Vereinnahmte MwSt."),
    "vat_deductible": ("TVA déductible", "VAT deductible", "Abziehbare MwSt."),
    "quick_links": ("RACCOURCIS RAPIDES", "QUICK LINKS", "SCHNELLZUGRIFF"),
    "income_statement": ("Compte de résultat", "Income statement", "GuV-Rechnung"),
    "vat_report": ("État de TVA", "VAT report", "MwSt.-Bericht"),
    "cash_flow": ("Trésorerie", "Cash flow", "Liquidität"),
    "sales_detail": ("Détail des ventes", "Sales detail", "Verkaufsdetails"),
    # cashier performance
    "cashier_perf": ("Performance des caissiers", "Cashier performance", "Kassenleistung"),
    "active_cashiers": ("Caissiers actifs", "Active cashiers", "Aktive Kassierer"),
    "refunds": ("Remboursements", "Refunds", "Erstattungen"),
    "revenue_per_cashier": ("Chiffre d'affaires par caissier", "Revenue per cashier", "Umsatz pro Kassierer"),
    "cashier_ranking": ("Classement des caissiers", "Cashier ranking", "Kassierer-Rangliste"),
    "sales_avg": ("{s} ventes  -  panier {a}", "{s} sales  -  avg {a}", "{s} Verkäufe  -  Ø {a}"),
    "period_demo": ("01/01/2026  ->  30/06/2026", "01/01/2026  ->  06/30/2026", "01.01.2026  ->  30.06.2026"),
    "tz_demo": ("Europe/Paris - UTC+2", "Europe/Paris - UTC+2", "Europe/Paris - UTC+2"),
    "now_demo": ("21/06/2026  -  14:25", "06/21/2026  -  2:25 PM", "21.06.2026  -  14:25"),
}

# Catalogues localises (listes par langue)
PRODUCTS = {  # (nom, categorie_key, prix, qty, statut)
    "fr": [
        ("Huile d'olive extra vierge Bio", "cat_condiments", 12.99, 45, "ok"),
        ("Café moulu espresso 250g", "cat_beverages", 8.75, 0, "out"),
        ("Riz blanc long grain 1kg", "cat_staples", 3.50, 2, "low"),
        ("Miel de châtaignier 500ml", "cat_fine", 9.99, 18, "ok"),
        ("Chocolat noir 70% 100g", "cat_confect", 4.50, 6, "low"),
        ("Pâtes intégrales 500g", "cat_staples", 2.40, 0, "out"),
        ("Thé vert sencha 100g", "cat_beverages", 6.20, 33, "ok"),
        ("Confiture abricot 370g", "cat_fine", 4.10, 27, "ok"),
    ],
    "en": [
        ("Extra virgin olive oil (organic)", "cat_condiments", 12.99, 45, "ok"),
        ("Ground espresso coffee 250g", "cat_beverages", 8.75, 0, "out"),
        ("Long grain white rice 1kg", "cat_staples", 3.50, 2, "low"),
        ("Chestnut honey 500ml", "cat_fine", 9.99, 18, "ok"),
        ("Dark chocolate 70% 100g", "cat_confect", 4.50, 6, "low"),
        ("Wholewheat pasta 500g", "cat_staples", 2.40, 0, "out"),
        ("Sencha green tea 100g", "cat_beverages", 6.20, 33, "ok"),
        ("Apricot jam 370g", "cat_fine", 4.10, 27, "ok"),
    ],
    "de": [
        ("Natives Olivenöl extra (Bio)", "cat_condiments", 12.99, 45, "ok"),
        ("Gemahlener Espresso 250g", "cat_beverages", 8.75, 0, "out"),
        ("Langkornreis weiß 1kg", "cat_staples", 3.50, 2, "low"),
        ("Kastanienhonig 500ml", "cat_fine", 9.99, 18, "ok"),
        ("Zartbitter 70% 100g", "cat_confect", 4.50, 6, "low"),
        ("Vollkornnudeln 500g", "cat_staples", 2.40, 0, "out"),
        ("Sencha Grüntee 100g", "cat_beverages", 6.20, 33, "ok"),
        ("Aprikosenmarmelade 370g", "cat_fine", 4.10, 27, "ok"),
    ],
}
CATS = {
    "cat_condiments": ("Condiments", "Condiments", "Gewürze"),
    "cat_beverages": ("Boissons", "Beverages", "Getränke"),
    "cat_staples": ("Féculents", "Staples", "Grundnahrung"),
    "cat_fine": ("Épicerie fine", "Fine food", "Feinkost"),
    "cat_confect": ("Confiserie", "Confectionery", "Süßwaren"),
}
POS_PRODUCTS = {
    "fr": [("Tomate Bio", 4.50, "/kg"), ("Pain complet 400g", 2.20, ""), ("Lait 1L", 1.05, ""),
           ("Fromage 250g", 8.50, ""), ("Eau 6×1,5L", 3.99, ""), ("Œufs x12", 3.40, ""),
           ("Bananes Bio", 2.30, "/kg"), ("Yaourt x4", 2.10, ""), ("Jus d'orange 1L", 2.60, ""),
           ("Café 250g", 8.75, ""), ("Riz 1kg", 3.50, ""), ("Beurre 250g", 2.95, "")],
    "en": [("Organic tomato", 4.50, "/kg"), ("Wholemeal bread 400g", 2.20, ""), ("Milk 1L", 1.05, ""),
           ("Cheese 250g", 8.50, ""), ("Water 6×1.5L", 3.99, ""), ("Eggs x12", 3.40, ""),
           ("Organic bananas", 2.30, "/kg"), ("Yogurt x4", 2.10, ""), ("Orange juice 1L", 2.60, ""),
           ("Coffee 250g", 8.75, ""), ("Rice 1kg", 3.50, ""), ("Butter 250g", 2.95, "")],
    "de": [("Bio-Tomate", 4.50, "/kg"), ("Vollkornbrot 400g", 2.20, ""), ("Milch 1L", 1.05, ""),
           ("Käse 250g", 8.50, ""), ("Wasser 6×1,5L", 3.99, ""), ("Eier x12", 3.40, ""),
           ("Bio-Bananen", 2.30, "/kg"), ("Joghurt x4", 2.10, ""), ("Orangensaft 1L", 2.60, ""),
           ("Kaffee 250g", 8.75, ""), ("Reis 1kg", 3.50, ""), ("Butter 250g", 2.95, "")],
}
CART = {  # (nom, qty, prix_unitaire) - index aligne sur POS_PRODUCTS pertinents
    "fr": [("Tomate Bio", 2, 4.50), ("Pain complet 400g", 3, 2.20), ("Fromage 250g", 1, 8.50), ("Eau 6×1,5L", 2, 3.99)],
    "en": [("Organic tomato", 2, 4.50), ("Wholemeal bread 400g", 3, 2.20), ("Cheese 250g", 1, 8.50), ("Water 6×1.5L", 2, 3.99)],
    "de": [("Bio-Tomate", 2, 4.50), ("Vollkornbrot 400g", 3, 2.20), ("Käse 250g", 1, 8.50), ("Wasser 6×1,5L", 2, 3.99)],
}
DOC_ROWS = {  # (designation, qty, total)
    "fr": [("Huile d'olive Bio", 10, 129.90), ("Café espresso 250g", 20, 175.00), ("Miel châtaignier", 15, 149.85)],
    "en": [("Organic olive oil", 10, 129.90), ("Espresso coffee 250g", 20, 175.00), ("Chestnut honey", 15, 149.85)],
    "de": [("Bio-Olivenöl", 10, 129.90), ("Espresso 250g", 20, 175.00), ("Kastanienhonig", 15, 149.85)],
}


def t(key, **kw):
    val = S[key][LANGS.index(LANG)]
    return val.format(**kw) if kw else val


def cat(key):
    return CATS[key][LANGS.index(LANG)]


def money(v, dec=2):
    neg = v < 0
    v = abs(v)
    s = f"{v:,.{dec}f}"  # 2,450.50
    intp, _, decp = s.partition(".")
    if LANG == "fr":
        intp = intp.replace(",", NBSP)
        body = intp + ("," + decp if dec else "")
        out = body + NBSP + "€"
    elif LANG == "de":
        intp = intp.replace(",", ".")
        body = intp + ("," + decp if dec else "")
        out = body + NBSP + "€"
    else:  # en
        out = "€" + s
    return ("-" + out) if neg else out


def num(v):
    s = f"{v:,}"
    if LANG == "fr":
        return s.replace(",", NBSP)
    if LANG == "de":
        return s.replace(",", ".")
    return s


def datestr(d, m, y):
    if LANG == "en":
        return f"{m:02d}/{d:02d}/{y}"
    if LANG == "de":
        return f"{d:02d}.{m:02d}.{y}"
    return f"{d:02d}/{m:02d}/{y}"


# =============================================================================
# Primitives de dessin
# =============================================================================
def esc(t_):
    return str(t_).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=14, color=C["n900"], weight=400, anchor="start", spacing=None, opacity=None):
    extra = ""
    if spacing is not None:
        extra += f' letter-spacing="{spacing}"'
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{extra}>'
            f'{esc(s)}</text>')


def rect(x, y, w, h, fill="none", rx=0, stroke=None, sw=1, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}{o}/>'


def line(x1, y1, x2, y2, color=C["n200"], sw=1, opacity=None):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"{o}/>')


def circle(cx, cy, r, fill="none", stroke=None, sw=1, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}{o}/>'


def card(x, y, w, h, rx=16, fill=C["n0"], stroke=C["n200"], shadow=True):
    flt = ' filter="url(#cardShadow)"' if shadow else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"{flt}/>'


def _ic_paths(name, color, sw):
    p = f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    pf = f'fill="{color}"'
    I = {
        "bell": f'<path {p} d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path {p} d="M10 19a2 2 0 0 0 4 0"/>',
        "person": f'<circle {p} cx="12" cy="8" r="3.4"/><path {p} d="M5.5 19a6.5 6.5 0 0 1 13 0"/>',
        "sparkle": f'<path {p} d="M12 3l1.8 4.7L18.5 9l-4.7 1.3L12 15l-1.8-4.7L5.5 9l4.7-1.3z"/><path {p} d="M18.5 14.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
        "help": f'<circle {p} cx="12" cy="12" r="9"/><path {p} d="M9.2 9.3a2.8 2.8 0 0 1 5.4 1c0 1.9-2.6 2.2-2.6 4"/><circle {pf} cx="12" cy="17" r="1"/>',
        "logout": f'<path {p} d="M14 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8"/><path {p} d="M16 8l4 4-4 4"/><path {p} d="M20 12H9"/>',
        "clock": f'<circle {p} cx="12" cy="12" r="8.5"/><path {p} d="M12 7.5V12l3 2"/>',
        "payments": f'<rect {p} x="3" y="7" width="15" height="10" rx="2"/><circle {p} cx="10.5" cy="12" r="2.2"/><path {p} d="M21 9v9a2 2 0 0 1-2 2H7"/>',
        "receipt": f'<path {p} d="M6 3h12v18l-2.2-1.5L13.6 21 11.4 19.5 9.2 21 7 19.5 6 21z"/><path {p} d="M9 8h6M9 12h6"/>',
        "error": f'<circle {p} cx="12" cy="12" r="8.5"/><path {p} d="M12 7.5V13"/><circle {pf} cx="12" cy="16.5" r="1"/>',
        "warning": f'<path {p} d="M12 4l8.5 15H3.5z"/><path {p} d="M12 10v4"/><circle {pf} cx="12" cy="16.5" r="1"/>',
        "pos": f'<rect {p} x="4" y="9" width="16" height="11" rx="2"/><path {p} d="M8 9V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v3"/><path {p} d="M8 14h4"/>',
        "history": f'<path {p} d="M4 12a8 8 0 1 1 2.3 5.6"/><path {p} d="M4 17v-4h4"/><path {p} d="M12 8v4l3 2"/>',
        "quote": f'<path {p} d="M6 3h9l4 4v14H6z"/><path {p} d="M14 3v5h5"/><path {p} d="M9 13h6M9 16h4"/>',
        "receipt_long": f'<path {p} d="M5 3h11v18l-1.6-1.2L12.8 21 11.2 19.8 9 21V3z"/><path {p} d="M19 7v14"/><path {p} d="M8 8h5M8 12h5"/>',
        "inventory": f'<path {p} d="M4 7l8-4 8 4v10l-8 4-8-4z"/><path {p} d="M4 7l8 4 8-4M12 11v10"/>',
        "analytics": f'<rect {p} x="3" y="3" width="18" height="18" rx="2"/><path {p} d="M8 15v-3M12 15V9M16 15v-5"/>',
        "accounting": f'<path {p} d="M4 21V8l8-5 8 5v13"/><path {p} d="M4 21h16M9 21v-6h6v6"/>',
        "search": f'<circle {p} cx="11" cy="11" r="6.5"/><path {p} d="M16 16l4.5 4.5"/>',
        "sort": f'<path {p} d="M6 5v14M6 5l-2.5 2.5M6 5l2.5 2.5"/><path {p} d="M14 7h6M14 11h4M14 15h2"/>',
        "tune": f'<path {p} d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle {p} cx="16" cy="7" r="2.2"/><circle {p} cx="8" cy="17" r="2.2"/>',
        "scan": f'<path {p} d="M4 8V5h3M20 8V5h-3M4 16v3h3M20 16v3h-3"/><path {p} d="M7 8v8M10 8v8M13 8v8M16 8v8"/>',
        "plus": f'<path {p} d="M12 5v14M5 12h14"/>',
        "chevron": f'<path {p} d="M9 6l6 6-6 6"/>',
        "basket": f'<path {p} d="M5 9h14l-1.4 9.4a2 2 0 0 1-2 1.6H8.4a2 2 0 0 1-2-1.6z"/><path {p} d="M9 9l3-5 3 5"/><path {p} d="M10 13v3M14 13v3"/>',
        "minus": f'<path {p} d="M6 12h12"/>',
        "close": f'<path {p} d="M7 7l10 10M17 7L7 17"/>',
        "email": f'<rect {p} x="3" y="5" width="18" height="14" rx="2"/><path {p} d="M3.5 7l8.5 6 8.5-6"/>',
        "pdf": f'<path {p} d="M7 3h7l4 4v14H7z"/><path {p} d="M14 3v4h4"/><path {p} d="M10 13h.5a1.3 1.3 0 0 1 0 2.6H10zM10 13v4M14.5 13H16M14.5 13v4M14.5 15.2H16"/>',
        "download": f'<path {p} d="M12 4v11M12 15l-4-4M12 15l4-4"/><path {p} d="M5 19h14"/>',
        "print": f'<path {p} d="M7 8V3h10v5"/><rect {p} x="4" y="8" width="16" height="8" rx="2"/><rect {p} x="7" y="14" width="10" height="6"/>',
        "gift": f'<rect {p} x="4" y="9" width="16" height="11" rx="1.5"/><path {p} d="M3 9h18M12 9v11"/><path {p} d="M12 9S10.5 4 8 4a2 2 0 0 0 0 5zM12 9s1.5-5 4-5a2 2 0 0 1 0 5z"/>',
        "cart": f'<path {p} d="M3 4h2l2.2 11.2a2 2 0 0 0 2 1.6h7.6a2 2 0 0 0 2-1.6L21 8H7"/><circle {p} cx="10" cy="20" r="1.3"/><circle {p} cx="17" cy="20" r="1.3"/>',
        "leaderboard": f'<rect {p} x="4" y="11" width="4" height="9"/><rect {p} x="10" y="5" width="4" height="15"/><rect {p} x="16" y="14" width="4" height="6"/>',
        "bars": f'<path {p} d="M4 20V4"/><path {p} d="M4 20h16"/><rect {pf} x="7" y="12" width="3" height="6"/><rect {pf} x="12" y="8" width="3" height="10"/><rect {pf} x="17" y="5" width="3" height="13"/>',
        "trend": f'<path {p} d="M3 17l6-6 4 4 8-8"/><path {p} d="M21 7v5M21 7h-5"/>',
        "wallet": f'<rect {p} x="3" y="6" width="18" height="13" rx="2.5"/><path {p} d="M3 10h18"/><circle {pf} cx="16.5" cy="14" r="1.4"/>',
        "warehouse": f'<path {p} d="M3 21V8l9-4 9 4v13"/><path {p} d="M7 21v-7h10v7"/><path {p} d="M7 17h10"/>',
        "groups": f'<circle {p} cx="9" cy="9" r="2.8"/><path {p} d="M3.5 19a5.5 5.5 0 0 1 11 0"/><path {p} d="M16 7.2a2.8 2.8 0 0 1 0 5.6"/><path {p} d="M16.5 14a5.5 5.5 0 0 1 4 5"/>',
        "return": f'<path {p} d="M4 9h11a5 5 0 0 1 0 10H9"/><path {p} d="M4 9l4-4M4 9l4 4"/>',
        "list_alt": f'<rect {p} x="4" y="4" width="16" height="16" rx="2"/><path {p} d="M8 9h8M8 13h8M8 17h5"/>',
        "calendar": f'<rect {p} x="4" y="5" width="16" height="16" rx="2"/><path {p} d="M4 9h16M8 3v4M16 3v4"/>',
        "credit": f'<rect {p} x="3" y="5" width="18" height="14" rx="2.5"/><path {p} d="M3 9.5h18"/><path {p} d="M6.5 14.5h4"/>',
        "logo": f'<path {pf} d="M5 4h9.5a4.5 4.5 0 0 1 1.3 8.8A4.8 4.8 0 0 1 14 21H5z"/><path fill="#FFFFFF" d="M8 7.5h5.6a1.8 1.8 0 0 1 0 3.6H8zM8 13h5.4a2 2 0 0 1 0 4H8z"/>',
    }
    return I.get(name, f'<circle {p} cx="12" cy="12" r="8"/>')


def icon(name, x, y, size, color=C["n600"], sw=2):
    sc = size / 24.0
    return f'<g transform="translate({x},{y}) scale({sc})">{_ic_paths(name, color, sw)}</g>'


def icon_chip(x, y, s, name, color, bg=None, rx=10):
    out = []
    if bg:
        out.append(rect(x, y, s, s, fill=bg, rx=rx))
    pad = s * 0.22
    out.append(icon(name, x + pad, y + pad, s - 2 * pad, color, sw=2))
    return "".join(out)


def tint(name):
    return {"brand": C["brand50"], "accent": C["brand50"], "info": C["infoBg"],
            "success": C["successBg"], "warning": C["warningBg"],
            "danger": C["dangerBg"], "teal": C["tealBg"]}.get(name, C["brand50"])


def status_chip(x, y, label, color, bg, fs=12):
    w = 16 + len(label) * fs * 0.58
    return rect(x, y, w, 22, fill=bg, rx=11) + text(x + 8, y + 15.5, label, fs, color, weight=600)


# -----------------------------------------------------------------------------
# Illustrations produit (flat design, vectorielles) - rendent le catalogue
# attractif (caisse + stock). Dessinees dans une boite normalisee 0..100.
# Cle "kind" independante de la langue (defini dans KINDS_*).
# -----------------------------------------------------------------------------
ART = {
    "tomato": ('<circle cx="50" cy="58" r="27" fill="#EF4444"/>'
               '<ellipse cx="40" cy="49" rx="8" ry="5" fill="#FFFFFF" opacity="0.4"/>'
               '<path d="M50 33c-4-8-11-10-17-8 3 2 5 5 5 9 4-2 8-2 12-1z" fill="#16A34A"/>'
               '<path d="M50 33c4-8 11-10 17-8-3 2-5 5-5 9-4-2-8-2-12-1z" fill="#15803D"/>'
               '<rect x="47" y="22" width="6" height="12" rx="3" fill="#15803D"/>'),
    "bread": ('<path d="M22 58c0-13 12-22 28-22s28 9 28 22c0 4-3 6-7 6H29c-4 0-7-2-7-6z" fill="#D9A066"/>'
              '<path d="M22 58c0-6 3-11 8-15 0 5 1 9 3 13-4 0-8 1-11 2z" fill="#E8C39E" opacity="0.6"/>'
              '<path d="M36 41l6 11M50 37l4 13M64 41l-6 11" stroke="#A9682E" stroke-width="3" fill="none" stroke-linecap="round"/>'),
    "milk": ('<path d="M37 34h26v6l4 7v23a3 3 0 0 1-3 3H36a3 3 0 0 1-3-3V47l4-7z" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>'
             '<path d="M33 47h34v7H33z" fill="#4361EE"/>'
             '<rect x="42" y="58" width="16" height="11" rx="2" fill="#4361EE" opacity="0.18"/>'),
    "cheese": ('<path d="M22 64l54-22 6 22z" fill="#FBBF24"/>'
               '<path d="M22 64l54-22 6 22z" fill="#F59E0B" opacity="0.18"/>'
               '<circle cx="58" cy="56" r="3.5" fill="#F59E0B"/><circle cx="69" cy="53" r="2.5" fill="#F59E0B"/>'
               '<circle cx="63" cy="61" r="2" fill="#F59E0B"/>'),
    "water": ('<g fill="#60A5FA"><rect x="33" y="38" width="12" height="31" rx="4"/>'
              '<rect x="47" y="38" width="12" height="31" rx="4"/><rect x="61" y="38" width="12" height="31" rx="4"/></g>'
              '<g fill="#2563EB"><rect x="35" y="32" width="8" height="8" rx="2"/>'
              '<rect x="49" y="32" width="8" height="8" rx="2"/><rect x="63" y="32" width="8" height="8" rx="2"/></g>'
              '<g fill="#FFFFFF" opacity="0.65"><rect x="33" y="51" width="12" height="8"/>'
              '<rect x="47" y="51" width="12" height="8"/><rect x="61" y="51" width="12" height="8"/></g>'),
    "eggs": ('<path d="M24 55h52v11a4 4 0 0 1-4 4H28a4 4 0 0 1-4-4z" fill="#94A3B8"/>'
             '<g fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5">'
             '<ellipse cx="35" cy="49" rx="7" ry="9"/><ellipse cx="50" cy="49" rx="7" ry="9"/><ellipse cx="65" cy="49" rx="7" ry="9"/></g>'),
    "banana": ('<path d="M28 40c0 19 16 31 36 28-7-3-10-10-10-18 0-6-2-9-6-11-4 9-13 7-20 1z" fill="#FACC15"/>'
               '<path d="M28 40c2 16 16 27 36 28" fill="none" stroke="#CA8A04" stroke-width="3" stroke-linecap="round"/>'
               '<rect x="25" y="36" width="7" height="8" rx="2" fill="#65A30D"/>'),
    "yogurt": ('<path d="M35 45h30l-3 25a4 4 0 0 1-4 3H42a4 4 0 0 1-4-3z" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>'
               '<rect x="33" y="38" width="34" height="9" rx="3" fill="#EC4899"/>'
               '<path d="M44 57c4 4 8 4 12 0" stroke="#EC4899" stroke-width="3" fill="none" stroke-linecap="round"/>'),
    "juice": ('<path d="M39 38h22l-3 32a4 4 0 0 1-4 3H46a4 4 0 0 1-4-3z" fill="#FB923C"/>'
              '<path d="M39 38h22l-1 9H40z" fill="#FDBA74"/>'
              '<circle cx="64" cy="34" r="8" fill="#F97316"/>'
              '<path d="M64 26v16M56 34h16" stroke="#FFFFFF" stroke-width="1.5"/>'),
    "coffee": ('<path d="M35 38h30v30a4 4 0 0 1-4 4H39a4 4 0 0 1-4-4z" fill="#6B4226"/>'
               '<path d="M35 38l4-6h22l4 6z" fill="#4A2E1A"/>'
               '<rect x="41" y="48" width="18" height="14" rx="2" fill="#FFFFFF" opacity="0.9"/>'
               '<ellipse cx="50" cy="55" rx="4" ry="5.5" fill="#6B4226"/>'),
    "rice": ('<path d="M35 36h30v32a4 4 0 0 1-4 4H39a4 4 0 0 1-4-4z" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>'
             '<rect x="35" y="51" width="30" height="10" fill="#16A34A"/>'
             '<path d="M41 44l3-6h12l3 6z" fill="#E2E8F0"/>'),
    "butter": ('<rect x="30" y="44" width="40" height="22" rx="3" fill="#FCD34D"/>'
               '<rect x="30" y="44" width="40" height="8" rx="3" fill="#FBBF24"/>'
               '<rect x="42" y="54" width="16" height="9" rx="2" fill="#FFFFFF" opacity="0.7"/>'),
    "oil": ('<rect x="44" y="24" width="12" height="9" fill="#3F6212"/>'
            '<path d="M44 33h12v8l6 8v23a4 4 0 0 1-4 4H42a4 4 0 0 1-4-4V49l6-8z" fill="#65A30D"/>'
            '<rect x="40" y="53" width="20" height="17" rx="2" fill="#FFFFFF" opacity="0.9"/>'
            '<circle cx="50" cy="61" r="3" fill="#65A30D"/>'),
    "honey": ('<path d="M34 45h32v21a6 6 0 0 1-6 6H40a6 6 0 0 1-6-6z" fill="#FBBF24"/>'
              '<rect x="32" y="38" width="36" height="8" rx="2" fill="#D97706"/>'
              '<rect x="41" y="51" width="18" height="15" rx="2" fill="#FFFFFF" opacity="0.85"/>'
              '<path d="M50 38v34" stroke="#D97706" stroke-width="2" opacity="0.5"/>'),
    "chocolate": ('<rect x="30" y="38" width="40" height="28" rx="3" fill="#6B4226"/>'
                  '<rect x="30" y="38" width="40" height="7" fill="#8B5A2B" opacity="0.6"/>'
                  '<g stroke="#4A2E1A" stroke-width="2" fill="none"><path d="M43 38v28M57 38v28M30 52h40"/></g>'),
    "pasta": ('<rect x="36" y="30" width="28" height="44" rx="4" fill="#FEF3C7" stroke="#FCD34D" stroke-width="2"/>'
              '<g stroke="#EAB308" stroke-width="2.5" stroke-linecap="round">'
              '<line x1="44" y1="34" x2="44" y2="70"/><line x1="50" y1="34" x2="50" y2="70"/><line x1="56" y1="34" x2="56" y2="70"/></g>'
              '<rect x="36" y="46" width="28" height="12" fill="#FFFFFF" opacity="0.75"/>'),
    "tea": ('<rect x="34" y="38" width="32" height="34" rx="3" fill="#16A34A"/>'
            '<path d="M50 44c-6 2-9 7-9 12 6 0 10-4 9-12z" fill="#86EFAC"/>'
            '<rect x="40" y="58" width="20" height="10" rx="2" fill="#FFFFFF" opacity="0.85"/>'),
    "jam": ('<path d="M34 46h32v20a6 6 0 0 1-6 6H40a6 6 0 0 1-6-6z" fill="#EF4444"/>'
            '<rect x="34" y="44" width="32" height="6" fill="#B91C1C"/>'
            '<rect x="32" y="36" width="36" height="9" rx="3" fill="#DC2626"/>'
            '<rect x="41" y="54" width="18" height="14" rx="2" fill="#FFFFFF" opacity="0.85"/>'
            '<circle cx="50" cy="61" r="3.5" fill="#EF4444"/>'),
    "box": ('<path d="M30 40l20-10 20 10v22l-20 10-20-10z" fill="#A5B4FC"/>'
            '<path d="M30 40l20 10 20-10M50 50v22" stroke="#6366F1" stroke-width="2" fill="none"/>'),
}

# Genre de produit par index (independant de la langue), aligne sur PRODUCTS / POS_PRODUCTS.
KINDS_STOCK = ["oil", "coffee", "rice", "honey", "chocolate", "pasta", "tea", "jam"]
KINDS_POS = ["tomato", "bread", "milk", "cheese", "water", "eggs",
             "banana", "yogurt", "juice", "coffee", "rice", "butter"]


def product_art(kind, x, y, w, h, fill=0.82):
    """Place une illustration produit centree dans la zone image (x,y,w,h)."""
    s = h * fill
    tx = x + (w - s) / 2
    ty = y + (h - s) / 2
    return f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s / 100:.3f})">{ART.get(kind, ART["box"])}</g>'


def defs():
    return ('<defs>'
            f'<linearGradient id="appbar" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{C["brand"]}"/><stop offset="1" stop-color="{C["accent"]}"/></linearGradient>'
            '<filter id="cardShadow" x="-8%" y="-8%" width="116%" height="124%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.06"/></filter>'
            '<filter id="floatShadow" x="-20%" y="-20%" width="140%" height="150%">'
            '<feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#0F172A" flood-opacity="0.12"/></filter>'
            '<linearGradient id="imgGrad" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2FF"/></linearGradient>'
            '<clipPath id="round"><rect x="0" y="0" width="1280" height="676" rx="2"/></clipPath></defs>')


def appbar_company(actions=("bell", "person", "sparkle", "help", "logout")):
    h = 60
    out = [rect(0, 0, W, h, fill="url(#appbar)")]
    out.append(rect(24, 14, 32, 32, fill=C["n0"], rx=9, opacity=0.96))
    out.append(icon("logo", 28, 18, 24, C["brand"]))
    out.append(text(66, 37, "BizCoRa", 18, C["n0"], weight=700, spacing="0.2"))
    ax = W - 28
    for a in reversed(actions):
        col = "#A5B4FC" if a == "sparkle" else C["n0"]
        if a == "person":
            out.append(circle(ax - 14, 30, 14, fill="rgba(255,255,255,0.18)"))
            out.append(circle(ax - 14, 30, 14, stroke="rgba(255,255,255,0.55)", sw=1.4))
            out.append(text(ax - 14, 34.5, "AM", 11, C["n0"], weight=700, anchor="middle"))
        else:
            out.append(icon(a, ax - 26, 18, 23, col, sw=1.9))
        ax -= 40
    return "".join(out), h


def back_appbar(title, actions=()):
    h = 60
    out = [rect(0, 0, W, h, fill="url(#appbar)")]
    p = f'fill="none" stroke="{C["n0"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    out.append(f'<g transform="translate(22,18)"><path {p} d="M15 5l-7 7 7 7"/><path {p} d="M8 12h11"/></g>')
    out.append(text(60, 38, title, 19, C["n0"], weight=600))
    ax = W - 28
    for a in reversed(actions):
        out.append(icon(a, ax - 26, 18, 23, C["n0"], sw=1.9))
        ax -= 42
    return "".join(out), h


def frame(body, appbar_svg, bg=None):
    bg = bg or C["n50"]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
        defs(), '<g clip-path="url(#round)">', rect(0, 0, W, H, fill=bg),
        body, appbar_svg, '</g></svg>'])


def kpi_card(x, y, w, label, value, iconname, colorkey):
    h = 116
    col = C.get(colorkey, colorkey)
    out = [card(x, y, w, h)]
    out.append(icon_chip(x + 18, y + 18, 40, iconname, col, tint(colorkey), rx=11))
    out.append(text(x + 18, y + 84, value, 26, C["n900"], weight=700))
    out.append(text(x + 18, y + 104, label, 13, C["n500"], weight=500))
    return "".join(out), h


def section_label(x, y, title):
    return text(x, y, title.upper(), 12, C["n500"], weight=700, spacing="0.8")


def action_tile(x, y, w, label, iconname, colorkey):
    h = 76
    col = C.get(colorkey, colorkey)
    out = [card(x, y, w, h)]
    out.append(icon_chip(x + 16, y + 18, 40, iconname, col, tint(colorkey), rx=10))
    out.append(text(x + 68, y + 44, label, 14.5, C["n800"], weight=600))
    out.append(icon("chevron", x + w - 30, y + 26, 22, C["n300"], sw=2))
    return "".join(out), h


# =============================================================================
# ECRANS
# =============================================================================
def screen_dashboard():
    ab, abh = appbar_company()
    b = []
    y = abh + 26
    b.append(text(28, y + 8, t("greeting"), 24, C["n900"], weight=700))
    b.append(rect(28, y + 22, 340, 34, fill=C["brand50"], rx=10, stroke=C["brand100"]))
    b.append(icon("clock", 38, y + 28, 22, C["brand"], sw=2))
    b.append(text(68, y + 36, t("business_time"), 12, C["n500"], weight=500))
    b.append(text(68, y + 51, t("now_demo"), 13, C["n800"], weight=700))
    b.append(text(W - 28, y + 44, t("tz_demo"), 12, C["n400"], anchor="end"))

    ky = y + 76
    b.append(section_label(28, ky, t("today_overview")))
    cy = ky + 14
    gap = 16
    cw = (W - 56 - gap * 3) / 4
    kpis = [(t("total_sales"), money(2450.50), "payments", "success"),
            (t("transactions"), "28", "receipt", "info"),
            (t("out_of_stock"), "3", "error", "danger"),
            (t("low_stock"), "12", "warning", "warning")]
    for i, (lab, val, ic, ck) in enumerate(kpis):
        s, _ = kpi_card(28 + i * (cw + gap), cy, cw, lab, val, ic, ck)
        b.append(s)

    sy = cy + 116 + 24
    b.append(section_label(28, sy, t("sec_sales_customers")))
    ty = sy + 12
    tgap = 16
    tw = (W - 56 - tgap * 3) / 4
    row1 = [(t("tile_sales"), "pos", "success"), (t("tile_sales_history"), "history", "info"),
            (t("tile_quotes"), "quote", "brand"), (t("tile_invoices"), "receipt_long", "accent")]
    for i, (lab, ic, ck) in enumerate(row1):
        s, _ = action_tile(28 + i * (tw + tgap), ty, tw, lab, ic, ck)
        b.append(s)

    sy2 = ty + 76 + 22
    b.append(section_label(28, sy2, t("sec_stock_finance")))
    ty2 = sy2 + 12
    row2 = [(t("tile_stock_mgmt"), "inventory", "brand"), (t("tile_transactions"), "analytics", "success"),
            (t("tile_accounting"), "accounting", "brand"), (t("tile_cashier_perf"), "leaderboard", "info")]
    for i, (lab, ic, ck) in enumerate(row2):
        s, _ = action_tile(28 + i * (tw + tgap), ty2, tw, lab, ic, ck)
        b.append(s)
    return frame("".join(b), ab)


def screen_transactions():
    ab, abh = back_appbar(t("tx_dashboard"), actions=("download", "tune"))
    b = []
    ty = abh
    b.append(rect(0, ty, W, 46, fill=C["n0"], stroke=C["n200"]))
    tabs = [(t("tab_overview"), True), (t("tab_tx_list"), False), (t("tab_reports"), False)]
    tx = 28
    for lab, active in tabs:
        col = C["brand"] if active else C["n500"]
        b.append(text(tx, ty + 29, lab, 14, col, weight=700 if active else 500))
        wlab = len(lab) * 8
        if active:
            b.append(rect(tx, ty + 42, wlab, 3, fill=C["brand"], rx=2))
        tx += wlab + 36

    y = ty + 46 + 22
    gap = 16
    cw = (W - 56 - gap * 3) / 4
    kpis = [(t("total_revenue"), money(874655.08), "trend", "success"),
            (t("transactions"), "219", "receipt", "info"),
            (t("avg_per_tx"), money(3993.86), "analytics", "warning"),
            (t("payment_methods"), t("types_3"), "payments", "accent")]
    for i, (lab, val, ic, ck) in enumerate(kpis):
        s, _ = kpi_card(28 + i * (cw + gap), y, cw, lab, val, ic, ck)
        b.append(s)

    py = y + 116 + 22
    ph = H - py - 24
    b.append(card(28, py, W - 56, ph))
    b.append(text(48, py + 30, t("payment_distribution"), 13, C["brand"], weight=700, spacing="0.5"))
    b.append(text(48, py + 50, t("payment_distribution_sub"), 13, C["n500"]))
    import math
    cx, cy = 200, py + 30 + (ph - 60) / 2 + 10
    r, rin = 78, 46
    segs = [(0.75, C["success"]), (0.125, C["teal"]), (0.125, C["info"])]
    a0 = -90
    for frac, col in segs:
        a1 = a0 + frac * 360
        large = 1 if frac > 0.5 else 0
        x0 = cx + r * math.cos(math.radians(a0)); y0 = cy + r * math.sin(math.radians(a0))
        x1 = cx + r * math.cos(math.radians(a1)); y1 = cy + r * math.sin(math.radians(a1))
        xi0 = cx + rin * math.cos(math.radians(a0)); yi0 = cy + rin * math.sin(math.radians(a0))
        xi1 = cx + rin * math.cos(math.radians(a1)); yi1 = cy + rin * math.sin(math.radians(a1))
        b.append(f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} '
                 f'L {xi1:.1f} {yi1:.1f} A {rin} {rin} 0 {large} 0 {xi0:.1f} {yi0:.1f} Z" fill="{col}"/>')
        a0 = a1
    b.append(text(cx, cy - 2, num(875) + "k" if LANG != "fr" else "874,7k", 22, C["n900"], weight=700, anchor="middle"))
    b.append(text(cx, cy + 18, t("total"), 13, C["n500"], anchor="middle"))

    lx = 360
    rows = [(t("cash"), 655633.29, "75,0%" if LANG != "en" else "75.0%", 0.75, C["success"]),
            (t("transfer"), 109613.58, "12,5%" if LANG != "en" else "12.5%", 0.125, C["teal"]),
            (t("credit_card"), 109408.21, "12,5%" if LANG != "en" else "12.5%", 0.125, C["info"])]
    ry = py + 70
    barw = W - 56 - lx - 40
    for lab, amt, pct, frac, col in rows:
        b.append(circle(lx + 6, ry + 6, 6, fill=col))
        b.append(text(lx + 22, ry + 11, lab, 14, C["n800"], weight=600))
        b.append(text(W - 76, ry + 11, money(amt), 14, C["n900"], weight=700, anchor="end"))
        b.append(rect(lx, ry + 22, barw, 8, fill=C["n100"], rx=4))
        b.append(rect(lx, ry + 22, max(10, barw * frac), 8, fill=col, rx=4))
        b.append(text(W - 76, ry + 46, pct, 12, C["n500"], anchor="end"))
        ry += 62
    return frame("".join(b), ab)


def screen_stock():
    ab, abh = back_appbar(t("product_mgmt"), actions=("scan", "tune", "sort"))
    b = []
    y = abh + 22
    gap = 16
    cw = (W - 56 - gap * 3) / 4
    kpis = [(t("total_products"), num(1482), "inventory", "info"),
            (t("low_stock"), "12", "warning", "warning"),
            (t("out_of_stock"), "3", "error", "danger"),
            (t("total_value"), money(156320, 0), "payments", "success")]
    for i, (lab, val, ic, ck) in enumerate(kpis):
        s, _ = kpi_card(28 + i * (cw + gap), y, cw, lab, val, ic, ck)
        b.append(s)

    fy = y + 116 + 18
    b.append(rect(28, fy, W - 56 - 200, 44, fill=C["n0"], rx=12, stroke=C["n200"]))
    b.append(icon("search", 42, fy + 11, 22, C["n400"]))
    b.append(text(74, fy + 28, t("search_product"), 14, C["n400"]))
    b.append(rect(W - 28 - 188, fy, 90, 44, fill=C["n0"], rx=12, stroke=C["n200"]))
    b.append(icon("sort", W - 28 - 178, fy + 11, 22, C["n600"]))
    b.append(text(W - 28 - 146, fy + 28, t("sort"), 14, C["n600"], weight=600))
    b.append(rect(W - 28 - 90, fy, 90, 44, fill=C["n0"], rx=12, stroke=C["n200"]))
    b.append(icon("tune", W - 28 - 80, fy + 11, 22, C["n600"]))
    b.append(text(W - 28 - 48, fy + 28, t("filters"), 14, C["n600"], weight=600))

    gy = fy + 44 + 18
    products = PRODUCTS[LANG]
    cols = 4
    cgap = 16
    pw = (W - 56 - cgap * (cols - 1)) / cols
    ph = (H - gy - 24 - cgap) / 2
    for i, (name, catkey, price, qty, st) in enumerate(products):
        cx = 28 + (i % cols) * (pw + cgap)
        cyy = gy + (i // cols) * (ph + cgap)
        b.append(card(cx, cyy, pw, ph))
        imgh = ph * 0.46
        b.append(rect(cx + 1, cyy + 1, pw - 2, imgh, fill="url(#imgGrad)", rx=15))
        b.append(rect(cx + 1, cyy + imgh - 15, pw - 2, 15, fill=C["brand50"]))
        b.append(product_art(KINDS_STOCK[i], cx + 1, cyy + 1, pw - 2, imgh, fill=0.92))
        if st == "out":
            b.append(status_chip(cx + pw - 16 - (16 + len(t("out_of_stock")) * 12 * 0.58), cyy + 12, t("out_of_stock"), C["n0"], C["danger"]))
        elif st == "low":
            lbl = t("left_qty", n=qty)
            b.append(status_chip(cx + pw - 16 - (16 + len(lbl) * 12 * 0.58), cyy + 12, lbl, C["n0"], C["warning"]))
        tyy = cyy + imgh + 24
        nm = name if len(name) <= 24 else name[:23] + "…"
        b.append(text(cx + 14, tyy, nm, 13.5, C["n900"], weight=700))
        cn = cat(catkey)
        b.append(rect(cx + 14, tyy + 12, 12 + len(cn) * 6.2, 18, fill=C["infoBg"], rx=9))
        b.append(text(cx + 20, tyy + 25, cn, 11, C["infoDark"], weight=600))
        b.append(text(cx + 14, tyy + 52, money(price), 15, C["success"], weight=700))
        stc = C["success"] if st == "ok" else (C["warning"] if st == "low" else C["danger"])
        b.append(text(cx + pw - 14, tyy + 52, t("stock_n", n=qty), 12, stc, weight=600, anchor="end"))

    b.append(circle(W - 64, H - 60, 30, fill=C["brand"]))
    b.append(icon("plus", W - 64 - 12, H - 60 - 12, 24, C["n0"], sw=2.4))
    return frame("".join(b), ab)


def screen_pos():
    ab, abh = back_appbar(t("new_sale"), actions=("scan", "quote"))
    b = []
    pad = 24
    topy = abh + pad
    leftw = 740
    b.append(rect(pad, topy, leftw, 44, fill=C["n0"], rx=12, stroke=C["n200"]))
    b.append(icon("search", pad + 14, topy + 11, 22, C["n400"]))
    b.append(text(pad + 46, topy + 28, t("search_product_dots"), 14, C["n400"]))
    b.append(icon("scan", pad + leftw - 38, topy + 11, 22, C["brand"]))

    gy = topy + 44 + 16
    prods = POS_PRODUCTS[LANG]
    cols = 4
    cgap = 14
    pw = (leftw - cgap * (cols - 1)) / cols
    ph = (H - gy - pad - cgap * 2) / 3
    for i, (nm, pr, unit) in enumerate(prods):
        cx = pad + (i % cols) * (pw + cgap)
        cyy = gy + (i // cols) * (ph + cgap)
        b.append(card(cx, cyy, pw, ph, shadow=False))
        ih = ph * 0.46
        b.append(rect(cx + 12, cyy + 12, pw - 24, ih, fill="url(#imgGrad)", rx=10, stroke=C["n100"]))
        b.append(product_art(KINDS_POS[i], cx + 12, cyy + 12, pw - 24, ih))
        nm2 = nm if len(nm) <= 18 else nm[:17] + "…"
        b.append(text(cx + 14, cyy + ph - 30, nm2, 12.5, C["n800"], weight=600))
        b.append(text(cx + 14, cyy + ph - 12, money(pr) + unit, 13, C["brand"], weight=700))

    rx0 = pad + leftw + 18
    rw = W - rx0 - pad
    b.append(card(rx0, topy, rw, H - topy - pad))
    b.append(icon("basket", rx0 + 18, topy + 16, 24, C["brand"]))
    b.append(text(rx0 + 50, topy + 33, t("cart"), 16, C["n900"], weight=700))
    b.append(status_chip(rx0 + 50 + len(t("cart")) * 9 + 16, topy + 18, "4", C["info"], C["infoBg"]))
    b.append(icon("close", rx0 + rw - 38, topy + 16, 22, C["danger"], sw=2))
    b.append(line(rx0 + 16, topy + 52, rx0 + rw - 16, topy + 52, C["n200"]))

    items = CART[LANG]
    sub = sum(q * p for _, q, p in items)
    iy = topy + 64
    for nm, q, p in items:
        b.append(rect(rx0 + 16, iy, rw - 32, 56, fill=C["n50"], rx=12))
        nm2 = nm if len(nm) <= 20 else nm[:19] + "…"
        b.append(text(rx0 + 28, iy + 22, nm2, 13.5, C["n900"], weight=600))
        b.append(text(rx0 + 28, iy + 42, f"{q} × {money(p)}", 12, C["n500"]))
        b.append(text(rx0 + rw - 28, iy + 22, money(q * p), 14, C["success"], weight=700, anchor="end"))
        b.append(rect(rx0 + rw - 92, iy + 32, 64, 18, fill=C["n0"], rx=9, stroke=C["n200"]))
        b.append(icon("minus", rx0 + rw - 88, iy + 33, 16, C["danger"], sw=2))
        b.append(text(rx0 + rw - 60, iy + 45, str(q), 12, C["n800"], weight=700, anchor="middle"))
        b.append(icon("plus", rx0 + rw - 46, iy + 33, 16, C["success"], sw=2))
        iy += 64

    vat = sub * 0.055
    sty = H - pad - 168
    b.append(line(rx0 + 16, sty, rx0 + rw - 16, sty, C["n200"]))
    b.append(text(rx0 + 24, sty + 26, t("subtotal_ht"), 13.5, C["n500"]))
    b.append(text(rx0 + rw - 24, sty + 26, money(sub), 13.5, C["n700"], weight=600, anchor="end"))
    b.append(text(rx0 + 24, sty + 50, t("vat"), 13.5, C["n500"]))
    b.append(text(rx0 + rw - 24, sty + 50, "+ " + money(vat), 13.5, C["warning"], weight=600, anchor="end"))
    b.append(text(rx0 + 24, sty + 80, t("total_ttc"), 16, C["n900"], weight=700))
    b.append(text(rx0 + rw - 24, sty + 80, money(sub + vat), 20, C["brand"], weight=700, anchor="end"))
    by = sty + 96
    b.append(rect(rx0 + 16, by, rw - 32, 46, fill=C["brand"], rx=12))
    lab = t("proceed_payment")
    b.append(icon("credit", rx0 + 16 + (rw - 32) / 2 - (len(lab) * 4 + 20), by + 12, 22, C["n0"], sw=2))
    b.append(text(rx0 + 16 + (rw - 32) / 2 + 14, by + 29, lab, 14.5, C["n0"], weight=700, anchor="middle"))
    return frame("".join(b), ab)


def _list_screen(title, filters, columns, rows, actions=("tune", "sort"), fab=True):
    ab, abh = back_appbar(title, actions=actions)
    b = []
    y = abh + 22
    fx = 28
    for lab, active in filters:
        w = 22 + len(lab) * 7.4
        col = C["n0"] if active else C["n600"]
        bg = C["brand"] if active else C["n0"]
        b.append(rect(fx, y, w, 32, fill=bg, rx=16, stroke=None if active else C["n200"]))
        b.append(text(fx + w / 2, y + 21, lab, 13, col, weight=600, anchor="middle"))
        fx += w + 10
    b.append(rect(W - 28 - 280, y, 280, 32, fill=C["n0"], rx=16, stroke=C["n200"]))
    b.append(icon("search", W - 28 - 270, y + 5, 22, C["n400"]))
    b.append(text(W - 28 - 240, y + 21, t("search_dots"), 13, C["n400"]))

    ty = y + 32 + 18
    b.append(card(28, ty, W - 56, H - ty - 24))
    widths = [c[1] for c in columns]
    accw = 28 + 26
    xs = []
    for w in widths:
        xs.append(accw)
        accw += w
    hy = ty + 34
    for (cl, w), x in zip(columns, xs):
        b.append(text(x, hy, cl, 12, C["n500"], weight=700, spacing="0.3"))
    b.append(line(44, hy + 14, W - 72, hy + 14, C["n200"]))
    ry = hy + 14
    rh = min((H - ty - 24 - (hy + 14 - ty)) / len(rows), 58)
    amount_cols = (t("col_amount_ttc"), t("col_amount"))
    for row in rows:
        ry2 = ry + rh / 2 + 5
        for (cl, w), x, val in zip(columns, xs, row):
            if isinstance(val, tuple):
                lab, ck = val
                b.append(status_chip(x, ry + rh / 2 - 11, lab, C[ck], tint(ck)))
            else:
                is_amt = cl in amount_cols
                is_num = cl == t("col_num") or cl == t("col_order_no")
                weight = 700 if (is_amt or is_num) else 500
                color = C["n900"] if (is_amt or is_num) else C["n700"]
                b.append(text(x, ry2, val, 13.5, color, weight=weight))
        b.append(line(44, ry + rh, W - 72, ry + rh, C["n100"]))
        ry += rh
    if fab:
        b.append(circle(W - 64, H - 60, 30, fill=C["brand"]))
        b.append(icon("plus", W - 64 - 12, H - 60 - 12, 24, C["n0"], sw=2.4))
    return frame("".join(b), ab)


def screen_invoicing():
    filters = [(t("all_f"), True), (t("st_paid"), False), (t("st_sent"), False),
               (t("st_draft"), False), (t("st_cancelled"), False)]
    cols = [(t("col_num"), 150), (t("col_customer"), 300), (t("col_date"), 180),
            (t("col_amount_ttc"), 200), (t("col_status"), 200)]
    data = [
        ("FAC-001", "Dupont SA", (15, 1, 2026), 1250.00, (t("st_paid"), "success")),
        ("FAC-002", "Martin EIRL", (14, 1, 2026), 89.50, (t("st_draft"), "warning")),
        ("FAC-003", "Leclerc Distribution", (13, 1, 2026), 3845.75, (t("st_sent"), "info")),
        ("FAC-004", "Boutique Centrale", (12, 1, 2026), 156.30, (t("st_cancelled"), "danger")),
        ("FAC-005", "Commerce XYZ", (11, 1, 2026), 2100.00, (t("st_paid"), "success")),
        ("FAC-006", "Épicerie du Coin", (10, 1, 2026), 445.99, (t("st_sent"), "info")),
        ("FAC-007", "Restaurant Le Midi", (9, 1, 2026), 678.40, (t("st_paid"), "success")),
    ]
    rows = [(n, c, datestr(*d), money(a), st) for n, c, d, a, st in data]
    return _list_screen(t("invoices"), filters, cols, rows)


def screen_quotes():
    filters = [(t("all_m"), True), (t("qs_sent"), False), (t("qs_accepted"), False),
               (t("qs_converted"), False), (t("qs_expired"), False)]
    cols = [(t("col_num"), 150), (t("col_customer"), 280), (t("col_items"), 120),
            (t("col_date"), 170), (t("col_amount"), 180), (t("col_status"), 180)]
    data = [
        ("DEV-001", "Dupont SA", 3, (15, 1, 2026), 2500.00, (t("qs_converted"), "success")),
        ("DEV-002", "Martin EIRL", 5, (14, 1, 2026), 750.00, (t("qs_sent"), "info")),
        ("DEV-003", "Leclerc Distribution", 2, (13, 1, 2026), 1200.50, (t("qs_accepted"), "teal")),
        ("DEV-004", "Boutique XYZ", 1, (12, 1, 2026), 89.99, (t("qs_draft"), "warning")),
        ("DEV-005", "Commerce ABC", 12, (11, 1, 2026), 5600.00, (t("qs_expired"), "warning")),
        ("DEV-006", "Café Central", 4, (10, 1, 2026), 320.00, (t("qs_sent"), "info")),
        ("DEV-007", "Hôtel Bellevue", 8, (9, 1, 2026), 3180.00, (t("qs_accepted"), "teal")),
    ]
    rows = []
    for n, c, it, d, a, st in data:
        itlbl = t("n_item", n=it) if it == 1 else t("n_items", n=it)
        rows.append((n, c, itlbl, datestr(*d), money(a), st))
    return _list_screen(t("quotes"), filters, cols, rows)


def screen_purchasing():
    filters = [(t("all_f"), True), (t("ps_received"), False), (t("ps_draft"), False), (t("ps_cancelled"), False)]
    cols = [(t("col_order_no"), 180), (t("col_supplier"), 320), (t("col_date"), 180),
            (t("col_amount_ttc"), 200), (t("col_status"), 200)]
    data = [
        ("ACH-001", "Fournitures Pro SARL", (15, 6, 2026), 2450.00, (t("ps_received"), "success")),
        ("ACH-002", "Électro Distribution", (18, 6, 2026), 1875.50, (t("ps_draft"), "warning")),
        ("ACH-003", "Emballages Plus", (10, 6, 2026), 890.75, (t("ps_cancelled"), "danger")),
        ("ACH-004", "Produits Bio France", (20, 6, 2026), 3200.25, (t("ps_received"), "success")),
        ("ACH-005", "Accessoires Import", (22, 6, 2026), 1125.00, (t("ps_draft"), "warning")),
        ("ACH-006", "Grossiste Méditerranée", (8, 6, 2026), 4760.00, (t("ps_received"), "success")),
        ("ACH-007", "Distrib Centrale", (5, 6, 2026), 612.40, (t("ps_received"), "success")),
    ]
    rows = [(n, s_, datestr(*d), money(a), st) for n, s_, d, a, st in data]
    return _list_screen(t("purchases"), filters, cols, rows)


def screen_document_emailing():
    ab, abh = back_appbar(t("invoice_no"), actions=("download", "print"))
    b = []
    pad = 24
    topy = abh + pad
    docw = 560
    b.append(card(pad, topy, docw, H - topy - pad))
    dx = pad + 36
    b.append(text(dx, topy + 50, t("invoice_word"), 22, C["n900"], weight=700, spacing="1"))
    b.append(text(dx, topy + 72, t("invoice_ref"), 13, C["n500"]))
    b.append(rect(pad + docw - 36 - 60, topy + 30, 60, 60, fill=C["brand50"], rx=12))
    b.append(icon("logo", pad + docw - 36 - 48, topy + 42, 36, C["brand"]))
    b.append(line(dx, topy + 92, pad + docw - 36, topy + 92, C["n200"]))
    b.append(text(dx, topy + 120, t("from"), 11, C["n400"], weight=700, spacing="0.4"))
    b.append(text(dx, topy + 140, t("demo_company"), 14, C["n900"], weight=600))
    b.append(text(dx, topy + 158, t("demo_address"), 12, C["n500"]))
    b.append(text(pad + docw - 36, topy + 120, t("to_customer"), 11, C["n400"], weight=700, spacing="0.4", anchor="end"))
    b.append(text(pad + docw - 36, topy + 140, "Dupont SA", 14, C["n900"], weight=600, anchor="end"))
    b.append(text(pad + docw - 36, topy + 158, "contact@dupont.fr", 12, C["n500"], anchor="end"))
    ly = topy + 188
    b.append(rect(dx, ly, docw - 72, 26, fill=C["n100"], rx=6))
    b.append(text(dx + 12, ly + 18, t("col_designation"), 11, C["n600"], weight=700))
    b.append(text(pad + docw - 200, ly + 18, t("col_qty"), 11, C["n600"], weight=700))
    b.append(text(pad + docw - 48, ly + 18, t("total"), 11, C["n600"], weight=700, anchor="end"))
    ry = ly + 26
    for nm, q, tot in DOC_ROWS[LANG]:
        ry += 32
        b.append(text(dx + 12, ry, nm, 12.5, C["n800"]))
        b.append(text(pad + docw - 196, ry, str(q), 12.5, C["n600"]))
        b.append(text(pad + docw - 48, ry, money(tot), 12.5, C["n900"], weight=600, anchor="end"))
        b.append(line(dx, ry + 12, pad + docw - 36, ry + 12, C["n100"]))
    b.append(text(pad + docw - 230, ry + 44, t("total_ttc"), 14, C["n900"], weight=700))
    b.append(text(pad + docw - 36, ry + 44, money(1250.00), 16, C["brand"], weight=700, anchor="end"))

    ex = pad + docw + 20
    ew = W - ex - pad
    b.append(card(ex, topy, ew, H - topy - pad))
    icx = ex + ew / 2
    b.append(icon_chip(icx - 30, topy + 30, 60, "email", C["brand"], C["brand50"], rx=16))
    b.append(text(icx, topy + 118, t("send_by_email"), 18, C["n900"], weight=700, anchor="middle"))
    b.append(text(icx, topy + 140, t("pdf_auto"), 13, C["n500"], anchor="middle"))

    def field(label, val, yy):
        out = [text(ex + 28, yy, label, 12, C["n500"], weight=600)]
        out.append(rect(ex + 28, yy + 8, ew - 56, 42, fill=C["n50"], rx=10, stroke=C["n200"]))
        out.append(text(ex + 42, yy + 34, val, 13.5, C["n800"], weight=500))
        return "".join(out)
    fy = topy + 168
    b.append(field(t("recipient"), "contact@dupont.fr", fy))
    b.append(field(t("subject"), t("subject_val"), fy + 66))
    b.append(text(ex + 28, fy + 132, t("message"), 12, C["n500"], weight=600))
    b.append(rect(ex + 28, fy + 140, ew - 56, 66, fill=C["n50"], rx=10, stroke=C["n200"]))
    b.append(text(ex + 42, fy + 164, t("msg_l1"), 13, C["n600"]))
    b.append(text(ex + 42, fy + 184, t("msg_l2"), 13, C["n600"]))
    ay = fy + 222
    b.append(rect(ex + 28, ay, ew - 56, 44, fill=C["dangerBg"], rx=10))
    b.append(icon("pdf", ex + 42, ay + 10, 24, C["danger"]))
    b.append(text(ex + 74, ay + 28, t("pdf_name"), 13, C["dangerDark"], weight=600))
    by = ay + 60
    b.append(rect(ex + 28, by, ew - 56, 48, fill=C["brand"], rx=12))
    b.append(icon("email", icx - (len(t("send")) * 4 + 50), by + 13, 22, C["n0"], sw=2))
    b.append(text(icx + 14, by + 30, t("send"), 15, C["n0"], weight=700, anchor="middle"))
    return frame("".join(b), ab)


def screen_loyalty():
    ab, abh = back_appbar(t("customer_loyalty"), actions=("history",))
    b = []
    pad = 24
    topy = abh + pad
    cw = 440
    ch = 200
    b.append(f'<rect x="{pad}" y="{topy}" width="{cw}" height="{ch}" rx="20" fill="url(#appbar)" filter="url(#floatShadow)"/>')
    b.append(icon("gift", pad + 28, topy + 28, 36, C["n0"], sw=2))
    b.append(text(pad + 28, topy + 96, "Jean Dupont", 17, C["n0"], weight=600, opacity=0.95))
    b.append(text(pad + 28, topy + 140, num(1250), 46, C["n0"], weight=700))
    b.append(text(pad + 28 + (len(num(1250)) * 28) + 12, topy + 140, t("points"), 16, C["n0"], opacity=0.9))
    b.append(text(pad + 28, topy + 168, t("redeemable", v=money(31.25)), 14, C["n0"], opacity=0.92))

    kx = pad + cw + 20
    kw = (W - kx - pad - 16) / 2
    mini = [(t("points_earned"), "+ " + num(2480), "trend", "success"),
            (t("points_used"), "- 350", "return", "danger")]
    for i, (lab, val, ic, ck) in enumerate(mini):
        x = kx + i * (kw + 16)
        b.append(card(x, topy, kw, 92))
        b.append(icon_chip(x + 16, topy + 16, 36, ic, C[ck], tint(ck), rx=10))
        b.append(text(x + 64, topy + 40, val, 22, C["n900"], weight=700))
        b.append(text(x + 64, topy + 62, lab, 12.5, C["n500"], weight=500))
    b.append(card(kx, topy + 108, kw * 2 + 16, 92))
    b.append(text(kx + 18, topy + 134, t("gold_tier"), 14, C["n900"], weight=700))
    b.append(text(kx + kw * 2 + 16 - 18, topy + 134, t("tier_progress"), 13, C["n500"], anchor="end"))
    b.append(rect(kx + 18, topy + 148, kw * 2 + 16 - 36, 12, fill=C["n100"], rx=6))
    b.append(rect(kx + 18, topy + 148, (kw * 2 + 16 - 36) * 0.83, 12, fill=C["gold"], rx=6))
    b.append(text(kx + 18, topy + 184, t("to_platinum"), 12.5, C["n500"]))

    hy = topy + ch + 24
    b.append(card(pad, hy, W - 2 * pad, H - hy - pad))
    b.append(text(pad + 24, hy + 34, t("points_history"), 15, C["n900"], weight=700))
    b.append(line(pad + 24, hy + 48, W - pad - 24, hy + 48, C["n200"]))
    hist = [
        ("add", t("loy_purchase", r="VTE-2026-001"), (20, 6, 2026, "14:30"), "+ 450", C["success"]),
        ("add", t("loy_purchase", r="VTE-2026-012"), (19, 6, 2026, "11:15"), "+ 280", C["success"]),
        ("return", t("loy_discount", r="VTE-2026-018"), (18, 6, 2026, "09:45"), "- 200", C["danger"]),
        ("return", t("loy_discount", r="VTE-2026-025"), (17, 6, 2026, "16:20"), "- 150", C["danger"]),
        ("add", t("loy_adjust"), (15, 6, 2026, "10:00"), "+ 50", C["success"]),
    ]
    ry = hy + 48
    rh = min((H - hy - pad - 48) / len(hist), 56)
    for ic, lab, dt, pts, col in hist:
        cyy = ry + rh / 2
        bgc = C["successBg"] if col == C["success"] else C["dangerBg"]
        b.append(icon_chip(pad + 24, cyy - 18, 36, "plus" if ic == "add" else "minus", col, bgc, rx=18))
        b.append(text(pad + 74, cyy - 2, lab, 13.5, C["n900"], weight=600))
        b.append(text(pad + 74, cyy + 16, f"{datestr(dt[0], dt[1], dt[2])}  {dt[3]}", 12, C["n400"]))
        b.append(text(W - pad - 24, cyy + 5, f"{pts} {t('pts')}", 15, col, weight=700, anchor="end"))
        b.append(line(pad + 24, ry + rh, W - pad - 24, ry + rh, C["n100"]))
        ry += rh
    return frame("".join(b), ab)


def screen_accounting():
    ab, abh = back_appbar(t("accounting"), actions=("calendar", "download"))
    b = []
    pad = 24
    y = abh + 20
    b.append(rect(pad, y, 260, 34, fill=C["n0"], rx=10, stroke=C["n200"]))
    b.append(icon("calendar", pad + 10, y + 6, 22, C["brand"]))
    b.append(text(pad + 42, y + 22, t("period_demo"), 13, C["n700"], weight=600))

    gy = y + 34 + 18
    cols = 3
    gap = 16
    cw = (W - 2 * pad - gap * (cols - 1)) / cols
    kpis = [(t("net_revenue_ht"), money(452305, 0), "trend", "success"),
            (t("gross_margin"), money(180922, 0), "bars", "info"),
            (t("cogs"), money(271383, 0), "inventory", "warning"),
            (t("vat_payable"), money(8549, 0), "receipt_long", "accent"),
            (t("net_cash"), money(124508, 0), "wallet", "teal"),
            (t("stock_value_cost"), money(156320, 0), "warehouse", "brand")]
    ch = 104
    for i, (lab, val, ic, ck) in enumerate(kpis):
        x = pad + (i % cols) * (cw + gap)
        cyy = gy + (i // cols) * (ch + gap)
        b.append(card(x, cyy, cw, ch))
        b.append(icon_chip(x + 18, cyy + 18, 38, ic, C[ck], tint(ck), rx=10))
        b.append(text(x + 18, cyy + 78, val, 24, C["n900"], weight=700))
        b.append(text(x + 18, cyy + 96, lab, 12.5, C["n500"], weight=500))

    sy = gy + 2 * ch + gap + 12
    sh = H - sy - pad
    b.append(card(pad, sy, W - 2 * pad, sh))
    b.append(text(pad + 24, sy + 32, t("vat_summary"), 15, C["n900"], weight=700))
    seg = (W - 2 * pad) / 3
    items = [(t("vat_collected"), money(8900.00), C["info"]),
             (t("vat_deductible"), money(351.90), C["warning"]),
             (t("vat_payable"), money(8549.10), C["accent"])]
    for i, (lab, val, col) in enumerate(items):
        x = pad + 24 + i * seg
        b.append(circle(x + 6, sy + 62, 6, fill=col))
        b.append(text(x + 22, sy + 67, lab, 13.5, C["n600"], weight=500))
        b.append(text(x, sy + 100, val, 22, col, weight=700))
        if i < 2:
            b.append(line(pad + i * seg + seg + 12, sy + 48, pad + i * seg + seg + 12, sy + 110, C["n200"]))
    b.append(line(pad + 24, sy + 132, W - pad - 24, sy + 132, C["n100"]))
    b.append(text(pad + 24, sy + 162, t("quick_links"), 12, C["n500"], weight=700, spacing="0.6"))
    links = [(t("income_statement"), "bars", "info"), (t("vat_report"), "receipt_long", "accent"),
             (t("cash_flow"), "wallet", "teal"), (t("sales_detail"), "list_alt", "warning")]
    lgap = 16
    lw = (W - 2 * pad - 48 - lgap * 3) / 4
    ly = sy + 178
    for i, (lab, ic, ck) in enumerate(links):
        x = pad + 24 + i * (lw + lgap)
        b.append(rect(x, ly, lw, 56, fill=C["n50"], rx=12, stroke=C["n200"]))
        b.append(icon_chip(x + 14, ly + 12, 32, ic, C[ck], tint(ck), rx=9))
        lab2 = lab if len(lab) <= 22 else lab[:21] + "…"
        b.append(text(x + 56, ly + 33, lab2, 13, C["n800"], weight=600))
    return frame("".join(b), ab)


def screen_cashier_performance():
    ab, abh = back_appbar(t("cashier_perf"), actions=("calendar", "download"))
    b = []
    pad = 24
    y = abh + 20
    gap = 16
    cw = (W - 2 * pad - gap * 3) / 4
    kpis = [(t("total_revenue"), money(125450.80), "payments", "success"),
            (t("total_sales"), "287", "receipt_long", "info"),
            (t("active_cashiers"), "8", "groups", "accent"),
            (t("refunds"), "12", "return", "warning")]
    for i, (lab, val, ic, ck) in enumerate(kpis):
        s, _ = kpi_card(pad + i * (cw + gap), y, cw, lab, val, ic, ck)
        b.append(s)

    gy = y + 116 + 18
    gh = H - gy - pad
    chartw = 520
    b.append(card(pad, gy, chartw, gh))
    b.append(text(pad + 24, gy + 32, t("revenue_per_cashier"), 14, C["n900"], weight=700))
    bars = [("AM", 0.92, C["gold"]), ("BD", 0.80, C["brand"]), ("CL", 0.67, C["brand"]),
            ("DP", 0.58, C["brand"]), ("EB", 0.50, C["brand"]), ("FR", 0.41, C["brand"]),
            ("GM", 0.33, C["brand"]), ("HT", 0.24, C["brand"])]
    bx = pad + 40
    baseY = gy + gh - 44
    bw = (chartw - 80) / len(bars) - 12
    maxh = gh - 90
    for lab, frac, col in bars:
        bh = maxh * frac
        b.append(rect(bx, baseY - bh, bw, bh, fill=col, rx=6))
        b.append(text(bx + bw / 2, baseY + 18, lab, 11, C["n500"], weight=600, anchor="middle"))
        bx += bw + 12

    rx0 = pad + chartw + 20
    rw = W - rx0 - pad
    b.append(card(rx0, gy, rw, gh))
    b.append(text(rx0 + 24, gy + 32, t("cashier_ranking"), 14, C["n900"], weight=700))
    b.append(line(rx0 + 24, gy + 46, rx0 + rw - 24, gy + 46, C["n200"]))
    rank = [
        (1, "Alice Martin", 45, 45.50, 2047.50, C["gold"]),
        (2, "Bernard Durand", 42, 41.30, 1734.60, C["silver"]),
        (3, "Christine Leroy", 38, 38.20, 1451.60, C["bronze"]),
        (4, "David Petit", 35, 36.15, 1265.25, C["n400"]),
        (5, "Éva Blanc", 32, 33.80, 1081.60, C["n400"]),
    ]
    ry = gy + 46
    rh = min((gh - 46 - 12) / len(rank), 64)
    for rk, nm, sales, avg, ca, col in rank:
        cyy = ry + rh / 2
        b.append(circle(rx0 + 42, cyy, 16, fill=col))
        b.append(text(rx0 + 42, cyy + 5, str(rk), 14, C["n0"], weight=700, anchor="middle"))
        b.append(text(rx0 + 72, cyy - 4, nm, 14, C["n900"], weight=600))
        b.append(text(rx0 + 72, cyy + 14, t("sales_avg", s=sales, a=money(avg)), 12, C["n500"]))
        b.append(text(rx0 + rw - 24, cyy + 5, money(ca), 15, C["success"], weight=700, anchor="end"))
        b.append(line(rx0 + 24, ry + rh, rx0 + rw - 24, ry + rh, C["n100"]))
        ry += rh
    return frame("".join(b), ab)


SCREENS = {
    "screenhot_app": screen_dashboard,
    "dashboards-reports": screen_transactions,
    "stock-management": screen_stock,
    "pos-checkout": screen_pos,
    "invoicing": screen_invoicing,
    "quotes": screen_quotes,
    "document-emailing": screen_document_emailing,
    "loyalty": screen_loyalty,
    "accounting": screen_accounting,
    "purchasing": screen_purchasing,
    "cashier-performance": screen_cashier_performance,
}


def main():
    global LANG
    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    for lang in LANGS:
        LANG = lang
        suffix = "" if lang == "fr" else f".{lang}"
        for name, fn in SCREENS.items():
            svg = fn()
            path = os.path.join(OUT_DIR, f"{name}{suffix}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            total += 1
        print(f"  {lang}: {len(SCREENS)} thumbnails")
    print(f"OK - {total} SVG generes ({len(SCREENS)} ecrans x {len(LANGS)} langues) dans {OUT_DIR}")


if __name__ == "__main__":
    main()
