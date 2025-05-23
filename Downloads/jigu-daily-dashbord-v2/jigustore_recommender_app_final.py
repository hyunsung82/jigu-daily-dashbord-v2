
import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.title("지구스토어 특가 상품 추천 대시보드")

uploaded_file = st.file_uploader("📂 엑셀 상품 데이터 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")

    # 할인율 및 분석 지표 추가
    df["할인율(%)"] = ((df["소비자가"] - df["특가"]) / df["소비자가"] * 100).round(1)
    df["D-데이"] = (pd.to_datetime(df["소비기한"]) - datetime.today()).dt.days
    df["임박"] = df["D-데이"] <= 5
    df["추천점수"] = df["할인율(%)"] + df["임박"].astype(int) * 10

    # 상위 3개 추천
    top_items = df.sort_values(by="추천점수", ascending=False).head(3)

    st.subheader("✅ 오늘의 특가 상품")
    st.dataframe(top_items[["상품명", "소비자가", "특가", "할인율(%)", "D-데이"]])

    # 세트 특가 계산
    total_special_price = top_items["특가"].sum()
    bundle_discount_price = int(total_special_price * 0.85)

    # 요일 기반 컨셉 생성
    weekday = datetime.today().weekday()
    concept_map = {
        0: "월요병 퇴치 세트 💪",
        1: "든든한 화요일 도시락 세트 🍱",
        2: "수요일 간식 대작전 세트 🍪",
        3: "목요 홈쿡 밀키트 세트 🍲",
        4: "불금 캠핑 간식 세트 🔥",
        5: "주말 소풍 도시락 세트 🧺",
        6: "일요일 냉장고 비우기 세트 🧊"
    }
    concept_title = concept_map.get(weekday, "오늘의 추천 세트 🌟")

    # 카카오톡 메시지 생성
    msg = f"[지구스토어 오늘의 특가 🎉]\n\n{concept_title}\n\n"
    for i, row in top_items.iterrows():
        msg += f"{i+1}. {row['상품명']}\n   (정가 {int(row['소비자가'])}원 → 특가 {int(row['특가'])}원, {row['할인율(%)']}% 할인)\n"

    msg += f"\n🎁 [3종 세트 구성]\n👉 단품가 합계: {total_special_price:,}원\n👉 세트 특가: {bundle_discount_price:,}원!"
    msg += f"\n(총 {total_special_price - bundle_discount_price:,}원 추가 할인!)"
    msg += "\n\n🛒 오늘 오후 6시까지 리센츠상가 매장에서 픽업하세요!\n⚠️ 수량 한정, 선착순 마감!"

    st.subheader("📢 카카오톡 메시지")
    st.text_area("복사해서 사용하세요!", value=msg, height=320)

    # 이미지 미리보기
    st.subheader("🖼️ 시각적 구성 (데모)")
    for _, row in top_items.iterrows():
        st.markdown(f"**{row['상품명']}** — 정가 {int(row['소비자가'])}원 → 특가 {int(row['특가'])}원 ({row['할인율(%)']}% 할인)")
        st.image("https://via.placeholder.com/300x180.png?text=Product+Image", width=300)
