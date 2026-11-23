# Dados do cardápio — Lanchonete, Churrascaria e Pizzaria Brasil (BR5)
# Fonte: cardápio digital do cliente, extraído em 23/11/2026.
# Formato de cada item: (nome, descrição, [(rótulo, preço), ...], extras)
# rótulo "" = preço único. extras: {"order": False} = só no salão; {"day": 1..7} = prato do dia (1 = segunda)


def I(name, desc="", prices=None, **extra):
    return {"name": name, "desc": desc, "prices": prices or [], **extra}


def one(name, price, desc="", **extra):
    return I(name, desc, [("", price)], **extra)


def flavors(name, price, labels, desc=""):
    return I(name, desc, [(l, price) for l in labels])


MENU = [
    {
        "id": "refeicoes",
        "title": "Churrascaria e refeições",
        "short": "Refeições",
        "sections": [
            {
                "title": "Pratos do dia",
                "note": "Almoço. O prato do dia de hoje aparece destacado.",
                "items": [
                    one("Strogonoff de frango", 28.00, day=1),
                    one("Ensopado de carneiro", 30.00, day=1),
                    one("Lombo ao molho", 30.00, day=2),
                    one("Porção de dobradinha", 25.00, day=2),
                    one("Feijoada", 38.00, day=3),
                    one("Bisteca frita", 28.00, day=3),
                    one("Porção de rabada", 28.00, day=4),
                    one("Moqueca de peixe", 28.00, day=5),
                    one("Bobó de camarão", 30.00, day=5),
                    one("Feijoada", 38.00, day=6),
                    one("Lombo bovino", 30.00, day=7),
                    one("Lasanha", 25.00, "Consulte os sabores do dia.", day=7),
                ],
            },
            {
                "title": "Self-service por quilo",
                "note": "Servido no salão.",
                "items": [
                    one("Churrasco", 90.00, "Carnes na brasa servidas no quilo.", order=False, unit="/kg"),
                    one("Almoço", 74.90, order=False, unit="/kg"),
                    one("Café da manhã", 65.00, order=False, unit="/kg"),
                    one("Janta", 65.00, order=False, unit="/kg"),
                ],
            },
            {
                "title": "Refeições",
                "items": [
                    one("Prato feito", 25.00),
                    I("Quentinha", "", [("P", 19.00), ("G", 22.00)]),
                    one("Comercial família", 75.00, "Serve 2 ou 3 pessoas."),
                    one("Café da manhã", 25.00),
                    one("Janta", 25.00),
                    one("Aipim (porção)", 15.00),
                ],
            },
            {
                "title": "Outros pratos",
                "items": [
                    one("Feijoada (porção)", 38.00),
                    one("Lasanha", 25.00),
                    I("Panqueca de carne", "", [("1 unidade", 10.00), ("2 unidades", 18.00)]),
                    I("Panqueca de frango", "", [("1 unidade", 10.00), ("2 unidades", 18.00)]),
                    one("Adicional de purê", 6.89),
                ],
            },
            {
                "title": "Sopas e caldos",
                "items": [
                    I("Sopa de carne", "", [("500 ml", 9.00), ("1 L", 18.00)]),
                    I("Sopa de frango", "", [("500 ml", 9.00), ("1 L", 18.00)]),
                    I("Sopa de charque", "", [("1 L", 18.00)]),
                    I("Caldo de aipim", "", [("Copo", 5.00), ("500 ml", 10.00)]),
                    I("Caldo de mocotó", "", [("Copo", 5.00), ("500 ml", 10.00)]),
                ],
            },
        ],
    },
    {
        "id": "lanchonete",
        "title": "Lanchonete",
        "short": "Lanchonete",
        "sections": [
            {
                "title": "Hambúrgueres",
                "items": [
                    one("X-Xandão", 39.90, "Pão com gergelim, 2 carnes (120 g), tomate, alface, molho especial, cebola caramelizada, cheddar e bacon."),
                    one("Moda da Casa", 35.90, "Pão com gergelim, 2 carnes (120 g), tomate, alface, molho especial, cebola, cheddar, picles, ovos e bacon."),
                    one("Nordestino", 29.90, "Pão com gergelim, carne artesanal (120 g), banana-da-terra, bacon e muçarela."),
                    one("X-Brasil", 28.90, "Pão com gergelim, carne (120 g), tomate, alface americana, molho especial, muçarela, cebola caramelizada e bacon."),
                    one("X-Tudo", 26.90, "Pão com gergelim, carne, tomate, alface, molho especial, ovo, bacon, frango, muçarela e presunto."),
                    one("Baby Burguer", 25.90, "Pão com gergelim, 2 carnes (120 g), tomate, alface, molho especial, cebola caramelizada e cheddar."),
                    one("X-Bacon", 22.90, "Pão com gergelim, carne, tomate, alface, molho especial, muçarela, presunto e bacon."),
                    one("X-Frango", 21.90, "Pão com gergelim, carne, tomate, alface, molho especial, muçarela e frango."),
                    one("X-Egg", 20.90, "Pão com gergelim, carne, tomate, alface, molho especial, muçarela, presunto, cebola e 2 ovos."),
                    one("X-Burguer", 19.90, "Pão com gergelim, carne, tomate, alface, molho especial, muçarela e presunto."),
                    one("X-Calabresa", 19.90, "Pão com gergelim, carne, tomate, cebola, alface, molho especial, muçarela, presunto e calabresa."),
                    one("X-Toscana", 16.90, "Pão francês, muçarela, vinagrete e linguiça toscana."),
                ],
            },
            {
                "title": "Tapiocas",
                "items": [
                    one("Carne seca", 22.99),
                    one("Frango", 19.99),
                    one("Nutella com morango", 18.00),
                    one("Calabresa com queijo", 16.99),
                    one("Queijo e presunto", 16.99),
                    one("Ovo com queijo", 14.99),
                    one("Manteiga", 9.99),
                ],
            },
            {
                "title": "Cuscuz",
                "items": [
                    I("Cuscuz carne seca com queijo", "", [("P", 17.99), ("G", 24.99)]),
                    I("Cuscuz carne seca com banana", "", [("P", 16.99), ("G", 23.99)]),
                    I("Cuscuz frango com queijo", "", [("P", 15.99), ("G", 22.99)]),
                    I("Cuscuz calabresa com queijo", "", [("P", 13.99), ("G", 21.99)]),
                    I("Cuscuz com manteiga", "", [("P", 10.00), ("G", 13.00)]),
                ],
            },
            {
                "title": "Salgados",
                "items": [
                    one("Coxinha", 7.00),
                    one("Empada de frango", 7.00),
                    one("Enroladinho", 7.00),
                    one("Banana real", 7.00),
                    one("Risole misto", 8.00),
                    one("Bauru", 9.00),
                    one("Esfirra de frango", 9.00),
                    one("Hambúrguer de forno", 9.00),
                    one("Pão delícia", 9.00),
                    one("Pastel", 5.00),
                    one("Torta salgada", 15.00),
                    one("Brotinho", 17.00),
                    one("Quiche", 17.00),
                    one("Churros (porção)", 15.00),
                    one("Mini salgados (unidade)", 1.50),
                    one("Combo mini salgados", 29.90),
                ],
            },
            {
                "title": "Padaria",
                "items": [
                    one("Pão", 1.00),
                    one("Pão com manteiga", 3.00),
                    one("Pão com ovo", 6.00),
                    one("Pão com queijo", 9.00),
                    one("Pão com requeijão", 9.00),
                    one("Pão recheado", 9.00),
                    one("Pão turbinado", 12.00),
                    one("Misto", 7.00),
                    one("Ovo (unidade)", 2.50),
                    one("Fatia de presunto", 3.00),
                    one("Fatia de queijo", 3.00),
                ],
            },
            {
                "title": "Petiscos",
                "items": [
                    I("Batata frita simples", "", [("P", 15.00), ("G", 30.00)]),
                    I("Batata frita especial", "", [("P", 23.00), ("G", 38.00)]),
                    one("Bala de licuri com banana", 16.00),
                    one("Bolacha de licuri", 17.00, "Consulte os sabores."),
                    one("Beiju canoinha", 9.00),
                    one("Beiju de coco", 9.00),
                    one("Beiju de goiaba com coco", 9.00),
                    one("Beiju de pote", 15.00),
                    one("Tapioca crocante de coco queimado", 15.00),
                    one("Tapioca crocante de leite condensado", 15.00),
                    I("Salgadinhos de pacote", "", [("Batata chips Maitá", 8.00), ("Cheetos", 7.00), ("Doritos", 7.00), ("Clube Social recheado", 10.00), ("Sol", 6.00), ("Torcida", 3.00)]),
                ],
            },
        ],
    },
    {
        "id": "pizzaria",
        "title": "Pizzaria",
        "short": "Pizzaria",
        "sections": [
            {
                "title": "Pizzas salgadas",
                "note": "Tamanhos média e família.",
                "items": [
                    I(n, "", [("Média", m), ("Família", f)]) for n, m, f in [
                        ("Rainha da BR", 57, 81), ("Tucaninha", 53, 72), ("Força do Sertão", 56, 78),
                        ("À Moda Xandão", 52, 68), ("Maré Alta", 57, 84), ("Camarão cremoso", 65, 90),
                        ("Salame com geleia de pimenta", 65, 90), ("Peito de peru e catupiry cremoso", 65, 90),
                        ("Sertaneja cremosa", 52, 75), ("Mineirinha", 53, 68), ("Baianinha", 42, 62),
                        ("Paixão Nacional", 42, 60), ("Frango Chiquem", 52, 68), ("Frango com catupiry", 48, 68),
                        ("Frango", 44, 62), ("Atum", 52, 79), ("Brócolis e bacon", 52, 68),
                        ("Portuguesa", 48, 68), ("Lombinho", 44, 67), ("Siciliana", 45, 67),
                        ("Marguerita", 43, 58), ("Vegetariana", 43, 60),
                    ]
                ],
            },
            {
                "title": "Pizzas doces",
                "items": [
                    I(n, "", [("Média", 45.00), ("Família", 67.00)]) for n in ["Brigadeiro com morango", "Dois Amores", "Romeu e Julieta"]
                ],
            },
        ],
    },
    {
        "id": "confeitaria",
        "title": "Confeitaria",
        "short": "Doces",
        "sections": [
            {
                "title": "Fatias e porções",
                "items": [
                    one("Sobremesa Brasil", 18.00),
                    one("Torta de café", 20.00),
                    one("Banoffee", 14.00),
                    one("Delícia de uva", 14.00),
                    one("Cheesecake", 12.00),
                    one("Mousse", 12.00),
                    one("Torta Oreo", 12.00),
                    one("Torta", 17.00, "Consulte os sabores."),
                    one("Brownie", 10.00, "Consulte os sabores."),
                    one("Bolo com cobertura", 10.00),
                    one("Bolo fit", 10.00),
                    one("Bolo de tapioca", 10.00),
                    one("Rocambole", 10.00),
                    one("Bolo simples", 7.00),
                    one("Banana real", 7.00),
                    one("Pavê", 9.00),
                    one("Pudim", 9.00),
                    one("Torta encanto de cereja", 8.00),
                    one("Salada de frutas", 6.00),
                    one("Mini vulcão", 25.00),
                    one("Rocambole salgado de salpicão", 20.00),
                ],
            },
            {
                "title": "Docinhos",
                "items": [
                    one("Brigadeiro de morango", 8.00),
                    one("Brigadeiro", 5.00, "Consulte os sabores."),
                    one("Caixa com 4 mini brigadeiros", 8.00),
                    one("Cupcake", 5.00),
                    one("Tortalete", 5.00),
                    one("Trufa", 3.00),
                ],
            },
            {
                "title": "Inteiros por encomenda",
                "note": "Combine a data de retirada pelo WhatsApp.",
                "items": [
                    I("Torta inteira", "", [("15 cm", 180.00), ("20 cm", 200.00), ("25 cm", 250.00)]),
                    one("Pudim inteiro", 90.00),
                    one("Torta encanto de cereja inteira", 85.00),
                    one("Bolo com cobertura inteiro", 60.00),
                    one("Bolo de abacaxi inteiro", 60.00),
                    one("Bolo fit inteiro", 60.00),
                    one("Bolo de aipim inteiro", 45.00),
                    one("Bolo simples inteiro", 45.00),
                ],
            },
        ],
    },
    {
        "id": "bebidas",
        "title": "Bebidas",
        "short": "Bebidas",
        "sections": [
            {
                "title": "Sucos naturais",
                "items": [
                    I(f"Suco de {s.lower()}", "", [("Copo", 8.00), ("Jarra", 12.00)]) for s in ["Acerola", "Goiaba", "Laranja", "Limão", "Manga", "Maracujá", "Umbu"]
                ] + [
                    I("Suco de morango", "", [("Copo", 9.00), ("Jarra", 18.00)]),
                    one("Vitamina (jarra)", 12.00),
                ],
            },
            {
                "title": "Cafés",
                "items": [
                    one("Café puro", 3.00),
                    one("Café com leite", 4.00),
                    one("Cappuccino", 5.00),
                    one("Café expresso", 6.00),
                ],
            },
            {
                "title": "Refrigerantes",
                "items": [
                    I("Coca-Cola", "", [("Lata ou KS", 6.00), ("1 L", 10.00)]),
                    I("Coca-Cola Zero", "", [("Lata ou KS", 6.00), ("1 L", 10.00)]),
                    I("Fanta Laranja", "", [("Lata", 6.00), ("1 L", 10.00)]),
                    I("Guaraná", "", [("Lata", 6.00), ("1 L", 10.00)]),
                    I("Kuat", "", [("Lata", 6.00), ("1 L", 10.00)]),
                    flavors("Refrigerante lata", 6.00, ["Fanta Uva", "Fanta Zero", "Guaraná Zero", "Kuat Zero", "Sprite", "Sprite Zero", "Schweppes"]),
                    one("Coca-Cola Café", 5.00),
                ],
            },
            {
                "title": "Águas",
                "items": [
                    I("Água mineral", "", [("Garrafa", 3.00), ("1,5 L", 6.00)]),
                    one("Água com gás", 4.00),
                    one("Água de coco", 6.00),
                    one("H2O", 7.00),
                    one("Sprite Água Fresh", 7.00),
                ],
            },
            {
                "title": "Sucos de caixinha, chás e achocolatados",
                "items": [
                    I("Del Valle", "", [("Del Valle", 6.00), ("Laranja, morango ou uva", 5.00)]),
                    I("Frutyba", "", [("290 ml", 4.00), ("500 ml", 8.00)]),
                    one("Kapo", 6.00),
                    one("Suco de uva 1 L", 20.00),
                    I("Leão Ice Tea", "", [("Garrafa", 4.00), ("Lata", 6.00)]),
                    I("Achocolatado", "", [("Nescau Zero", 5.00), ("Nesquik", 5.00), ("Alpino Nestlé", 12.00), ("Nescau Nestlé", 12.00), ("Neston", 12.00)]),
                ],
            },
            {
                "title": "Energéticos e isotônicos",
                "items": [
                    one("Monster", 15.00),
                    one("Red Bull", 15.00),
                    one("Taff Man", 8.00),
                    one("Powerade", 7.00),
                ],
            },
        ],
    },
    {
        "id": "sorvetes",
        "title": "Sorvetes e açaí",
        "short": "Sorvetes",
        "sections": [
            {
                "title": "Quy Sorvetto",
                "items": [
                    I("Pote Quy Sorvetto", "", [("1,5 L", 22.90), ("2 L", 29.90), ("Light", 19.90), ("Zero", 19.90), ("Premium", 33.90)]),
                    I("Açaí Quy", "", [("P", 12.00), ("G", 28.00), ("1 L", 28.00)]),
                    I("Quy Dueto", "", [("Unidade", 5.00), ("G", 18.90)]),
                    I("Picolés e gelados Quy", "", [
                        ("Kids", 1.50), ("Cremosinho", 2.00), ("Quy Gelo", 2.99), ("Suco Palito", 3.00), ("Quy Milk", 3.50),
                        ("Frutas Brasil", 4.00), ("Quy Frutti", 4.00), ("Quy Sucesso", 4.00), ("Trufados", 5.00), ("Supremo", 6.00),
                        ("Pé de Moleque", 7.00), ("Quy Diversão", 7.00), ("Sundae", 7.00), ("Supremo Brigadeiro", 8.00),
                        ("Quy Copão", 9.90), ("Quyblitto", 9.99), ("Sublime", 9.99), ("Bombom Gelado", 10.00), ("Quy Cone", 10.00), ("Refinatto", 13.00),
                    ]),
                ],
            },
            {
                "title": "Kibon",
                "items": [
                    flavors("Cremosíssimo 1,5 L", 31.99, ["Chocolate", "Creme", "Flocos", "Napolitano"]),
                    I("Potes grandes Kibon", "", [
                        ("Cremosíssimo 4 em 1", 39.90), ("Cremosíssimo 4 em 1 Chocoleite", 39.90), ("Tropical 2 em 1 Coco e Abacaxi", 39.90),
                        ("Pote 2 L", 42.90), ("Leitinho Trufado Sundae 1,4 L", 44.90), ("Chocolate Sundae 1,4 L", 44.99),
                    ]),
                    I("Pote 800 ml", "", [("Ovomaltine", 38.99), ("Snickers", 38.99), ("Chicabon Menos Açúcar", 39.99)]),
                    flavors("Gelartier", 42.90, ["Chocolate com raspas", "Macadâmia caramelizada", "Morango em pedaços"]),
                    flavors("Magnum pote 184 g", 39.99, ["Branco", "Chocolate", "Clássico"]),
                    I("Pote mini Kibon", "", [("Morango", 27.90), ("Doce de Leite", 29.99), ("Eskibon", 29.99), ("Chicabon", 38.99)]),
                    flavors("Kibon Mini", 15.00, ["Chicabon", "Doce de Leite", "Eskibon", "Morango"]),
                    I("Picolé Magnum", "", [("Branco", 18.99), ("Clássico", 18.99), ("Amêndoas", 19.99), ("Avelã", 19.99), ("Cookies & Cream", 19.99), ("Menos Açúcar", 19.99), ("Pistache", 19.99)]),
                    flavors("Magnum Bombom", 20.99, ["Cookies & Cream", "Pistache"]),
                    I("Cornetto", "", [("Crocante", 10.99), ("Brigadeiro", 14.99), ("M&M's", 14.99), ("Unicornetto", 14.99)]),
                    I("Favorito", "", [("Brigadeiro", 9.99), ("Chicabon", 9.99), ("Eskibon", 9.99), ("Menos Açúcar", 10.49), ("Tablito", 10.49), ("Tablito 3 Chocolates", 10.49), ("Tablito Max Avelã", 10.49)]),
                    flavors("Frutare", 7.99, ["Abacaxi", "Coco", "Limão", "Morango", "Uva"]),
                    one("Frutilly Kids Chiclete", 5.49),
                ],
            },
            {
                "title": "Guttos Sorvetes",
                "items": [
                    I("Açaí Guttos", "", [
                        ("Palito", 3.99), ("Pote banana 240 ml", 12.99), ("Pote morango 240 ml", 12.99), ("Pote grego 240 ml", 13.99),
                        ("Pote La Ele 240 ml", 13.99), ("Com granola 250 ml", 13.99), ("Pote 500 ml", 16.80), ("Pote 1 L", 29.99), ("Pote grego 1 L", 30.00),
                    ]),
                    I("Pote Guttos 1 L", "", [("Tradicionais", 23.90), ("Premium", 24.90), ("Zero Açúcar", 29.90)]),
                    I("Picolés Guttos", "", [
                        ("Fruit", 3.99), ("Milks", 3.99), ("Drink Melancia", 5.00), ("Maçã Verde", 5.00), ("Kids", 6.00),
                        ("Brigadeiro", 7.70), ("Skimo", 7.70), ("Paleten", 8.00), ("Gukitto", 9.00), ("Cookies", 9.99),
                        ("Frambuito", 9.99), ("Guttolito", 9.99), ("Nutgutto", 9.99), ("Chocoblack", 11.99), ("Chocodubai", 11.99),
                        ("Guttoniker", 11.99), ("Pistache", 11.99), ("Paleta Premium", 12.00),
                    ]),
                    flavors("Cremosas Guttos", 10.00, ["Chocolate belga", "Coco", "Tapioca"]),
                    flavors("Bombom Especialista", 13.99, ["Açaí", "Skimo"]),
                    I("Copos Guttos", "", [("Sundae", 6.00), ("Copo Premium", 13.99), ("Copo Premium Zero Açúcar", 14.00)]),
                    I("Linha Zero Açúcar Guttos", "", [("Coco", 6.00), ("Iogurte", 8.00), ("Ninho Trufado", 10.00), ("Chocolate", 12.00), ("Mousse de Maracujá", 12.00), ("Torta de Limão", 12.00)]),
                ],
            },
        ],
    },
    {
        "id": "bomboniere",
        "title": "Bombonière",
        "short": "Bombonière",
        "sections": [
            {
                "title": "Bombonière",
                "items": [
                    I("Balas, pirulitos e chicletes", "", [
                        ("Bala sortida", 0.20), ("Big Big", 0.30), ("Bala Toffee", 0.50), ("Bubbaloo", 0.50), ("Caramelo", 0.50),
                        ("Pirulito Big Big", 0.60), ("Flics", 3.00), ("Mentos Pure Fruit", 3.00), ("Minty", 3.00), ("Halls", 4.00),
                        ("Mentos", 4.00), ("Trident", 4.00), ("Haribo Bananada", 7.99), ("Trident Max", 8.00), ("Haribo Chamallows", 9.99),
                        ("Trident 14 un", 10.00), ("Kiss Mentos", 15.00), ("Mentos Fresh", 15.00), ("Mentos Pure Fresh 56 g", 15.00), ("Trident X Senses", 15.00),
                    ]),
                    I("Chocolates", "", [
                        ("Baton Garoto", 2.00), ("Bombom Oreo", 2.00), ("Ouro Branco", 2.00), ("Sonho de Valsa", 2.00), ("Tortuguita", 2.00),
                        ("Lacta 20 g", 3.00), ("Lollo", 3.00), ("Prestígio", 4.00), ("Talento 25 g", 4.00), ("Chokito", 4.50),
                        ("KitKat", 4.50), ("Choco Tubes Hershey's", 5.00), ("Bis 10 un", 5.50), ("Sonho de Valsa 25 g", 6.00), ("Snickers", 9.00),
                        ("Garoto ao leite 80 g", 10.00), ("Garoto meio amargo", 10.00), ("M&M's", 10.00), ("Talento 85 g", 12.00),
                    ]),
                    I("Biscoitos e cereais", "", [
                        ("Oreo", 3.00), ("Barra de cereais", 5.00), ("Mini Oreo", 5.00), ("Nescau Cereal", 5.00),
                        ("Biscoito Canudinho", 6.00), ("Biscoito de nata", 7.00), ("Sequilhos", 7.00),
                    ]),
                    I("Doces caseiros e regionais", "", [
                        ("Bananada (unidade)", 2.00), ("Cocada", 3.00), ("Doce de leite caseiro", 4.00), ("Doce de leite Curaçá", 6.00), ("Bananada (pacote)", 18.00),
                    ]),
                ],
            },
        ],
    },
]
