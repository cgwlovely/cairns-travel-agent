# D6–D7 路线重构评估

调研日期 2026-09-05。所有驾驶数据来自 Google Maps 实查（浏览器直连 maps 路线页），交叉核对 Rome2Rio / Wanderlog。查不到的地方我直接写「未查到」。

---

## 0. 一句话结论（细节见第 7 节）

**「不去 Hunter Valley 还用转场日么？」——转场日必须留，但不该留在 Pokolbin。**

从 Nelson Bay 回到 Gold Coast，不论怎么排，D6→D8 三天的净驾驶时间都在 **11.5 小时**左右，这是地理决定的，省不掉。现方案的问题不是「多了一天」，而是**把这 11.5 小时切成了 1:6:4**。把过夜点从 Pokolbin 北移到 **Tamworth**，同样的三天变成 **4:3.5:4**，而且 D7 从「纯赶路」变成「New England 高原观光日」。

**推荐方案 A（Tamworth 过夜）**，理由和代价在第 7 节。

---

## 1. 驾驶时间与距离（核心数据）

**主数据源：Google Maps 路线页**（2026-09-05 查询，"现在出发"默认估算，未做 2026-09-22 周二时段模拟）。括号内为交叉核对源。

### 1.1 现方案（对照组）

| 路段 | 时间 | 距离 | 走法 |
|---|---|---|---|
| Nelson Bay → Pokolbin | **1 h 21 min** | 103 km | Nelson Bay Rd/B63 |
| Pokolbin → Tenterfield | **6 h 10 min** | 528 km | New England Hwy/A15 |

> 用户说的「约 6.5 小时」基本准确，Google 给 6 h 10 min（Rome2Rio 给 6 h 32 min / 533 km）。
> **两天合计 7 h 31 min / 631 km，分配比 1 : 4.6。**

### 1.2 Nelson Bay 出发的三个终点

| 路段 | 时间 | 距离 | 走法 |
|---|---|---|---|
| Nelson Bay → **Tamworth**（经 Scone） | **3 h 59 min** | 323 km | New England Hwy/A15 |
| Nelson Bay → Tamworth **加 Burning Mountain 停靠** | **4 h 11 min** | 326 km | 同上（绕行仅 +12 min，Burning Mountain 就在路边） |
| Nelson Bay → **Armidale**（Google 默认最快） | **4 h 07 min** | 337 km | **Thunderbolts Way**（Gloucester–Walcha 山路） |
| Nelson Bay → Armidale **经 Tamworth**（New England Hwy） | **5 h 17 min**（3 h 59 + 1 h 18 分段和） | 434 km | New England Hwy/A15 |
| Nelson Bay → **Tenterfield**（最快） | **6 h 17 min** | 525 km | Thunderbolts Way + New England Hwy |
| Nelson Bay → Tenterfield（全程 New England Hwy） | **7 h 13 min** | 614 km | A15 |

**⚠ 一个容易踩的坑**：Google 默认给的 Nelson Bay → Armidale 4 h 07 min 是走 **Thunderbolts Way**，那条路**不经过 Scone、不经过 Burning Mountain、不经过 Tamworth**。如果你要 Burning Mountain + Tamworth，必须走 New England Hwy，实际是 **5 h 17 min（含停靠约 5 h 29 min）**，比 Google 首选路线多 1 小时 20 分。查距离时如果只看首页那个数字，会把方案 B 的驾驶量低估一小时。

（交叉核对：Rome2Rio 给 Nelson Bay → Tamworth 3 h 58 min / 311 km；Wanderlog 给 4 h 25 min / 319 km。Rome2Rio 给 Nelson Bay → Armidale 4 h 20 min / 337 km，同样是 Thunderbolts Way 口径。）

### 1.3 Nelson Bay 一天开到 Tenterfield 可行吗

**技术上可行，体验上不推荐。** 6 h 17 min 净驾驶（最快路线是 Thunderbolts Way 那条山路，弯多、车速低、没有像样的午餐点），加上加油、午饭、上厕所，实际 7.5 小时以上。而且这条路把 Burning Mountain 和整个 New England Hwy 沿线全部跳过了。走 New England Hwy 版本则是 7 h 13 min 净驾驶——那就是一整天在车里。

### 1.4 内陆北段

| 路段 | 时间 | 距离 | 走法 |
|---|---|---|---|
| Tamworth → Armidale | **1 h 18 min** | 111 km | New England Hwy/A15 |
| Tamworth → Tenterfield（经 Uralla / Armidale / Glen Innes） | **3 h 25 min** | 301 km | New England Hwy/A15 |
| Armidale → Tenterfield | **2 h 08 min** | 190 km | New England Hwy/A15 |
| Tamworth → **Stanthorpe** | **4 h 04 min** | 356 km | New England Hwy/A15 |
| Armidale → **Stanthorpe** | 未单独查（Rome2Rio 给 2 h 55 min / 243 km） | — | — |
| Tamworth → **Girraween NP** | **3 h 52 min** | 337 km | New England Hwy/A15 |
| Armidale → **Girraween NP** | **2 h 38 min** | 228 km | New England Hwy/A15 |
| Tenterfield → Girraween NP | **约 38–45 min / 28 km**（Rome2Rio 38 min；QLD Parks 官网写 Wyberba 在 Tenterfield 以北 30 km，之后是 Pyramids Road 沥青弯道） | — | — |

