import os,json,urllib.parse,urllib.request,re,html,time
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'assets/stops'); os.makedirs(OUT,exist_ok=True)
queries={
'Cairns Airport':'Cairns Airport terminal','Cairns':'Cairns Esplanade Lagoon','Palm Cove':'Palm Cove Queensland beach','Rex Lookout':'Rex Lookout Queensland','Port Douglas':'Four Mile Beach Port Douglas Queensland','Outer Reef':'Reef Snorkelling on the Great Barrier Reef',
'Mossman Gorge':'Mossman Gorge Queensland','Daintree River':'Daintree River Queensland crocodile','Alexandra Lookout':'Alexandra Range Lookout Daintree','Cape Tribulation':'Cape Tribulation Beach Queensland','Mount Molloy':'Mount Molloy Queensland','Mareeba':'Mareeba Queensland','Lake Barrine':'Lake Barrine Queensland','Yungaburra':'Yungaburra Queensland','Lake Eacham':'Lake Eacham North Queensland','Curtain Fig':'Curtain Fig Tree Queensland','Atherton':'Atherton Queensland town','Millaa Millaa':'MillaaMillaaFallsOct272024','Zillie Falls':'Zillie Falls Queensland','Ellinjaa Falls':'Ellinjaa Falls Queensland','Josephine Falls':'Josephine Falls Queensland','Babinda Boulders':'Babinda Boulders Queensland','Kuranda':'Kuranda Scenic Railway Queensland','Barron Falls':'Barron Falls Queensland'}
preferred={'Palm Cove':'File:Beach at Palm Cove, Queensland, 2020, 11.jpg','Rex Lookout':'File:Rex Lookout, 2015 (02).JPG','Port Douglas':'File:Four Mile Beach, Port Douglas, Queensland, 2020 01.jpg','Outer Reef':'File:Reef Snorkelling on the Great Barrier Reef.jpg','Mossman Gorge':'File:MossmanGorge1.jpg','Alexandra Lookout':'File:Mount Alexandra Lookout - 2013.04 - panoramio.jpg','Cape Tribulation':'File:Cape Tribulation Beach North Queensland-01 (6287300630).jpg','Mareeba':'File:Mareeba Shire Hall (former) (2010).jpg','Lake Barrine':'File:Lakebarrinephoto.jpg','Yungaburra':'File:Lake Eacham Hotel, Yungaburra QUT-7300.jpg','Lake Eacham':'File:Lake Eacham North Queensland.jpg','Millaa Millaa':'File:MillaaMillaaFallsOct272024 01.jpg','Zillie Falls':'File:ZillieFallsOct272024.jpg','Barron Falls':'File:Barron Falls, Queensland.jpg'}
def clean(s): return re.sub('<[^>]+>','',html.unescape(s or '')).strip()
credit_path=os.path.join(OUT,'credits.json'); credits=json.load(open(credit_path)) if os.path.exists(credit_path) else {}
for key,q in queries.items():
    if key in credits and os.path.exists(credits[key]['file']) and key not in ('Palm Cove','Rex Lookout','Alexandra Lookout','Mareeba','Lake Barrine','Yungaburra','Zillie Falls'): continue
    time.sleep(1.5)
    if key in preferred: params={'action':'query','titles':preferred[key],'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':900,'format':'json','origin':'*'}
    else: params={'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':6,'gsrlimit':1,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':900,'format':'json','origin':'*'}
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params); req=urllib.request.Request(url,headers={'User-Agent':'Codex travel guide/1.0'})
    for attempt in range(4):
        try: data=json.load(urllib.request.urlopen(req,timeout=30)); break
        except Exception:
            if attempt==3: raise
            time.sleep(5*(attempt+1))
    page=next(iter(data['query']['pages'].values())); info=page['imageinfo'][0]; meta=info.get('extmetadata',{}); src=info.get('thumburl',info['url']); ext='.jpg' if 'jpeg' in info.get('mime','') or '.jpg' in src.lower() else '.png'; dest=os.path.join(OUT,re.sub(r'[^a-z0-9]+','_',key.lower()).strip('_')+ext)
    open(dest,'wb').write(urllib.request.urlopen(urllib.request.Request(src,headers={'User-Agent':'Codex travel guide/1.0'}),timeout=60).read())
    credits[key]={'title':page['title'][5:],'author':clean(meta.get('Artist',{}).get('value','Wikimedia Commons contributor')),'license':clean(meta.get('LicenseShortName',{}).get('value','')),'page':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(page['title'].replace(' ','_')),'file':dest}
    print(key,'=>',page['title']); json.dump(credits,open(credit_path,'w'),ensure_ascii=False,indent=2)
