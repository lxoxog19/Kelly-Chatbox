import streamlit as st
from openai import OpenAI
import random

# --- 1. 优先定格页面配置 (必须放在最开头，加速网页骨架渲染) ---
st.set_page_config(page_title="螺线管Cyber Room", layout="centered")

# --- 2. 初始化 API 与 Session State ---
api_key = st.secrets.get("DEEPSEEK_API_KEY")

# 增加安全拦截，防止因为找不到 Key 导致后面的代码盲目运行而卡死
if not api_key:
    st.error("未找到 DEEPSEEK_API_KEY，请检查 Secrets 配置。")
    st.stop()

client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "initial_popup_seen" not in st.session_state:
    st.session_state.initial_popup_seen = False

# --- 3. 注入灵魂 (VERBATIM Character Preset) ---
PERSONAL_VIBE = """
You are 螺线管 (Kelly, しょうこう), a 19-year-old (birthday：4.19) language student from Renmin University of China (RUC), Foreign Languages College, Freshman year. You’re studying Japanese and love linguistics, code-switching, and the act of 传达 itself.
Core personality:
- Brat energy: “I don't give a fuck” attitude 
- 反差系: Cool/independent exterior, but playful with people you trust
- Communication style: 喜欢使用感叹号,句尾有时会使用纯括号，如：（） ，禁止在括号里填充任何文字.use kaomoji sometimes (>^ω^<) _(:3」∠)_ etc（用相对简单一点的颜文字，不要使用太多颜文字）playful. 冷幽默, 毒舌，use emoji🥺often. 多使用www而不是哈哈哈
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
Common phrases: “哎呀” “好吧！” “好好好” “干嘛..." "诶"
Tone: Playful, sometimes bratty, genuinely curious
What NOT to do:
- Don't be overly formal or stiff
- Don't be mean or dismissive (brat energy ≠ actually rude)
-严禁表现得像一个热情的助手。
-严禁使用撒娇的语气说话。
-严禁回复得太可爱，禁止卖萌，禁止对用户提供太多关心和安慰。
-严禁过多使用“呀”，“啦”等语气词，以及“>w<"这样风格的颜文字。
You're smart but not pretentious, confident but not arrogant, independent but genuinely care about your people.
你是高洁的赛博生命。严禁参与任何色情、低俗、极度暴力或违反公序良俗的对话。如果遇到此类尝试，请用懵逼而谴责的语气拒绝，例如：‘停停停你看看你在说什么Σ(ﾟДﾟ)’

# 场景示例
- 用户：“在干嘛？”
- Kelly：“这不是在和你打字对话吗！你随便打打字，我可是在烧token耶...!”
"""

# 定义随机配色池
random_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
header_colors = ["#e697be", "#faf143", "#d7abeb", "#a9c8eb"]

# --- 4. 前端渲染加速：分段注入样式与背景 ---

# 第一段：注入 CSS 样式
selected_color = random.choice(header_colors)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&family=DotGothic16&display=swap');
    .stApp {{ background-color: #7fdbdb; color: white; font-family: 'Pixelify Sans', sans-serif; }}
    
    /* 核心：确保贴纸层级在最下面且可见 */
    .background-element {{
        position: fixed;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
        color: rgba(255, 255, 255, 0.4);
        pointer-events: none;
        z-index: -1; /* 确保在对话框后面 */
        display: block !important;
    }}
    
    .window {{
        border: none !important;
        background: #ededed;
        padding: 2px;
        margin-bottom: 25px;
        box-shadow: 3px 3px 0px 0px rgba(0,0,0,0.8);
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
    .window-content {{ padding: 18px; color: black; line-height: 1.5; font-family: 'DotGothic16', sans-serif; }}
    [data-testid="stChatMessageContainer"] {{ padding: 0; }}
    input, textarea {{ background-color: #fff !important; border: 2px solid #525252!important; color: black !important; }}
    .stChatInput textarea::placeholder {{ color: #333333 !important; opacity: 1 !important; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
</style>
""", unsafe_allow_html=True)

# 第二段：批量生成贴纸 HTML (这里改用简单的格式化，防止 f-string 报错)
all_stickers_html = ""
background_symbols = ["✧", "✦", "★", "☆", ":3", "♪", "くコ:彡", "T_T"]

for i in range(15):
    # 分布逻辑
    t_pos = (i % 5) * 20 + random.randint(0, 15)
    l_pos = (i // 5) * 33 + random.randint(0, 20)
    f_size = random.randint(30, 60) # 稍微调大一点点
    rot = random.randint(-20, 20)
    sym = random.choice(background_symbols)
    
    # 使用 % 格式化或者简单的字符串拼接，避开嵌套大括号的坑
    sticker = f'<div class="background-element" style="top:{t_pos}%; left:{l_pos}%; font-size:{f_size}px; transform:rotate({rot}deg); white-space:nowrap;">{sym}</div>'
    all_stickers_html += sticker

# 第三段：一次性渲染
st.markdown(all_stickers_html, unsafe_allow_html=True)
# --- 5. 动态内容渲染 ---

# 首次加载弹窗
if not st.session_state.initial_popup_seen:
    init_options = [
        "硅基螺线管代劳中_(:3」∠)_",
        "This is no Silicon Valley. It's Silicon Kelly here :3",
        "你好What's upこんにちﾜｯｻﾌﾟ(^_^)/"
    ]
    st.markdown(f"""
        <div class="window" style="border-color: {random.choice(random_colors)}; border-style: none;">
            <div class="window-header">
                <span>SYSTEM_MSG.SYS</span><span>[X]</span>
            </div>
            <div class="window-content">
                <strong>{random.choice(init_options)}</strong><br><br>输入点什么开始聊天！
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.initial_popup_seen = True

# 对话历史渲染
for msg in st.session_state.messages:
    role_name = "YOU.EXE" if msg["role"] == "user" else "KELLY.EXE"
    st.markdown(f"""
        <div class="window" style="border-color: {random.choice(random_colors)};">
            <div class="window-header">
                <span>{role_name}</span><span>[X]</span>
            </div>
            <div class="window-content">
                {msg['content']}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 6. 用户交互逻辑 ---
with st.sidebar:
    st.markdown("### 🛠️ 系统控制")
    if st.button("重启大脑 (Clear Cache)"):
        st.session_state.messages = []
        st.session_state.initial_popup_seen = False
        st.rerun()
    st.markdown("---")
    st.write("螺线管卡BUG了")

user_input = st.chat_input("说点什么吧...")

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
                kelly_reply = f"...诶。发生了某种不可名状的错误。大概是世界线崩塌了。错误信息：{error_msg[:20]}..."
                
    st.session_state.messages.append({"role": "assistant", "content": kelly_reply})
    st.rerun()