（交叉核对：Rome2Rio 给 Tamworth → Tenterfield 3 h 35 min / 298 km；Armidale → Tenterfield 2 h 14 min / 187 km。与 Google 差 7–10 分钟，一致。）

### 1.5 收尾段（回 Gold Coast）

| 路段 | 时间 | 距离 | 走法 |
|---|---|---|---|
| Tenterfield → Labrador (Gold Coast) | **3 h 42 min** | 325 km | National Hwy 15 / Cunningham Hwy，**有收费站** |
| 同上（备选） | 3 h 51 min | 299 km | Bruxner Hwy/B60 + M1 |
| **Girraween NP → Gold Coast** | **3 h 27 min** | 302 km | National Hwy 15，有收费站 |
| 同上（备选） | 3 h 50 min | 249 km | Mount Lindesay Rd |

**⚠ 数据分歧提示**：Rome2Rio 给 Girraween NP → Gold Coast **4 h 09 min**，比 Google 的 3 h 27 min 多 42 分钟。我采信 Google（因为它同时给出了 Tenterfield → Gold Coast 3 h 42 min，两个数字互相自洽：Girraween 比 Tenterfield 更靠北 28 km）。但如果你想留安全余量，按 **3 h 45 min** 排。

---

## 2. 三个重构方案

### 方案 A：过夜点移到 Tamworth

**D6（周二 22/9）**：Nelson Bay → Burning Mountain（Wingen）→ Tamworth
- 净驾驶 **4 h 11 min / 326 km**
- Burning Mountain Walk：NSW National Parks 官网写 **4 km 往返、建议 1–2 小时、Grade 3**，全年开放（恶劣天气/火险时临时关闭）。看点是燃烧了 **5,500 年**的地下煤层火，观景平台能看到排气口和被高温改性的岩石。这是全澳唯一的一处，**完全符合「独特的自然现象」这一条**，而且是免费路边步道，绕行只多 12 分钟。
- 建议节奏：Nelson Bay 8:30 出发 → 11:10 到 Burning Mountain → 走完 12:40 → Scone 或 Murrurundi 午饭 → Tamworth 约 15:30 入住。**下午还剩 2–3 小时。**

**D7（周三 23/9）**：Tamworth → Uralla → Armidale → Glen Innes → Tenterfield
- 净驾驶 **3 h 25 min / 301 km**
- 有 4 小时可用于停靠。可选：Uralla（Thunderbolt's Rock，路边）、Armidale 午饭、**Wollomombi Falls**（Armidale 往东 30 分钟走 Waterfall Way，往返约 +1 小时；220 m 落差、澳洲第二高瀑布、峡谷观景台；Google 4.6 / 831 条，「Wollomombi Falls Picnic Area」）、**Glen Innes Australian Standing Stones**（Google **4.5 / 1,254 条**；TripAdvisor 4.2 / 301 条；24 小时开放、免费）。

**两天驾驶：4 h 11 min + 3 h 25 min。均衡度：1 : 0.82。**
D8 不变：Tenterfield → Girraween（约 40 min）→ The Pyramid（2 h）→ Gold Coast（3 h 27 min），净驾驶 **4 h 05 min**。
**D6–D8 三天合计约 11 h 41 min。**

**优点**：分配最平；D7 从赶路变成观光日；不减任何一晚；Burning Mountain 和 Wollomombi 都命中他们的口味（步道 / 观景台 / 独特自然现象）；风险最低。
**缺点**：Tamworth 的镇本身不如 Armidale 有内容（见第 3 节）；仍然要住 Tenterfield 那一晚。

---

### 方案 B：过夜点移到 Armidale

**D6**：Nelson Bay → Burning Mountain → Tamworth（停留）→ Armidale
- 净驾驶 **5 h 29 min / 437 km**（**必须走 New England Hwy，不能用 Google 首选的 Thunderbolts Way**）
- 加上 Burning Mountain 步道 1.5 h + 午饭 1 h，8:00 出发大概 17:30–18:00 到 Armidale。**这是一个满档的一天，没有余量。**

**D7 变体 1（保留 Tenterfield 那一晚）**：Armidale → Tenterfield 只有 **2 h 08 min**。这等于把失衡从「D6 太短」搬到「D7 太短」，没解决问题。**不推荐。**

