import pathlib

HERE = pathlib.Path(__file__).parent

BAD = [
    ("bad01_cookies", "Печенье, кексы, рулеты", "Много сахара и маргарина"),
    ("bad02_yogurt", "Сладкие йогурты", "До 4 ложек сахара в баночке"),
    ("bad03_juice", "Соки в пакетиках", "Жидкий сахар, портит зубы"),
    ("bad04_cereal", "Сухие завтраки", "Сахар и белая мука"),
    ("bad05_sausage", "Сосиски и колбаса", "Нитриты и много соли"),
    ("bad06_candy", "Мармелад и конфеты", "Сахар и яркие красители"),
    ("bad07_soda", "Сладкая газировка", "Сахар и кислота вредят зубам"),
    ("bad08_chips", "Чипсы и сухарики", "Жир, соль и акриламид"),
    ("bad09_porridge", "Быстрые каши в пакетиках", "Сахар и ароматизаторы"),
    ("bad10_syrok", "Глазированные сырки", "Пальмовое масло и сахар"),
]
GOOD = [
    ("good01_fruit", "Фрукты", "Витамины и клетчатка"),
    ("good02_veg", "Овощи", "Для роста и здорового животика"),
    ("good03_berries", "Ягоды", "Сладко и полезно"),
    ("good04_yogurt", "Йогурт без сахара и кефир", "Для здорового животика"),
    ("good05_tvorog", "Творог", "Кальций для зубов и костей"),
    ("good06_oats", "Овсяная каша", "Энергия надолго"),
    ("good07_eggs", "Яйца", "Белок для роста"),
    ("good08_meat", "Курица и рыба", "Сила и крепкие мышцы"),
    ("good09_cheese", "Сыр и хлеб из цельного зерна", "Сытно и полезно"),
    ("good10_water", "Вода и молоко", "Самое лучшее питьё"),
]

CROSS = """<svg class="mark" viewBox="0 0 100 100"><g stroke-linecap="round">
<line x1="14" y1="14" x2="86" y2="86" stroke="#fff" stroke-width="19"/>
<line x1="86" y1="14" x2="14" y2="86" stroke="#fff" stroke-width="19"/>
<line x1="14" y1="14" x2="86" y2="86" stroke="#E0201B" stroke-width="12"/>
<line x1="86" y1="14" x2="14" y2="86" stroke="#E0201B" stroke-width="12"/></g></svg>"""

CHECK = """<svg class="badge" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#22A045" stroke="#fff" stroke-width="7"/>
<polyline points="28,52 44,67 73,36" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def page(kind, items, title, sub, icon):
    cards = []
    for i, (img, name, why) in enumerate(items, 1):
        overlay = CROSS if kind == "bad" else CHECK
        cards.append(f"""<div class="card">
  <div class="ph"><img src="big/{img}.jpg">{overlay}</div>
  <div class="tx"><div class="num">{i}</div><div class="name">{name}</div><div class="why">{why}</div></div>
</div>""")
    return f"""<section class="page {kind}">
  <header><div class="icon">{icon}</div><div><h1>{title}</h1><p>{sub}</p></div></header>
  <div class="grid">{''.join(cards)}</div>
</section>"""


ICON_BAD = """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#fff" stroke-width="10"/><line x1="19" y1="19" x2="81" y2="81" stroke="#fff" stroke-width="10"/></svg>"""
ICON_GOOD = """<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#fff" stroke-width="10"/><polyline points="29,52 44,66 72,37" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

html = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Еда для детей</title>
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter', 'DejaVu Sans', sans-serif; background: #fff; }}
.page {{ width: 210mm; height: 297mm; padding: 9mm 9mm 8mm; overflow: hidden; page-break-after: always; display: flex; flex-direction: column; }}
.page:last-child {{ page-break-after: auto; }}
header {{ display: flex; align-items: center; gap: 6mm; border-radius: 6mm; padding: 5mm 8mm; color: #fff; margin-bottom: 5mm; }}
.bad header {{ background: #E0201B; }}
.good header {{ background: #22A045; }}
header .icon svg {{ width: 24mm; height: 24mm; display: block; }}
h1 {{ font-size: 21mm; font-weight: 900; letter-spacing: 1.5mm; line-height: 1; }}
header p {{ font-size: 6mm; font-weight: 600; margin-top: 2mm; opacity: .95; }}
.grid {{ flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(5, 44mm); gap: 4mm; align-content: start; }}
.card {{ min-width: 0; overflow: hidden; display: flex; align-items: center; gap: 4mm; border-radius: 5mm; padding: 2.5mm; border: 1.2mm solid; }}
.bad .card {{ border-color: #E0201B; background: #FFF3F2; }}
.good .card {{ border-color: #22A045; background: #F1FBF3; }}
.ph {{ position: relative; width: 36mm; height: 36mm; flex: none; border-radius: 3.5mm; overflow: hidden; background: #fff; }}
.ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.bad .ph img {{ filter: saturate(.85); }}
.mark {{ position: absolute; inset: 4%; width: 92%; height: 92%; }}
.badge {{ position: absolute; right: 3%; bottom: 3%; width: 38%; height: 38%; }}
.tx {{ min-width: 0; }}
.num {{ display: inline-block; font-size: 4mm; font-weight: 800; color: #fff; border-radius: 3mm; padding: .4mm 2.4mm; margin-bottom: 1.5mm; }}
.bad .num {{ background: #E0201B; }}
.good .num {{ background: #22A045; }}
.name {{ font-size: 5.3mm; font-weight: 800; line-height: 1.12; color: #1d1d1d; }}
.why {{ font-size: 3.7mm; font-weight: 500; line-height: 1.25; color: #555; margin-top: 1.5mm; }}
</style></head><body>
{page("bad", BAD, "НЕЛЬЗЯ", "Это вредно для здоровья", ICON_BAD)}
{page("good", GOOD, "МОЖНО", "Это полезно, ешь на здоровье!", ICON_GOOD)}
</body></html>"""

(HERE / "poster.html").write_text(html, encoding="utf-8")
print("ok")
