import json,html
d=json.load(open('data.json'));PL=set(json.load(open('plans.json')))
E=html.escape
import math,itertools,re
def num(p): return int(re.sub(r'[^0-9]','',p))
def money(v): return '$'+f'{v:,}'.replace(',','\u00a0')
def citizenship(o):
    A=[(num(p),s) for p,s in o['apts']]
    ok=sorted([a for a in A if a[0]>=400000])
    if ok:
        return 'ok',f'Подходит покупка одной квартиры — например, {ok[0][1]} за {money(ok[0][0])}.'
    best=None
    for n in range(2,8):
        for combo in itertools.combinations_with_replacement(sorted(set(A)),n):
            t=sum(c[0] for c in combo)
            if t>=400000 and (best is None or t<best[0]): best=(t,combo)
        if best: break
    t,combo=best
    from collections import Counter
    parts=' + '.join(f'{k}× {s} по {money(v)}' if k>1 else f'{s} за {money(v)}' for (v,s),k in Counter(combo).items())
    return 'multi',f'Подходит при покупке {len(combo)} квартир на общую сумму от $400\u00a0000. Например: {parts} = {money(t)}. Можно сочетать с квартирами из других объектов каталога.'
def residence(o):
    A=sorted((num(p),s) for p,s in o['apts'])
    ok=[a for a in A if a[0]>=200000]
    if ok:
        return 'ok',f'Подходит: квартира от $200 000 — например, {ok[0][1]} за {money(ok[0][0])}.'
    return 'no',f'Квартиры здесь дешевле $200 000 — минимальной суммы для ВНЖ по покупке в Стамбуле. Для ВНЖ выберите объект от $200 000.'

LOC={'Büyükçekmece':'Бююкчекмедже','Esenyurt':'Эсеньюрте','Bağcılar':'Багджыларе','Beylikdüzü':'Бейликдюзю','Maltepe':'Малтепе','Beşiktaş':'Бешикташе','Zeytinburnu':'Зейтинбурну','Küçükçekmece':'Кючюкчекмедже','Avcilar':'Авджыларе','Avcılar':'Авджыларе','Pendik':'Пендике','Ümraniye':'Умрание','Beyoğlu':'Бейоглу','Sarıyer':'Сарыере','Göktürk':'Гёктюрке','Bahçelievler':'Бахчелиэвлере'}
def seo_text(o):
    dist=o['loc'].split(', ')[1].strip();ru=LOC[dist]
    P=[num(p) for p,_ in o['apts']];am=set(o['amen']);tr=dict(o['chars']).get('Транспорт','').lower()
    sea='Пляж рядом' in am or 'море' in tr or 'пляж' in tr or o['num'] in(5,15,16,25)
    villa=o['num']==1
    obj='виллу' if villa else ('недорогую квартиру' if min(P)<200000 else 'квартиру')
    s=f"Купить {obj} в Стамбуле в {ru} ({dist})"
    if sea: s+=" — недвижимость в Турции у моря"
    s+=". "
    s+="Объект подходит для получения гражданства Турции за инвестиции в недвижимость" + (" — достаточно одной покупки от $400 000" if max(P)>=400000 else " при покупке нескольких квартир на сумму от $400 000")
    if max(P)>=200000: s+=", а также для оформления ВНЖ Турции по недвижимости, в том числе семейного ВНЖ"
    s+=". Ferta Estate сопровождает покупку недвижимости в Турции для россиян и иностранцев под ключ."
    return s
def seo_short(o):
    first=seo_text(o).split('. ')[0]
    return first+'. Ferta Estate сопровождает покупку недвижимости в Турции для россиян и иностранцев под ключ.'
