from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, Flowable
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
import os, math, json, re

ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(ROOT,'output/pdf/Cairns_2026_熊仔鸡仔旅行手册.pdf')
FONT='/System/Library/Fonts/STHeiti Medium.ttc'
pdfmetrics.registerFont(TTFont('CN',FONT))
pdfmetrics.registerFont(TTFont('CNB',FONT))

TEAL=colors.HexColor('#167C80'); DARK=colors.HexColor('#203C3B'); CORAL=colors.HexColor('#EF775D')
CREAM=colors.HexColor('#FFF8E9'); MINT=colors.HexColor('#EAF6F1'); YELLOW=colors.HexColor('#F7C95C'); GREY=colors.HexColor('#526564')

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CNTitle',fontName='CNB',fontSize=27,leading=34,textColor=DARK,alignment=TA_CENTER,spaceAfter=8))
styles.add(ParagraphStyle(name='CNSub',fontName='CN',fontSize=11,leading=17,textColor=GREY,alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1CN',fontName='CNB',fontSize=21,leading=27,textColor=DARK,spaceAfter=7))
styles.add(ParagraphStyle(name='H2CN',fontName='CNB',fontSize=12.5,leading=17,textColor=TEAL,spaceBefore=4,spaceAfter=4))
styles.add(ParagraphStyle(name='BodyCN',fontName='CN',fontSize=9.2,leading=14,textColor=DARK,spaceAfter=4))
styles.add(ParagraphStyle(name='DenseBodyCN',fontName='CN',fontSize=8.15,leading=11.15,textColor=DARK,spaceAfter=2))
styles.add(ParagraphStyle(name='DenseH2CN',fontName='CNB',fontSize=11.2,leading=14,textColor=TEAL,spaceBefore=2,spaceAfter=2))
styles.add(ParagraphStyle(name='SmallCN',fontName='CN',fontSize=7.7,leading=11,textColor=GREY))
styles.add(ParagraphStyle(name='TinyCN',fontName='CN',fontSize=6.8,leading=9,textColor=GREY))
styles.add(ParagraphStyle(name='WhiteCN',fontName='CNB',fontSize=9,leading=12,textColor=colors.white))

coords={
'Cairns Airport':(-16.873,145.752),'Cairns':(-16.920,145.778),'Palm Cove':(-16.744,145.670),'Rex Lookout':(-16.617,145.552),'Port Douglas':(-16.484,145.466),
'Outer Reef':(-16.20,145.90),'Mossman Gorge':(-16.472,145.329),'Daintree River':(-16.289,145.414),'Alexandra Lookout':(-16.209,145.421),'Cape Tribulation':(-16.081,145.462),
'Mount Molloy':(-16.674,145.330),'Mareeba':(-16.992,145.423),'Lake Barrine':(-17.247,145.632),'Yungaburra':(-17.271,145.584),
'Lake Eacham':(-17.285,145.625),'Curtain Fig':(-17.286,145.571),'Atherton':(-17.268,145.475),'Millaa Millaa':(-17.514,145.613),'Zillie Falls':(-17.461,145.690),'Ellinjaa Falls':(-17.448,145.705),'Josephine Falls':(-17.434,145.863),
'Babinda Boulders':(-17.344,145.872),'Botanic Gardens':(-16.899,145.746),'Smithfield':(-16.836,145.695),'Kuranda':(-16.819,145.638),'Barron Falls':(-16.835,145.644)
}

class RouteMap(Flowable):
    def __init__(self, stops, width=174*mm, height=47*mm):
        super().__init__(); self.stops=stops; self.width=width; self.height=height
    def draw(self):
        c=self.canv; pts=[coords[s] for s in self.stops]
        lats=[p[0] for p in pts]; lons=[p[1] for p in pts]
        pad=13*mm; x0=pad; y0=8*mm; w=self.width-2*pad; h=self.height-15*mm
        latmin,latmax=min(lats),max(lats); lonmin,lonmax=min(lons),max(lons)
        if latmax-latmin<.12: latmin-=.06; latmax+=.06
        if lonmax-lonmin<.12: lonmin-=.06; lonmax+=.06
        def xy(p): return (x0+(p[1]-lonmin)/(lonmax-lonmin)*w, y0+(p[0]-latmin)/(latmax-latmin)*h)
        c.setFillColor(MINT); c.roundRect(0,0,self.width,self.height,5*mm,fill=1,stroke=0)
        c.setStrokeColor(colors.HexColor('#A9D4CB')); c.setLineWidth(.5)
        for i in range(1,4): c.line(x0,y0+i*h/4,x0+w,y0+i*h/4)
        c.setStrokeColor(TEAL); c.setLineWidth(2.3); c.setLineCap(1)
        for a,b in zip(pts,pts[1:]): c.line(*xy(a),*xy(b))
        for i,(name,p) in enumerate(zip(self.stops,pts)):
            x,y=xy(p); c.setFillColor(CORAL if i in (0,len(pts)-1) else YELLOW); c.circle(x,y,3.1,fill=1,stroke=0)
            c.setFillColor(DARK); c.setFont('CN',6.5)
            off=7 if i%2==0 else -11
            c.drawCentredString(x,y+off,name)
        c.setFillColor(GREY); c.setFont('CN',6); c.drawRightString(self.width-4*mm,3*mm,'↑ 北｜按真实经纬度比例绘制；连线为行程顺序示意')

class OverviewMap(RouteMap):
    def __init__(self):
        super().__init__(['Cairns Airport','Palm Cove','Port Douglas','Mossman Gorge','Daintree River','Cape Tribulation','Mount Molloy','Mareeba','Lake Barrine','Yungaburra','Millaa Millaa','Josephine Falls','Cairns'],174*mm,122*mm)
    def draw(self):
        super().draw(); c=self.canv
        c.setFillColor(colors.Color(0.1,0.48,0.58,alpha=.08)); c.roundRect(120*mm,13*mm,45*mm,94*mm,4*mm,fill=1,stroke=0)
        c.setFillColor(TEAL); c.setFont('CNB',8); c.drawString(139*mm,102*mm,'珊瑚海岸')
        c.setFillColor(colors.Color(0.75,0.55,0.15,alpha=.10)); c.roundRect(28*mm,12*mm,82*mm,43*mm,4*mm,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#8C6B22')); c.drawString(31*mm,16*mm,'Atherton Tablelands 高原')

def p(txt,style='BodyCN'): return Paragraph(txt,styles[style])
def link(label,url): return f'<link href="{url}" color="#167C80"><u>{label}</u></link>'
PHOTO_DIR=os.path.join(ROOT,'assets/photos')
PHOTO_CREDITS={x['key']:x for x in json.load(open(os.path.join(PHOTO_DIR,'credits.json')))}
PHOTO_LABELS={'port_douglas':'Four Mile Beach｜抵达后沿海滩散步、看日落','reef':'大堡礁浮潜｜面镜下可见珊瑚与热带鱼','mossman':'Mossman Gorge｜巨石、溪流与湿热雨林','cape':'Cape Tribulation｜雨林直接延伸到热带海滩','lake_eacham':'Lake Eacham｜火山口湖环湖步行','millaa':'Millaa Millaa Falls｜瀑布环线的代表景观','barron':'Barron Falls｜景观铁路与雨林峡谷'}
def crop_photo(key,w=1400,h=390):
    src=PHOTO_CREDITS[key]['file']; dest=os.path.join(PHOTO_DIR,key+'_crop.jpg')
    im=PILImage.open(src).convert('RGB'); scale=max(w/im.width,h/im.height); im=im.resize((round(im.width*scale),round(im.height*scale)))
    left=(im.width-w)//2; top=(im.height-h)//2; im.crop((left,top,left+w,top+h)).save(dest,quality=90); return dest
def photo_card(key,width=174*mm):
    cr=PHOTO_CREDITS[key]; cap=PHOTO_LABELS[key]+'　｜　'+link(f"{cr['author']} · {cr['license']}",cr['page'])
    t=Table([[Image(crop_photo(key),width=width,height=width*390/1400)],[p(cap,'TinyCN')]],colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#C9D8D4')),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(0,0),0),('BOTTOMPADDING',(0,0),(0,0),0),('LEFTPADDING',(0,1),(0,1),5),('TOPPADDING',(0,1),(0,1),3),('BOTTOMPADDING',(0,1),(0,1),3)])); return t
STOP_DIR=os.path.join(ROOT,'assets/stops'); STOP_CREDITS=json.load(open(os.path.join(STOP_DIR,'credits.json')))
STOP_ACTION={'Cairns Airport':'取车 / 还车','Cairns':'泻湖、海滨步道与吃饭','Palm Cove':'午餐、椰林海滩','Rex Lookout':'俯瞰海岸公路','Port Douglas':'海滩、码头与住宿','Outer Reef':'浮潜看珊瑚与热带鱼','Mossman Gorge':'雨林步道与溪谷','Daintree River':'乘船寻找鳄鱼','Alexandra Lookout':'俯瞰河口与珊瑚海','Cape Tribulation':'雨林与海滩交界','Mount Molloy':'转场休息小镇','Mareeba':'午餐与本地咖啡','Lake Barrine':'湖景、茶屋与游船','Yungaburra':'住宿、老街与鸭嘴兽','Lake Eacham':'火山口湖环湖步行','Curtain Fig':'巨型垂帘榕树','Atherton':'补给与小镇休息','Millaa Millaa':'主瀑布与拍照','Zillie Falls':'瀑布观景','Ellinjaa Falls':'林间步道与瀑布','Josephine Falls':'雨林水潭','Babinda Boulders':'巨石溪谷步道','Kuranda':'雨林村与景观铁路','Barron Falls':'峡谷瀑布观景'}
def stop_crop(name,w=700,h=330):
    src=STOP_CREDITS[name]['file']; dest=os.path.join(STOP_DIR,re.sub(r'[^a-z0-9]+','_',name.lower()).strip('_')+'_crop.jpg')
    im=PILImage.open(src).convert('RGB'); scale=max(w/im.width,h/im.height); im=im.resize((round(im.width*scale),round(im.height*scale))); left=(im.width-w)//2; top=(im.height-h)//2; im.crop((left,top,left+w,top+h)).save(dest,quality=86); return dest
def stop_gallery(stops):
    cols=4; cw=42.75*mm; rows=[]
    for base in range(0,len(stops),cols):
        chunk=stops[base:base+cols]; pics=[]; caps=[]
        for j,name in enumerate(chunk):
            idx=base+j+1; pics.append(Image(stop_crop(name),width=cw,height=17.2*mm)); caps.append(p(f'<b>{idx} {name}</b><br/>{STOP_ACTION[name]}','TinyCN'))
        while len(pics)<cols: pics.append(''); caps.append('')
        rows.extend([pics,caps])
    t=Table(rows,colWidths=[cw]*cols)
    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.35,colors.HexColor('#C9D8D4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)])); return t
def pill(txt,bg=TEAL):
    t=Table([[p(txt,'WhiteCN')]],colWidths=[174*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),0,bg),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])); return t
def box(title,content,bg=CREAM):
    data=[[p(title,'H2CN')],[p(content,'BodyCN')]]; t=Table(data,colWidths=[174*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),.6,colors.HexColor('#D9D2BD')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])); return t
