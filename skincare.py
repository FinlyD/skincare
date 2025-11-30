import streamlit as st

# === 页面配置 ===
st.set_page_config(page_title="智能护肤管家", page_icon="✨")

st.title("✨ 你的私人智能护肤管家")
st.markdown("根据你的 **肤质** 和 **环境**，定制最科学的护肤方案。")

# === 1. 左侧边栏：收集用户数据 ===
st.sidebar.header("👤 请完善你的档案")

# 输入：肤质
skin_type = st.sidebar.selectbox(
    "你的肤质是？",
    ("干性皮肤", "油性皮肤", "混合性皮肤", "敏感肌")
)

# 输入：天气
weather = st.sidebar.selectbox(
    "现在的天气如何？",
    ("炎热/潮湿 🥵", "寒冷/干燥 🥶", "舒适/春秋 🌤️")
)

# 输入：核心诉求
concern = st.sidebar.multiselect(
    "你最近想解决什么问题？(可多选)",
    ["美白/提亮", "抗老/去皱", "祛痘/控油", "修复屏障"]
)

# === 2. 核心逻辑：生成护肤建议 ===

def get_routine(skin, wea, con):
    morning = []
    evening = []
    tips = ""

    # --- 洁面逻辑 ---
    if skin == "干性皮肤" or skin == "敏感肌":
        morning.append("清水洁面 (不要用洗面奶)")
        evening.append("温和氨基酸洁面 / 卸妆油")
    elif skin == "油性皮肤":
        morning.append("清爽控油洁面")
        evening.append("皂基或复配洁面 / 卸妆水")
    else: # 混合
        morning.append("温和洁面 (重点洗T区)")
        evening.append("氨基酸洁面")

    # --- 功能性精华逻辑 (基于诉求) ---
    active_added = False
    if "美白/提亮" in con:
        morning.append("👉 VC精华 (抗氧化)")
        evening.append("👉 烟酰胺/377精华")
        active_added = True
    
    if "抗老/去皱" in con:
        if not active_added: morning.append("👉 胜肽精华")
        evening.append("👉 A醇/视黄醇 (避光使用)")
    
    if "祛痘/控油" in con:
        morning.append("👉 水杨酸棉片 (局部擦拭)")
        evening.append("👉 壬二酸/积雪草精华")

    if "修复屏障" in con or skin == "敏感肌":
        morning.append("👉 B5/神经酰胺喷雾")
        evening.append("👉 玻尿酸原液")

    # --- 保湿逻辑 (基于天气 + 肤质) ---
    moisturizer = ""
    if "寒冷" in wea:
        moisturizer = "高保湿面霜 (厚涂)" if skin != "油性皮肤" else "清爽面霜"
    elif "炎热" in wea:
        moisturizer = "清爽乳液/啫喱" if skin != "干性皮肤" else "轻薄面霜"
    else:
        moisturizer = "日常乳液/面霜"
    
    morning.append(moisturizer)
    evening.append(moisturizer)

    # --- 防晒 (早上必须有) ---
    spf = "高倍防晒霜 (SPF50+)" if "炎热" in wea else "日常通勤防晒 (SPF30)"
    morning.append(f"☀️ {spf} (雷打不动)")

    return morning, evening

# 获取建议
am_routine, pm_routine = get_routine(skin_type, weather, concern)

# === 3. 显示护肤流程 ===

st.divider() # 分割线

col1, col2 = st.columns(2)

with col1:
    st.subheader("☀️ 早间流程 (Morning)")
    for step in am_routine:
        st.success(step)

with col2:
    st.subheader("🌙 晚间流程 (Evening)")
    for step in pm_routine:
        st.info(step)

# === 4. 创新功能：成分冲突实验室 ===
st.divider()
st.subheader("🧪 成分冲突实验室")
st.write("想混用两个猛药？先查查会不会烂脸！")

c1, c2 = st.columns(2)
with c1:
    ing1 = st.selectbox("成分 A", ["A醇 (视黄醇)", "水杨酸/果酸", "维生素C", "烟酰胺", "酒精", "蓝铜胜肽"])
with c2:
    ing2 = st.selectbox("成分 B", ["水杨酸/果酸", "A醇 (视黄醇)", "高浓度VC", "烟酰胺", "酒精", "蓝铜胜肽"])

# 简单的冲突数据库
bad_mix = [
    {"pair": {"A醇 (视黄醇)", "水杨酸/果酸"}, "msg": "❌ **危险！** 酸类会破坏皮肤屏障，A醇也会，一起用脸皮会掉！建议早晚分开。"},
    {"pair": {"A醇 (视黄醇)", "高浓度VC"}, "msg": "⚠️ **刺激！** 两者都需要特定的pH值，混用可能失效且刺激。建议早C晚A。"},
    {"pair": {"蓝铜胜肽", "高浓度VC"}, "msg": "❌ **失效！** 铜离子会氧化VC，两个一起用等于白涂。"},
    {"pair": {"蓝铜胜肽", "水杨酸/果酸"}, "msg": "❌ **失效！** 酸性环境会破坏胜肽的结构。"},
    {"pair": {"酒精", "A醇 (视黄醇)"}, "msg": "⚠️ **太干了！** 两个都会拔干，大油田由于，干皮慎重。"}
]

# 检查逻辑
result_msg = "✅ **看起来安全** (但请先在耳后测试)"
current_pair = {ing1, ing2}

if ing1 == ing2:
    result_msg = "🤔 **你自己跟自己怎么打架？** 请选择两个不同的成分。"
else:
    for mix in bad_mix:
        if mix["pair"] == current_pair:
            result_msg = mix["msg"]
            break

# 显示结果
if "❌" in result_msg:
    st.error(result_msg)
elif "⚠️" in result_msg:
    st.warning(result_msg)
else:
    st.success(result_msg)