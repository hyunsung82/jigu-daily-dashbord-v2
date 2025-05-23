
import streamlit as st
import pandas as pd
from datetime import datetime

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
    st.dataframe(top_items[["상품명", "소비자가", "특가", "소비기한", "할인율(%)", "D-데이"]])

    # 세트 특가 계산
    total_price = top_items["소비자가"].sum()
    set_price = int(top_items["특가"].sum() * 0.85)
    discount_rate = round((1 - (set_price / total_price)) * 100, 1)

    # 요일별 문구 생성
    weekday = datetime.today().weekday()
    weekday_label = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"][weekday]
    concept_name = "실속 주방 3종 세트"

    # 카카오톡 메시지 생성
    msg = f"[🥄 지구스토어 {weekday_label} 특가 알림]\n\n"
    msg += "오늘 하루, 주방부터 다시 채워볼까요?\n\n"
    msg += f"✨ “{concept_name}”\n\n"

    for i, row in top_items.iterrows():
        msg += f"✔ {row['상품명']} – 소비자가 {int(row['소비자가']):,}원 – 소비기한: {pd.to_datetime(row['소비기한']).strftime('%Y.%m.%d')}\n"

    msg += f"\n💰 총 소비자가 {int(total_price):,}원 → 세트 특가 {int(set_price):,}원"
    msg += f"\n🔥 무려 {discount_rate}% 할인! 오늘 하루만!\n"
    msg += "\n📍 지구스토어 잠실새내 리센츠상가"
    msg += "\n🕙 오전 10시부터 카카오톡 채널 예약"
    msg += "\n🚶 당일 매장 픽업 전용"

    st.subheader("📢 카카오톡 메시지")
    st.text_area("복사해서 사용하세요!", value=msg, height=350)