def dense_box(title,content,bg=CREAM):
    data=[[p(title,'DenseH2CN')],[p(content,'DenseBodyCN')]]
    t=Table(data,colWidths=[174*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#D9D2BD')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    return t

days=[
('DAY 1｜9月17日 周四','Cairns Airport → Palm Cove → Port Douglas','约 70 km｜净驾驶约 1小时20分',['Cairns Airport','Palm Cove','Rex Lookout','Port Douglas'],
'上午从 Brisbane 飞抵 Cairns，机场取车。沿 Captain Cook Highway 北上；Palm Cove 午餐与海滩散步 1–1.5 小时，Rex Lookout 停 15 分钟，傍晚到 Four Mile Beach 看日落。',
'<b>Palm Cove｜顺路午餐：</b>Nu Nu（海景与热带食材，主食约 $25–40，首选但需预约）；Chill at Portofino（汉堡/海鲜约 $20–35，时间紧更合适）。<br/><b>Port Douglas｜抵达后晚餐：</b>Jungle Fowl（本地食材，两人约 $100–170，社区口碑首选）或 Salsa（热带融合，约 $45–75/人）；预算版 N17 Burger Co（约 $18–28）。',
'机场柜台取车比先接驳到 PD 再租省一次搬运行李。天黑后沿海路视线差，尽量日落前抵达。'),
('DAY 2｜9月18日 周五','Port Douglas → Agincourt Ribbon Reefs → Port Douglas','全天出海｜08:30–16:30 左右',['Port Douglas','Outer Reef','Port Douglas'],
'核心日：Silversonic 外堡礁，通常游览 3 个外礁点；含浮潜装备、午餐与讲解。不会潜水也可参加导潜浮潜；想水肺可另加体验潜。',
'<b>出海前早餐：</b>Grant Street Kitchen（面包、咖啡，约 $10–22；早到外带）。<br/><b>码头回港晚餐：</b>Wrasse & Roe（精致海鲜，约 $60–100/人，庆祝型首选）；若前晚没吃，可选 Jungle Fowl 或 Salsa。<br/><b>省钱：</b>The Mexican（分享菜约 $25–40/人）。',
'2026/27 官方 Silversonic 成人 $328；体验潜 1 次 $98，持证潜 1 次 $72。易晕船者提前咨询药师，开船前按药品说明服用并坐船尾下层。海况差可优先改到 9/25。'),
('DAY 3｜9月19日 周六','Port Douglas → Mossman Gorge → Daintree River → Cape Tribulation','约 105 km｜分段驾驶约 2–2.5小时',['Port Douglas','Mossman Gorge','Daintree River','Alexandra Lookout','Cape Tribulation'],
'08:00 出发，Mossman Gorge 走 Rainforest Circuit；中午前往 Daintree River 野生动物巡航，过车渡后停 Alexandra Lookout，傍晚 Cape Tribulation Beach。',
'<b>午餐：</b>Mossman Gorge Centre Café 或 Daintree Village 轻食（约 $18–30）。<br/><b>Cape：</b>Turtle Rock Café（咖啡 $5.5 起、午餐约 $18–30，15:00 前）；Mason’s Café 可试本地热带水果 smoothie；晚餐优先住宿内餐厅并提前确认。',
'Mossman Gorge 2026/27 接驳成人 $15.50，8:00–17:00 每 15 分钟；末班回程 16:30。Solar Whisper 1 小时巡航 $35，野生动物不保证。车渡可能排队，油箱在 Mossman 补足。'),
('DAY 4｜9月20日 周日','Cape Tribulation → Mount Molloy → Mareeba<br/>→ Lake Barrine → Yungaburra','约 240 km｜净驾驶约 3.5–4小时',['Cape Tribulation','Mount Molloy','Mareeba','Lake Barrine','Yungaburra'],
'这是最长转场。早上走短版 Dubuji Boardwalk，随后原路过渡轮，经 Mount Molloy 进入高原；Mareeba 午餐/咖啡，Lake Barrine 湖畔停留后到 Yungaburra。',
'<b>Mareeba｜途中休息：</b>Skybury Café（本地咖啡与木瓜，视营业日；约 $15–30）或 Coffee Works（咖啡/巧克力采购）。<br/><b>Yungaburra｜到店后晚餐：</b>Our Place（两人约 $80–140，就近少开夜路，提前确认营业）或 Nick’s Restaurant（披萨意面约 $25–45，周日通常营业）。',
'北段手机信号不稳定，离线地图和水要提前备好。不要把 Daintree 至 Yungaburra 当 3 小时整：渡轮、午饭和观景后建议预留 6–7 小时。'),
('DAY 5｜9月21日 周一','Yungaburra → Lake Eacham → Curtain Fig → Atherton → Yungaburra','约 55 km｜净驾驶约 1小时15分',['Yungaburra','Lake Eacham','Curtain Fig','Atherton','Yungaburra'],
'上午 Lake Eacham 环湖步道（约 3 km）与湖边放松；午后 Curtain Fig Tree 木栈道、Atherton 补给，再回小镇找鸭嘴兽观景点等候黄昏。',
'<b>Yungaburra 早餐/午餐：</b>Whistle Stop Café（花园咖啡馆，约 $15–28；周一约 7:30–15:00）。<br/><b>Lake Barrine 下午茶：</b>Tea House（司康/茶约 $12–25，通常 9:00–14:30）。<br/><b>晚餐：</b>Our Place（若前晚没吃，须确认周一营业）或 Yungaburra Hotel（pub 餐约 $22–38）；Nick’s 周一通常休息。',
'湖泊为自然水域，是否下水看现场警示。鸭嘴兽最好清晨/黄昏安静等候，不用追赶或打灯。高原夜间比海边凉，带薄外套。'),
('DAY 6｜9月22日 周二','Yungaburra → Millaa Millaa Falls → Zillie → Ellinjaa → Josephine Falls → Cairns','约 190 km｜净驾驶约 3小时',['Yungaburra','Millaa Millaa','Zillie Falls','Ellinjaa Falls','Josephine Falls','Cairns'],
'早出发跑 Waterfall Circuit：Millaa Millaa 主瀑、Zillie 观景、Ellinjaa 林间步道；午后南下 Josephine Falls，再沿 Bruce Highway 北返 Cairns。',
'<b>出发前：</b>Whistle Stop 外带咖啡。<br/><b>瀑布途中：</b>Millaa Millaa 小镇 bakery/pub 简餐约 $15–28。<br/><b>抵达 Cairns：</b>Prawn Star（码头船上海鲜，两人约 $90–160，体验感首选）或 Ganbaranba 拉面（约 $18–25，省钱但常排队）。',
'雨后石面极滑；只在开放区域下水，Josephine Falls 以现场封闭标识为准。瀑布间不是高速路，切勿按导航最短时间连续赶场。'),
('DAY 7｜9月23日 周三','Cairns 弹性日：Babinda / 植物园 / 泻湖','0–140 km｜按天气决定',['Cairns','Babinda Boulders','Cairns'],
'晴天且愿意开车：Babinda Boulders 半日；想休息：Flecker Botanic Gardens、Esplanade Lagoon、夜市。若后面不再自驾，今天在市区还车最省停车费。',
'<b>植物园/Edge Hill 前：</b>Guyala Café（咖啡与早午餐，两人约 $45–75，社区推荐）最顺路；留在市中心则选 Caffiend（主食约 $17–42）。<br/><b>正式晚餐：</b>Ochre（澳洲原生食材，约 $60–100/人，需预约）或 Bellocale（海鲜意面、意大利菜）。<br/><b>省钱：</b>Ganbaranba 或 Orchid Plaza 亚洲餐。',
'Babinda 水流可非常危险，绝不越过护栏或进入封闭水道。这个弹性日也可用于处理前段天气变化，但 Reef 改期要看船位。'),
('DAY 8｜9月24日 周四','Cairns → Kuranda（2026 工程期特别版）→ Cairns','公共交通/接驳为主',['Cairns','Kuranda','Barron Falls','Kuranda','Cairns'],
'上午搭 Kuranda Scenic Railway 上山，逛村 2–3 小时；因 2026 年 8月19日至10月25日 Skyrail 升级，正常“火车上、缆车下”不可照常运行。可选 Scenic Train 往返 + Kuranda–Barron Falls–Kuranda 的 Skyrail Loop。',
'<b>Kuranda｜白天：</b>Frogs Restaurant 或市场轻食约 $18–32；咖啡/冰淇淋约 $6–12。<br/><b>Cairns｜回程后：</b>Salt House（码头小食/披萨约 $25–45）或 Dundee’s Waterfront（海鲜/牛排约 $45–80）；想吃当地人推荐的意大利菜可改 Bellocale。',
'工程期参考组合成人约 $128（具体班次以预订页为准）；Skyrail Loop 单独成人约 $41，且标示周三至周日运行。9/24 是周四，原则上匹配，但必须在付款前核对当天班次与接驳。'),
('DAY 9｜9月25日 周五','Cairns 弹性日（二）<br/>外礁备用日','市区步行或全天出海',['Cairns','Cairns'],
'若 9/18 因海况取消，今天优先安排 Cairns 出发的外礁船，而不是强行赶回 Port Douglas；若原计划完成，则睡到自然醒，Esplanade、Lagoon、Marina 与夜市慢游。',
'<b>早午餐：</b>植物园方向选 Guyala Café；市中心选 Caffiend（约 $18–32/人）。<br/><b>海鲜：</b>Prawn Star 适合轻松体验；正式晚餐选 Ochre，意大利菜选 Bellocale。<br/><b>若前几天都没订到：</b>把这一晚留给最想吃的店；甜点可在夜市周边吃水果冰沙或 gelato（约 $7–12）。',
'备用 Reef 的船公司、出发码头、潜水要求和取消条款会不同，不能直接把 Silversonic 票平移。至少提前 48–72 小时与原供应商确认改签方案。'),
('DAY 10｜9月26日 周六','Cairns → Cairns Airport → Brisbane','市区至机场约 15–20分钟',['Cairns','Cairns Airport'],
'悠闲早午餐、最后采购，按国内航班建议预留时间前往机场。若租车留到今天，先加油再还车；若已还车，用 taxi/rideshare。',
'<b>机场前早午餐：</b>住宿在市中心选 Caffiend、Bang & Grind 或 Wharf ONE（约 $18–32）；若租车尚未归还且时间充足，可去 Guyala Café。<br/><b>带走：</b>本地咖啡豆、Daintree 茶、Tablelands 巧克力；液体与易融食品注意手提行李限制。',
'航班未提供，手册不假设起降时刻。建议在航班起飞前约 2 小时抵达机场，并把周末活动/道路延误留进缓冲。')]

# 每日页的“旅行指南”补充：强调现场体验与味觉预期，不照搬任何出版物文字。
DAY_SCENE={
1:'Captain Cook Highway 一侧是珊瑚海、一侧是陡升的湿热带山地。Palm Cove 适合脱鞋走椰林海滩；Rex Lookout 看的是海岸公路弧线和山海夹缝；Four Mile Beach 的乐趣是宽阔沙滩与小镇度假感，不是追逐密集景点。每站宁可停足，也不要一路下车拍照。',
2:'快艇离岸后颜色会从近岸灰蓝转为外礁的深蓝和泻湖蓝。三个礁点的能见度、流速和鱼群会不同：先听船员简报，再根据体力选择跟导游或自己浮潜。常见看点是枝状珊瑚、巨型蛤、鹦嘴鱼和成群小鱼；海龟或礁鲨属于惊喜，并非保证。全天日晒、风和上下船比想象中耗体力。',
3:'Mossman Gorge 的主角是花岗岩巨石、清水与浓密树冠；Daintree River 则要把速度慢下来，导游会从树根、泥滩和水面纹路中找鳄鱼与鸟。过河后道路更窄，Alexandra Lookout 能看见河口、低地雨林和珊瑚海叠在一起。Cape Tribulation 最迷人的是雨林几乎贴到沙滩边。',
4:'一天内会从潮湿海岸雨林切换到较干燥的高原农地，景观变化本身就是重点。Mareeba 周围常见咖啡、甘蔗与热带果园；Lake Barrine 是火山口湖，水面安静、林缘适合短暂停留。当天不要追求“再塞一个景点”，渡轮排队和山路会消耗时间。',
5:'Lake Eacham 是被雨林围住的火山口湖，环湖步道阴凉但潮湿，适合慢走听鸟声。Curtain Fig 的气根像一整面垂落的帘幕，木栈道短而直观。黄昏看鸭嘴兽需要耐心：站定、少说话，寻找水面缓慢扩散的圆形波纹，比沿岸不停走动更有效。',
6:'三座高原瀑布气质不同：Millaa Millaa 正面开阔、最适合完整瀑布照片；Zillie 从上方听水势，视角较局促；Ellinjaa 要走湿滑林径，但更有藏在森林里的感觉。Josephine Falls 的巨石与水槽很漂亮，水量上升时也最危险，现场封闭线永远优先于网络照片。',
7:'Babinda Boulders 是清澈溪水穿过巨大花岗岩，观景步道安全、禁入水道则可能有致命暗流。若留在 Cairns，植物园不是普通城市花园：蕨类、棕榈、姜花和湿热带鸟类很集中；Red Arrow 是短而陡的台阶型锻炼。Esplanade Lagoon 适合把节奏降下来。',
8:'景观铁路的看点是老式山地工程、隧道、桥梁和 Barron Gorge，而不只是抵达 Kuranda。坐靠峡谷一侧通常更容易看瀑布与山谷，但方向以当天列车编组为准。Kuranda 的市场和动物园商业感较强，给自己 2–3 小时足够；重点放在铁路景观和 Barron Falls。',
9:'这是“根据天气兑现遗憾”的一天：海况好且外礁未完成才出海；否则用步行串起 Lagoon、Esplanade、Marina、Rusty’s Market 与咖啡馆。Cairns 市区不是沙滩目的地，魅力在热带海滨生活、候鸟泥滩、码头和多元餐饮。安排 Spa 时至少预留疗程前后各半小时。',
10:'返程日的目标是从容而不是再完成清单。海滨晨走能看到城市慢慢醒来；采购优先选择有明确产地的 Tablelands 咖啡、Daintree 茶或本地巧克力。热带水果、酱料和液体要先确认航空与检疫要求，避免在安检前临时处理。'
}
DAY_TASTE={
1:'Palm Cove 的海景餐厅常把热带水果、青柠、椰香和海鲜放在同一盘里；Nu Nu 更偏精致而有地域感。Port Douglas 的 Jungle Fowl 适合分享式小盘和本地农产，Salsa 则是热带亚洲风味。第一天若航班延误，选汉堡或海边简餐比勉强赶预约更舒服。',
2:'出海前宜吃面包、香蕉或简单鸡蛋，避免油腻大早餐。回港后通常会想吃咸鲜和碳水：Wrasse & Roe 可期待生蚝、当日鱼类与精致摆盘；The Mexican 更适合分享、喝一杯并控制预算。把最贵的晚餐留在确认没有晕船之后。',
3:'Mossman 与 Daintree 的餐饮选择明显变少，期待的是咖啡馆简餐、三明治、派和热带水果，而不是城市级精致餐饮。Cape 可试当地种植的水果制成的冰淇淋或 smoothie；晚餐依赖住宿时，要同时确认最后点餐时间和是否必须预订。',
4:'高原是北昆士兰的“食物篮”：咖啡、木瓜、香蕉、乳制品和牛肉比海鲜更值得期待。Skybury 的重点是产地咖啡和木瓜产品；Coffee Works 适合买豆与巧克力。到 Yungaburra 后选择就近晚餐，避免摸黑山路。',
5:'这天适合慢食：花园咖啡馆的早餐、Lake Barrine 的司康与茶、晚上小镇 pub 或家常餐。重点不是复杂菜单，而是高原凉爽空气、老建筑和本地食材。若想吃 Our Place，先问当天菜单和营业时间，小镇餐厅临时休息并不少见。',
6:'瀑布线路上不要等到饿了才找店，面包店的肉派、香肠卷和咖啡最可靠。抵达 Cairns 后，Prawn Star 的乐趣是坐在渔船上用手吃虾、牡蛎或拼盘；Ganbaranba 则是浓郁拉面、速度快、价格低，适合淋雨或走累后的热食。',
7:'Guyala 适合咖啡、鸡蛋、酸种面包和偏现代澳式的早午餐；Ochre 的看点是把袋鼠、鳄鱼、柠檬桃金娘等原生食材做成较正式的菜单；Bellocale 更偏意大利海鲜与手工面。三者体验差异很大，不必只按评分选择。',
8:'Kuranda 午餐以市场轻食、汉堡、沙拉和咖啡为主，景区价与等待时间可能高于市区。回 Cairns 后再认真吃：Salt House 胜在码头气氛和分享小食，Dundee’s 是传统海鲜牛排，Bellocale 更适合在意面与海鲜上追求味道。',
9:'Rusty’s Market 适合认识红毛丹、山竹、释迦、木瓜等热带水果，但先少量试吃。Prawn Star 重气氛与海鲜本味，Ochre 重澳洲原生食材，Bellocale 重意大利烹调；三家不要当作同一类“海鲜餐厅”比较。下午 Spa 后宜选轻松晚餐。',
10:'早午餐选离住宿或机场动线最近的一家即可：澳式 café 常见 flat white、鸡蛋、酸种吐司、牛油果和烘焙点心。若购买咖啡豆，询问烘焙日期与风味；送礼用巧克力注意车内和行李舱温度。'
}

def footer(c,doc):
    c.saveState(); c.setStrokeColor(colors.HexColor('#CFE4DE')); c.line(18*mm,14*mm,192*mm,14*mm)
    c.setFont('CN',7); c.setFillColor(GREY); c.drawString(18*mm,9*mm,'熊仔 × 鸡仔｜Cairns 2026 行程手册')
    c.drawRightString(192*mm,9*mm,str(doc.page)); c.restoreState()

story=[]
# Cover
cover=os.path.join(ROOT,'assets/cover.png'); story.append(Spacer(1,4*mm)); story.append(Image(cover,width=174*mm,height=174*mm*1536/1056))
story.append(Spacer(1,-104*mm)); story.append(p('凯恩斯 · 雨林 · 高原 · 大堡礁','CNTitle')); story.append(p('2026.09.17—09.26｜10天9晚自驾环线','CNSub')); story.append(Spacer(1,77*mm)); story.append(p('熊仔与鸡仔的热带旅行手册','CNSub')); story.append(PageBreak())

story += [p('先看这一页｜路线与关键提醒','H1CN'), Image(os.path.join(ROOT,'assets/highlights.png'),width=174*mm,height=52*mm), Spacer(1,3*mm),
Image(os.path.join(ROOT,'assets/maps/day01.png'),width=174*mm,height=65*mm), Spacer(1,4*mm),
box('住宿节奏','Port Douglas 2晚 → Cape Tribulation 1晚 → Yungaburra 2晚 → Cairns 4晚。三次搬酒店，形成顺时针感的环线；Daintree 北段仍需原路返回渡轮。'),Spacer(1,3*mm),
box('2026 年最重要的变化','9月24日落在 Skyrail 升级工程期（8月19日–10月25日）。不要购买/期待常规“火车上山、缆车一路下山”；本手册已改为火车往返 + Kuranda 端 Skyrail Loop 的可行思路。',colors.HexColor('#FFF0E9')),Spacer(1,3*mm),
box('价格口径','所有金额均为澳元 AUD、以成人为主。已公布的 2026/27 官方价直接列出；餐饮为菜单/当地常见消费区间。未付款前都不是锁价，营业日与供应情况须再次确认。'),PageBreak()]

story += [p('全程总览地图','H1CN'),p('OpenStreetMap 道路底图，北在上；蓝绿色线路按公开道路路线绘制，实际驾驶仍请用实时导航。','BodyCN'),Image(os.path.join(ROOT,'assets/maps/overview.png'),width=174*mm,height=113.7*mm),Spacer(1,5*mm),
box('路线方向','Cairns Airport 沿海岸向北到 Port Douglas；继续北上进入 Daintree 与 Cape Tribulation；随后返回渡轮，向西南穿过 Mount Molloy / Mareeba 进入高原，再经瀑布带回到 Cairns。'),PageBreak()]

summary=[
['日期','住宿 / 入住','主要地点','核心项目','当日参考价/2人'],
['9/17','Port Douglas｜14:00 后','机场–Palm Cove–PD','海岸公路、日落','餐饮 $80–150'],
['9/18','Port Douglas｜续住','PD–Outer Reef–PD','Silversonic','$656 + 可选潜水'],
['9/19','Cape Trib｜14:00 后','Mossman–Daintree–Cape','峡谷、鳄鱼巡航','$91 起 + 住宿'],
['9/20','Yungaburra｜14:00 后','Cape–Mareeba–湖区','长途转场、咖啡','$70–130'],
['9/21','Yungaburra｜续住','Eacham–Curtain Fig–Atherton','环湖、巨型榕树','$60–120'],
['9/22','Cairns｜14:00 后','瀑布环线–Josephine–Cairns','三瀑布、雨林水潭','$70–140'],
['9/23','Cairns｜续住','Babinda / 植物园 / Lagoon','天气弹性日','$40–160'],
['9/24','Cairns｜续住','Cairns–Kuranda–Cairns','工程期火车 + Loop','$256 起'],
['9/25','Cairns｜续住','市区 / Reef 备用','海滨慢游或补 Reef','$50–700'],
['9/26','退房 10:00 左右','Cairns–机场–Brisbane','返程','机票另计']]
st=Table([[p(x,'TinyCN') for x in row] for row in summary],colWidths=[16*mm,35*mm,47*mm,43*mm,33*mm],repeatRows=1)
st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#B8CBC6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,MINT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [p('10天总表｜住哪里、几点入住、当天花多少','H1CN'),p('住宿尚未由你指定，以下时间采用推荐酒店公布规则或常见 14:00 入住 / 10:00 退房；订房后以确认邮件为准。','BodyCN'),st,Spacer(1,4*mm),p('“当日参考价”不含对应住宿与机票；9/19 的 $91 起约为两人 Mossman Gorge 接驳 + Daintree 1小时巡航。','SmallCN'),PageBreak()]

accom=[
['住几晚','推荐住宿','地址','入住 / 退房','参考房价','预订入口'],
['2晚\n9/17–19','Lazy Lizard Motor Inn','121 Davidson St, Port Douglas','14:00 / 10:00','实时页面约 $263/晚；2晚约 $526',link('官网查价','https://www.lazylizardinn.com.au/')],
['1晚\n9/19–20','Ferntree Rainforest Lodge','36 Camelot Cl, Cape Tribulation','14:00 / 10:00','房型约 $249–399+/晚；实时为准',link('官网预订','https://www.ferntreelodge.com/')],
['2晚\n9/20–22','Eden House Retreat','20 Gillies Hwy, Yungaburra','约 14:00 / 10:00','Spa Cottage 周日–四 $230/晚；2晚约 $460',link('官网预订','https://edenhouse.com.au/apartments/')],
['4晚\n9/22–26','Coral Tree Inn','166–172 Grafton St, Cairns','联系酒店确认；晚到需通知','9月预算按 $200–230/晚；4晚约 $800–920',link('查房入口','https://www.visitcairns.com.au/store/Product.aspx?ProductID=c4165d9b-63cd-4361-b637-b9b3c350e815')]
]
at=Table([[p(x,'TinyCN') for x in row] for row in accom],colWidths=[20*mm,34*mm,38*mm,27*mm,36*mm,19*mm],repeatRows=1)
at.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#CEBEB4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,CREAM]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [p('住宿总表｜推荐选项与可点击入口','H1CN'),p('这些是按“性价比、停车方便、位置合路线”选出的候选，不代表已经替你下单。房价会随日期和房型变化，点击入口填入 2026 年日期获取最终含税价。','BodyCN'),at,Spacer(1,5*mm),
box('住宿小计（两人一间）','按上表当前参考：约 $2,035–2,305。Cape Tribulation 房价波动较大；所有住宿建议选可取消价，并核对停车、早餐和晚到安排。'),PageBreak()]

bookings=[
['项目 / 日期','价格','集合地点 / 时间','直接入口'],
['Silversonic 外堡礁｜9/18','成人 $328；2人 $656','Crystalbrook Superyacht Marina, Port Douglas；约 8:00 报到',link('官方预订','https://www.silversonic.com.au/')],
['Mossman Gorge 接驳｜9/19','成人 $15.50；2人 $31','Mossman Gorge Cultural Centre；8:00–17:00',link('购买接驳票','https://mossmangorge.rezdy.com/404022/shuttle-bus-tickets?lang=en')],
['Solar Whisper 1小时巡航｜9/19','$35/人；2人 $70','Daintree River；按订单提前报到',link('官方预订','https://www.solarwhisper.com/eco-tours')],
['Kuranda 工程期组合｜9/24','参考成人 $128；2人 $256','Cairns Central / Freshwater；依所选班次',link('2026工程期入口','https://www.visitcairns.com.au/store/Product.aspx?ProductID=845a7c9a-df21-40bc-b287-49d1c3dca675')],
['租车｜9/17–约9/23','约 $650–950 + 油费','Cairns Airport 取车；Cairns 市区或机场还车',link('机场租车公司','https://www.cairnsairport.com.au/travelling/parking-and-transport/car-rentals/')]
]
kt=Table([[p(x,'TinyCN') for x in row] for row in bookings],colWidths=[43*mm,34*mm,65*mm,32*mm],repeatRows=1)
kt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#B8CBC6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,MINT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [p('活动与交通｜价格、地点、订购入口','H1CN'),p('蓝绿色下划线文字可直接点击。付款前再次确认姓名、日期、集合点、取消条款和是否含接送。','BodyCN'),kt,Spacer(1,5*mm),box('必须留意','Skyrail 2026 升级期会改变 9/24 的正常动线；只能订明确标注工程期的产品。Silversonic 若天气取消，先与原供应商确认改期，不要自行重复购票。',colors.HexColor('#FFF0E9')),PageBreak()]

for day_no,(title,route,drive,stops,plan,food,tip) in enumerate(days,1):
    story += [pill(title,CORAL),Spacer(1,2*mm),p(route,'H1CN'),p(drive,'CNSub'),Spacer(1,2*mm),Image(os.path.join(ROOT,f'assets/maps/day{day_no:02d}.png'),width=174*mm,height=57*mm),Spacer(1,2*mm)]
    story += [stop_gallery(stops),Spacer(1,2*mm)]
    plan_full=plan+f'<br/><b>现场感：</b>{DAY_SCENE[day_no]}'
    food_full=food+f'<br/><b>可以期待：</b>{DAY_TASTE[day_no]}'
    story += [dense_box('今天怎么走｜为什么值得',plan_full),Spacer(1,1.4*mm),dense_box('附近值得吃｜点什么、期待什么',food_full,MINT),Spacer(1,1.4*mm),dense_box('活动价格与预订提示',tip,CREAM),PageBreak()]

EX_DIR=os.path.join(ROOT,'assets/experiences'); EX_COMMONS=json.load(open(os.path.join(EX_DIR,'commons.json')))
def ex_crop(src,name,w=700,h=430):
    dest=os.path.join(EX_DIR,name+'_crop.jpg'); im=PILImage.open(src).convert('RGB'); scale=max(w/im.width,h/im.height); im=im.resize((round(im.width*scale),round(im.height*scale))); l=(im.width-w)//2;t=(im.height-h)//2;im.crop((l,t,l+w,t+h)).save(dest,quality=87);return dest
def ex_card(img,title,text,source=None):
    cap=title
    if source: cap += f'<br/><font size="6">照片：{link(source[0],source[1])}</font>'
    left=Table([[Image(ex_crop(img,re.sub(r'[^a-z0-9]+','_',title.lower()).strip('_')),width=55*mm,height=34*mm)],[p(cap,'TinyCN')]],colWidths=[55*mm])
    t=Table([[left,p(text,'BodyCN')]],colWidths=[58*mm,116*mm]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#D6CDB6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
spa_src=(f"{EX_COMMONS['spa']['author']} · {EX_COMMONS['spa']['license']}",EX_COMMONS['spa']['page'])
marina_src=(f"{EX_COMMONS['marina']['author']} · {EX_COMMONS['marina']['license']}",EX_COMMONS['marina']['page'])
seafood_src=(f"{EX_COMMONS['seafood']['author']} · {EX_COMMONS['seafood']['license']}",EX_COMMONS['seafood']['page'])
story += [p('特别体验｜留一点时间给放松和夜晚','H1CN'),p('这些不是必须打卡，但能让旅程从“看景点”变成真正度假。建议只选 1–2 项。Spa 配图为可授权体验氛围图，并非店内实拍。','BodyCN'),
ex_card(EX_COMMONS['spa']['file'],'Niramaya Day Spa｜Port Douglas',f'<b>适合：</b>9/17 抵达后的下午，或另行留出半天。热带花园环境，60分钟 Signature Massage 官方公开价 $160/人；周一至周六 9:00–17:00。<br/><b>地点：</b>1 Bale Drive。<br/><b>预订：</b>{link("Niramaya 官网", "https://events.niramaya.com.au/day-spa")}　取消不足24小时通常收全额。',spa_src),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'massage2.jpg'),'Eléme Day Spa｜Cairns',f'<b>适合：</b>9/23 弹性日下午。Riley 店周一至周六 10:00–19:00，Flynn 店周二至周六 10:00–18:00；可做按摩、面部或双人护理。活动页曾列泳池/桑拿/蒸汽房组合 $99，疗程价以付款页为准。<br/><b>预订：</b>{link("Eléme Cairns", "https://www.crystalbrookcollection.com/eleme-spa/cairns")}。',('Alvina Atye Gakya · CC BY-SA 4.0','https://commons.wikimedia.org/wiki/File:Massage_at_Emotions_Spa.jpg')),Spacer(1,4*mm),
ex_card(STOP_CREDITS['Cape Tribulation']['file'],'雨林夜游｜Cape Tribulation',f'<b>适合：</b>9/19 入住雨林后。Jungle Escapes 19:30–21:30 夜游 $50/人，使用手电和热成像寻找蝙蝠、负鼠、蛙类、雨林龙与昆虫；野生动物不保证。<br/><b>集合：</b>Camelot Close 附近，须穿包脚软底鞋。<br/><b>预订：</b>{link("官方 Tours 页面", "https://jungleescapes.com.au/tours")}。',(STOP_CREDITS['Cape Tribulation']['author']+' · '+STOP_CREDITS['Cape Tribulation']['license'],STOP_CREDITS['Cape Tribulation']['page'])),Spacer(1,4*mm),
ex_card(EX_COMMONS['marina']['file'],'Spirit of Cairns 晚餐游船',f'<b>适合：</b>Cairns 的轻松晚上，不安排在 Kuranda 当晚更舒服。2026 官方资料为成人 $155；两人约 $310。17:45 登船、18:15 出发、20:45 返回，含欢迎饮品、海鲜及热菜自助餐。<br/><b>集合：</b>A Finger, Cairns Marlin Marina。<br/><b>预订：</b>{link("Spirit of Cairns 官网", "https://www.spiritofcairns.com.au/dinner-cruise/")}。',marina_src),PageBreak()]

