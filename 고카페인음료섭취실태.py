import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("청소년 고카페인 에너지 음료 섭취 실태 (2016~2022)")

# 데이터 불러오기 (깃허브 RAW URL로 불러와야 함)
url = 'https://raw.githubusercontent.com/사용자명/저장소명/브랜치명/energy_drink_data.csv'
df = pd.read_csv(url)

# 데이터 확인
st.dataframe(df)

# 선 그래프 시각화
fig, ax = plt.subplots()
ax.plot(df['연도'], df['섭취율(%)'], marker='o', color='orange', linewidth=2)
ax.set_xlabel("연도")
ax.set_ylabel("섭취율 (%)")
ax.set_title("청소년 고카페인 에너지 음료 섭취율 변화")
ax.grid(True)

# 그래프 보여주기
st.pyplot(fig)
