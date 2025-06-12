import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 경로
CSV_URL = "https://raw.githubusercontent.com/iissyyii/finalproject/main/gogo.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL, encoding='cp949')  # 한글 인코딩
    return df

df = load_data()

st.title("청소년 고카페인 음료 섭취 실태 분석 (2016~2022)")

# 기본 정보
st.markdown("#### 데이터 미리보기")
st.dataframe(df.head())

# 년도 필터
years = sorted(df['년도'].unique())
selected_year = st.selectbox("연도 선택", years)

# 성별, 학교급 등 필터링 UI
col1, col2 = st.columns(2)
with col1:
    selected_gender = st.selectbox("성별", df['성별'].unique())
with col2:
    selected_school = st.selectbox("학교급", df['학교급'].unique())

# 필터 적용
filtered_df = df[(df['년도'] == selected_year) &
                 (df['성별'] == selected_gender) &
                 (df['학교급'] == selected_school)]

# 시각화
st.markdown("### 섭취 빈도별 분포")
if not filtered_df.empty:
    fig = px.bar(filtered_df, 
                 x='섭취빈도', 
                 y='백분율',
                 color='성별',
                 barmode='group',
                 labels={'섭취빈도': '섭취 빈도', '백분율': '비율(%)'},
                 title=f"{selected_year}년 {selected_gender} ({selected_school}) 고카페인 음료 섭취 분포")
    st.plotly_chart(fig)
else:
    st.warning("해당 조건에 맞는 데이터가 없습니다.")