story += [p('认真吃一顿｜值得提前订位的餐厅','H1CN'),p('以下“预算”按两人点前菜/主菜并含少量饮品估算，并非固定套餐价。菜单季节性变化；配图为可授权海鲜或环境氛围照片，不代表店内具体菜品。','BodyCN'),
ex_card(EX_COMMONS['seafood']['file'],'Salsa Bar & Grill｜Port Douglas',f'<b>为什么去：</b>热带亚洲风味与本地海鲜，气氛轻松但菜品认真；适合 9/17 欢迎晚餐或 9/18 Reef 后庆祝。两人约 $160–230；官方团体晚餐套餐参考 $95/人。<br/><b>地址：</b>26 Wharf Street。<br/><b>订位/菜单：</b>{link("Salsa 官网", "https://salsaportdouglas.com.au/menus/")}。',seafood_src),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'lobster.jpg'),'Wrasse & Roe｜Port Douglas',f'<b>为什么去：</b>以可持续海鲜为主角，适合生蚝、珊瑚鳟和精致小盘；比普通海鲜店更偏约会感。两人约 $180–280。每日约14:00–22:00，晚餐建议提前订。<br/><b>地址：</b>56–64 Macrossan Street。<br/><b>订位：</b>{link("查看菜单与预约", "https://tourismportdouglas.com.au/wrasse-and-roe")}。',('Charles Haynes · CC BY-SA 2.0','https://commons.wikimedia.org/wiki/File:Lobster_at_Quay.jpg')),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'swordfish.jpg'),'Ochre Restaurant｜Cairns',f'<b>为什么去：</b>澳洲原生食材体验，可尝袋鼠、鳄鱼、柠檬桃金娘、卡卡杜李等风味；适合作为旅程最后一顿正式晚餐。两人约 $160–260。周一至周六晚餐 17:30–21:30，周日休息。<br/><b>地址：</b>1 Marlin Parade。<br/><b>订位：</b>{link("Ochre 官网", "https://ochrerestaurant.com.au/book-now/")}。',('Misaochan · CC BY-SA 3.0','https://commons.wikimedia.org/wiki/File:Swordfish_dish_at_jellyfish_seafood_restaurant_Brisbane.jpg')),Spacer(1,4*mm),
ex_card(STOP_CREDITS['Palm Cove']['file'],'Nu Nu｜Palm Cove',f'<b>为什么去：</b>正对海滩，主打雨林、珊瑚礁与高原食材；最适合 9/17 北上途中的长午餐。两人约 $130–220，若航班延误则改成普通咖啡馆，避免影响日落前到达 Port Douglas。<br/><b>地址：</b>1 Veivers Road。<br/><b>订位：</b>{link("Nu Nu 官网", "https://www.nunu.com.au/")}。',(STOP_CREDITS['Palm Cove']['author']+' · '+STOP_CREDITS['Palm Cove']['license'],STOP_CREDITS['Palm Cove']['page'])),PageBreak()]

