#!/usr/bin/env python3
"""Gera a página de links + cardápio da Churrascaria Brasil (BR5).
Uso: python3 _gerador/build.py  -> reescreve index.html, 404.html, robots.txt, sitemap.xml e llms.txt na raiz do site
Para trocar o domínio, altere SITE_URL e rode de novo."""
import json, re, unicodedata, html
from pathlib import Path
from data import MENU

SITE_URL = "https://churrascariabrasil.github.io/"  # trocar pelo domínio final
NAME = "Lanchonete, Churrascaria e Pizzaria Brasil"
WHATS = "5575992140916"
PHONE_DISPLAY = "(75) 99214-0916"
INSTA = "https://www.instagram.com/churrascariabrasill/"
MAPS = "https://www.google.com/maps/place/Lanchonete,+Churrascaria+e+Pizzaria+Brasil/@-10.9757599,-38.7941972,17z/data=!4m6!3m5!1s0x71223be39fcfa05:0x5e86154c583b7c29!8m2!3d-10.9757599!4d-38.7941972"
LAT, LNG = -10.975649324676777, -38.793794930841116
TITLE = "Churrascaria Brasil em Tucano-BA | Cardápio, churrasco, pizzas e lanches"
DESC = ("Cardápio da Lanchonete, Churrascaria e Pizzaria Brasil (BR5) em Tucano, Bahia: churrasco e self-service "
        "por quilo, pratos do dia, pizzas, hambúrgueres, tapiocas, doces e bebidas. Lanchonete 24 horas. "
        "Área kids grátis. Peça pelo WhatsApp (75) 99214-0916.")
