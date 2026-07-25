import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(ROOT, "common2.css"), encoding="utf-8").read()

FOOTER = '''
<div class="footer">
  <div class="foot-row">
    <div class="foot-id">
      <img class="avatar" src="../../photos/avatar.jpg">
      <div>
        <div class="foot-name">山竹</div>
        <div class="foot-role">《辩论怪物 Debate Beasts》主理人｜巴生光华独立中学辩论队教练</div>
      </div>
    </div>
    <div class="foot-cta">私信我 → <span class="ig">@zhou_shanzhu</span></div>
  </div>
</div>
'''

def meta(idx):
    return f'''<div class="meta"><div class="brand">DEBATE BEASTS · 山竹辩论私教</div><div class="idx">{idx} / 04</div></div>'''

def photo_card(idx, photo_h_story, photo_h_car, kicker, title_html, intro, list_items):
    li = "".join(
        f'<div class="item"><div class="n">{n}</div><div class="t">{t}</div></div>'
        for n, t in list_items
    )
    return f'''
<div class="page on-photo">
  {meta(idx)}
  <div class="photo-wrap" data-h-story="{photo_h_story}" data-h-car="{photo_h_car}">
    <img src="../../photos/hero.jpg">
    <div class="photo-head">
      <div class="kicker">{kicker}</div>
      <h1 class="title">{title_html}</h1>
    </div>
  </div>
  <div class="content">
    <p class="intro">{intro}</p>
    <div class="list">{li}</div>
  </div>
  {FOOTER}
</div>
'''

def flat_card(idx, kicker, title_html, tagline, intro, list_items=None, pair=None):
    inner = ""
    if list_items:
        li = "".join(
            f'<div class="item"><div class="n">{n}</div><div class="t">{t}</div></div>'
            for n, t in list_items
        )
        inner = f'<div class="list">{li}</div>'
    elif pair:
        rows = "".join(
            f'<div class="row {cls}"><span class="mark">{m}</span><span class="txt">{t}</span></div>'
            for cls, m, t in pair
        )
        inner = f'<div class="pair">{rows}</div>'
    return f'''
<div class="page">
  {meta(idx)}
  <div class="watermark">{idx}</div>
  <div class="head-zone">
    <div class="kicker">{kicker}</div>
    <h1 class="title">{title_html}</h1>
    <div class="tagline">{tagline}</div>
  </div>
  <div class="content">
    <p class="intro">{intro}</p>
    {inner}
  </div>
  {FOOTER}
</div>
'''

CARD1 = dict(
    kind="photo", idx="01",
    kicker="DEBATE COACHING",
    title="辩论私教<br>招生中",
    intro='质询、对辩、结辩、陈词——<b>说服力、逻辑、举证、临场组织</b>，通用基本功一起打牢。',
    list=[("01", "逻辑清楚，不靠稿子念"), ("02", "现场组织语言，不是资料轰炸"), ("03", "初中生・高中生・大学生 都欢迎")],
)

CARD2 = dict(
    kind="flat", idx="02",
    kicker="PHILOSOPHICAL DEBATE",
    title="哲理辩",
    tagline="想得深不深，比资料多不多更重要",
    intro='用<b>"倒推法"</b>一路追问"为什么"，挖到你真正相信的东西；还会练"活人感"——像说话，不像念稿。',
    list=[("01", "讲完一句话，先停下来"), ("02", '一直追问"为什么"'), ("03", "挖到你真正相信的东西"), ("04", "找到你和对方到底在吵什么")],
)

CARD3 = dict(
    kind="flat", idx="03",
    kicker="POLICY DEBATE",
    title="奥瑞冈<br>政策辩",
    tagline='纯正统政策辩 · "我国应不应该 XXX"',
    intro="要打赢，得从四个点下手——正方证明四点都成立，反方打掉一点就赢。",
    list=[("01", "需要性 —— 这事有多严重"), ("02", "根属性 —— 为什么现在解决不了"), ("03", "解决力 —— 方案能不能解决"), ("04", "损益 —— 划不划算")],
)

CARD4 = dict(
    kind="flat", idx="04",
    kicker="POLITICAL & INTERNATIONAL AFFAIRS",
    title="政治辩＋<br>国际局势",
    tagline="不是背时事，是讲清楚政治逻辑",
    intro="我会带你把复杂时政讲成人话，在国际议题里找到一个你自己讲得清、站得住的立场。",
    pair=[("no", "✕", "堆时事、堆数据"), ("yes", "✓", "讲清楚背后的政治逻辑")],
)

CARDS = [CARD1, CARD2, CARD3, CARD4]

def build_html(card, variant):
    body_class = "carousel" if variant == "carousel" else "story"
    if card["kind"] == "flat":
        body_class += " tinted"
    if card["kind"] == "photo":
        body = photo_card(card["idx"], 1080, 740, card["kicker"], card["title"], card["intro"], card["list"])
    else:
        body = flat_card(card["idx"], card["kicker"], card["title"], card["tagline"], card["intro"],
                          list_items=card.get("list"), pair=card.get("pair"))
    photo_h = 1080 if variant == "story" else 740
    extra_css = f".photo-wrap{{height:{photo_h}px;}}" if card["kind"] == "photo" else ""
    return f'''<!doctype html>
<html><head><meta charset="utf-8"/>
<style>{CSS}
{extra_css}</style>
</head>
<body class="{body_class}">
{body}
</body></html>'''

for variant in ["story", "carousel"]:
    outdir = os.path.join(ROOT, "v2", variant)
    os.makedirs(outdir, exist_ok=True)
    for i, card in enumerate(CARDS, 1):
        html = build_html(card, variant)
        path = os.path.join(outdir, f"{variant}{i}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)