story += [p('当地社区高性价比｜少花钱也很精彩','H1CN'),p('结合 2026 年 Cairns 当地社区近期讨论筛选，再以官网价格和开放信息复核。优先选择顺路、低重复度、可以自己掌握节奏的项目。','BodyCN'),
ex_card(STOP_CREDITS['Daintree River']['file'],'Solar Whisper｜安静找野生鳄鱼',f'<b>推荐度：</b>★★★★★　9/19 前往 Cape Tribulation 途中最顺路。1小时成人 $35，2人 $70；太阳能小船安静、人数少，比再买一个整日雨林团更划算。<br/><b>提示：</b>野生动物不保证出现，提前订较凉爽的时段。<br/><b>预订：</b>{link("Solar Whisper 官网", "https://www.solarwhisper.com/eco-tours")}。',(STOP_CREDITS['Daintree River']['author']+' · '+STOP_CREDITS['Daintree River']['license'],STOP_CREDITS['Daintree River']['page'])),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'snorkel.jpg'),'Reef Sprinter｜半日礁体验',f'<b>推荐度：</b>★★★★☆　Low Isles 约 $180/人，Outer Reef 半日约 $270/人；最多约14人，适合不想把整天都用在船上的旅客。<br/><b>取舍：</b>若已保留 Silversonic 全天外礁就不要重复购买；它更适合作为替换方案。<br/><b>预订：</b>{link("Reef Sprinter 官网", "https://www.reefsprinter.com.au/")}。',('Queensland / Wikivoyage · CC BY-SA','https://commons.wikimedia.org/wiki/File:Reef_Snorkelling_on_the_Great_Barrier_Reef.jpg')),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'platypus.jpg'),'Peterson Creek｜免费等鸭嘴兽',f'<b>推荐度：</b>★★★★★　住 Yungaburra 时连续两个清晨或黄昏各留 30–45 分钟，费用 $0。安静观察水面慢慢扩散的圆形波纹。<br/><b>入口：</b>目前优先从 Penda Street 的 Allumbah Pocket 进入，部分旧路段关闭。<br/><b>地图：</b>{link("步道最新状况", "https://petersoncreek.org.au/walking-tracks/")}。',('Maria Grist · CC BY-SA 4.0','https://commons.wikimedia.org/wiki/File:Platypus_swimming.jpg')),Spacer(1,4*mm),
ex_card(os.path.join(EX_DIR,'botanic.jpg'),'Cairns Botanic Gardens＋Red Arrow',f'<b>推荐度：</b>★★★★★　植物园门票 $0，可搭配免费导览、Red Arrow 步道和 Edge Hill 咖啡。适合 9/23 弹性日，也适合作为海况不佳的陆上备选。<br/><b>提示：</b>中午炎热，建议早上或下午；带水、防晒和防蚊。<br/><b>信息：</b>{link("Cairns 市政府官网", "https://www.cairns.qld.gov.au/experience-cairns/botanic-gardens")}。',('Kerry Raymond · CC BY-SA 4.0','https://commons.wikimedia.org/wiki/File:Cairns_Botanic_Gardens,_Edge_Hill,_2018_07.jpg')),PageBreak()]

