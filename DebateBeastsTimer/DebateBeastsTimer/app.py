import streamlit as st
import time
import base64
import os
import platform
import subprocess
import wave
import math
import struct

st.set_page_config(page_title="Debate Beasts Timer", layout="wide")

# =========================
# 0. 文件路径
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BATTLE_BG_CANDIDATES = [
    "timer_bg.jpeg",
    "timer_bg.jpg",
    "background.jpeg",
    "background.jpg",
]

SELECTION_BG_CANDIDATES = [
    "selection_bg.jpeg",
    "selection_bg.jpg",
    "selection_background.jpeg",
    "selection_background.jpg",
]

BEEP_FILE = os.path.join(BASE_DIR, "debate_beast_beeeee.wav")


def find_file(candidates):
    for filename in candidates:
        path = os.path.join(BASE_DIR, filename)
        if os.path.exists(path):
            return path
    return None


BATTLE_BG_PATH = find_file(BATTLE_BG_CANDIDATES)
SELECTION_BG_PATH = find_file(SELECTION_BG_CANDIDATES)

# =========================
# 1. 赛制规则
# =========================

def clash_rounds(total_segments):
    return [
        ("Beast Clash", "正方" if i % 2 == 0 else "反方", 15)
        for i in range(total_segments)
    ]


RULES = {
    # 海选顺序：1 → 4 → 2 → 5 → 3 → 6
    # 1、2、3 为正方；4、5、6 为反方
    "哲理圈海选": [
        ("个人陈词", "1号 正方", 40),
        ("个人陈词", "4号 反方", 40),
        ("个人陈词", "2号 正方", 40),
        ("个人陈词", "5号 反方", 40),
        ("个人陈词", "3号 正方", 40),
        ("个人陈词", "6号 反方", 40),
    ],

    "政治圈海选": [
        ("个人陈词", "1号 正方", 55),
        ("个人陈词", "4号 反方", 55),
        ("个人陈词", "2号 正方", 55),
        ("个人陈词", "5号 反方", 55),
        ("个人陈词", "3号 正方", 55),
        ("个人陈词", "6号 反方", 55),
    ],

    "圈内 TOP32 → TOP4": [
        ("正方立论", "正方", 50),
        ("反方立论", "反方", 50),
        *clash_rounds(4),
        ("反方总结", "反方", 40),
        ("正方总结", "正方", 40),
    ],

    "总 TOP8 → TOP4": [
        ("正方立论", "正方", 60),
        ("反方立论", "反方", 60),
        *clash_rounds(6),
        ("反方总结", "反方", 45),
        ("正方总结", "正方", 45),
    ],

    "半决赛": [
        ("正方立论", "正方", 60),
        ("反方立论", "反方", 60),
        *clash_rounds(16),
        ("反方总结", "反方", 60),
        ("正方总结", "正方", 60),
    ],

    "总决赛": [
        ("正方立论", "正方", 120),
        ("反方立论", "反方", 120),
        *clash_rounds(24),
        ("反方总结", "反方", 60),
        ("正方总结", "正方", 60),
    ],
}

# =========================
# 2. 提示音：一声 beeeee
# =========================

def create_loud_beep():
    sample_rate = 44100
    amplitude = 32000
    freq = 1050
    duration = 0.75

    frames = []
    total_samples = int(sample_rate * duration)
    fade_samples = int(sample_rate * 0.025)

    for i in range(total_samples):
        volume = 1.0

        if i < fade_samples:
            volume = i / fade_samples
        elif i > total_samples - fade_samples:
            volume = max((total_samples - i) / fade_samples, 0)

        value = int(amplitude * volume * math.sin(2 * math.pi * freq * i / sample_rate))
        frames.append(struct.pack("<h", value))

    with wave.open(BEEP_FILE, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))


