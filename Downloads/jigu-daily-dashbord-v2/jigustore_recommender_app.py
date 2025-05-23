
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("지구스토어 특가 상품 추천 대시보드")

uploaded_file = st.file_uploader("📂 엑셀 상품 데이터 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")

    # 할인율 계산
    df["할인율(%)"] = ((df["소비자가"] - df["특가"]) / df["소비자가"] * 100).round(1)
    df["D-데이"] = (pd.to_datetime(df["소비기한"]) - datetime.today()).dt.days
    df["임박"] = df["D-데이"] <= 5
    df["추천점수"] = df["할인율(%)"] + df["임박"].astype(int) * 10

    # 상위 3~4개 상품 추천
    top_items = df.sort_values(by="추천점수", ascending=False).head(4)

    st.subheader("✅ 오늘의 특가 상품 추천")
    st.dataframe(top_items[["상품명", "소비자가", "특가", "할인율(%)", "D-데이"]])

    # 카카오톡 메시지 포맷
    st.subheader("📢 카카오톡 메시지")
    msg = "[지구스토어 오늘의 특가 🎉]\n\n"
    for i, row in top_items.iterrows():
        msg += f"{i+1}. {row['상품명']}\n   (정가 {int(row['소비자가'])}원 → 특가 {int(row['특가'])}원, {row['할인율(%)']}% 할인)\n"
    msg += "\n🛒 오늘 오후 6시까지 리센츠상가 매장에서 픽업하세요!\n⚠️ 수량 한정, 선착순 마감!"
    st.text_area("복사해서 사용하세요!", value=msg, height=200)