story += [p('当地人吃什么｜轻松、顺路、有记忆点','H1CN'),p('社区推荐会随厨师与经营状况变化；这里按你的住宿点安排，而不是为了“网红店”额外长途开车。预算为两人常规点餐估算。','BodyCN'),
ex_card(STOP_CREDITS['Port Douglas']['file'],'Jungle Fowl｜Port Douglas',f'<b>适合：</b>9/17 或 9/18 晚餐。本地社区近期多次推荐，强调当地食材和轻松气氛；两人约 $100–170。<br/><b>取舍：</b>与 Salsa 二选一即可，不必连续吃两顿正式餐。<br/><b>菜单/订位：</b>{link("Jungle Fowl 官网", "https://www.junglefowl.com.au/")}。',(STOP_CREDITS['Port Douglas']['author']+' · '+STOP_CREDITS['Port Douglas']['license'],STOP_CREDITS['Port Douglas']['page'])),Spacer(1,4*mm),
ex_card(STOP_CREDITS['Cairns']['file'],'Guyala Café｜Cairns 早餐咖啡',f'<b>适合：</b>弹性日上午或植物园之前。社区常把它列为认真做咖啡和早午餐的选择；两人约 $45–75。<br/><b>省钱方法：</b>用一顿丰盛早午餐替代酒店早餐加午餐。<br/><b>店铺：</b>{link("Guyala Café 官网", "https://www.guyalacafe.com.au/")}。',(STOP_CREDITS['Cairns']['author']+' · '+STOP_CREDITS['Cairns']['license'],STOP_CREDITS['Cairns']['page'])),Spacer(1,4*mm),
ex_card(EX_COMMONS['seafood']['file'],'Prawn Star｜码头船上海鲜',f'<b>适合：</b>Cairns 轻松晚餐。重点是船上用餐的气氛与海鲜拼盘，不需要正式着装；两人约 $90–160。<br/><b>提示：</b>热门时段可能排队，先看当天营业和菜单；确认海鲜产地，不要默认全部来自 Cairns。<br/><b>入口：</b>{link("Prawn Star 官网", "https://www.prawnstarcairns.com/")}。',seafood_src),Spacer(1,4*mm),
ex_card(STOP_CREDITS['Yungaburra']['file'],'Our Place｜Yungaburra',f'<b>适合：</b>9/20 或 9/21 晚餐。住在高原时就近吃，比天黑后为了餐厅跨镇驾驶更合理；两人约 $80–140。<br/><b>提示：</b>小镇餐厅座位与营业日有限，至少提前一天确认。<br/><b>位置：</b>{link("地图与最新资料", "https://www.google.com/maps/search/?api=1&query=Our+Place+Restaurant+Yungaburra")}。',(STOP_CREDITS['Yungaburra']['author']+' · '+STOP_CREDITS['Yungaburra']['license'],STOP_CREDITS['Yungaburra']['page'])),PageBreak()]