**D7 变体 2（砍掉 Tenterfield，当天直插 Gold Coast）——这才是方案 B 的真正价值**：
- Armidale → Girraween NP **2 h 38 min / 228 km**
- The Pyramid 步道 **2 h**（QLD Parks 官网：3.6 km 往返、Grade 4、建议 2 小时；起点 Bald Rock Creek day-use area；从 Wyberba 上 Pyramids Road，**沥青路，普通车可达**）
- Girraween NP → Gold Coast **3 h 27 min / 302 km**
- **合计：驾驶 6 h 05 min + 徒步 2 h = 8 h 05 min 净时间。**
- 时刻表推演：7:30 离开 Armidale → 10:10 到 Girraween → 12:15 下山 → 简餐到 13:00 → **16:30 到 Gold Coast**。**可行，但没有任何弹性**，且周三早上在 Armidale 一件事都做不了。

**优点（变体 2）**：省掉 Tenterfield 一晚，多出一整天可以还给海岸；Armidale 的晚餐和周边（gorges）比 Tamworth 强。
**缺点**：D6 5 h 29 min、D7 6 h 05 min + 2 h 爬山，**连着两天硬开**，正好是这次重构想解决的问题的另一种版本；周三早上完全被牺牲；一旦 The Pyramid 上山慢了或天气不好，当天到 Gold Coast 会拖到天黑。

> **不要考虑「从 Tamworth 一天到 Girraween 再到 Gold Coast」**：Tamworth → Girraween 就要 **3 h 52 min**，加 2 h 爬山加 3 h 27 min，净时间 9 h 19 min，实际 11 小时以上。卡死的就是 Tamworth → Girraween 这一段。

---

### 方案 C：放弃内陆，原路沿海岸北上

**驾驶量**：Nelson Bay → Byron Bay **6 h 28 min / 621 km**（Pacific Hwy/A1 + M1），Byron 到 Gold Coast 再约 1 小时。也就是说**沿海北上同样要两天硬开**，总里程比内陆线**更长**（约 700+ km vs 内陆 630 km）。方案 C 并不省时间。

**有没有 D2–D4 没停过的新点位？**（避开 Port Macquarie、Coffs、Yamba）

已核实评分的：
- **Smoky Cape Lighthouse**（South West Rocks，Hat Head NP）— Google **4.8 / 804 条**，TripAdvisor 4.6 / 520 条。NSW 最高的灯塔。
- **Trial Bay Gaol**（South West Rocks）— Google **4.6 / 1.3K**，TripAdvisor 4.5 / 667 条。海边监狱废墟。
- **Dorrigo Rainforest Centre + Skywalk**（Waterfall Way 上）— Google 4.8 / 635 条（中心）、Skywalk lookout 4.7 / 147 条、Wonga walk 4.8 / 38 条。**注意这是内陆山上，不在海岸线上。**
- **Cape Byron Lighthouse** — Google **4.7 / 9,555 条**。澳洲大陆最东点，绕岬步道。
- **Minyon Falls**（Nightcap NP）— TripAdvisor 4.5 / 226 条。
- **Natural Bridge, Springbrook NP** — Google **4.8 / 4.4K**。免费、24 小时开放，天黑后可看 glow worms（QLD Parks 官网明确：「walk in daylight hours only, unless viewing the glow-worms at Natural Bridge」）。**这是方案 C 里最强的一张牌**，而且它离 Gold Coast 很近，其实**任何方案的 D8 晚上都能加进去**。
- Snapper Rocks（Gold Coast）— Google 4.8 / 3,168 条。

未逐个核实评分的候选：Crowdy Bay NP（Diamond Head）、North Brother Lookout（Laurieton）、Nambucca Heads V-Wall、Iluka Nature Reserve、Evans Head、Pat Morton Lookout（Lennox Head）。

**会不会导致必须放弃 Girraween 的 The Pyramid？——是的，必然放弃。** Girraween 在内陆，距海岸线 300 km 以上；从 Gold Coast 当日往返是 3 h 27 min × 2，不成立。

**方案 C 的真实代价**：不只是「重复 Pacific Highway」，而是**整个 New England Tablelands 从行程里消失**——那是这趟九天里唯一一段与海岸完全不同的地貌（海拔约 1,000 m 的花岗岩高原、峡谷、瀑布、冷凉气候）。对一对喜欢步道、观景台和独特自然现象的情侣，用「再看一次海岸」换掉「Burning Mountain + Wollomombi + Standing Stones + The Pyramid」，性价比是负的。

**方案 C 只在一种情况下成立**：他们其实不想爬 Grade 4/5 的山，只想躺海边。从他们已经排了 Tomaree（Grade 5）和 The Pyramid（Grade 4）看，不是这种情况。

---

## 3. Tamworth vs Armidale 作为过夜地

### 3.1 周二晚（2026-09-22）能做什么

#### Tamworth

**餐**（评分平台已分别标注）：

