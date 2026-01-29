import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression

# ========= 页面设置 ==========
st.set_page_config(page_title="智能作息生活助手", layout="centered")

st.title("🧠 智能作息生活助手")
st.write("上传你的生活记录（Excel），预测明天的状态并给出建议。")

# ========= 上传文件 ==========
uploaded_file = st.file_uploader("上传你的生活记录 Excel 文件", type=["xlsx"])

# ========= 文件存在时 ==========
if uploaded_file is not None:
    # 读取用户上传的 Excel
    df = pd.read_excel(uploaded_file)

    # ========= 数据预处理 ==========
    features = [
        "昨晚睡了多久",
        "今天刷手机时长",
        "今天学习时长",
        "今天是否喝咖啡",
        "今天压力等级"
    ]

    # 检查是否存在必要列
    if "第二天状态" not in df.columns:
        st.error("❌ Excel 文件缺少『第二天状态』列！")
        st.stop()

    train_df = df.dropna(subset=["第二天状态"])

    if len(train_df) < 5:
        st.warning("⚠️ 数据太少，建议至少记录 5 天以上")
        st.stop()

    X = train_df[features]
    y = train_df["第二天状态"]

    # ========= 训练模型 ==========
    model = LogisticRegression()
    model.fit(X, y)

    # ========= 获取今天的数据 ==========
    today = df.iloc[-1]
    X_today = today[features].values.reshape(1, -1)

    # ========= 预测结果 ==========
    pred = model.predict(X_today)[0]
    prob = model.predict_proba(X_today)[0][1]

    # ========= 显示预测结果 ==========
    st.subheader("📊 预测结果")
    st.metric("明天状态好的概率", f"{prob:.2%}")

    # ========= 给建议 ==========
    st.subheader("🧠 今日建议")

    if prob >= 0.7:
        advice = "状态很稳，保持当前作息即可 😄"
    elif prob >= 0.4:
        advice = "状态一般，建议今晚早点休息 🙂"
    else:
        advice = "状态偏差，今晚强烈建议早点睡 😴"

    # 补充解释
    reasons = []
    if today["昨晚睡了多久"] < 6:
        reasons.append("睡眠偏少")
    if today["今天刷手机时长"] > 4:
        reasons.append("刷手机偏多")
    if today["今天压力等级"] >= 4:
        reasons.append("压力较大")

    st.success(advice)

    if reasons:
        st.caption("可能原因：" + "、".join(reasons))

    st.divider()

    st.caption("📁 数据来源：上传的生活记录 Excel 文件")

else:
    st.write("请上传一个 Excel 文件。")

