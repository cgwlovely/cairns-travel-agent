import os, json, urllib.parse, urllib.request, re, html
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'assets/photos'); os.makedirs(OUT,exist_ok=True)
files={
'port_douglas':'File:Four Mile Beach, Port Douglas, Queensland, 2020 01.jpg',
'reef':'File:Reef Snorkelling on the Great Barrier Reef.jpg',
'mossman':'File:MossmanGorge1.jpg',
'cape':'File:Cape Tribulation Beach North Queensland-01 (6287300630).jpg',
'lake_eacham':'File:Lake Eacham North Queensland.jpg',
'millaa':'File:MillaaMillaaFallsOct272024 01.jpg',
'barron':'File:Barron Falls, Queensland.jpg'}
def clean(s): return re.sub('<[^>]+>','',html.unescape(s or '')).strip()
credits=[]
for key,title in files.items():
    params={'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1500,'format':'json','origin':'*'}
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={'User-Agent':'Codex travel guide/1.0'}); data=json.load(urllib.request.urlopen(req,timeout=30)); page=next(iter(data['query']['pages'].values())); info=page['imageinfo'][0]; meta=info.get('extmetadata',{})
    src=info.get('thumburl',info['url']); ext='.jpg' if '.jpg' in src.lower() or '.jpeg' in src.lower() else '.png'; dest=os.path.join(OUT,key+ext)
    req=urllib.request.Request(src,headers={'User-Agent':'Codex travel guide/1.0'}); open(dest,'wb').write(urllib.request.urlopen(req,timeout=60).read())
    credits.append({'key':key,'title':title[5:],'author':clean(meta.get('Artist',{}).get('value','Wikimedia Commons contributor')),'license':clean(meta.get('LicenseShortName',{}).get('value','')),'page':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),'file':dest})
    print(key,dest,credits[-1]['license'])
json.dump(credits,open(os.path.join(OUT,'credits.json'),'w'),ensure_ascii=False,indent=2)
