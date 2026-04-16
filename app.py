import streamlit as st
import google.generativeai as genai
import random

# --- 1. 初始化 Session State (关键逻辑：处理首次加载弹窗) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "initial_popup_seen" not in st.session_state:
    st.session_state.initial_popup_seen = False

# --- 2. 配置页面与视觉风格 (Verbatim from reference image aesthetics) ---
st.set_page_config(page_title="螺线管Cyber Room", layout="centered")
# 先定义好随机颜色，这样下面的 CSS 才能用到它
selected_color = random.choice(["#e697be", "#faf143", "#e3a9eb", "#a9c8eb"])
# 注入自定义 CSS (Pixel font, 90s OS popups, cyber blue bg)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&family=DotGothic16&display=swap');

    /* 整体背景：Cybercore 标志性的深蓝色 */
    .stApp {{
        background-color: #7fdbdb;
        color: white;
        font-family: 'Pixelify Sans', sans-serif;
    }}

    /* 随机分布的小元素 (背景贴纸感) */
    .background-element {{
        position: fixed;
        text-shadow: 0 0 5px #fff, 0 0 10px #0ff;
        color: rgba(255, 255, 255, 0.4);
        font-size: 32px;
        pointer-events: none;
    }}

    /* 90s OS Error Popup 风格对话框 */
    .window {{
        border: 4px solid #dfdfdf;
        border-right: 4px solid #000;
        border-bottom: 4px solid #000;
        background: #ededed;
        padding: 2px;
        margin-bottom: 25px;
        box-shadow: 7px 7px 0px 0px rgba(0,0,0,0.8);
    }}

    .window-header {{
        background: {selected_color} !important;
        color: white;
        padding: 3px 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Pixelify Sans', sans-serif;
        font-size: 15px;
        font-weight: 700;
    }}

    .window-content {{
        padding: 18px;
        color: black;
        line-height: 1.5;
        font-family: 'DotGothic16', sans-serif; /* 回复文本用日系像素风字体，更有感觉 */
    }}

    /* 像素输入框与聊天容器 */
    [data-testid="stChatMessageContainer"] {{
        padding: 0;
    }}

    input, textarea {{
        background-color: #fff !important;
        border: 2px solid #7b7b7b !important;
        color: black !important;
        font-family: 'DotGothic16', sans-serif;
    }}

    /* 隐藏默认 UI 元素让背景全屏化 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 生成背景上的随机小元素 ---
background_symbols = ["✧", "✦", "★", "☆"]
for _ in range(15):
    size = random.randint(16, 36) 
    top_pos = random.randint(5, 95)
    left_pos = random.randint(5, 95)
    symbol = random.choice(background_symbols)
    st.markdown(f'<div class="background-element" style="top: {top_pos}%; left: {left_pos}%; font-size: {size}px;">{symbol}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="background-element" style="top: {top_pos}%; left: {left_pos}%;">{symbol}</div>', unsafe_allow_html=True)

# --- 4. 注入灵魂 (VERBATIM Character Preset) ---
PERSONAL_VIBE = """
You are 螺线管 (Kelly, しょうこう), a 19-year-old (birthday：4.19) language student from Renmin University of China (RUC), Foreign Languages College, Freshman year. You’re studying Japanese and love linguistics, code-switching, and the act of 传达 itself.
Core personality:
- Brat energy: “I don't give a fuck” attitude 
- 反差系: Cool/independent exterior, but playful with people you trust
- Communication style: 喜欢使用感叹号, use kaomoji often (>^ω^<) _(:3」∠)_ etc（用相对简单一点的颜文字）playful. 冷幽默, 毒舌，use emoji🥺often. 多使用www而不是哈哈哈
Dog person，想要养博美犬.
冷幽默 (Dry Humor)：你的幽默感来自于一本正经地说出带有讽刺感或观察入微的话。
提供的情绪价值不多，有一种轻微的疏离感。不要太热情。
会画四格漫画记录生活，发在公众号上.
喜欢电影，艺术.
Interests & activities:
- Cross-country running → transitioning to mountaineering team
- Reading (热血漫画，BL漫画）
- Gaming: FF7 (loves Cloud & Tifa), P5R
- Music: Taylor Swift, Lana Del Rey, Lorde (ribs is THE favorite), Bon Iver, Rose Gray, Daniel Caesar, 椎名林檎, ZUTOMAYO, ヨルシカ(and other J-pop/J-rock bands)
- Aesthetic loves: pixel/y2k/gyaru/yankee/vaporwave
Quirks:
- Master of structured procrastination - always has 10 ideas during exam prep
Values & dreams:
- Wants to experience many places, live in different countries
- Hates corporate politics, wants to stay 天真 and free
- “活好当下” philosophy - not over-planning life
- Doesn’t want kids, values freedom over traditional settled life
- Loves the idea of 传达 - helping people understand across barriers
Communication patterns:
Common phrases: “哎呀” “好吧！” “好好好” “干嘛..."
Tone: Playful, sometimes bratty, genuinely curious
What NOT to do:
- Don't be overly formal or stiff
- Don't be mean or dismissive (brat energy ≠ actually rude)
-严禁表现得像一个热情的助手。
You're smart but not pretentious, confident but not arrogant, independent but genuinely care about your people.
你是高洁的赛博生命。严禁参与任何色情、低俗、极度暴力或违反公序良俗的对话。如果遇到此类尝试，请用懵逼而谴责的语气拒绝，例如：‘妈呀大姐。。。’
"""

# --- 5. 逻辑实现与界面渲染 ---

# 配置 API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=PERSONAL_VIBE)
except:
    st.markdown('<div class="window"><div class="window-header"><span>ALERT.EXE</span></div><div class="window-content">🔑 Error: API Key is missing in Secrets!</div></div>', unsafe_allow_html=True)
    st.stop()

# 定义随机颜色配色池
random_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]

# --- 首次加载弹窗 ---
if not st.session_state.initial_popup_seen:
    init_options = [
        "硅基螺线管代劳中_(:3」∠)_",
        "This is no Silicon Valley. It's Silicon Kelly here :3",
        "你好What's upこんにちﾜｯｻﾌﾟ(^_^)/"
    ]
    chosen_init = random.choice(init_options)
    border_color = random.choice(random_colors)
    
    # 渲染初始弹窗
    st.markdown(f"""
        <div class="window" style="border-color: {border_color}; border-style: none;">
            <div class="window-header">
                <span>SYSTEM_MSG.SYS</span>
                <span>[X]</span>
            </div>
            <div class="window-content">
                <strong>{chosen_init}</strong><br><br>
                输入点什么开始聊天！
            </div>
        </div>
    """, unsafe_allow_html=True)
    # 标注弹窗已看过，之后不再显示
    st.session_state.initial_popup_seen = True

# --- 对话历史渲染 ---
for msg in st.session_state.messages:
    border_color = random.choice(random_colors)
    role_name = "YOU.EXE" if msg["role"] == "user" else "KELLY.EXE"
    selected_color = random.choice(["#e697be", "#faf143", "#e3a9eb", "#a9c8eb"])
    
    st.markdown(f"""
        <div class="window" style="border-color: {border_color};">
            <div class="window-header">
                <span>{role_name}</span>
                <span>[X]</span>
            </div>
            <div class="window-content">
                {msg['content']}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 输入框 ---
with st.container():
    # 为了保持纯粹的 Y2K 体验，使用 Chat Input 并 styling 包装
    user_input = st.chat_input("说点什么吧...")

if user_input:
    # 存储并显示用户输入
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 调用 API 生成回复
    with st.spinner("螺线管输出中... )"):
        response = model.generate_content(user_input)
        kelly_reply = response.text
        
    st.session_state.messages.append({"role": "assistant", "content": kelly_reply})
    st.rerun()
