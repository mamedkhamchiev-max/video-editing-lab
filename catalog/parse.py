import json,re,glob,os,sys,html as H,urllib.request
site=sys.argv[1]; out=sys.argv[2]
os.makedirs(out+'/img',exist_ok=True)
objs=[]
for f in glob.glob(site+'/det/*.json'):
    d=json.load(open(f)); pid=d['id']
    raw=open(f'{site}/html/{pid}.html',encoding='utf-8').read()
    lines=[H.unescape(l).strip() for l in re.sub(r'<[^>]*>','\n',raw).split('\n')]
    lines=[l for l in lines if l]
    a=lines.index('← Назад к объектам'); b=lines.index('Связаться с продавцом')
    L=lines[a+1:b]
    o={'id':pid,'title':L[0],'price':L[1],'loc':L[2],'desc':'','chars':[],'amen':[],'apts':[]}
    i=3
    if L[i]=='Описание': o['desc']=L[i+1]; i+=2
    assert L[i]=='Характеристики'; i+=1
    while L[i] not in('Инфраструктура и удобства','Доступные квартиры в этом объекте'):
        o['chars'].append((L[i],L[i+1])); i+=2
    if L[i]=='Инфраструктура и удобства':
        i+=1
        while L[i]!='Доступные квартиры в этом объекте': o['amen'].append(L[i]); i+=1
    i+=1
    while i<len(L):
        if L[i].startswith('$') or L[i][0].isdigit():
            price=L[i]; spec=L[i+1]; o['apts'].append((price,spec)); i+=2
            if i<len(L) and L[i].startswith('Квартира'): i+=1
            if i<len(L) and not L[i].startswith('$') and not L[i][0].isdigit(): i+=1
        else: i+=1
    ph=sorted(d['photos'],key=lambda p:(not p['is_main'],p['order']))[:3]
    o['photos']=[]
    for k,p in enumerate(ph):
        ext=os.path.splitext(p['url'])[1]; fn=f'img/{pid}-{k}{ext}'
        if not os.path.exists(out+'/'+fn): urllib.request.urlretrieve('https://fertaestate.com'+p['url'],out+'/'+fn)
        o['photos'].append(fn)
    o['num']=int(re.search(r'\d+',o['title']).group())
    objs.append(o)
objs.sort(key=lambda o:o['num'])
json.dump(objs,open(out+'/data.json','w'),ensure_ascii=False,indent=1)
print(len(objs)); print(json.dumps(objs[0],ensure_ascii=False)[:800])
for o in objs: print(o['num'],o['price'],o['loc'],len(o['apts']),len(o['amen']),bool(o['desc']))
