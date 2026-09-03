import os, math, io, json, urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'assets/maps'); os.makedirs(OUT,exist_ok=True)
coords={
'Cairns Airport':(-16.873,145.752),'Cairns':(-16.920,145.778),'Palm Cove':(-16.744,145.670),'Rex Lookout':(-16.617,145.552),'Port Douglas':(-16.484,145.466),'Outer Reef':(-16.20,145.90),
'Mossman Gorge':(-16.472,145.329),'Daintree River':(-16.289,145.414),'Alexandra Lookout':(-16.209,145.421),'Cape Tribulation':(-16.081,145.462),'Mount Molloy':(-16.674,145.330),'Mareeba':(-16.992,145.423),'Lake Barrine':(-17.247,145.632),'Yungaburra':(-17.271,145.584),'Lake Eacham':(-17.285,145.625),'Curtain Fig':(-17.286,145.571),'Atherton':(-17.268,145.475),'Millaa Millaa':(-17.514,145.613),'Zillie Falls':(-17.461,145.690),'Ellinjaa Falls':(-17.448,145.705),'Josephine Falls':(-17.434,145.863),'Babinda Boulders':(-17.344,145.872),'Kuranda':(-16.819,145.638),'Barron Falls':(-16.835,145.644)}

routes={
'overview':['Cairns Airport','Palm Cove','Port Douglas','Mossman Gorge','Daintree River','Cape Tribulation','Mount Molloy','Mareeba','Lake Barrine','Yungaburra','Millaa Millaa','Josephine Falls','Cairns'],
'day01':['Cairns Airport','Palm Cove','Rex Lookout','Port Douglas'],'day02':['Port Douglas','Outer Reef','Port Douglas'],
'day03':['Port Douglas','Mossman Gorge','Daintree River','Alexandra Lookout','Cape Tribulation'],
'day04':['Cape Tribulation','Mount Molloy','Mareeba','Lake Barrine','Yungaburra'],
'day05':['Yungaburra','Lake Eacham','Curtain Fig','Atherton','Yungaburra'],
'day06':['Yungaburra','Millaa Millaa','Zillie Falls','Ellinjaa Falls','Josephine Falls','Cairns'],
'day07':['Cairns','Babinda Boulders','Cairns'],'day08':['Cairns','Kuranda','Barron Falls','Kuranda','Cairns'],
'day09':['Cairns'],'day10':['Cairns','Cairns Airport']}

UA='Codex travel guide map renderer/1.0'
def fetch(url, timeout=30):
    req=urllib.request.Request(url,headers={'User-Agent':UA}); return urllib.request.urlopen(req,timeout=timeout).read()
def merc(lat,lon,z):
    n=2**z; x=(lon+180)/360*n*256; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n*256; return x,y
def route_osrm(names):
    if 'Outer Reef' in names or len(names)<2: return [coords[n] for n in names]
    pts=[]; seq=[]
    # Remove consecutive/repeated terminal points for API, then close visually if needed.
    for n in names:
        if not seq or n!=seq[-1]: seq.append(n)
    q=';'.join(f'{coords[n][1]},{coords[n][0]}' for n in seq)
    url=f'https://router.project-osrm.org/route/v1/driving/{q}?overview=full&geometries=geojson&steps=false'
    try:
        data=json.loads(fetch(url).decode('utf-8')); line=data['routes'][0]['geometry']['coordinates']; pts=[(lat,lon) for lon,lat in line]
    except Exception:
        pts=[coords[n] for n in names]
    return pts
def make(name,names):
    points=[coords[n] for n in names]; road=route_osrm(names)
    allp=points+road; latmin=min(p[0] for p in allp); latmax=max(p[0] for p in allp); lonmin=min(p[1] for p in allp); lonmax=max(p[1] for p in allp)
    latpad=max(.035,(latmax-latmin)*.16); lonpad=max(.035,(lonmax-lonmin)*.16); latmin-=latpad; latmax+=latpad; lonmin-=lonpad; lonmax+=lonpad
    W,H=1500,560 if name!='overview' else 980
    for z in range(13,6,-1):
        ax,ay=merc(latmax,lonmin,z); bx,by=merc(latmin,lonmax,z)
        if bx-ax<=W*1.15 and by-ay<=H*1.15: break
    ax,ay=merc(latmax,lonmin,z); bx,by=merc(latmin,lonmax,z); cx=(ax+bx)/2; cy=(ay+by)/2; left=cx-W/2; top=cy-H/2
    tx0=int(left//256); ty0=int(top//256); tx1=int((left+W)//256); ty1=int((top+H)//256)
    canvas=Image.new('RGB',(W,H),'#e9f3ef')
    for tx in range(tx0,tx1+1):
        for ty in range(ty0,ty1+1):
            try:
                tile=Image.open(io.BytesIO(fetch(f'https://tile.openstreetmap.org/{z}/{tx}/{ty}.png',20))).convert('RGB')
                canvas.paste(tile,(round(tx*256-left),round(ty*256-top)))
            except Exception: pass
    d=ImageDraw.Draw(canvas,'RGBA');
    def xy(p): x,y=merc(p[0],p[1],z); return (round(x-left),round(y-top))
    line=[xy(p) for p in road]
    if len(line)>1:
        d.line(line,fill=(255,255,255,235),width=14,joint='curve'); d.line(line,fill=(8,130,139,255),width=8,joint='curve')
    font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',22); small=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',17)
    for i,n in enumerate(names):
        x,y=xy(coords[n]); col=(239,119,93,255) if i in (0,len(names)-1) else (247,201,92,255); d.ellipse((x-13,y-13,x+13,y+13),fill=col,outline=(255,255,255,255),width=4)
        num=str(i+1); nb=d.textbbox((0,0),num,font=small); d.text((x-(nb[2]-nb[0])/2,y-(nb[3]-nb[1])/2-1),num,font=small,fill=(20,60,58,255))
        label=n; bb=d.textbbox((0,0),label,font=small); tw=bb[2]-bb[0]; th=bb[3]-bb[1]; lx=max(5,min(W-tw-15,x+12)); ly=max(5,min(H-th-12,y-30 if i%2==0 else y+12)); d.rounded_rectangle((lx-5,ly-3,lx+tw+5,ly+th+3),radius=5,fill=(255,255,255,220)); d.text((lx,ly),label,font=small,fill=(26,60,58,255))
    d.rounded_rectangle((8,H-32,410,H-7),radius=5,fill=(255,255,255,220)); d.text((16,H-29),f'© OpenStreetMap contributors  |  zoom {z}',font=small,fill=(60,70,70,255))
    canvas.save(os.path.join(OUT,f'{name}.png'),quality=92)
    print(name,z,len(road))

for name,names in routes.items(): make(name,names)