| 店 | 周二晚是否营业 | Google | TripAdvisor | 依据 |
|---|---|---|---|---|
| **The Pig & Tinder Box**（429 Peel St） | **开**（官网：「Open for lunch and dinner daily」） | **4.3 / 837 条** | 4.3 / 555 条 | 官网 thepigandtinderbox.com.au + Google 知识面板 |
| **Tudor Hotel**（327 Peel St） | **开**（官网：Bistro 7 天，晚餐 17:30–21:00；**周一、周二是 Steak Night**） | **4.2 / 752 条** | 3.8 / 157 条 | 官网 tudorhoteltamworth.com.au + Google |
| Joe Maguires | 开（官网：Bistro 一周 7 天午晚餐） | 未查 | 未查 | 官网 joemaguires.com.au |
| Wests Tamworth — The Courts at East Bistro | 开（官网：周二–周日） | 未查 | 未查 | 官网 wtlc.com.au |
| ~~**Hopscotch Restaurant & Bar**~~ | **周二晚不开** | 4.3 / 849 条 | 4.4 / 677 条 | Google 面板 + 官方 Facebook「All Day Breakfast & Lunch: 7 Days, 7am–2:30pm」；AGFG 逐日表显示 Tue 07:00–14:30、晚餐只有周三–周六 |

> **两个必须纠正的坑**：
> 1. **Hopscotch 是 TripAdvisor 上 Tamworth 排第一的餐厅，但周二晚上不开。** 很多攻略会推它，照抄会扑空。
> 2. **The Welder's Dog Tamworth（37 Dowe St）已经卖掉了**，官网 theweldersdog.com.au 现在明写该店已改为 "Turtle's Bar & Taphouse"。所有推荐「周二 pizza night + 精酿」的攻略都过期了。反正他们不喝酒，这条本来也不重要。

**免费 / 户外**：
- **Oxley Scenic Lookout**（White Street 顶，距 CBD 2 km）— 免费，**开放 07:00–22:00**，俯瞰 Tamworth 城与 Peel River Valley，有厕所、野餐桌、免费燃气 BBQ。**TripAdvisor 4.5 / 327 条**。日落和天黑后都好。这是 Tamworth 周二晚最值得去的一件事。
- Bicentennial Park / Tamworth Regional Playground — 24 小时开放，河边散步。

#### Armidale

**餐**：

| 店 | 周二晚是否营业 | Google | 依据 |
|---|---|---|---|
| **The Cottage Restaurant and Bar**（86 Barney St） | **开，17:30 起**（Google 面板明示 "Opens 5:30 pm Tue"；需预订） | **4.9 / 261 条** | Google 知识面板 + 官网 thecottagearmidale.au |
| **Manny's On Marsh**（Level 2/117 Marsh St，意大利菜） | **开，17:00 起**（Google 面板 "Opens 5 pm Tue"；厨房 20:45 收） | 3.9 / 75 条 | Google 面板 + 官网 mannysonmarsh.com |
| **Tattersalls Hotel** 餐厅 | **开**（官网：晚餐 周二–周六 17:30–20:30） | 未查（Booking 8.9 / 453 条） | 官网 tattersallsarmidale.com.au |
| Whitebull Hotel | **开**（官网：Tuesday 10am–late，一周 7 天） | 未查 | 官网 whitebull.net.au |

> **The Cottage 的 Google 4.9 / 261 条，是本次调研里两个镇上分数最高的餐厅**，且明确周二开门。这是 Armidale 相对 Tamworth 最实在的一个优势。

**免费 / 户外（周二晚）**：Armidale 的强项是**白天**的峡谷（见下），晚上镇内没有查到与 Oxley Scenic Lookout 对等的免费观景点。Dangars Falls 在镇南 22 km（其中 10 km 非铺装路），**不适合天黑后去**。

**气候差异（实际影响穿着和晚上出门意愿）**：climate-data.org 给 Armidale 九月均温 19 °C / 6 °C，Tamworth 22 °C / 6 °C。Armidale 海拔约 1,000 m，白天明显更冷。（**非 BOM 官方数据，只是气候站汇总站点。**）

### 3.2 住宿（Booking.com，2026-09-22 → 09-23，2 成人 1 房，未登录价，AUD 含税费，2026-09-05 查询）

硬性要求：两人独立房间 + 独立卫浴 + 非 hostel/dorm + 免费停车。

**Tamworth（该日期共 40 家可订）**

| 住宿 | Booking 评分 | 价格 | 房型 | 备注 |
|---|---|---|---|---|
| **Edward Parry Motel & Apartments**（261 Goonoo Goonoo Rd） | **9.5 / 545 条** | **A$186** | 行政大号床间，免费取消 | **Google 4.8 / 296 条；TripAdvisor 4.7 / 434 条；Google Hotels 明确「free self-parking」**。距中心 2.5 km |
| Almond Inn Motel | 8.7 / 1,027 条 | **A$153** | Comfort Queen，含早餐，免费取消，到店付款 | 距中心 1.7 km |
| CH Boutique Hotel (Ascend) | 8.9 / 1,265 条 | A$251 | 豪华大号床间 | 距中心 **250 m**，位置分 9.5 |
| Powerhouse Hotel Tamworth by Rydges | 9.1 / 946 条 | A$269 | 特大号床间，免费取消 | 楼内有 Workshop Kitchen 餐厅 |
| Roydons Motor Inn | 8.9 / 1,144 条 | A$163 | Superior Queen，免费取消，到店付款 | 距中心 0.9 km |
| The Aston Motel Tamworth | 8.1 / 1,060 条 | A$136 | Executive Queen | 距中心 6.2 km |
| Econo Lodge Savannah Park | 9.0 / 486 条 | A$134 | 大号床间 | 距中心 5.9 km |