def play_sound():
    create_loud_beep()
    system = platform.system()

    try:
        if system == "Darwin":
            subprocess.Popen(
                ["afplay", "-v", "25", BEEP_FILE],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        elif system == "Windows":
            import winsound
            winsound.PlaySound(BEEP_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            subprocess.Popen(
                ["aplay", BEEP_FILE],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    except Exception:
        pass

# =========================
# 3. 背景图
# =========================

def image_to_base64(path):
    if path is None or not os.path.exists(path):
        return ""

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =========================
# 4. 状态初始化
# =========================

DEFAULT_MODE = "哲理圈海选"


def reset_whole_match(mode):
    st.session_state.mode = mode
    st.session_state.mode_selector = mode
    st.session_state.step = 0
    st.session_state.remaining = RULES[mode][0][2]
    st.session_state.running = False


if "mode" not in st.session_state:
    reset_whole_match(DEFAULT_MODE)

# =========================
# 5. 工具函数
# =========================

def rules():
    return RULES[st.session_state.mode]


def current():
    return rules()[st.session_state.step]


def is_selection_mode():
    return "海选" in st.session_state.mode


def current_bg_path():
    if is_selection_mode() and SELECTION_BG_PATH is not None:
        return SELECTION_BG_PATH
    return BATTLE_BG_PATH


def current_background_css():
    bg = image_to_base64(current_bg_path())

    if bg:
        return f"""
            background-image:
                linear-gradient(rgba(0,0,0,0.03), rgba(0,0,0,0.03)),
                url("data:image/jpeg;base64,{bg}");
        """

    return """
        background:
            radial-gradient(circle at top left, rgba(122,31,22,0.40), transparent 30%),
            radial-gradient(circle at bottom right, rgba(88,55,140,0.35), transparent 35%),
            linear-gradient(135deg, #050505, #260909);
    """


def change_mode():
    reset_whole_match(st.session_state.mode_selector)


def start_timer():
    st.session_state.running = True


def pause_timer():
    st.session_state.running = False


def next_step():
    st.session_state.running = False

    if st.session_state.step < len(rules()) - 1:
        st.session_state.step += 1
        st.session_state.remaining = rules()[st.session_state.step][2]


def previous_step():
    st.session_state.running = False

    if st.session_state.step > 0:
        st.session_state.step -= 1
        st.session_state.remaining = rules()[st.session_state.step][2]


def reset_current_step():
    st.session_state.running = False
    st.session_state.remaining = current()[2]


def go_first_step():
    reset_whole_match(st.session_state.mode)


def test_sound():
    play_sound()


def round_text():
    phase, speaker, duration = current()

    if is_selection_mode():
        return f"发言顺序 {st.session_state.step + 1} / {len(rules())}"

    if phase != "Beast Clash":
        return f"环节 {st.session_state.step + 1} / {len(rules())}"

    clash_indices = [i for i, r in enumerate(rules()) if r[0] == "Beast Clash"]
    now = clash_indices.index(st.session_state.step) + 1
    total = len(clash_indices)
    return f"Clash {now} / {total}"


def auto_advance():
    phase, speaker, duration = current()

    # 海选 / 立论 / 总结：时间到就停，手动下一环节
    if phase != "Beast Clash":
        st.session_state.remaining = 0
        st.session_state.running = False
        play_sound()
        return

    # Beast Clash 内部自动切换
    if st.session_state.step < len(rules()) - 1:
        next_phase = rules()[st.session_state.step + 1][0]

        if next_phase == "Beast Clash":
            st.session_state.step += 1
            st.session_state.remaining = rules()[st.session_state.step][2]
            st.session_state.running = True
            play_sound()
            return

    # Beast Clash 结束，停住，手动进总结
    st.session_state.remaining = 0
    st.session_state.running = False
    play_sound()

# =========================
# 6. CSS：背景和文字绑定到同一个 scene
# =========================

BACKGROUND_CSS = current_background_css()

st.markdown(f"""
<style>
[data-testid="stHeader"] {{
    display: none !important;
}}

[data-testid="stToolbar"] {{
    display: none !important;
}}

#MainMenu {{
    visibility: hidden !important;
}}

footer {{
    visibility: hidden !important;
}}

html, body {{
    background: #050505 !important;
    overflow: hidden !important;
    height: 100% !important;
}}

.stApp {{
    background: #050505 !important;
    overflow: hidden !important;
    height: 100vh !important;
}}

[data-testid="stAppViewContainer"] {{
    overflow: hidden !important;
    height: 100vh !important;
}}

main {{
    overflow: hidden !important;
    height: 100vh !important;
}}

* {{
    font-family:
        "Source Han Sans SC",
        "Noto Sans CJK SC",
        "PingFang SC",
        "Microsoft YaHei",
        Arial,
        sans-serif !important;
}}

.block-container {{
    padding: 0 !important;
    margin: 0 !important;
    max-width: none !important;
}}

/* 可见区域：底部留给按钮 */
.viewport {{
    position: fixed;
    left: 0;
    top: 0;
    width: 100vw;
    height: calc(100vh - 86px);
    overflow: hidden;
    background: #050505;
}}

/*
核心：
scene 永远保持 1672:941 比例。
背景和文字都在 scene 里面。
scene 整体铺满 viewport，所以文字不会和背景错位。
*/
.scene {{
    position: absolute;
    left: 50%;
    top: 50%;
    width: max(100vw, calc((100vh - 86px) * 1672 / 941));
    aspect-ratio: 1672 / 941;
    transform: translate(-50%, -50%);
    transform-origin: center center;
    {BACKGROUND_CSS}
    background-size: 100% 100%;
    background-position: center center;
    background-repeat: no-repeat;
    overflow: hidden;
    container-type: inline-size;
}}

/* 顶部标题：压进上方长框内，居中，不顶边 */
/* 顶部标题：严格压在上方长框内 */
/* 顶部标题：保持大，但往框内压 */
.top-title {{
    position: absolute;
    left: 21%;
    top: 17.3%;
    width: 58%;
    height: 6%;
    text-align: center;
    font-size: 2.35cqw;
    font-weight: 900;
    color: white;
    text-shadow:
        0 0 10px rgba(255,255,255,0.95),
        0 0 18px rgba(255,70,50,1);
    white-space: nowrap;
    line-height: 1.05;
}}

.top-round {{
    position: absolute;
    left: 38%;
    top: 22.4%;
    width: 24%;
    height: 4%;
    text-align: center;
    font-size: 1.75cqw;
    font-weight: 900;
    color: #f7d7a1;
    text-shadow: 0 0 14px rgba(255,180,80,0.95);
    line-height: 1.05;
}}

/* 左右框：不缩小字体，只把内容放回框内中心 */
.panel {{
    position: absolute;
    width: 33.0%;
    height: 36.5%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    transform: scale(1.47);
    transform-origin: center center;
}}

/* 左框安全区 */
.left-panel {{
    left: 13.2%;
    top: 40.0%;
}}

/* 右框安全区 */
.right-panel {{
    left: 55.0%;
    top: 40.5%;
}}

.name-active {{
    font-size: 4.55cqw;
    font-weight: 900;
    color: white;
    text-shadow:
        0 0 14px rgba(255,255,255,1),
        0 0 26px rgba(255,255,255,0.75);
    line-height: 0.95;
    margin-bottom: 0.45%;
}}

.name-waiting {{
    font-size: 3.65cqw;
    font-weight: 900;
    color: rgba(255,255,255,0.20);
    line-height: 0.95;
    margin-bottom: 1.5%;
}}

.status-active {{
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 0.48cqw;
    font-size: 1.95cqw;
    font-weight: 900;
    color: #ffcf74;
    text-shadow: 0 0 16px rgba(255,120,50,1);
    margin-bottom: 0.05%;
    white-space: nowrap;
}}

.fire-emoji {{
    font-family:
        "Apple Color Emoji",
        "Segoe UI Emoji",
        "Noto Color Emoji",
        sans-serif !important;
    font-size: 1.95cqw;
    line-height: 1;
}}

.speaking-word {{
    font-family: "Times New Roman", serif !important;
    font-weight: 900;
    letter-spacing: 0.09em;
    white-space: nowrap;
}}

.status-waiting {{
    font-size: 1.45cqw;
    font-weight: 900;
    color: rgba(255,255,255,0.14);
    font-family: "Times New Roman", serif !important;
    letter-spacing: 0.07em;
}}

/* 时间：高度保持大，只横向轻微压缩，视觉仍然很猛 */
.time {{
    font-size: 11.2cqw;
    font-weight: 900;
    color: white;
    line-height: 0.82;
    transform: scaleX(0.88);
    transform-origin: center center;
    text-shadow:
        0 0 18px rgba(255,255,255,1),
        0 0 38px rgba(255,80,40,0.92),
        0 0 58px rgba(255,80,40,0.55);
    font-family: "Times New Roman", serif !important;
}}
    
/* 海选模式：中间单框，字号保持大，只横向压缩时间 */
.solo-panel {{
    position: absolute;
    left: 29.5%;
    top: 40.4%;
    width: 41.0%;
    height: 37.0%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    transform: scale(1.58);
    transform-origin: center center;
}}

.solo-name {{
    font-size: 4.45cqw;
    font-weight: 900;
    color: white;
    text-shadow:
        0 0 14px rgba(255,255,255,1),
        0 0 26px rgba(255,255,255,0.75);
    line-height: 0.95;
    margin-bottom: 0.55%;
}}

.solo-time {{
    font-size: 11.8cqw;
    font-weight: 900;
    color: white;
    line-height: 0.82;
    transform: scaleX(0.88);
    transform-origin: center center;
    text-shadow:
        0 0 18px rgba(255,255,255,1),
        0 0 38px rgba(255,80,40,0.92),
        0 0 58px rgba(255,80,40,0.55);
    font-family: "Times New Roman", serif !important;
}}

/* 固定底部按钮 */
.st-key-control_bar {{
    position: fixed !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    z-index: 999999 !important;
    background: rgba(5, 5, 5, 0.97) !important;
    padding: 10px 12px 10px 12px !important;
    border-top: 1px solid rgba(255,255,255,0.12);
}}

.st-key-control_bar div.stButton > button {{
    font-size: 16px;
    font-weight: 800;
    border-radius: 12px;
    height: 46px;
}}

.st-key-control_bar .stSelectbox label {{
    color: white !important;
    font-weight: 800 !important;
}}

.st-key-control_bar [data-baseweb="select"] {{
    font-size: 16px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# 7. 主舞台
# =========================

phase, speaker, duration = current()
m = st.session_state.remaining // 60
s = st.session_state.remaining % 60
time_text = f"{m:02d}:{s:02d}"

if is_selection_mode():
    main_html = f"""
    <div class="solo-panel">
        <div class="solo-name">{speaker}</div>
        <div class="status-active">
            <span class="fire-emoji">🔥</span>
            <span class="speaking-word">SPEAKING</span>
        </div>
        <div class="solo-time">{time_text}</div>
    </div>
    """

elif speaker == "正方":
    main_html = f"""
    <div class="panel left-panel">
        <div class="name-active">正方</div>
        <div class="status-active">
            <span class="fire-emoji">🔥</span>
            <span class="speaking-word">SPEAKING</span>
        </div>
        <div class="time">{time_text}</div>
    </div>

    <div class="panel right-panel">
        <div class="name-waiting">反方</div>
        <div class="status-waiting">WAITING</div>
    </div>
    """

else:
    main_html = f"""
    <div class="panel left-panel">
        <div class="name-waiting">正方</div>
        <div class="status-waiting">WAITING</div>
    </div>

    <div class="panel right-panel">
        <div class="name-active">反方</div>
        <div class="status-active">
            <span class="fire-emoji">🔥</span>
            <span class="speaking-word">SPEAKING</span>
        </div>
        <div class="time">{time_text}</div>
    </div>
    """

st.markdown(
    f"""
    <div class="viewport">
        <div class="scene">
            <div class="top-title">{st.session_state.mode} ｜ {phase}</div>
            <div class="top-round">{round_text()}</div>
            {main_html}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 8. 固定底部控制区
# =========================

with st.container(key="control_bar"):
    mode_col, c1, c2, c3, c4, c5, c6, c7 = st.columns([2.2, 1, 1, 1, 1, 1.3, 1, 1])

    with mode_col:
        st.selectbox(
            "选择赛制",
            list(RULES.keys()),
            key="mode_selector",
            on_change=change_mode,
            label_visibility="collapsed"
        )

    with c1:
        st.button("开始", use_container_width=True, on_click=start_timer)

    with c2:
        st.button("暂停", use_container_width=True, on_click=pause_timer)

    with c3:
        st.button("下一环节", use_container_width=True, on_click=next_step)

    with c4:
        st.button("上一环节", use_container_width=True, on_click=previous_step)

    with c5:
        st.button("重置当前环节", use_container_width=True, on_click=reset_current_step)

    with c6:
        st.button("第一环节", use_container_width=True, on_click=go_first_step)

    with c7:
        st.button("测试音量", use_container_width=True, on_click=test_sound)

# =========================
# 9. 倒计时
# =========================

if st.session_state.running:
    time.sleep(1)

    if st.session_state.remaining > 1:
        st.session_state.remaining -= 1
    else:
        auto_advance()

    st.rerun()