def highlights(o):
    ch=dict(o['chars']);H=[];am=set(o['amen'])
    specs=' '.join(s for p,s in o['apts'])
    if ch.get('Готовность','').startswith('Готов'): H.append('Готовый объект — можно заселяться или сдавать в аренду сразу')
    else: H.append(f"Покупка на этапе строительства, сдача — {ch.get('Срок сдачи','уточняйте')}")
    if 'Рассрочка' in ch: H.append('Рассрочка от застройщика')
    if ch.get('Цель покупки'): H.append('Цель покупки: '+ch['Цель покупки'].lower())
    if ch.get('Транспорт'):
        t=ch['Транспорт'];w=t.split()[0]
        if w in('Море','Метро','Пляж','Метробус','Ж/д','Автомагистраль','Автострада','Аэропорт','Национальный','Улица','Пролив'): t=t[0].lower()+t[1:]
        H.append('Рядом: '+t.replace('национальный заповедник','лесной заповедник').replace('пролив Босфор','Босфор'))
    tr=ch.get('Транспорт','').lower()
    if 'Пляж рядом' in am and 'пляж' not in tr and 'море' not in tr: H.append('Пляж рядом')
    elif 'Причал / марина' in am: H.append('Рядом причал / марина')
    if re.search(r'(1\+1|1\+0|Студия)',specs): H.append('Формат 1+1 / студия — самый востребованный в аренде')
    elif re.search(r'\b[3-7]\+',specs) and ({'Детская площадка','Детский сад','Школа'}&am): H.append('Просторные планировки для семей, детская инфраструктура')
    sec=[x for x in ['Охрана 24/7','Бассейн','СПА / хаммам','Фитнес-зал'] if x in am]
    if len(sec)>=3: H.append('Закрытая территория: '+', '.join(x.lower() for x in sec))
    return H[:6]

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
.grid{display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:38mm 38mm 26mm;gap:1.6mm;padding:4mm 10mm 0;flex:none}
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
.desc{font-size:9.4pt;line-height:1.5;margin-top:3.5mm;color:var(--text)}
.cols{display:grid;grid-template-columns:1.1fr 1fr;gap:7mm;margin-top:4mm}
h3{font-family:Montserrat;font-weight:700;font-size:8.5pt;text-transform:uppercase;letter-spacing:.5mm;color:var(--navy);margin-bottom:2mm;padding-bottom:1.5mm;border-bottom:.5mm solid var(--accent)}
.kv{display:flex;justify-content:space-between;gap:3mm;font-size:8.6pt;padding:1.25mm 0;border-bottom:.2mm solid var(--border)}
.kv span{color:var(--text2)}.kv b{font-weight:600;text-align:right}
.apt{display:flex;justify-content:space-between;align-items:center;padding:1.6mm 2.5mm;background:var(--bg);border-radius:1.5mm;margin-bottom:1.4mm;font-size:8.8pt}
.apt b{font-family:Montserrat;font-weight:700;color:var(--navy);font-size:10pt}
.amen{margin-top:3mm;display:flex;flex-wrap:wrap;gap:1.4mm}
.amen span{font-size:7.6pt;padding:1mm 2.4mm;border:.25mm solid var(--border);border-radius:10mm;color:var(--text)}
.foot{height:13mm;background:var(--navy);color:#CBD9E6;display:flex;align-items:center;justify-content:space-between;padding:0 10mm;font-size:8.2pt;flex:none;margin-top:auto}
.foot b{color:#fff;font-weight:600}.foot a{color:var(--accent);text-decoration:none;font-weight:600}
.spacer{flex:1}

.law{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:4mm}
.law div{border-radius:2mm;padding:2.6mm 3.2mm;font-size:8.6pt;line-height:1.45;background:var(--bg);border-left:1.2mm solid var(--accent)}
.law div.cz{background:rgba(231,177,90,.13);border-left-color:var(--gold)}
.law div.no{border-left-color:#9FB6C4}
.law b{display:block;font-family:Montserrat;font-weight:800;font-size:8.6pt;text-transform:uppercase;letter-spacing:.3mm;color:var(--navy);margin-bottom:.8mm}
.hlu{list-style:none}
.hlu li{font-size:8.8pt;line-height:1.4;padding:1.1mm 0 1.1mm 5mm;position:relative;border-bottom:.2mm solid var(--border)}
.hlu li:before{content:"✓";position:absolute;left:0;color:var(--accent);font-weight:800}
.hl ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:1mm 6mm}
.hl li{font-size:8.6pt;line-height:1.35;padding-left:4.5mm;position:relative}
.hl li:before{content:"✓";position:absolute;left:0;color:var(--accent);font-weight:800}
.info{padding:12mm 14mm;flex:1}
.info h1{font-family:Montserrat;font-weight:800;font-size:24pt;color:var(--navy)}
.info .lead{font-size:10.5pt;color:var(--text2);margin-top:3mm;line-height:1.5}
.box{margin-top:7mm;border-radius:3mm;padding:6mm 7mm;background:var(--bg)}
.box.g{background:rgba(231,177,90,.12)}
.box h2{font-size:14pt}
.box ul{margin-top:3mm;padding-left:5mm}
.box li{font-size:10pt;line-height:1.55;margin-bottom:1.4mm}
.note{margin-top:7mm;font-size:8.6pt;color:var(--text2);line-height:1.5}
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
<h1>Недвижимость в Турции:<br>квартиры в <em>Стамбуле</em> 2026</h1>
<p>Купить квартиру в Стамбуле под гражданство Турции и ВНЖ — для россиян и иностранцев, для жизни и инвестиций.<br>На каждой странице — один объект: фото, описание, характеристики и цены.</p>
<div class="stats"><div><b>{len(d)}</b>объектов</div><div><b>от ${mins:,}</b>стартовая цена</div><div><b>$400 000</b>порог гражданства</div></div>
<div class="contacts"><div><b>+90 551 639 64 64</b> · WhatsApp · Telegram @fertaestate34</div><div>fertaestate.com</div></div>
</div></div>'''.replace(',',' ',1) if False else '')
pg=f'''<div class="page cover"><div class="mosaic">{m}</div><div class="cv">
<div class="logo"><img src="img_s/logo.jpg">FERTA <b>ESTATE</b></div>
<h1>Недвижимость в Турции:<br>квартиры в <em>Стамбуле</em> 2026</h1>
<p>Купить квартиру в Стамбуле под гражданство Турции и ВНЖ — для россиян и иностранцев, для жизни и инвестиций.<br>На каждой странице — один объект: фото, описание, характеристики и цены.</p>
<div class="stats"><div><b>{len(d)}</b>объектов</div><div><b>от ${mins:,}</b>стартовая цена</div><div><b>$400 000</b>порог гражданства</div></div>
<div class="contacts"><div><b>+90 551 639 64 64</b> · WhatsApp · Telegram @fertaestate34</div><div>fertaestate.com</div></div>
</div></div>'''.replace(f'${mins:,}',f'${mins:,}'.replace(',',' '))
info=f'''<div class="page">{top("Гражданство и ВНЖ")}<div class="info">
<h1>Как получить гражданство Турции и ВНЖ через покупку недвижимости</h1>
<div class="lead">На странице каждого объекта мы посчитали, как получить гражданство или ВНЖ именно в этом проекте: одной квартирой или несколькими.</div>
<div class="box g"><h2>🇹🇷 Гражданство Турции за инвестиции в недвижимость — от $400 000</h2><ul>
<li>Нужно купить недвижимость общей стоимостью от <b>$400 000</b>. Можно одну квартиру или несколько — суммы складываются.</li>
<li>Стоимость подтверждается официальной оценкой (экспертизой) — она должна быть не ниже $400 000.</li>
<li>Недвижимость нельзя продавать 3 года — это фиксируется в документах.</li>
<li>Оплата — в валюте через турецкий банк.</li>
<li>Гражданство получают вместе с супругом(ой) и детьми до 18 лет.</li></ul></div>
<div class="box"><h2>ВНЖ Турции по недвижимости — от $200 000</h2><ul>
<li>В Стамбуле для ВНЖ по покупке недвижимости стоимость должна быть от <b>$200 000</b>.</li>
<li>Семейное ВНЖ: выдаётся на собственника и членов семьи и продлевается, пока у вас есть недвижимость.</li>
<li>ВНЖ оформляется только в районах, открытых для регистрации иностранцев, — конкретный адрес мы проверяем перед сделкой.</li></ul></div>
<div class="note">Условия приведены по действующим правилам на момент составления каталога и могут меняться. Перед сделкой менеджер Ferta Estate подтвердит актуальные требования и подберёт объект под вашу цель.</div>
</div>{foot()}</div>'''
pages=[pg,info]
for o in d:
    ph=o['photos'];n=len(ph)
    cl=lambda p:' plan' if p in PL else ''
    cells=[f'<img class="big{cl(ph[0])}" src="{ph[0]}">']
    cells+= [f'<img class="side{cl(p)}" src="{p}">' for p in ph[1:3]]
    rest=ph[3:]
    for p in rest: cells.append(f'<img class="{cl(p).strip()}" style="grid-column:span {12//len(rest)}" src="{p}">')
    gridstyle='' if rest else ' style="grid-template-rows:38mm 38mm"'
    ch=dict(o['chars'])
    tags=[]
    if ch.get('Готовность'): tags.append(f'<span class="tag">{E(ch["Готовность"])}</span>')
    tags.append('<span class="tag g">Под гражданство</span>')
    if any(num(p)>=200000 for p,_ in o['apts']): tags.append('<span class="tag">Под ВНЖ</span>')
    if 'Рассрочка' in ch: tags.append('<span class="tag">Рассрочка</span>')
    kv=''.join(f'<div class="kv"><span>{E(k)}</span><b>{E(v)}</b></div>' for k,v in o['chars'] if k not in('Гражданство','ВНЖ'))
    cs,ct=citizenship(o);rs,rt=residence(o)
    law=f'<div class="law"><div class="cz"><b>🇹🇷 Гражданство Турции за инвестиции</b>{E(ct)}</div><div class="{rs}"><b>ВНЖ Турции по недвижимости</b>{E(rt)}</div></div>'
    hl='<div><h3>Главное об объекте</h3><ul class="hlu">'+''.join(f'<li>{E(h)}</li>' for h in highlights(o))+'</ul></div>'
    apts=''.join(f'<div class="apt"><span>{E(s)}</span><b>{E(p)}</b></div>' for p,s in o['apts'])
    amen=''.join(f'<span>{E(a)}</span>' for a in o['amen'])
    price=o['price'].replace('от ','')
    pages.append(f'''<div class="page">{top(f"Объект №{o['num']} · {o['loc']}")}
<div class="grid"{gridstyle}>{''.join(cells)}</div>
<div class="body"><div class="head"><div><h2>Объект №{o['num']}</h2><div class="loc">{E(o['loc'])}</div></div><div class="price"><small>цена от</small>{E(price)}</div></div>
<div class="tags">{''.join(tags)}</div>
<div class="desc">{E(o['text'])} {E(seo_short(o))}</div>
{law}
<div class="cols"><div>{hl}</div><div><h3>Квартиры в продаже</h3>{apts}</div></div>
<div class="amen">{amen}</div></div>{foot(o)}</div>''')
open('catalog.html','w').write(f'''<!doctype html><html><head><meta charset="utf-8"><title>Каталог Ferta Estate</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>{''.join(pages)}</body></html>''')

json.dump({str(o['num']):{'id':o['id'],'text':o['text']+' '+seo_text(o)} for o in d},open('descriptions_site.json','w'),ensure_ascii=False,indent=1)
