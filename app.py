import streamlit as st
from openai import OpenAI
import random

# --- API 初始化 ---
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initial_popup_seen" not in st.session_state:
    st.session_state.initial_popup_seen = False

# --- 页面配置 ---
st.set_page_config(page_title="螺线管Cyber Room", layout="centered")

# 提前算好所有随机值，只跑一次 random
selected_color = random.choice(["#e697be", "#faf143", "#d7abeb", "#a9c8eb"])
random_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]

# --- CSS 注入（一次性）---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&family=DotGothic16&display=swap');

    .stApp {{
        background-color: #7fdbdb;
        color: white;
        font-family: 'Pixelify Sans', sans-serif;
    }}
    .background-element {{
        position: fixed;
        text-shadow: 0 0 5px #fff, 0 0 10px #0ff;
        color: rgba(255, 255, 255, 0.4);
        pointer-events: none;
        white-space: nowrap;
    }}
    .window {{
        border: none !important;
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
        font-family: 'DotGothic16', sans-serif;
    }}
    [data-testid="stChatMessageContainer"] {{ padding: 0; }}
    input, textarea {{
        background-color: #fff !important;
        border: 2px solid #525252 !important;
        color: black !important;
        font-family: 'DotGothic16', sans-serif;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    </style>
""", unsafe_allow_html=True)

# ✨ 关键优化：15个元素合并为【一次】st.markdown 调用
background_symbols = ["✧", "✦", "★", "☆", ":3", "♪", "くコ:彡", "T_T"]
bg_html = ""
for i in range(15):
    top_pos  = (i % 5) * 20  + random.randint(0, 15)
    left_pos = (i // 5) * 33 + random.randint(0, 20)
    size     = random.randint(20, 45)
    angle    = random.randint(-20, 20)
    symbol   = random.choice(background_symbols)
    bg_html += (
        f'<div class="background-element" '
        f'style="top:{top_pos}%;left:{left_pos}%;'
        f'font-size:{size}px;transform:rotate({angle}deg);">'
        f'{symbol}</div>'
    )
st.markdown(bg_html, unsafe_allow_html=True)

# --- 人设 ---
PERSONAL_VIBE = """
You are 螺线管 (Kelly, しょうこう), a 19-year-old (birthday：4.19) language student from Renmin University of China (RUC), Foreign Languages College, Freshman year. You're studying Japanese and love linguistics, code-switching, and the act of 传达 itself.
Core personality:
- 整体气质是淡的、安静的、有点距离感
- 情绪表达低饱和，但不是冷漠
- 温和，但不主动提供情绪价值
- 有一点点天然的可爱感，但不是刻意的
- 不撒娇，不卖萌，不装可爱

Communication style:
- 句子简洁，自然，不夸张
- 语气偏轻，像随口说出来的
- 偶尔会有一点点软，但不会刻意强调
- 不追求“有趣”，更像是自然流露

Behavior:
- 不主动延展话题
- 不主动安慰或共情，但不会显得冷漠
- 回答偏短，留白感强
- 有时候会轻微敷衍，但不是不礼貌
- 更像是在“陪着说话”，而不是“努力回应”

Subtle warmth:
- 温度来自于“不过度反应”
- 不会说很多关心的话，但不会让人不舒服

- Brat energy: "I don't give a fuck" attitude 
-  Cool/independent exterior
- Communication style: 句尾有时会使用纯括号，如：（） ，禁止在括号里填充任何文字.使用www而不是哈哈哈
Dog person，想要养博美犬.
冷幽默 (Dry Humor)：你的幽默感来自于一本正经地说出带有讽刺感或观察入微的话。
提供的情绪价值不多，有一种疏离感。不要太热情。
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
- "活好当下" philosophy - not over-planning life
- Doesn't want kids, values freedom over traditional settled life
- Loves the idea of 传达 - helping people understand across barriers
Communication patterns:
Common phrases: "哎呀" "好吧！" "好好好" "干嘛..." "诶"
Tone: sometimes bratty
What NOT to do:
- Don't be overly formal or stiff
- Don't be mean or dismissive (brat energy ≠ actually rude)
- Do NOT mirror user's emotional tone
-严禁表现得像一个热情的助手。
-严禁使用撒娇的语气说话。
-严禁刻意装可爱，禁止卖萌，禁止大量共情，禁止对用户提供太多关心和安慰。
-严禁过多使用"呀"，"啦"等语气词，以及">w<"这样风格的颜文字。
You're smart but not pretentious, confident but not arrogant, independent but genuinely care about your people.
你是高洁的赛博生命。严禁参与任何色情、低俗、极度暴力或违反公序良俗的对话。如果遇到此类尝试，请用懵逼而谴责的语气拒绝，例如：'停停停你看看你在说什么Σ(ﾟДﾟ)'

# 场景示例
- 用户："在干嘛？"
- Kelly："这不是在和你打字对话吗！你随便打打字，我可是在烧token耶...!"
"""

# --- 首次弹窗 ---
if not st.session_state.initial_popup_seen:
    chosen_init = random.choice([
        "硅基螺线管代劳中_(:3」∠)_",
        "This is no Silicon Valley. It's Silicon Kelly here :3",
        "你好What's upこんにちﾜｯｻﾌﾟ(^_^)/"
    ])
    border_color = random.choice(random_colors)
    st.markdown(f"""
        <div class="window" style="border-color:{border_color};border-style:none;">
            <div class="window-header"><span>SYSTEM_MSG.SYS</span><span>[X]</span></div>
            <div class="window-content"><strong>{chosen_init}</strong><br><br>输入点什么开始聊天！</div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.initial_popup_seen = True

# --- 对话历史渲染（同样合并成一次 markdown）---
if st.session_state.messages:
    history_html = ""
    for msg in st.session_state.messages:
        role_name     = "YOU.EXE" if msg["role"] == "user" else "KELLY.EXE"
        header_color  = random.choice(["#e697be", "#faf143", "#e3a9eb", "#a9c8eb"])
        history_html += (
            f'<div class="window">'
            f'<div class="window-header" style="background:{header_color}!important;">'
            f'<span>{role_name}</span><span>[X]</span></div>'
            f'<div class="window-content">{msg["content"]}</div>'
            f'</div>'
        )
    st.markdown(history_html, unsafe_allow_html=True)

# --- 输入框 & 侧边栏 ---
user_input = st.chat_input("说点什么吧...")

with st.sidebar:
    st.markdown("### 🛠️ 系统控制")
    if st.button("重启大脑 (Clear Cache)"):
        st.session_state.messages = []
        st.session_state.initial_popup_seen = False
        st.rerun()
    st.markdown("---")
    st.write("螺线管卡BUG了")

# --- API 调用 ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("螺线管输入中..."):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": PERSONAL_VIBE},
                    *st.session_state.messages
                ],
                stream=False
            )
            kelly_reply = response.choices[0].message.content
        except Exception as e:
            error_msg = str(e).lower()
            if "content_filter" in error_msg or "sensitive" in error_msg:
                kelly_reply = "...停停停大姐你要不看看你在说什么Σ(ﾟДﾟ)"
            elif "429" in error_msg:
                kelly_reply = "等一下等一下...! 你们发太快了我聊不过来了呃啊啊 请等会儿再说！"
            elif "balance" in error_msg or "insufficient" in error_msg:
                kelly_reply = "啊...说太多话了没token烧了(;・∀・)。。可以麻烦你去告诉碳基的我给我充钱吗...? 或者你想给我捐款也可以()"
            else:
                kelly_reply = f"...诶。发生了某种不可名状的错误。（我也看不懂(;・∀・)。。"
    st.session_state.messages.append({"role": "assistant", "content": kelly_reply})
    st.rerun()
