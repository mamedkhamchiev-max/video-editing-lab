import json,html
d=json.load(open('data.json'));PL=set(json.load(open('plans.json')))
E=html.escape
css='''
@page{size:A4;margin:0}
:root{--navy:#0E1B2A;--navy2:#13283B;--accent:#35C5DD;--gold:#E7B15A;--bg:#F7F9FB;--text:#1A2530;--text2:#6B7A88;--border:#E3E8ED}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;color:var(--text);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff;display:flex;flex-direction:column}
.top{height:14mm;background:var(--navy);display:flex;align-items:center;justify-content:space-between;padding:0 10mm;color:#fff;flex:none}
.logo{display:flex;align-items:center;gap:3mm;font-family:Montserrat;font-weight:800;letter-spacing:.6mm;font-size:10pt}
.logo img{width:8mm;height:8mm;border-radius:50%}
.logo b{color:var(--accent)}
.top .r{font-family:Montserrat;font-weight:600;font-size:9pt;color:#9FB6C4;letter-spacing:.3mm}
.grid{display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:49mm 49mm 36mm;gap:1.6mm;padding:4mm 10mm 0;flex:none}
.grid img{width:100%;height:100%;object-fit:cover;border-radius:2mm;display:block}
.grid img.plan{object-fit:contain;background:#fff;border:.25mm solid var(--border)}
.grid .big{grid-column:span 8;grid-row:span 2}
.grid .side{grid-column:span 4}
.body{padding:5mm 10mm 0;flex:1;display:flex;flex-direction:column}
.head{display:flex;justify-content:space-between;align-items:flex-end;gap:6mm}
h2{font-family:Montserrat;font-weight:800;font-size:21pt;color:var(--navy);line-height:1.1}
.loc{font-size:10.5pt;color:var(--text2);margin-top:1.2mm;font-weight:500}
.price{text-align:right;font-family:Montserrat;font-weight:800;font-size:22pt;color:var(--navy);white-space:nowrap}
.price small{display:block;font-size:8pt;font-weight:600;color:var(--text2);letter-spacing:.4mm;text-transform:uppercase}
.tags{display:flex;gap:2mm;margin-top:3.5mm;flex-wrap:wrap}
.tag{font-size:8pt;font-weight:600;padding:1.2mm 3mm;border-radius:10mm;background:rgba(53,197,221,.12);color:#1C8FA3}
.tag.g{background:rgba(231,177,90,.18);color:#A8721E}
.desc{font-size:9.6pt;line-height:1.55;margin-top:4mm;color:var(--text)}
.cols{display:grid;grid-template-columns:1.1fr 1fr;gap:7mm;margin-top:4.5mm}
h3{font-family:Montserrat;font-weight:700;font-size:8.5pt;text-transform:uppercase;letter-spacing:.5mm;color:var(--navy);margin-bottom:2mm;padding-bottom:1.5mm;border-bottom:.5mm solid var(--accent)}
.kv{display:flex;justify-content:space-between;gap:3mm;font-size:8.6pt;padding:1.25mm 0;border-bottom:.2mm solid var(--border)}
.kv span{color:var(--text2)}.kv b{font-weight:600;text-align:right}
.apt{display:flex;justify-content:space-between;align-items:center;padding:1.6mm 2.5mm;background:var(--bg);border-radius:1.5mm;margin-bottom:1.4mm;font-size:8.8pt}
.apt b{font-family:Montserrat;font-weight:700;color:var(--navy);font-size:10pt}
.amen{margin-top:4mm;display:flex;flex-wrap:wrap;gap:1.4mm}
.amen span{font-size:7.6pt;padding:1mm 2.4mm;border:.25mm solid var(--border);border-radius:10mm;color:var(--text)}
.foot{height:13mm;background:var(--navy);color:#CBD9E6;display:flex;align-items:center;justify-content:space-between;padding:0 10mm;font-size:8.2pt;flex:none;margin-top:auto}
.foot b{color:#fff;font-weight:600}.foot a{color:var(--accent);text-decoration:none;font-weight:600}
.spacer{flex:1}
/* cover */
.cover{background:var(--navy);color:#fff}
.mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:1.5mm;height:150mm}
.mosaic img{width:100%;height:100%;object-fit:cover;display:block}
.mosaic .w{grid-column:span 2;grid-row:span 2}
.cv{padding:12mm 14mm 0;flex:1;display:flex;flex-direction:column}
.cv .logo{font-size:13pt}.cv .logo img{width:12mm;height:12mm}
.cv h1{font-family:Montserrat;font-weight:800;font-size:34pt;line-height:1.08;margin-top:9mm}
.cv h1 em{font-style:normal;color:var(--accent)}
.cv p{font-size:12pt;color:#9FB6C4;margin-top:5mm;line-height:1.5}
.stats{display:flex;gap:10mm;margin-top:9mm}
.stats div{font-size:9pt;color:#9FB6C4;text-transform:uppercase;letter-spacing:.4mm}
.stats b{display:block;text-transform:none;font-family:Montserrat;font-size:20pt;color:var(--gold);letter-spacing:0;margin-bottom:1mm}
.cv .contacts{margin-top:auto;padding:7mm 0 10mm;border-top:.3mm solid rgba(255,255,255,.15);display:flex;justify-content:space-between;font-size:10pt}
.cv .contacts b{color:#fff}
'''
def foot(o=None):
    link=f'<a>fertaestate.com/obyekt/{o["id"]}</a>' if o else '<a>fertaestate.com</a>'
    return f'<div class="foot"><div><b>+90 551 639 64 64</b> &nbsp;·&nbsp; WhatsApp &nbsp;·&nbsp; Telegram @fertaestate34</div>{link}</div>'
