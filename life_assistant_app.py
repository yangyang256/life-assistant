import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from io import BytesIO

# ================= 页面基础设置 =================
st.set_page_config(
    page_title="智能作息生活助手",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 智能作息生活助手")
st.write("上传你的生活记录 Excel，预测明天的状态，并给出作息建议。")

# ================= 示例 Excel 下载 =================
st.subheader("📄 示例数据模板（首次使用请下载）")

example_df = pd.DataFrame({
    "昨晚睡了多久": [7, 6, 8],
    "今天刷手机时长": [2, 4, 1],
    "今天学习时长": [5, 3, 6],
    "今天是否喝咖啡": [0, 1, 0],
    "今天压力等级": [2, 4, 1],
    "第二天状态": [1, 0, 1]
})

buffer = BytesIO()
example_df.to_excel(buffer, index=False)
buffer.seek(0)

st.download_button(
    label="📥 下载示例 Excel 模板",
    data=buffer,
    file_name="生活数据示例.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ================= 上传 Excel =================
st.subheader("📤 上传你的生活数据 Excel")

uploaded_file = st.file_uploader(
    "请选择 .xlsx 文件",
    type=["xlsx"]
)

# ================= 主逻辑 =================
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error("❌ Excel 文件读取失败，请确认格式正确")
        st.stop()

    required_columns = [
        "昨晚睡了多久",
        "今天刷手机时长",
        "今天学习时长",
        "今天是否喝咖啡",
        "今天压力等级",
        "第二天状态"
    ]

    # 检查列是否齐全
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"❌ Excel 缺少以下列：{missing}")
        st.stop()

    # 只用有标签的数据训练
    train_df = df.dropna(subset=["第二天状态"])

    if len(train_df) < 5:
        st.warning("⚠️ 数据太少，建议至少 5 天以上再预测")
        st.stop()

    features = [
        "昨晚睡了多久",
        "今天刷手机时长",
        "今天学习时长",
        "今天是否喝咖啡",
        "今天压力等级"
    ]

    X = train_df[features]
    y = train_df["第二天状态"]

    # ================= 训练模型 =================
    model = LogisticRegression()
    model.fit(X, y)

    # ================= 取今天的数据 =================
    today = df.iloc[-1]
    X_today = today[features].values.reshape(1, -1)

    prob = model.predict_proba(X_today)[0][1]

    # ================= 展示结果 =================
    st.subheader("📊 预测结果")
    st.metric("明天状态好的概率", f"{prob:.2%}")

    st.subheader("🧠 今日作息建议")

    if prob >= 0.7:
        advice = "状态很稳，保持当前作息即可 😄"
    elif prob >= 0.4:
        advice = "状态一般，建议今晚早点休息 🙂"
    else:
        advice = "状态偏差，今晚强烈建议早点睡 😴"

    reasons = []
    if today["昨晚睡了多久"] < 6:
        reasons.append("睡眠偏少")
    if today["今天刷手机时长"] > 4:
        reasons.append("刷手机偏多")
    if today["今天压力等级"] >= 4:
        reasons.append("压力较大")

    st.success(advice)

    if reasons:
        st.caption("可能影响因素：" + "、".join(reasons))

else:
    st.info("👆 请先上传你的 Excel 文件")

st.divider()

# ================= 安全说明 =================
st.caption("🔒 所有数据仅用于当前预测，不会被保存或记录。")


else:
    st.write("请上传一个 Excel 文件。")

