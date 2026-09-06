# Review-Driven Travel Planning ｜ 评分驱动的旅行规划

A reusable method for planning self-drive trips from **verifiable review data** instead of
blog roundups — plus two fully worked Australian road trips built with it.

用**可核验的评分数据**（而不是攻略文章）规划自驾行程的一套方法，以及用它做出来的两趟完整澳洲公路旅行。

---

## The idea ｜ 这套方法在做什么

Most trip planning starts from a route and fills it with whatever the internet recommends.
This repo inverts that: **screen experiences first against a hard, stated gate, then let the
route fall out of what survives.**

多数行程规划是先定路线、再往里塞网上推荐的东西。这个仓库反过来：**先用一条写死的硬闸门筛体验，
活下来的点自己决定路线长什么样。**

**The gate ｜ 闸门：Google ≥ 4.7 AND ≥ 200 reviews**

- Platforms are recorded separately and **never averaged or substituted** for one another.
  平台分开记，**绝不混用、不取平均**。
- A park's overall score does not stand in for one of its trails; a business's overall score
  does not stand in for one of its packages.
  公园总评分不代表其中某条步道；商家总评分不代表其中某个套餐。
- Anything not found is written as **"not found"**, never estimated.
  查不到就写**「未查到」**，绝不编造。

Accommodation has its own hard gate: a private room for two, an **ensuite confirmed at room
level**, no hostel/dorm/shared bathroom, and free parking that is **free *and* on-site *and*
a dedicated space** — any one missing is recorded as unconfirmed.

住宿另有硬闸门：两人独立房间、**房型层面**确认独立浴室、非 hostel/dorm/共用浴室、免费停车
**三项齐全**（免费 / 场地内 / 专用车位），缺一项即记为未确认。

**→ Read the method: [`METHOD.md`](METHOD.md)** — 17 sections, English body with a
one-page Chinese digest at the top.
**→ 方法全文见 [`METHOD.md`](METHOD.md)**，共 17 节，正文英文、开头有一页中文摘要。

---

## The trips ｜ 两趟行程

### NSW / QLD 2026 · 7 days, 6 nights ｜ 七天六晚

`Brisbane → Yamba → Coffs Harbour → Port Macquarie (×2) → Ballina → Stanthorpe → Brisbane`
17–23 Sep 2026 · two adults · own car

The main worked example. Hour-by-hour plan with per-day route maps, every rating labelled by
platform, a points table **split into "cleared the gate" and "did not"**, verified opening
hours, BOM climate data per station, a booked-accommodation ledger with check-in/check-out
conflicts resolved, and per-day clothing and footwear notes.

主样板。逐小时安排 + 每日路线图，所有评分标明平台，点位表**分「过闸门」与「未过闸门」两段**，
营业时间逐条核实，气象数据按站点取自 BOM，住宿表记录实付金额并已解掉入住/退房时间冲突，
每天附穿衣与鞋子提示。

- 🌐 [Web ｜ 网页版](docs/nsw-final.html) · 📄 [PDF](docs/nsw-final.pdf)
- 🗒 [Annotated earlier version ｜ 带批注的旧版（留档）](docs/nsw.html)

### Cairns / Far North Queensland 2026 · 10 days ｜ 十天

`Cairns → Port Douglas → Cape Tribulation → Yungaburra → Cairns`

The first trip the method was developed on.
方法最初就是在这趟行程里长出来的。

- 🌐 [Web ｜ 网页版](docs/cairns-2026.html) · 📄 [PDF](docs/pdf/cairns-2026-travel-guide.pdf)
- 🍽 [Port Douglas dining deep-dive ｜ 餐饮深度样板](research/port-douglas-dining.md)

---

## Repository layout ｜ 仓库结构

```text
METHOD.md    the method itself — 17 sections ｜ 方法本体，17 节
README.md    this file ｜ 本文件
docs/        published site (GitHub Pages root); index.html is the hub
             ｜ 发布站点，index.html 是双语索引首页
research/    raw research: segments, pricing, accommodation scans ｜ 原始调查稿
scripts/     map, PDF and image generation tools ｜ 地图/PDF/图片生成脚本
assets/      images and their source records ｜ 图片与来源记录
```

`research/nsw-roadtrip/` holds the scans behind the NSW plan — route segments, restaurant
pricing passes, and dated Booking.com accommodation sweeps. Files are named by the date they
were gathered, because **every one of these facts expires**.

`research/nsw-roadtrip/` 是 NSW 行程背后的原始扫描——路段、餐厅价格轮、按日期命名的 Booking
住宿扫描。文件按采集日期命名，因为**这里面每一条事实都会过期**。

---

## Data boundaries ｜ 数据边界

Read this before using any figure.
用这里任何一个数字之前，先读这一段。

- **Everything expires.** Prices, opening hours, tour schedules and room inventory change.
  Dates of collection are recorded throughout; re-verify against the operator's own page
  before you travel.
  **一切都会过期。** 价格、营业时间、班次、房量都会变。文中标注了采集日期，出行前必须以运营方
  自己的页面为准。
- **Ratings are labelled by platform and never mixed.** A number without a platform label is
  a bug, not a shorthand.
  **评分一律标注平台、绝不混用。** 没标平台的数字是错误，不是省略。
- **"Not found" means the search actually failed.** It is never a placeholder for a guess.
  **「未查到」表示确实检索未果**，不是猜测的占位符。
- Route maps are for planning. They do not replace live navigation, road-closure feeds or
  weather warnings.
  路线图用于规划，不替代实时导航、道路封闭与天气警报。
- Image credits live in each asset directory's `credits.json` / `commons.json`. Check licence
  and attribution before redistributing.
  图片来源记录在各素材目录的 `credits.json` / `commons.json`，再发布前请逐项核对许可与署名。

---

## Licence ｜ 许可

[MIT](LICENSE) for the method, code and prose. Third-party images keep their own licences —
see the credit files.

方法、代码与文字采用 [MIT](LICENSE)；第三方图片沿用各自许可，见来源文件。