budget=[['项目','经济估算（2人）','舒适估算（2人）'],['住宿 9晚','$1,800','$3,000'],['租车/油费/停车','$850','$1,200'],['餐饮','$1,000','$1,650'],['Silversonic','$656','$656'],['Kuranda 工程期组合','$256','$256'],['其他门票/巡航','$120','$260'],['机票 BNE–CNS 往返','$400','$900'],['合计','$5,082','$7,922']]
bt=Table([[p(x,'SmallCN') for x in row] for row in budget],colWidths=[68*mm,53*mm,53*mm]); bt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#B8CBC6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,MINT]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story += [p('预算与预订优先级','H1CN'),p('以下不含购物；住宿与机票波动最大。经济/舒适并非最低价和豪华价，而是更现实的两人旅行区间。','BodyCN'),bt,Spacer(1,6*mm),
box('先订 ①','9/18 Silversonic：核心项目且船位有限；确认取消/改期条款。'),Spacer(1,3*mm),box('先订 ②','9/19 Cape Tribulation 特色住宿：北岸选择少，晚餐座位也要一并确认。'),Spacer(1,3*mm),box('先订 ③','9/24 Kuranda：必须选择工程期产品，核对火车班次、Skyrail Loop 运营日和接驳。'),Spacer(1,3*mm),box('再订','热门晚餐 Salsa / Wrasse & Roe / Ochre，以及自动挡租车。尽量选择可取消房价，给天气调整留空间。'),PageBreak()]