**Armidale（该日期共 34 家可订）**

| 住宿 | Booking 评分 | 价格 | 房型 | 备注 |
|---|---|---|---|---|
| **The Alluna Motel (Ascend Collection)**（180 Dangar St） | **9.2 / 605 条** | **A$189** | 大号床间，免费取消，到店付款 | **Google 4.5 / 249 条；Google Hotels 明确「free-of-charge self-parking」**。距中心 0.9 km |
| Armidale Pines Motel | 9.0 / 269 条 | A$204 | 豪华大号床间，免费取消 | 距中心 400 m，位置分 9.5 |
| Loloma House | **9.7 / 122 条** | A$249 | 豪华大号床套房（54 m²，独立卧室+客厅+浴室），免费取消 | 距中心 500 m，位置分 9.8 |
| Armidale Club Motel | 8.8 / 527 条 | A$167 | 标准大号床间，免费取消 | 距中心 **350 m**，位置分 9.6 |
| Cedar Lodge Motel | 8.2 / 688 条 | **A$140** | 豪华大号床间，免费取消，到店付款 | 距中心 400 m |
| Tattersalls Hotel | 8.9 / 453 条 | A$279 | 高级大号床间 | 距中心 **50 m**，楼下就是周二开门的餐厅 |
| New England Motor Inn | 8.4 / 359 条 | A$165 | 大号床间，免费取消，到店付款 | 距中心 350 m |

> **诚实标注**：免费停车我只逐个核实了 **Edward Parry Motel** 和 **The Alluna Motel** 两家（Google Hotels 明确写 free self-parking）。其余各家我只能说 Booking 的筛选面板显示「停车场：Tamworth 40/40、Armidale 34/34 家都有」，但**该筛选项不区分免费/收费**。澳洲 motel 绝大多数是门口免费车位，但下单前请在具体房源页确认。
> Lindsay House Guest House（Booking 9.4 / 106 条，A$187）是 guest house，房型页未标 private bathroom，**需确认是否独立卫浴**，我未核实。
> 价格是 2026-09-05 查询的未登录价，会变。

### 3.3 次日一早（周三 23/9）出发前 30–60 分钟

**Tamworth（明显更强）**
- **Tamworth Powerstation Museum**（216 Peel St）— **周三–周六 09:00–13:00**，成人 **$7**、优惠票 $5。**Google 4.7 / 143 条**。1888 年 Tamworth 成为澳洲第一个装市政电灯的城市，馆里是当年的发电站和蒸汽机，志愿者会带讲解。**正好周三开，正好 45 分钟，正好在主街上。** 依据：官网 tamworthpowerstationmuseum.com.au + Google 面板 + MGNSW。
- Oxley Scenic Lookout — 07:00 开，早上再上去一次也行（免费）。

**Armidale（明显更弱）**
- **Goldfish Bowl Cafe & Bakery**（3/160 Rusden St）— **Google 4.5 / 977 条**，木火炉有机 sourdough + 精品咖啡。Google 面板显示早上 7 点开门，但**周三逐日营业时间我未核实**。
- Armidale Heritage Bus Tour — 每天（周一–周六）**10:00** 从 Visitor Information Centre（82 Marsh St）发车，**2.5–3 小时**。TripAdvisor 4.8 / 52 条。**对「30–60 分钟」太长，10 点发车对早出发也太晚。**
- NERAM（New England Regional Art Museum）— Google 4.6 / 342 条。**开门时间我未核实**，一般是 10:00，同样对早出发不友好。
- 更好的做法是**把 30–60 分钟放在路上**：Armidale 往北 1 小时的 **Glen Innes Australian Standing Stones**（Google 4.5 / 1,254 条，24 小时开放，免费）。

### 3.4 小结：谁更适合过夜

| | Tamworth | Armidale |
|---|---|---|
| 周二晚吃饭 | 可以（Pig & Tinder Box 4.3/837） | **更好**（The Cottage 4.9/261） |
| 周二晚免费活动 | **有**（Oxley Scenic Lookout，4.5/327 TA，开到 22:00） | 未查到对等的 |
| 周三早上 | **有**（Powerstation Museum，周三 9–13 点，$7，4.7/143） | 弱（早上没东西开门） |
| 住宿性价比 | 略好、房源多 8 家 | 略贵、更冷 |
| 白天周边 | 一般 | **强**（Wollomombi Falls、Oxley Wild Rivers 峡谷） |

**关键洞察：Armidale 的价值在白天（峡谷），不在晚上。** 方案 A 让他们**白天经过 Armidale 并绕去 Wollomombi Falls，晚上睡在 Tamworth**，正好各取所长。