DAYS = ["", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

HERE = Path(__file__).parent
# No repositório o gerador fica em _gerador/ e escreve na raiz; aqui, em ./site
OUT = HERE.parent if HERE.name == "_gerador" else HERE / "site"
e = lambda s: html.escape(str(s), quote=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


ICONS = """<svg class="sprite" width="0" height="0" aria-hidden="true">
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" d="M3.4 20.6l1.3-4.3A8.7 8.7 0 1 1 7.9 19.4z"/><path fill="currentColor" transform="translate(12.1 11.5) scale(.43) translate(-12 -12)" d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.98.98 0 0 0-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 4.5h11.5a2 2 0 0 1 2 2v13H7a2 2 0 0 1-2-2zM5 17.5a2 2 0 0 1 2-2h11.5M9 8.5h6M9 11.5h4"/></symbol>
<symbol id="i-ig" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3.6" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="16.8" cy="7.2" r="1" fill="currentColor"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M6.5 4h2.6l1.4 3.6-1.8 1.2a9.5 9.5 0 0 0 4.5 4.5l1.2-1.8L18 13v2.6A2.4 2.4 0 0 1 15.4 18 11.5 11.5 0 0 1 4 6.6 2.4 2.4 0 0 1 6.5 4z"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M10 7l5 5-5 5"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6" fill="none" stroke="currentColor" stroke-width="1.8"/><path stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M15.5 15.5L20 20"/></symbol>
<symbol id="i-bag" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" d="M5.5 8h13l-1 12h-11zM9 8V6.5a3 3 0 0 1 6 0V8"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 6v12M6 12h12"/></symbol>
<symbol id="i-minus" viewBox="0 0 24 24"><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M6 12h12"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M7 7l10 10M17 7L7 17"/></symbol>
</svg>"""


def icon(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def render_item(cat, sec, item, idx):
    iid = f"{cat['id']}-{slug(sec['title'])}-{slug(item['name'])}-{idx}"
    prices = item["prices"]
    orderable = item.get("order", True)
    search = norm(" ".join([item["name"], item["desc"], sec["title"], cat["title"]] + [p[0] for p in prices]))
    attrs = f'class="item" id="{iid}" data-name="{e(item["name"])}" data-search="{e(search)}"'
    if "day" in item:
        attrs += f' data-day="{item["day"]}"'
    head = f'<span class="item-name">{e(item["name"])}</span>'
    if "day" in item:
        head = f'<span class="item-day">{DAYS[item["day"]]}</span>' + head
    body = head
    if item["desc"]:
        body += f'<span class="item-desc">{e(item["desc"])}</span>'
    unit = item.get("unit", "")
    same = len(prices) > 1 and len({p[1] for p in prices}) == 1
    if not orderable:
        opts = f'<span class="price-static">{brl(prices[0][1])}<small>{e(unit)}</small></span>'
    elif len(prices) == 1 and not prices[0][0]:
        p = prices[0][1]
        opts = (f'<button type="button" class="add add-single" data-id="{iid}" data-label="" data-price="{p:.2f}" '
                f'aria-label="Adicionar {e(item["name"])} à sacola, {brl(p)}">'
                f'<span class="price">{brl(p)}</span>{icon("plus", "ic ic-plus")}</button>')
    else:
        btns = []
        for label, p in prices:
            txt = f'<span class="v-label">{e(label)}</span>' if same else f'<span class="v-label">{e(label)}</span><span class="v-price">{brl(p)}</span>'
            btns.append(f'<button type="button" class="add add-var" data-id="{iid}" data-label="{e(label)}" data-price="{p:.2f}" '
                        f'aria-label="Adicionar {e(item["name"])} {e(label)} à sacola, {brl(p)}">{txt}</button>')
        lead = f'<span class="price-lead">{brl(prices[0][1])} cada</span>' if same else ""
        opts = f'{lead}<div class="variants">{"".join(btns)}</div>'
    cls_row = "item-row" + (" item-row--wide" if len(prices) > 1 else "")
    return f'<li {attrs}><div class="{cls_row}"><div class="item-text">{body}</div><div class="item-opts">{opts}</div></div></li>'


def render_menu():
    chips, cats = [], []
    for ci, cat in enumerate(MENU):
        chips.append(f'<button type="button" class="chip" data-cat="{cat["id"]}" aria-pressed="{"true" if ci == 0 else "false"}">{e(cat["short"])}</button>')
        secs = []
        for sec in cat["sections"]:
            sid = f'{cat["id"]}-{slug(sec["title"])}'
            items = "".join(render_item(cat, sec, it, i) for i, it in enumerate(sec["items"]))
            note = f'<p class="sec-note">{e(sec["note"])}</p>' if sec.get("note") else ""
            heading = "" if sec["title"] == cat["title"] else f'<h4 class="sec-title" id="{sid}-t">{e(sec["title"])}</h4>'
            secs.append(f'<section class="menu-sec" aria-labelledby="{sid}-t">{heading}{note}<ul class="items" role="list">{items}</ul></section>'
                        if heading else f'<section class="menu-sec">{note}<ul class="items" role="list">{items}</ul></section>')
        cats.append(f'<section class="cat" id="cat-{cat["id"]}" data-cat="{cat["id"]}" aria-labelledby="cat-{cat["id"]}-t">'
                    f'<h3 class="cat-title" id="cat-{cat["id"]}-t">{e(cat["title"])}</h3>{"".join(secs)}</section>')
    return "".join(chips), "".join(cats)


def jsonld():
    sections = []
    for cat in MENU:
        for sec in cat["sections"]:
            items = []
            for it in sec["items"]:
                offers = [{"@type": "Offer", "price": f"{p:.2f}", "priceCurrency": "BRL", **({"name": l} if l else {})} for l, p in it["prices"]]
                d = {"@type": "MenuItem", "name": it["name"] + (f" ({DAYS[it['day']]})" if "day" in it else ""), "offers": offers if len(offers) > 1 else offers[0]}
                if it["desc"]:
                    d["description"] = it["desc"]
                items.append(d)
            sections.append({"@type": "MenuSection", "name": f'{cat["title"]}: {sec["title"]}' if sec["title"] != cat["title"] else cat["title"], "hasMenuItem": items})
    data = {
        "@context": "https://schema.org",
        "@type": ["Restaurant", "FastFoodRestaurant"],
        "@id": SITE_URL + "#restaurante",
        "name": NAME,
        "alternateName": ["Churrascaria Brasil", "BR5", "Pizzaria Brasil"],
        "url": SITE_URL,
        "logo": SITE_URL + "assets/logo-512.png",
        "image": SITE_URL + "assets/og.jpg",
        "description": DESC,
        "telephone": "+55-75-99214-0916",
        "servesCuisine": ["Churrasco", "Comida brasileira", "Comida nordestina", "Pizza", "Hambúrguer", "Lanches", "Doces"],
        "priceRange": "R$",
        "acceptsReservations": False,
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "Área kids gratuita", "value": True}],
        "address": {"@type": "PostalAddress", "addressLocality": "Tucano", "addressRegion": "BA", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
        "hasMap": MAPS,
        "sameAs": [INSTA],
        "potentialAction": {"@type": "OrderAction", "target": f"https://wa.me/{WHATS}"},
        "hasMenu": {"@type": "Menu", "name": "Cardápio", "url": SITE_URL + "#cardapio", "inLanguage": "pt-BR", "hasMenuSection": sections},
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def build():
    chips, cats = render_menu()
    tpl = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    page = (tpl.replace("{{ICONS}}", ICONS).replace("{{CHIPS}}", chips).replace("{{MENU}}", cats)
            .replace("{{JSONLD}}", jsonld()).replace("{{TITLE}}", e(TITLE)).replace("{{DESC}}", e(DESC))
            .replace("{{URL}}", SITE_URL).replace("{{WHATS}}", WHATS).replace("{{PHONE}}", PHONE_DISPLAY)
            .replace("{{INSTA}}", INSTA).replace("{{MAPS}}", e(MAPS)))
    (OUT / "index.html").write_text(page, encoding="utf-8")
    for f in ["404.html", "robots.txt", "sitemap.xml", "llms.txt"]:
        src = Path(__file__).parent / "static" / f
        (OUT / f).write_text(src.read_text(encoding="utf-8").replace("{{URL}}", SITE_URL), encoding="utf-8")
    n = sum(len(s["items"]) for c in MENU for s in c["sections"])
    print("ok", n, "itens,", len(page) // 1024, "KB")


if __name__ == "__main__":
    build()
