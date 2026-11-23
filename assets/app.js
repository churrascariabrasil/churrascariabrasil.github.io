/* Churrascaria Brasil (BR5) — cardápio, busca, prato do dia e sacola para WhatsApp.
   Sem dependências e sem servidor: nada sai do aparelho até o cliente tocar em "Enviar". */
(() => {
  "use strict";

  const WHATS = "5575992140916";
  const FEE = 3;
  const STORE_KEY = "br5-sacola-v1";
  const MAX_QTY = 99;
  const DAYS = ["", "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"];

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const brl = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  const norm = (s) => s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
  const clean = (s, max) => String(s || "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);

  /* Eventos de conversão: funcionam com Google Tag Manager / GA4 se forem instalados depois. */
  const track = (name, params = {}) => {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: name, ...params });
      if (typeof window.gtag === "function") window.gtag("event", name, params);
    } catch (_) { /* sem analytics */ }
  };
  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("[data-evt]");
    if (a) track(a.dataset.evt, { label: a.dataset.evtLabel || "" });
  });

  /* ---------- Toast ---------- */
  const toastEl = $("#toast");
  let toastT;
  const toast = (msg) => {
    toastEl.textContent = msg;
    toastEl.classList.add("is-on");
    clearTimeout(toastT);
    toastT = setTimeout(() => toastEl.classList.remove("is-on"), 1800);
  };

  /* ---------- Categorias e busca ---------- */
  const cats = $$(".cat");
  const chips = $$(".chip");
  const chipsBar = $(".chips");
  const q = $("#q");
  const empty = $("#empty");
  const tools = $(".menu-tools");
  let current = chips[0] ? chips[0].dataset.cat : null;

  const showCat = (id) => {
    current = id;
    chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.cat === id)));
    cats.forEach((c) => { c.hidden = c.dataset.cat !== id; });
  };

  chips.forEach((chip) => chip.addEventListener("click", () => {
    if (q.value) { q.value = ""; applySearch(); }
    showCat(chip.dataset.cat);
    chip.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    const top = tools.getBoundingClientRect().top + window.scrollY - 1;
    if (window.scrollY > top) window.scrollTo({ top, behavior: "smooth" });
    track("menu_category", { category: chip.dataset.cat });
  }));

  const applySearch = () => {
    const term = norm(q.value);
    chipsBar.classList.toggle("is-search", !!term);
    if (!term) {
      $$(".item, .menu-sec").forEach((el) => { el.hidden = false; });
      empty.hidden = true;
      showCat(current);
      return;
    }
    const words = term.split(/\s+/);
    let total = 0;
    cats.forEach((cat) => {
      let catHits = 0;
      $$(".menu-sec", cat).forEach((sec) => {
        let secHits = 0;
        $$(".item", sec).forEach((it) => {
          const hit = words.every((w) => it.dataset.search.includes(w));
          it.hidden = !hit;
          if (hit) secHits++;
        });
        sec.hidden = secHits === 0;
        catHits += secHits;
      });
      cat.hidden = catHits === 0;
      total += catHits;
    });
    empty.hidden = total > 0;
  };
  let searchT;
  q.addEventListener("input", () => {
    clearTimeout(searchT);
    searchT = setTimeout(() => {
      applySearch();
      if (q.value.length > 2) track("menu_search", { term: q.value.slice(0, 40) });
    }, 120);
  });

  /* Borda na barra de busca quando ela gruda no topo */
  if ("IntersectionObserver" in window) {
    const sentinel = document.createElement("div");
    tools.before(sentinel);
    new IntersectionObserver(([e]) => tools.classList.toggle("is-stuck", !e.isIntersecting)).observe(sentinel);
  }

  /* ---------- Prato do dia ---------- */
  const todayNum = (() => {
    try {
      const wd = new Intl.DateTimeFormat("en-US", { weekday: "short", timeZone: "America/Bahia" }).format(new Date());
      return { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 }[wd] || 0;
    } catch (_) {
      const d = new Date().getDay();
      return d === 0 ? 7 : d;
    }
  })();
  const todayItems = $$(`.item[data-day="${todayNum}"]`);
  if (todayItems.length) {
    const box = $("#today");
    const eyebrow = document.createElement("p");
    eyebrow.className = "today-eyebrow";
    eyebrow.textContent = `Hoje é ${DAYS[todayNum]}`;
    const title = document.createElement("p");
    title.className = "today-title";
    title.textContent = todayItems.length > 1 ? "Pratos do dia no almoço" : "Prato do dia no almoço";
    const ul = document.createElement("ul");
    ul.className = "today-list";
    ul.setAttribute("role", "list");
    todayItems.forEach((it) => {
      it.classList.add("is-today");
      const li = document.createElement("li");
      const name = document.createElement("span");
      name.textContent = it.dataset.name;
      li.append(name);
      const btn = $(".add", it);
      if (btn) li.append(btn.cloneNode(true));
      ul.append(li);
    });
    box.append(eyebrow, title, ul);
    box.hidden = false;
  }

  /* ---------- Sacola ---------- */
  // Índice dos itens válidos lido do próprio HTML: preço e nome nunca vêm do armazenamento.
  const catalog = new Map();
  $$(".item .add").forEach((b) => {
    const item = b.closest(".item");
    const key = `${b.dataset.id}|${b.dataset.label}`;
    if (!catalog.has(key)) catalog.set(key, { name: item.dataset.name, label: b.dataset.label, price: Number(b.dataset.price) });
  });

  let bag = new Map(); // key -> qty
  const load = () => {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || "[]");
      if (!Array.isArray(raw)) return;
      raw.slice(0, 200).forEach((row) => {
        if (!Array.isArray(row) || typeof row[0] !== "string") return;
        const qty = Math.floor(Number(row[1]));
        if (catalog.has(row[0]) && qty >= 1) bag.set(row[0], Math.min(qty, MAX_QTY));
      });
    } catch (_) { bag = new Map(); }
  };
  const save = () => {
    try { localStorage.setItem(STORE_KEY, JSON.stringify([...bag])); } catch (_) { /* modo privado */ }
  };

  const subtotal = () => [...bag].reduce((s, [k, qn]) => s + catalog.get(k).price * qn, 0);
  const count = () => [...bag.values()].reduce((s, n) => s + n, 0);

  const bagbar = $("#bagbar");
  const renderBar = (bump) => {
    const n = count();
    bagbar.hidden = n === 0;
    $("#bagCount").textContent = String(n);
    $("#bagTotal").textContent = brl(subtotal());
    $("#openBag").setAttribute("aria-label", `Ver sacola: ${n} ${n === 1 ? "item" : "itens"}, ${brl(subtotal())}`);
    if (bump) {
      bagbar.classList.remove("is-bump");
      void bagbar.offsetWidth;
      bagbar.classList.add("is-bump");
    }
  };

  const add = (key) => {
    const it = catalog.get(key);
    if (!it) return;
    bag.set(key, Math.min((bag.get(key) || 0) + 1, MAX_QTY));
    save();
    renderBar(true);
    toast(`Na sacola: ${it.name}${it.label ? ` (${it.label})` : ""}`);
    track("add_to_cart", { item: it.name, variant: it.label, value: it.price, currency: "BRL" });
  };

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest(".add");
    if (!b) return;
    add(`${b.dataset.id}|${b.dataset.label}`);
    b.classList.add("is-added");
    setTimeout(() => b.classList.remove("is-added"), 450);
  });

  /* ---------- Dialogs ---------- */
  const dlgBag = $("#bag");
  const openDialog = (dlg) => {
    if (typeof dlg.showModal === "function") dlg.showModal();
    else dlg.setAttribute("open", "");
  };
  const closeDialog = (dlg) => {
    if (typeof dlg.close === "function") dlg.close();
    else dlg.removeAttribute("open");
  };
  $$("dialog").forEach((dlg) => {
    dlg.addEventListener("click", (ev) => {
      if (ev.target === dlg || ev.target.closest("[data-close]")) closeDialog(dlg);
    });
  });
  $$("[data-open]").forEach((b) => b.addEventListener("click", () => openDialog($(`#${b.dataset.open}`))));

  const list = $("#bagList");
  const mkBtn = (cls, label, iconId) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = cls;
    b.setAttribute("aria-label", label);
    if (iconId) {
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "ic");
      svg.setAttribute("aria-hidden", "true");
      const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
      use.setAttribute("href", `#i-${iconId}`);
      svg.append(use);
      b.append(svg);
    }
    return b;
  };

  const renderBag = () => {
    list.replaceChildren();
    bag.forEach((qty, key) => {
      const it = catalog.get(key);
      const li = document.createElement("li");
      const name = document.createElement("span");
      name.className = "bag-name";
      name.textContent = it.name;
      if (it.label) {
        const sm = document.createElement("small");
        sm.textContent = it.label;
        name.append(sm);
      }
      const price = document.createElement("span");
      price.className = "bag-price";
      price.textContent = brl(it.price * qty);
      const qtyBox = document.createElement("div");
      qtyBox.className = "qty";
      const minus = mkBtn("", `Diminuir ${it.name}`, "minus");
      const out = document.createElement("output");
      out.textContent = String(qty);
      const plus = mkBtn("", `Aumentar ${it.name}`, "plus");
      const rm = mkBtn("rm", `Remover ${it.name}`);
      rm.textContent = "Remover";
      minus.addEventListener("click", () => setQty(key, qty - 1));
      plus.addEventListener("click", () => setQty(key, qty + 1));
      rm.addEventListener("click", () => setQty(key, 0));
      qtyBox.append(minus, out, plus, rm);
      li.append(name, price, qtyBox);
      list.append(li);
    });
    const has = bag.size > 0;
    $("#bagEmpty").hidden = has;
    $("#checkout").hidden = !has;
    renderTotals();
  };

  const setQty = (key, n) => {
    if (n <= 0) bag.delete(key);
    else bag.set(key, Math.min(n, MAX_QTY));
    save();
    renderBag();
    renderBar(false);
  };

  const form = $("#bagForm");
  const isDelivery = () => form.elements.mode.value === "entrega";
  const renderTotals = () => {
    const sub = subtotal();
    const fee = isDelivery() ? FEE : 0;
    $("#tSub").textContent = brl(sub);
    $("#tFeeRow").hidden = !fee;
    $("#tTotal").textContent = brl(sub + fee);
    $("#addrField").hidden = !isDelivery();
    $("#trocoField").hidden = form.elements.pag.value !== "Dinheiro";
  };
  form.addEventListener("change", renderTotals);

  $("#openBag").addEventListener("click", () => {
    renderBag();
    openDialog(dlgBag);
    track("view_cart", { value: subtotal(), currency: "BRL" });
  });

  const err = $("#formErr");
  const fail = (msg, field) => {
    err.textContent = msg;
    err.hidden = false;
    if (field) {
      field.closest(".field").classList.add("is-invalid");
      field.focus();
    }
  };
  form.addEventListener("input", (ev) => {
    const f = ev.target.closest(".field");
    if (f) f.classList.remove("is-invalid");
    err.hidden = true;
  });

  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    if (!bag.size) return;
    const nome = clean($("#fNome").value, 60);
    const end = clean($("#fEnd").value, 160);
    const obs = clean($("#fObs").value, 200);
    const troco = clean($("#fTroco").value, 10).replace(/[^\d,.]/g, "");
    const pag = form.elements.pag.value;
    const delivery = isDelivery();
    if (nome.length < 2) return fail("Informe seu nome.", $("#fNome"));
    if (delivery && end.length < 8) return fail("Informe o endereço com rua, número e bairro.", $("#fEnd"));

    const lines = ["*Pedido pela página da Churrascaria Brasil*", ""];
    bag.forEach((qty, key) => {
      const it = catalog.get(key);
      lines.push(`${qty}x ${it.name}${it.label ? ` (${it.label})` : ""}: ${brl(it.price * qty)}`);
    });
    const sub = subtotal();
    const fee = delivery ? FEE : 0;
    lines.push("", `Itens: ${brl(sub)}`);
    if (fee) lines.push(`Entrega: ${brl(fee)}`);
    lines.push(`*Total: ${brl(sub + fee)}*`, "");
    lines.push(`Nome: ${nome}`);
    lines.push(delivery ? `Entrega em: ${end}` : "Vou retirar no balcão");
    lines.push(`Pagamento: ${pag}${pag === "Dinheiro" && troco ? ` (troco para R$ ${troco})` : ""}`);
    if (obs) lines.push(`Observações: ${obs}`);

    const url = `https://wa.me/${WHATS}?text=${encodeURIComponent(lines.join("\n"))}`;
    track("whatsapp_order", { value: sub + fee, currency: "BRL", items: count(), mode: delivery ? "entrega" : "retirada" });
    const a = document.createElement("a");
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener";
    document.body.append(a);
    a.click();
    a.remove();
  });

  /* ---------- Início ---------- */
  load();
  if (current) showCat(current);
  renderBar(false);
  renderTotals();
})();