---

## 4. 砍掉 Hunter Valley 后，Tenterfield 那一晚还需要吗

### 4.1 从 Tamworth 出发：**不行**

Tamworth → Girraween **3 h 52 min** + The Pyramid **2 h** + Girraween → Gold Coast **3 h 27 min** = 净 **9 h 19 min**。加午饭、加油、找停车、下山缓冲，实际 11 小时以上。**卡在 Tamworth → Girraween 这 337 km 上。** 不推荐。

### 4.2 从 Armidale 出发：**可以，但很满**

Armidale → Girraween **2 h 38 min** + The Pyramid **2 h** + Girraween → Gold Coast **3 h 27 min** = 净 **8 h 05 min**。
7:30 出发 → 10:10 到 → 12:15 下山 → 13:00 再出发 → **16:30 到 Gold Coast**。可行。

**但代价链条是这样的**：要在 Armidale 过 D6 的夜，D6 就得开 **5 h 29 min**（Nelson Bay → Burning Mountain → Tamworth → Armidale）。所以「省一晚」的真实成本是：
- D6 5 h 29 min + Burning Mountain 步道
- D7 6 h 05 min 驾驶 + 2 h Grade 4 爬山
- 周三早上 Armidale 什么都做不了
- 零弹性：The Pyramid 顶上那段裸露岩壁若遇雨/大风（QLD Parks 官网提示需要 "good level of fitness and stamina to climb the steep section of exposed rock near the summit"）就会全盘拖后

**省下来的那一晚可以怎么用**：
1. 还给海岸——Nelson Bay / Port Stephens 多住一晚，D5 的 Tomaree（Grade 5）就不用赶；
2. 或者 Gold Coast 多一晚，D9 的 Harbour Town 购物不用挤。

### 4.3 顺带一个重复项提醒

如果保留 Tenterfield 那一晚，注意 **Bald Rock National Park**（Tenterfield 以北）的 Bald Rock Summit walk：NSW National Parks 官网写 **2.7 km 往返、建议 2 小时、Grade 5**，全澳最大的花岗岩独石，TripAdvisor 4.8 / 229 条。它和 Girraween 的 The Pyramid **是同一类体验**（爬花岗岩巨石顶看全景），两个都做会重复。**二选一即可**，The Pyramid 已在计划里就别再加 Bald Rock。

---

## 5. 观鲸重复问题

### 5.1 是不是同一批鲸？——**是。**

两地在 2026 年 9 月看到的都是**同一支东澳座头鲸族群的南迁个体**。依据：
- Moonshadow-TQC 官网：2026 观鲸季 **5 月 23 日 – 11 月 8 日**。
- Port Jet 官网：**5 月至 11 月**。
- 迁徙节律（visitnsw / Newcastle Herald / Port Macquarie News 等报道口径一致）：北迁 5–8 月，**南迁约 8 月中至 10 月中**，9–11 月南下的主要是**带幼崽的母鲸**，游得慢、贴着海岸走，浮出水面的时间长，因此 9 月下旬两地看到的都是「mums and bubs」。

**Port Macquarie 在 Port Stephens 以北约 240 km**，同一批鲸南下会先经过 Port Macquarie（D4，20/9 周日），两天后经过 Port Stephens（D6，22/9 周二）。**是同一批鲸的同一个行为阶段，重复度非常高。**

### 5.2 两地差异

| | **Port Jet Cruise Adventures**（Port Macquarie，D4） | **Moonshadow-TQC**（Nelson Bay，D6） |
|---|---|---|
| 船型 | **Wave Rider / Ocean Rider**，10.5 m 专造快艇，官方称「NSW 最快的商业船」；有顶棚；**船上装 hydrophone**，可通过环绕音响实时听鲸鱼叫声 | **Hinchinbrook Explorer 或 MV Osprey**，大型双体船 |
| 时长 | **90 分钟** | **2.5 小时** |
| 价格 | **A$95**（Rezdy 官方订位页） | **A$85**（15 岁以上，官网） |
| 出发 | Short St, Port Macquarie；一天多班（当日班次表显示 9:45 / 10:00 / 11:45 / 13:00 等） | d'Albora Marina, Nelson Bay；**10:00 与 13:30 两班** |
| 营业日 | 官网 "Opening Hours: Tuesday – Sunday 9am"，**周一可能不开**（D4 = 20/9 周日，不受影响） | 季内每天 |
| 海况 | 小快艇、直接冲出海，**更颠**；官方明说孕妇/腰颈伤者不适合 | 大船更稳，但离水面远；有 TripAdvisor 差评抱怨晕船（个例，不足以定性） |
| 成功率 | **未查到官方数字** | **未查到官方数字**；官网写「鲸鱼是野生动物，不保证」，未看到鲸鱼可获**不可转让的补乘券** |
| **Google** | **4.7 / 523 条** | **4.6 / 836 条** |
| **TripAdvisor** | **4.9 / 603 条** | **4.6 / 1,239 条** |

