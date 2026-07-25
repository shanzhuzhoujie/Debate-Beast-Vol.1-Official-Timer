import os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(ROOT, "common.css"), encoding="utf-8").read()

ICONS = {
    "mic": '''<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="24" y="8" width="16" height="30" rx="8" stroke="#6B1626" stroke-width="3"/>
      <path d="M16 28v4c0 8.837 7.163 16 16 16s16-7.163 16-16v-4" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
      <line x1="32" y1="48" x2="32" y2="58" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
      <line x1="21" y1="58" x2="43" y2="58" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
    </svg>''',
    "spiral": '''<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M32 44a12 12 0 1 1 8.49-3.51" stroke="#6B1626" stroke-width="3" stroke-linecap="round"/>
      <path d="M32 50a18 18 0 1 1 12.73-5.27" stroke="#C5A059" stroke-width="3" stroke-linecap="round"/>
      <path d="M32 56a24 24 0 1 1 16.97-7.03" stroke="#C5A059" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
      <circle cx="32" cy="32" r="3" fill="#6B1626"/>
    </svg>''',
    "grid": '''<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="9" y="9" width="20" height="20" rx="2" stroke="#6B1626" stroke-width="3"/>
      <rect x="35" y="9" width="20" height="20" rx="2" stroke="#C5A059" stroke-width="3"/>
      <rect x="9" y="35" width="20" height="20" rx="2" stroke="#C5A059" stroke-width="3"/>
      <rect x="35" y="35" width="20" height="20" rx="2" stroke="#6B1626" stroke-width="3"/>
    </svg>''',
    "globe": '''<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="32" cy="32" r="23" stroke="#6B1626" stroke-width="3"/>
      <ellipse cx="32" cy="32" rx="10" ry="23" stroke="#C5A059" stroke-width="2.5"/>
      <line x1="9" y1="32" x2="55" y2="32" stroke="#C5A059" stroke-width="2.5"/>
      <path d="M12 20c8 5 32 5 40 0" stroke="#C5A059" stroke-width="2.2"/>
      <path d="M12 44c8 -5 32 -5 40 0" stroke="#C5A059" stroke-width="2.2"/>
    </svg>''',
}

FOOTER = '''
<div class="footer">
  <div class="hair"></div>
  <div class="foot-wrap">
    <div class="foot-name">山竹</div>
    <div class="foot-role">《辩论怪物 Debate Beasts》主理人｜巴生光华独立中学辩论队教练</div>
    <div class="foot-cta">私信我，聊聊你想加强哪里 → <span class="ig">@zhou_shanzhu</span></div>
  </div>
</div>
'''

def page(icon, kicker, title, subtitle, body_html, crumb_idx):
    return f'''
<div class="page">
  <div class="crumb">
    <div class="left"><b>DEBATE BEASTS</b> · 山竹辩论私教</div>
    <div class="right">{crumb_idx} / 04</div>
  </div>
  <div class="hair"></div>

  <div class="header">
    <div class="badge">{ICONS[icon]}</div>
    <div class="kicker">{kicker}</div>
    <h1 class="title">{title}</h1>
    <div class="rule-short"></div>
    <div class="subtitle">{subtitle}</div>
  </div>

  <div class="body">
    {body_html}
  </div>

  {FOOTER}
  <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
</div>
'''

# ---------------- CARD 1 : Overview ----------------
CARD1_BODY = '''
<div class="panel">
  <div class="tag-label">主理人身份</div>
  <p class="copy" style="margin-top:14px;">
    <b>《辩论怪物 Debate Beasts》</b>主理人｜<b>巴生光华独立中学</b>辩论队教练｜马来西亚知名辩手，成绩拿得出手。
  </p>
</div>

<div class="panel plain">
  <div class="tag-label">通用基本功，我都能带你练</div>
  <p class="copy" style="margin-top:14px;">
    不管你打质询、对辩、结辩还是陈词，这些能力都是通用的：说话<b>有没有说服力</b>、情绪<b>带不带得动人</b>、逻辑<b>清不清楚</b>、举证<b>到不到位</b>、用词<b>准不准</b>。
  </p>
</div>

<div class="callout">
  <div class="qmark">"</div>
  <h3>我想带出来的辩手</h3>
  <p>是不靠稿子说话的那种——逻辑清楚、论述干净、能现场组织语言。如果你喜欢提前准备好一堆资料数据去"轰炸"对手，那可能不是我的风格，可以跳过我～</p>
</div>

<div class="pills">
  <div class="pill lead">适合对象</div>
  <div class="pill">初中生</div>
  <div class="pill">高中生</div>
  <div class="pill">大学生</div>
</div>
'''

