import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(ROOT, "common3.css"), encoding="utf-8").read()

def footer():
    return '''
<div class="footer">
  <div class="foot-row">
    <div>
      <div class="foot-name">山竹</div>
      <div class="foot-role">巴生光华独立中学辩论队教练｜马来西亚辩手</div>
    </div>
    <div class="foot-cta">私信我 → @zhou_shanzhu</div>
  </div>
</div>
'''

def meta(idx):
    return f'''<div class="meta"><div class="brand">山竹辩论私教</div><div class="idx">{idx} / 04</div></div>'''

def card(idx, photo, kicker, title_html, tagline, scale=100):
    return f'''
<div class="page">
  {meta(idx)}
  <div class="figure"><img src="../../photos/{photo}" style="width:{scale}%;"></div>
  <div class="head">
    <div class="kicker">{kicker}</div>
    <h1 class="title">{title_html}</h1>
    <div class="tagline">{tagline}</div>
  </div>
  {footer()}
</div>
'''

CARDS = [
    dict(idx="01", photo="blazer_cut_t.png", kicker="DEBATE COACHING",
         title="山竹<br>辩论私教",
         tagline='逻辑清楚 · 现场组织 · 不靠稿子念<br>初中生・高中生・大学生 都欢迎',
         scale=138),
    dict(idx="02", photo="thinking_cut2_t.png", kicker="PHILOSOPHICAL DEBATE",
         title="哲理辩",
         tagline='用<b>"倒推法"</b>一路追问"为什么"<br>练出你的"活人感"',
         scale=108),
    dict(idx="03", photo="hero_cut_t.png", kicker="POLICY DEBATE",
         title="奥瑞冈<br>政策辩",
         tagline='需要性 · 根属性 · 解决力 · 损益<br>四点拆清楚，攻防都不慌',
         scale=140),
    dict(idx="04", photo="blazer_cut_flip_t.png", kicker="POLITICAL & INTERNATIONAL AFFAIRS",
         title="政治辩＋<br>国际局势",
         tagline='不是背时事，是讲清楚<b>政治逻辑</b><br>找到你讲得清、站得住的立场',
         scale=138),
]

def build_html(c, variant):
    body_class = "carousel" if variant == "carousel" else "story"
    body = card(c["idx"], c["photo"], c["kicker"], c["title"], c["tagline"], c["scale"])
    return f'''<!doctype html>
<html><head><meta charset="utf-8"/>
<style>{CSS}</style>
</head>
<body class="{body_class}">
{body}
</body></html>'''

for variant in ["story", "carousel"]:
    outdir = os.path.join(ROOT, "v3", variant)
    os.makedirs(outdir, exist_ok=True)
    for i, c in enumerate(CARDS, 1):
        html = build_html(c, variant)
        path = os.path.join(outdir, f"{variant}{i}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", path)