### 5.3 只能选一个 → **选 D4 的 Port Jet，砍掉 D6 的 Moonshadow**

三个理由：
1. **评分两个平台都赢**：Google 4.7 vs 4.6，TripAdvisor **4.9 vs 4.6**。
2. **体验差异度更高**：小快艇 + 水听器，和这趟行程里其他任何海上/陆上活动都不重样；Moonshadow 是标准大船观光，和他们已排的 Nelson Bay 海湾风光重叠。
3. **正好解开 D6 的死结**：Moonshadow 早班 10:00 出发、2.5 小时，返岸就 12:30 了，再加上岸整理，**Nelson Bay 最早 13:30 才能上路**——那样方案 A 的 4 h 11 min 会拖到晚上 18:00 才到 Tamworth，方案 B 的 5 h 29 min 更是根本不成立。**砍掉它，D6 早上就腾出来了。**

（如果他们其实更想要「2.5 小时慢慢看 + 稳」，那就反过来砍 Port Jet、留 Moonshadow，但那样 D6 必须放弃内陆长途，只能退回方案 C。）

---

## 6. 我没能核实的部分

- Google Maps 的时间是查询当日「现在出发」的默认估算，**未做 2026-09-22 周二具体时段的交通模拟**。New England Hwy 是货车干道，实际会略慢。
- **The Pig & Tinder Box 的周二逐日营业时间**：官网只写「Open for lunch and dinner daily」，Google 面板显示的是查询当天（周六）的时间。周二具体几点开我未逐日核实。
- **Goldfish Bowl Bakery 周三开门时间**未逐日核实。
- **NERAM、Tamworth Regional Botanic Gardens 的开放时间**未核实。
- **免费停车**只逐个核实了 Edward Parry 与 Alluna 两家（见 3.2 注）。
- **观鲸成功率**：两家都未公布数字，任何「95% 成功率」之类的说法我都没查到出处。
- **Girraween → Gold Coast**：Google 3 h 27 min 与 Rome2Rio 4 h 09 min 相差 42 分钟，我采信 Google 但建议按 3 h 45 min 排。
- Armidale → Stanthorpe 我只有 Rome2Rio 的 2 h 55 min，未用 Google 复核。

---

## 7. 明确推荐

### 首选：**方案 A（Tamworth 过夜）+ 砍掉 Nelson Bay 的 Moonshadow 观鲸**

```
D5 周一 21/9  Forster → Seal Rocks → Nelson Bay 过夜
              （下午/傍晚从容爬 Tomaree Head，Grade 5）

D6 周二 22/9  Nelson Bay 8:30 出发
              → Burning Mountain（Wingen）4 km / Grade 3 / 免费，走 1.5 h
              → Scone 或 Murrurundi 午饭
              → Tamworth 约 15:30 入住
              傍晚：Oxley Scenic Lookout 看日落（免费，开到 22:00，TA 4.5/327）
              晚餐：The Pig & Tinder Box（Google 4.3/837）或 Tudor Hotel（周二 Steak Night，Google 4.2/752）
              住：Edward Parry Motel & Apartments，A$186（Booking 9.5/545，免费停车已核实）
              净驾驶 4 h 11 min

D7 周三 23/9  Tamworth 8:00 出发，先逛 Powerstation Museum（9:00 开，$7，Google 4.7/143，45 分钟）
              → Uralla（Thunderbolt's Rock，路边 15 分钟）
              → Armidale 午饭
              → Wollomombi Falls（往东 30 min，220 m 落差峡谷观景台，Google 4.6/831）往返 +1 h
              → Glen Innes Australian Standing Stones（免费，24 h，Google 4.5/1,254）
              → Tenterfield 过夜
              净驾驶 3 h 25 min（不含 Wollomombi 绕行 1 h）

D8 周四 24/9  Tenterfield → Girraween NP（约 40 min）
              → The Pyramid（3.6 km 往返 / Grade 4 / 2 h）
              → Gold Coast (Labrador)，3 h 27 min
              可选：天黑后去 Springbrook NP 的 Natural Bridge 看 glow worms
                    （免费、24 h 开放、Google 4.8/4.4K，距 Gold Coast 约 1 h）
              净驾驶 4 h 05 min

D9 周五 25/9  Harbour Town → Brisbane（不变）
```

**为什么是它**：三天驾驶 4:3.5:4，没有一天超过 4 h 15 min；D7 从「6 小时纯赶路」变成一条有瀑布、有巨石阵、有小镇午饭的高原观光线；命中他们全部四个喜好（海岸风景已在前段、观景台 ×3、步道 ×2、独特自然现象 ×2），完全避开酒庄/spa/动物园/骑马；不减任何一晚，不需要重订后段酒店。

