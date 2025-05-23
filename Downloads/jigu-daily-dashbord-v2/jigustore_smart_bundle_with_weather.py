
import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="지구스토어 특가 추천", layout="centered")

st.title("📦 지구스토어 특가 상품 자동 구성 대시보드")

uploaded_file = st.file_uploader("📂 엑셀 상품 데이터 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")

    # 전처리: 할인율 및 D-Day 계산
    df["할인율(%)"] = ((df["소비자가"] - df["특가"]) / df["소비자가"] * 100).round(1)
    df["D-데이"] = (pd.to_datetime(df["소비기한"]) - datetime.today()).dt.days
    df["임박"] = df["D-데이"] <= 5
    df["추천점수"] = df["할인율(%)"] + df["임박"].astype(int) * 10

    # 추천 상위 3개 상품
    top_items = df.sort_values(by="추천점수", ascending=False).head(3)

    st.subheader("✅ 추천 단품 특가 상품")
    st.dataframe(top_items[["상품명", "소비자가", "특가", "할인율(%)", "소비기한"]])

    # 요일 + 계절 + 날씨(임시 랜덤) 기반 컨셉 명 생성
    weekday = datetime.today().weekday()
    month = datetime.today().month
    weekday_labels = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    season_map = {12: "겨울", 1: "겨울", 2: "겨울", 3: "봄", 4: "봄", 5: "봄",
                  6: "여름", 7: "여름", 8: "여름", 9: "가을", 10: "가을", 11: "가을"}
    season = season_map[month]
    mock_weather = random.choice(["맑음", "비", "흐림", "더움", "쌀쌀함"])

    concept_pool = [
        f"{season}철 추천 🌸 오늘은 '{mock_weather}' 날씨!",
        f"{weekday_labels[weekday]} 🌤 냉장고 채우기 세트",
        f"오늘은 캠핑 어때요? 🔥 캠핑 간식 세트",
        f"혼밥족을 위한 간편식 모음 🍱",
        f"아이 간식 걱정 끝! 🧃 주말 간식세트",
        f"{season} 대비 면역력 챙기기 세트 💪"
    ]
    concept_title = random.choice(concept_pool)

    # 세트 특가 계산
    sum_special = top_items["특가"].sum()
    set_price = int(sum_special * 0.85)  # 추가 15% 할인
    sum_retail = top_items["소비자가"].sum()
    discount_rate = round((1 - set_price / sum_retail) * 100, 1)

    # 카카오 스타일 메시지 생성
    msg = f"[📦 지구스토어 {weekday_labels[weekday]} 특가 알림]\n\n"
    msg += f"{concept_title}\n\n"
    msg += f"✨ “{top_items.iloc[0]['상품명']} 외 2종”\n\n"
    for i, row in top_items.iterrows():
        msg += f"✔ {row['상품명']}\n   – 소비자가 {int(row['소비자가']):,}원\n   – 오늘의 단품 특가: {int(row['특가']):,}원\n"

    msg += f"\n💰 단품 특가 합계: {int(sum_special):,}원 → 세트 구매 시 {int(set_price):,}원!"
    msg += f"\n🔥 총 {discount_rate}% 할인 혜택! 오늘 하루만!\n"
    msg += "\n📍 지구스토어 잠실새내 리센츠상가"
    msg += "\n🕙 오전 10시 카카오톡 채널 예약 시작"
    msg += "\n🚶 당일 매장 픽업 전용"

    st.subheader("📢 자동 생성된 카카오 메시지")
    st.text_area("아래 내용을 복사해서 발송에 활용하세요!", value=msg, height=350)