def top(r):
    return f'<div class="top"><div class="logo"><img src="img_s/logo.jpg">FERTA <b>ESTATE</b></div><div class="r">{r}</div></div>'
pages=[]
mins=min(int(o['price'].replace('от $','').replace(' ','').replace('\xa0','')) for o in d)
cover_imgs=[d[21]['photos'][0],d[26]['photos'][0],d[0]['photos'][0],d[25]['photos'][0],d[18]['photos'][0],d[15]['photos'][0]]
m=''.join(f'<img class="{"w" if i==0 else ""}" src="{p}">' for i,p in enumerate(cover_imgs))
pages.append(f'''<div class="page cover"><div class="mosaic">{m}</div><div class="cv">
<div class="logo"><img src="img_s/logo.jpg">FERTA <b>ESTATE</b></div>
<h1>Каталог недвижимости<br><em>Стамбула</em> 2026</h1>
<p>Квартиры и виллы под гражданство Турции, ВНЖ, для жизни и инвестиций.<br>На каждой странице — один объект: фото, описание, характеристики и цены.</p>
<div class="stats"><div><b>{len(d)}</b>объектов</div><div><b>от ${mins:,}</b>стартовая цена</div><div><b>$400 000</b>порог гражданства</div></div>
<div class="contacts"><div><b>+90 551 639 64 64</b> · WhatsApp · Telegram @fertaestate34</div><div>fertaestate.com</div></div>
</div></div>'''.replace(',',' ',1) if False else '')
pg=f'''<div class="page cover"><div class="mosaic">{m}</div><div class="cv">
<div class="logo"><img src="img_s/logo.jpg">FERTA <b>ESTATE</b></div>
<h1>Каталог недвижимости<br><em>Стамбула</em> 2026</h1>
<p>Квартиры и виллы под гражданство Турции, ВНЖ, для жизни и инвестиций.<br>На каждой странице — один объект: фото, описание, характеристики и цены.</p>
<div class="stats"><div><b>{len(d)}</b>объектов</div><div><b>от ${mins:,}</b>стартовая цена</div><div><b>$400 000</b>порог гражданства</div></div>
<div class="contacts"><div><b>+90 551 639 64 64</b> · WhatsApp · Telegram @fertaestate34</div><div>fertaestate.com</div></div>
</div></div>'''.replace(f'${mins:,}',f'${mins:,}'.replace(',',' '))
pages=[pg]
for o in d:
    ph=o['photos'];n=len(ph)
    cl=lambda p:' plan' if p in PL else ''
    cells=[f'<img class="big{cl(ph[0])}" src="{ph[0]}">']
    cells+= [f'<img class="side{cl(p)}" src="{p}">' for p in ph[1:3]]
    rest=ph[3:]
    for p in rest: cells.append(f'<img class="{cl(p).strip()}" style="grid-column:span {12//len(rest)}" src="{p}">')
    gridstyle='' if rest else ' style="grid-template-rows:49mm 49mm"'
    ch=dict(o['chars'])
    tags=[]
    if ch.get('Готовность'): tags.append(f'<span class="tag">{E(ch["Готовность"])}</span>')
    if 'Гражданство' in ch: tags.append('<span class="tag g">Гражданство Турции</span>')
    if 'ВНЖ' in ch: tags.append('<span class="tag">ВНЖ</span>')
    if 'Рассрочка' in ch: tags.append('<span class="tag">Рассрочка</span>')
    kv=''.join(f'<div class="kv"><span>{E(k)}</span><b>{E(v)}</b></div>' for k,v in o['chars'])
    apts=''.join(f'<div class="apt"><span>{E(s)}</span><b>{E(p)}</b></div>' for p,s in o['apts'])
    amen=''.join(f'<span>{E(a)}</span>' for a in o['amen'])
    price=o['price'].replace('от ','')
    pages.append(f'''<div class="page">{top(f"Объект №{o['num']} · {o['loc']}")}
<div class="grid"{gridstyle}>{''.join(cells)}</div>
<div class="body"><div class="head"><div><h2>Объект №{o['num']}</h2><div class="loc">{E(o['loc'])}</div></div><div class="price"><small>цена от</small>{E(price)}</div></div>
<div class="tags">{''.join(tags)}</div>
<div class="desc">{E(o['text'])}</div>
<div class="cols"><div><h3>Характеристики</h3>{kv}</div><div><h3>Квартиры в продаже</h3>{apts}</div></div>
<div class="amen">{amen}</div></div>{foot(o)}</div>''')
open('catalog.html','w').write(f'''<!doctype html><html><head><meta charset="utf-8"><title>Каталог Ferta Estate</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{''.join(pages)}</body></html>''')