**取舍代价（老实说）**：
1. **不省时间也不省钱**——D6–D8 总驾驶 11 h 41 min，和现方案的 11 h 36 min 几乎一样。这次重构买到的是**分配**和**内容**，不是**总量**。
2. **Tamworth 本身不是目的地**，就是个功能性的落脚镇。它的价值是「4 小时开到、有饭吃、有免费观景台、第二天早上有个 45 分钟的小博物馆」，仅此而已。如果他们期待的是「值得专程去的镇」，Tamworth 会让他们失望——但 Pokolbin 在剔除酒庄后同样不是，而 Tamworth 至少位置对。
3. **牺牲了 Nelson Bay 的观鲸**。如果他们对 Port Jet 那 90 分钟不满意，就没有第二次机会了。缓解办法：D5 傍晚在 Tomaree Head 顶上其实也能看到南迁鲸的水柱（陆基观鲸，免费），当作补充。

### 备选：**方案 B 变体 2（Armidale 过夜 + 砍掉 Tenterfield 那一晚）**

**只在他们明确说「宁可两天硬开，也想多要一个海边日」时才选。**
- D6 5 h 29 min（**记住要手动指定走 New England Hwy 经 Scone/Tamworth，别用 Google 首选的 Thunderbolts Way**）
- D7 6 h 05 min 驾驶 + 2 h 爬山，7:30 出发、16:30 到 Gold Coast，零弹性
- 换来一整晚可以还给 Port Stephens 或 Gold Coast
- 晚餐能吃到 The Cottage（Google **4.9 / 261**，本次调研两镇最高分），住 The Alluna Motel A$189（Booking 9.2/605，免费停车已核实）
- 但周三早上在 Armidale 一件事都做不了

### 不推荐：方案 C

沿海北上里程更长（700+ km vs 630 km）、同样要开两天、必然放弃 The Pyramid，并且把整趟行程唯一一段非海岸地貌全部删掉。**唯一值得从方案 C 里抢救出来的是 Natural Bridge 的 glow worms——而那个不用改路线，D8 晚上到了 Gold Coast 再开 1 小时就能去。**

---

**Sources:**

驾驶数据：[Google Maps 路线（Nelson Bay–Tamworth 等各段，2026-09-05 实查）](https://www.google.com/maps/dir/Nelson+Bay+NSW/Tamworth+NSW)、[Rome2Rio](https://www.rome2rio.com/s/Nelson-Bay/Tenterfield)、[Wanderlog](https://wanderlog.com/drive/between/147529/82755/nelson-bay-to-tamworth-drive)
步道与国家公园：[NSW National Parks — Burning Mountain walk](https://www.nationalparks.nsw.gov.au/things-to-do/walking-tracks/burning-mountain-walk)、[QLD Parks — The Pyramid, Girraween NP](https://parks.qld.gov.au/parks/girraween/journeys/the-pyramid)、[NSW National Parks — Bald Rock Summit walk](https://www.nationalparks.nsw.gov.au/things-to-do/walking-tracks/bald-rock-summit-walk)、[QLD Parks — Springbrook NP visiting safely](https://parks.qld.gov.au/parks/springbrook/visiting-safely)
观鲸：[Moonshadow-TQC Whale Watching](https://moonshadow-tqc.com.au/cruises/whale-watching/)、[Port Jet Cruises](https://portjet.com.au/)、[Port Jet 官方订位页（Rezdy）](https://cruiseadventures.rezdy.com/200100/whale-watching-wave-rider)、[Newcastle Herald — 南迁母鲸与幼崽](https://www.newcastleherald.com.au/story/8384225/its-humpback-season-baby-mums-and-calves-have-a-whale-of-a-time/)
餐厅与景点：[The Pig & Tinder Box](https://www.thepigandtinderbox.com.au/)、[Tudor Hotel Tamworth](https://www.tudorhoteltamworth.com.au/)、[Hopscotch Restaurant & Bar](https://www.hopscotchrestaurant.com.au/)、[The Cottage Armidale](https://www.thecottagearmidale.au/)、[Manny's on Marsh](https://mannysonmarsh.com/)、[Tattersalls Hotel Armidale](https://www.tattersallsarmidale.com.au/)、[Whitebull Hotel](https://www.whitebull.net.au/)、[The Welder's Dog（该店已售出）](https://theweldersdog.com.au/tamworth)、[Tamworth Powerstation Museum](https://tamworthpowerstationmuseum.com.au/visit)、[TripAdvisor — Oxley Scenic Lookout](https://www.tripadvisor.com.au/Attraction_Review-g255331-d7171111-Reviews-Oxley_Scenic_Lookout-Tamworth_New_South_Wales.html)、[Visit NSW — Wollomombi Falls](https://www.visitnsw.com/destinations/country-nsw/armidale-area/armidale/attractions/wollomombi-falls)、[Visit Armidale — Heritage Tour](https://www.visitarmidale.com.au/)
住宿与气候：[Booking.com（Tamworth / Armidale，2026-09-22 至 09-23，2 成人，未登录）](https://www.booking.com/)、[Google Hotels — Edward Parry Motel / Alluna Motel](https://www.google.com/travel/hotels)、[climate-data.org — Armidale / Tamworth](https://en.climate-data.org/oceania/australia/new-south-wales/armidale-1021/)
