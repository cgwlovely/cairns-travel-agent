import os,re,html,urllib.request,urllib.parse,json
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'assets/experiences'); os.makedirs(OUT,exist_ok=True)
pages={
'niramaya':('Niramaya Day Spa','https://events.niramaya.com.au/day-spa'),
'eleme':('Eléme Day Spa Cairns','https://www.crystalbrookcollection.com/eleme-spa/cairns'),
'nightwalk':('Jungle Escapes Night Walk','https://jungleescapes.com.au/tours'),
'spirit':('Spirit of Cairns Dinner Cruise','https://www.spiritofcairns.com.au/dinner-cruise/'),
'salsa':('Salsa Bar & Grill','https://salsaportdouglas.com.au/'),
'ochre':('Ochre Restaurant','https://ochrerestaurant.com.au/')}
ua={'User-Agent':'Mozilla/5.0 Codex travel guide'}; data={}
for key,(label,url) in pages.items():
    raw=urllib.request.urlopen(urllib.request.Request(url,headers=ua),timeout=30).read().decode('utf-8','ignore')
    pats=[r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image']
    img=None
    for pat in pats:
        m=re.search(pat,raw,re.I)
        if m: img=html.unescape(m.group(1)); break
    if not img:
        m=re.search(r'<img[^>]+src=["\']([^"\']+)',raw,re.I); img=html.unescape(m.group(1)) if m else None
    if not img: print('NOIMAGE',key); continue
    img=urllib.parse.urljoin(url,img); blob=urllib.request.urlopen(urllib.request.Request(img,headers=ua),timeout=60).read(); ext='.png' if '.png' in img.lower() else '.jpg'; dest=os.path.join(OUT,key+ext); open(dest,'wb').write(blob)
    data[key]={'label':label,'page':url,'file':dest}; print(key,img)
json.dump(data,open(os.path.join(OUT,'sources.json'),'w'),ensure_ascii=False,indent=2)