# ---------------- CARD 2 : 哲理辩 ----------------
CARD2_BODY = '''
<div class="panel plain">
  <div class="tag-label">比的不是资料多，是想得深不深</div>
  <p class="copy" style="margin-top:14px;">
    哲理辩比的不是资料多不多，是你<b>想得深不深</b>。我会带你用<b>"倒推法"</b>，一路挖到你真正相信的东西，找到你和对方到底在吵什么。
  </p>
</div>

<div class="panel">
  <div class="tag-label">倒推法怎么练</div>
  <div class="steps" style="margin-top:10px;">
    <div class="step"><div class="dot">1</div><div class="txt">讲完<b>一句话</b>，先停下来</div></div>
    <div class="step"><div class="dot">2</div><div class="txt">一直追问<b>"为什么"</b></div></div>
    <div class="step"><div class="dot">3</div><div class="txt">一路挖到<b>你真正相信</b>的东西</div></div>
    <div class="step"><div class="dot">4</div><div class="txt">找到你和对方<b>到底在吵什么</b></div></div>
  </div>
</div>

<div class="callout">
  <div class="qmark">"</div>
  <h3>还会练"活人感"</h3>
  <p>让评委觉得你是在<b>说话</b>，不是在<b>念稿</b>——这也是哲理辩最容易被忽略、但最影响印象分的一环。</p>
</div>
'''

# ---------------- CARD 3 : 政策辩 ----------------
CARD3_BODY = '''
<div class="panel plain">
  <div class="tag-label">辩题长这样</div>
  <p class="copy" style="margin-top:14px;">
    辩题通常是：<b>"我国应不应该 XXX"</b>。要打赢，得从四个点下手，正方要证明这四点都成立，反方只要打掉其中一点。
  </p>
</div>

<div class="grid4">
  <div class="gcard"><div class="num">01 · NEED</div><h4>需要性</h4><p>这事现在<b>有多严重</b>？</p></div>
  <div class="gcard"><div class="num">02 · INHERENCY</div><h4>根属性</h4><p>为什么<b>现在解决不了</b>？</p></div>
  <div class="gcard"><div class="num">03 · SOLVENCY</div><h4>解决力</h4><p>方案能不能<b>真的解决</b>？</p></div>
  <div class="gcard"><div class="num">04 · COST-BENEFIT</div><h4>损益</h4><p>做了之后<b>划不划算</b>？</p></div>
</div>

<div class="callout">
  <div class="qmark">"</div>
  <h3>这套逻辑，我一步步带你拆</h3>
  <p>纯正统政策辩的攻防都从这四点展开——搞懂结构，你就知道该往哪打、该守哪里。</p>
</div>
'''

# ---------------- CARD 4 : 政治辩+国际局势 ----------------
CARD4_BODY = '''
<div class="panel plain">
  <div class="tag-label">不是背时事就够了</div>
  <p class="copy" style="margin-top:14px;">
    政治辩＋国际局势，不是背时事就够了，是要讲清楚<b>"这件事背后到底是什么政治逻辑在运作"</b>。
  </p>
</div>

<div class="compare">
  <div class="cbox no"><div class="mark">✕ 单纯背资料</div><p>堆时事、堆数据，讲不出背后的因果和立场</p></div>
  <div class="cbox yes"><div class="mark">✓ 讲清楚政治逻辑</div><p>把复杂时政讲成人话，逻辑站得住</p></div>
</div>

<div class="callout">
  <div class="qmark">"</div>
  <h3>找到一个讲得清、站得住的立场</h3>
  <p>我会带你把复杂的时政资料讲成人话，还有怎么在国际议题里，找到一个自己讲得清、站得住的立场。</p>
</div>
'''

CARDS = [
    dict(name="story1", icon="mic", kicker="DEBATE COACHING · 山竹", title="辩论私教 招生中",
         subtitle="DEBATE COACHING", body=CARD1_BODY, idx="01"),
    dict(name="story2", icon="spiral", kicker="PHILOSOPHICAL DEBATE", title="哲理辩 专项",
         subtitle="PHILOSOPHICAL DEBATE", body=CARD2_BODY, idx="02"),
    dict(name="story3", icon="grid", kicker="POLICY DEBATE", title="奥瑞冈政策辩 专项",
         subtitle="POLICY DEBATE · 纯正统政策辩", body=CARD3_BODY, idx="03"),
    dict(name="story4", icon="globe", kicker="POLITICAL & INTERNATIONAL AFFAIRS", title="政治辩＋国际局势 专项",
         subtitle="POLITICAL & INTERNATIONAL AFFAIRS", body=CARD4_BODY, idx="04"),
]

def build_html(card, variant):
    body_class = "carousel" if variant == "carousel" else "story"
    html = f'''<!doctype html>
<html><head><meta charset="utf-8"/>
<style>{CSS}</style>
</head>
<body class="{body_class}">
{page(card["icon"], card["kicker"], card["title"], card["subtitle"], card["body"], card["idx"])}
</body></html>'''
    return html

for variant, subdir in [("story", "story"), ("carousel", "carousel")]:
    for card in CARDS:
        html = build_html(card, variant)
        out_path = os.path.join(ROOT, subdir, f'{card["name"].replace("story", variant)}.html')
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", out_path)
