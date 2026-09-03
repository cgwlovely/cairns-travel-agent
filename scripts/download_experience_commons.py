import os,json,urllib.parse,urllib.request,re,html,time
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'assets/experiences'); os.makedirs(OUT,exist_ok=True)
items={'spa':'File:Treatment rooms Spa 5 (29788069680).jpg','seafood':'File:Wanneroo seafood platter 20170216 2.jpg','marina':'File:Cairns Marina at Dusk-04and (4196823788).jpg'}
def clean(s): return re.sub('<[^>]+>','',html.unescape(s or '')).strip()
data={}
for key,title in items.items():
 p={'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1400,'format':'json','origin':'*'}; u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p); q=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex travel guide/1.0'}))); page=next(iter(q['query']['pages'].values())); ii=page['imageinfo'][0]; em=ii.get('extmetadata',{}); src=ii.get('thumburl',ii['url']); dest=os.path.join(OUT,key+'.jpg'); open(dest,'wb').write(urllib.request.urlopen(urllib.request.Request(src,headers={'User-Agent':'Codex travel guide/1.0'})).read()); data[key]={'file':dest,'page':'https://commons.wikimedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),'author':clean(em.get('Artist',{}).get('value','')),'license':clean(em.get('LicenseShortName',{}).get('value',''))}; print(key)
json.dump(data,open(os.path.join(OUT,'commons.json'),'w'),ensure_ascii=False,indent=2)