story += [p('出发前清单','H1CN'),
box('车与路','驾照与租车条款｜离线地图｜轮胎与玻璃保险范围｜Daintree Ferry 营业/排队｜北岸加油｜不夜驾'),Spacer(1,3*mm),
box('水上与天气','防晒衣/礁石友好防晒｜晕船药先咨询药师｜泳衣与快干毛巾｜关注海况｜不触碰珊瑚｜雨后不下急流'),Spacer(1,3*mm),
box('热带实用物','驱蚊｜可重复水瓶｜薄雨衣｜高原薄外套｜防滑鞋｜防水袋｜充电宝'),Spacer(1,3*mm),
box('每日确认','前一晚看天气与道路｜餐厅是否营业｜活动集合时间｜停车/接驳点｜下载订单截图｜给家人留路线'),Spacer(1,6*mm),
p('资料核对日期：2026-09-03。事实与价格优先依据 Quicksilver 2026/27 价格表、Mossman Gorge 接驳价格、Skyrail/Kuranda 2026 工程期说明、经营方官网，以及 Tourism Tropical North Queensland、Tourism Port Douglas Daintree、Atherton Tablelands 官方资料；并参考 Lonely Planet 的目的地指南组织思路重新编写，未复制其文字。餐厅菜单、渡轮、天气、道路及活动可能临时变化。','SmallCN'),Spacer(1,3*mm),
p('说明：封面和景点画面为本手册原创旅行插画；所有路线小地图使用真实经纬度比例绘制，但线路为停靠顺序示意，不代替实时道路导航。','SmallCN')]

credit_rows=[['地点','照片作者 / 许可','来源']]
for name,cr in STOP_CREDITS.items(): credit_rows.append([name,f"{cr['author']} · {cr['license']}",link('Wikimedia Commons',cr['page'])])
ct=Table([[p(x,'TinyCN') for x in row] for row in credit_rows],colWidths=[38*mm,91*mm,45*mm],repeatRows=1)
ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#B8CBC6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,MINT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [PageBreak(),p('停靠点实景照片来源','H1CN'),p('地图编号与每日图鉴编号一一对应。照片为便于排版经过等比例裁切；点击来源可查看原图、作者和完整许可。','BodyCN'),ct]

doc=SimpleDocTemplate(OUT,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm,title='Cairns 2026 熊仔鸡仔旅行手册',author='OpenAI Codex')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
