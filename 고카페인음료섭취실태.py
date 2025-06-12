import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub CSV URL로 교체하세요
CSV_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/고카페인_에너지__음료_이용_빈도(16182022).csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL, encoding='cp949')
    df_long = pd.DataFrame()

    years = ['2016', '2018', '2020', '2022']
    frequency_cols = {
        '거의 매일': '.1',
        '일주일에 1~2번': '.2',
        '한 달에 1~2번': '.3',
        '전혀 없음': '.4'
    }

    for year in years:
        for freq_label, suffix in frequency_cols.items():
            temp = df[['특성별(1)', '특성별(2)', f'{year}{suffix}']].copy()
            temp.columns = ['범주', '집단', '섭취율']
            temp['섭취빈도'] = freq_label
            temp['연도'] = int(year)
            df_long = pd.concat([df_long, temp], ignore_index=True)

    # 숫자형으로 변환
    df_long['섭취율'] = pd.to_numeric(df_long['섭취율'], errors='coerce')
    return df_long

df = load_data()

st.title("청소년 고카페인 음료 섭취 실태 (2016~2022)")
group_type = st.selectbox("비교 기준 선택 (예: 성별, 시도, 학교급 등)", df['범주'].unique())

# 선택된 기준에 따라 집단 필터
subgroups = df[df['범주'] == group_type]['집단'].unique()
selected_subgroups = st.multiselect("비교할 세부 집단 선택", subgroups, default=list(subgroups))

freq_options = df['섭취빈도'].unique()
selected_freq = st.selectbox("섭취 빈도 선택", freq_options)

# 필터링
filtered = df[
    (df['범주'] == group_type) &
    (df['집단'].isin(selected_subgroups)) &
    (df['섭취빈도'] == selected_freq)
]

# 시각화
fig = px.line(
    filtered,
    x='연도',
    y='섭취율',
    color='집단',
    markers=True,
    title=f"{group_type}별 '{selected_freq}' 섭취율 추세"
)
st.plotly_chart(fig, use_container_width=True)
