import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def show_home():
    st.header("<오늘의 분석>")
    st.subheader("주요도시별 인구현황 분석시간입니다.!")

    
    st.write("")
    st.write("")

    col1, col2 = st.columns([1, 2])  # 비율 조절 가능

    with col1:
        st.image("area.jpg", width=200)

    with col2:
        st.markdown("### 🇰🇷 대한민국 인구 분석 대시보드")

        st.write("대한민국 인구를 자세히 분류해보겠습니다.")
        st.write("왼쪽 사이드바에서 원하는 분석 방식을 선택해주세요")
        st.write("연령별 분석, 성별 분석, 도시별 분석이 있습니다.")
    st.divider()
    st.markdown("#### 대한민국은 !")   
    st.write("대한민국(한국 한자: 大韓民國)은 동아시아의 한반도 군사 분계선 남부에 위치한 나라이다. 약칭으로 한국(한국 한자: 韓國), 별칭으로 남한(한국 한자: 南韓, 문화어: 남조선)이라 부르며 현정체제는 대한민국 제6공화국이다. 대한민국의 국기는 대한민국 국기법에 따라 태극기[6]이며, 국가는 관습상 애국가, 국화는 관습상 무궁화이다. 공용어는 한국어와 한국 수어이다. 수도는 서울특별시이다. .")
    st.video("https://www.youtube.com/watch?v=n6WaTObHRJM&list=RDn6WaTObHRJM&start_radio=1")
    st.image("sliding.gif")
def show_age(): 
    st.header("<연령별 분석>")
    st.subheader("대한민국의 인구를 연령별로 분석한것입니다.!")


    st.set_page_config(page_title="연령대별 인구 분석", layout="wide")
    st.title("📊 대한민국 17개 시도 연령대별 인구 분석")

    # 1. CSV 불러오기
    df = pd.read_csv("korea.csv", encoding="cp949")

    # 2. 첫 번째 열 이름 지정
    df.rename(columns={df.columns[0]: "행정구역"}, inplace=True)

    # 3. 연령대 열만 추출
    age_columns = [col for col in df.columns if "2025년10월_계_" in col and ("~" in col or "이상" in col)]

    # 4. 열 이름에서 접두어 제거
    new_age_columns = [col.replace("2025년10월_계_", "") for col in age_columns]
    df.rename(columns=dict(zip(age_columns, new_age_columns)), inplace=True)

    # 5. 정확히 일치하는 17개 시도 이름
    target_regions = [
        "서울특별시  (1100000000)", "부산광역시  (2600000000)", "대구광역시  (2700000000)", "인천광역시  (2800000000)",
        "광주광역시  (2900000000)", "대전광역시  (3000000000)", "울산광역시  (3100000000)", "세종특별자치시  (3600000000)",
        "경기도  (4100000000)", "강원특별자치도  (5100000000)", "충청북도  (4300000000)", "충청남도  (4400000000)",
        "전북특별자치도  (5200000000)", "전라남도  (4600000000)", "경상북도  (4700000000)", "경상남도  (4800000000)",
        "제주특별자치도  (5000000000)"
    ]

    # 6. 시도 필터링
    df_filtered = df[df["행정구역"].isin(target_regions)]

    # 7. 연령대별 인구만 추출
    result = df_filtered[["행정구역"] + new_age_columns]

    # 8. 표 출력
    st.subheader("📋 연령대별 인구 데이터 (17개 시도)")
    st.dataframe(result, use_container_width=True)

    # 9. 선택한 시도별 시각화
    selected_region = st.selectbox("시도 선택", result["행정구역"].unique())

    if selected_region:
        region_data = result[result["행정구역"] == selected_region].iloc[0, 1:]
        fig = px.bar(x=region_data.index, y=region_data.values,
                    labels={"x": "연령대", "y": "인구수"},
                    title=f"{selected_region} 연령대별 인구 분포")
        st.plotly_chart(fig, use_container_width=True)
def show_gender():

    st.set_page_config(page_title="성별 인구 분석", layout="wide")
    st.header("<성별 인구 분석>")
    st.subheader("2025년 10월 기준 대한민국 17개 시도의 남자/여자 인구를 각각 인구수 기준으로 정확히 정렬한 표입니다.")

    # 1. CSV 불러오기 (인코딩 수정)
    df = pd.read_csv("korea.csv", encoding="cp949")

    df.rename(columns={df.columns[0]: "행정구역"}, inplace=True)

    # 2. 열 이름 자동 확인
    columns = df.columns.tolist()
    male_col = [col for col in columns if "남" in col and "총" in col][0]
    female_col = [col for col in columns if "여" in col and "총" in col][0]

    # 3. 대상 시도 이름
    target_regions = [
        "서울특별시  (1100000000)", "부산광역시  (2600000000)", "대구광역시  (2700000000)", "인천광역시  (2800000000)",
        "광주광역시  (2900000000)", "대전광역시  (3000000000)", "울산광역시  (3100000000)", "세종특별자치시  (3600000000)",
        "경기도  (4100000000)", "강원특별자치도  (5100000000)", "충청북도  (4300000000)", "충청남도  (4400000000)",
        "전북특별자치도  (5200000000)", "전라남도  (4600000000)", "경상북도  (4700000000)", "경상남도  (4800000000)",
        "제주특별자치도  (5000000000)"
    ]

    # 4. 필터링 및 시도명 정리
    df_filtered = df[df["행정구역"].isin(target_regions)].copy()
    df_filtered["행정구역"] = df_filtered["행정구역"].str.extract(r"^(.*?)(?=\s+\()")[0].str.strip()

    # 5. 숫자형 변환 + NaN 제거
    df_filtered[male_col] = pd.to_numeric(df_filtered[male_col].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered[female_col] = pd.to_numeric(df_filtered[female_col].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered.dropna(subset=[male_col, female_col], inplace=True)

    # 6. 남자 인구 기준 정렬
    male_df = df_filtered[["행정구역", male_col]].sort_values(by=male_col, ascending=False).reset_index(drop=True)

    # 7. 여자 인구 기준 정렬
    female_df = df_filtered[["행정구역", female_col]].sort_values(by=female_col, ascending=False).reset_index(drop=True)

    # 8. 표 출력
    st.subheader("👨 남자 인구 순위표 (내림차순)")
    st.dataframe(male_df, use_container_width=True)

    st.subheader("👩 여자 인구 순위표 (내림차순)")
    st.dataframe(female_df, use_container_width=True)
def show_city():
    st.set_page_config(page_title="성별 인구 비교", layout="wide")
    st.header("<성별 인구 비교>")
    st.subheader("2025년 10월 기준 대한민국 17개 시도의 남녀 인구 및 성비를 비교한 표입니다.")

    # 1. CSV 불러오기
    df = pd.read_csv("korea.csv", encoding="cp949")
    df.rename(columns={df.columns[0]: "행정구역"}, inplace=True)

    # 2. 대상 시도 이름
    target_regions = [
        "서울특별시  (1100000000)", "부산광역시  (2600000000)", "대구광역시  (2700000000)", "인천광역시  (2800000000)",
        "광주광역시  (2900000000)", "대전광역시  (3000000000)", "울산광역시  (3100000000)", "세종특별자치시  (3600000000)",
        "경기도  (4100000000)", "강원특별자치도  (5100000000)", "충청북도  (4300000000)", "충청남도  (4400000000)",
        "전북특별자치도  (5200000000)", "전라남도  (4600000000)", "경상북도  (4700000000)", "경상남도  (4800000000)",
        "제주특별자치도  (5000000000)"
    ]

    # 3. 필터링 및 시도명 정리
    df_filtered = df[df["행정구역"].isin(target_regions)].copy()
    df_filtered["행정구역"] = df_filtered["행정구역"].str.extract(r"^(.*?)(?=\s+\()")[0].str.strip()

    # 4. 숫자형 변환 + NaN 제거
    df_filtered["2025년10월_남_총인구수"] = pd.to_numeric(df_filtered["2025년10월_남_총인구수"].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered["2025년10월_여_총인구수"] = pd.to_numeric(df_filtered["2025년10월_여_총인구수"].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered.dropna(subset=["2025년10월_남_총인구수", "2025년10월_여_총인구수"], inplace=True)

    # 5. 전체 인구 및 성비 계산
    df_filtered["총인구"] = df_filtered["2025년10월_남_총인구수"] + df_filtered["2025년10월_여_총인구수"]
    df_filtered["성비(남/여)"] = (df_filtered["2025년10월_남_총인구수"] / df_filtered["2025년10월_여_총인구수"]).round(3)

    # 6. 필요한 열만 정리
    result_df = df_filtered[["행정구역", "2025년10월_남_총인구수", "2025년10월_여_총인구수", "총인구", "성비(남/여)"]]
    result_df = result_df.sort_values(by="총인구", ascending=False).reset_index(drop=True)

    # 7. 표 출력
    st.subheader("📊 17개 시도별 성별 인구 비교표")
    st.dataframe(result_df, use_container_width=True)
def vs():
    st.set_page_config(page_title="수도권 vs 비수도권 인구 비교", layout="wide")
    st.header("<수도권 vs 비수도권 인구 비교>")
    st.subheader("2025년 10월 기준 수도권과 비수도권의 남자/여자/전체 인구를 비교한 그래프입니다.")
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
    # 1. 시도별 인구 데이터 (직접 입력)
    data = {
        "지역": ["수도권", "비수도권"],
        "남자": [4489067 + 3049315 + 6893167,  # 서울 + 인천 + 경기
                3246304 + 2355677 + 1395869 + 1442046 + 1130000 + 180000 + 563285 + 860355 +
                811762 + 758837 + 718579 + 688690 + 4489067 + 332332],
        "여자": [4824465 + 1523210 + 6930000,
                1578085 + 1154160 + 688690 + 718579 + 560000 + 170000 + 707179 + 866599 +
                781154 + 750227 + 723467 + 707179 + 4824465 + 880555]
    }

    df = pd.DataFrame(data)
    df["전체"] = df["남자"] + df["여자"]

    # 2. 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.25
    index = range(len(df))

    ax.bar(index, df["남자"], bar_width, label="남자", color="#4A90E2")
    ax.bar([i + bar_width for i in index], df["여자"], bar_width, label="여자", color="#F15A5A")
    ax.bar([i + bar_width * 2 for i in index], df["전체"], bar_width, label="전체", color="#7ED321")

    ax.set_xlabel("지역")
    ax.set_ylabel("인구 수")
    ax.set_title("수도권 vs 비수도권 성별 인구 비교")
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(df["지역"])
    ax.legend()

    # 3. 그래프 출력
    st.pyplot(fig)
def choose():
    
    st.set_page_config(page_title="두 지역 인구 비교", layout="wide")
    st.header("<두 지역 인구 비교>")
    st.subheader("2025년 10월 기준으로 선택한 두 지역의 인구 데이터를 비교합니다.")

    # 1. 데이터 불러오기
    df = pd.read_csv("korea.csv", encoding="cp949")
    df.rename(columns={df.columns[0]: "행정구역"}, inplace=True)

    # 2. 대상 시도 목록
    target_regions = [
        "서울특별시  (1100000000)", "부산광역시  (2600000000)", "대구광역시  (2700000000)", "인천광역시  (2800000000)",
        "광주광역시  (2900000000)", "대전광역시  (3000000000)", "울산광역시  (3100000000)", "세종특별자치시  (3600000000)",
        "경기도  (4100000000)", "강원특별자치도  (5100000000)", "충청북도  (4300000000)", "충청남도  (4400000000)",
        "전북특별자치도  (5200000000)", "전라남도  (4600000000)", "경상북도  (4700000000)", "경상남도  (4800000000)",
        "제주특별자치도  (5000000000)"
    ]

    # 3. 필터링
    df_filtered = df[df["행정구역"].isin(target_regions)].copy()
    df_filtered["행정구역"] = df_filtered["행정구역"].str.extract(r"^(.*?)(?=\s+\()")[0].str.strip()

    # 4. 숫자형 변환
    df_filtered["남자"] = pd.to_numeric(df_filtered["2025년10월_남_총인구수"].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered["여자"] = pd.to_numeric(df_filtered["2025년10월_여_총인구수"].astype(str).str.replace(",", ""), errors="coerce")
    df_filtered["전체"] = df_filtered["남자"] + df_filtered["여자"]

    # 5. 지역 선택
    col1, col2 = st.columns(2)
    with col1:
        region1 = st.selectbox("지역 1 선택", df_filtered["행정구역"].unique())
    with col2:
        region2 = st.selectbox("지역 2 선택", df_filtered["행정구역"].unique())

    # 6. 비교 시각화
    if region1 and region2 and region1 != region2:
        compare_df = df_filtered[df_filtered["행정구역"].isin([region1, region2])]
        fig = px.bar(compare_df, x="행정구역", y=["남자", "여자", "전체"],
                     barmode="group", title=f"{region1} vs {region2} 인구 비교",
                     labels={"value": "인구 수", "variable": "성별"})
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(compare_df[["행정구역", "남자", "여자", "전체"]], use_container_width=True)
    else:
        st.info("서로 다른 두 지역을 선택해주세요.")
def finish():
    st.header("<대한민국 인구 통계 요약>")
    st.subheader("2025년 10월 기준 대한민국 17개 시도의 인구 통계를 요약합니다.")

    # 1. 데이터 불러오기
    df = pd.read_csv("korea.csv", encoding="cp949")
    df.rename(columns={df.columns[0]: "행정구역"}, inplace=True)

    # 2. 대상 시도 필터링
    target_regions = [
        "서울특별시  (1100000000)", "부산광역시  (2600000000)", "대구광역시  (2700000000)", "인천광역시  (2800000000)",
        "광주광역시  (2900000000)", "대전광역시  (3000000000)", "울산광역시  (3100000000)", "세종특별자치시  (3600000000)",
        "경기도  (4100000000)", "강원특별자치도  (5100000000)", "충청북도  (4300000000)", "충청남도  (4400000000)",
        "전북특별자치도  (5200000000)", "전라남도  (4600000000)", "경상북도  (4700000000)", "경상남도  (4800000000)",
        "제주특별자치도  (5000000000)"
    ]
    df = df[df["행정구역"].isin(target_regions)].copy()

    # 3. 성별 인구 열 자동 탐색
    male_col = [col for col in df.columns if "남" in col and "총" in col][0]
    female_col = [col for col in df.columns if "여" in col and "총" in col][0]

    # 4. 숫자형 변환
    df["남자"] = pd.to_numeric(df[male_col].astype(str).str.replace(",", ""), errors="coerce")
    df["여자"] = pd.to_numeric(df[female_col].astype(str).str.replace(",", ""), errors="coerce")
    df["총인구"] = df["남자"] + df["여자"]

    # 5. 전체 합계 및 성비
    total_male = int(df["남자"].sum())
    total_female = int(df["여자"].sum())
    total_population = total_male + total_female
    gender_ratio = round(total_male / total_female, 3)

    # 6. 연령대 열 추출 및 합계
    age_columns = [col for col in df.columns if "2025년10월_계_" in col and ("~" in col or "이상" in col)]
    df_age = df[age_columns].copy()
    df_age = df_age.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(",", ""), errors="coerce"))
    age_totals = df_age.sum().sort_values(ascending=False)

    # 7. 고령화 지수 계산
    young_keys = [key for key in age_totals.index if any(age in key for age in ["0~4세", "5~9세", "10~14세"])]
    old_keys = [key for key in age_totals.index if any(age in key for age in ["65~69세", "70~74세", "75~79세", "80세이상"])]
    young = age_totals[young_keys].sum()
    old = age_totals[old_keys].sum()
    aging_index = round((old / young) * 100, 1)

    # 8. 결과 출력
    st.markdown("### 📊 인구 요약")
    st.write(f"- 총인구: **{total_population:,}명**")
    st.write(f"- 남성 인구: **{total_male:,}명**")
    st.write(f"- 여성 인구: **{total_female:,}명**")
    st.write(f"- 성비(남/여): **{gender_ratio}**")
    st.write(f"- 고령화 지수: **{aging_index}** (유소년 100명당 노년 인구 수)")

    st.markdown("### 🧓 연령대별 인구 순위")
    age_df = pd.DataFrame({
        "연령대": age_totals.index.str.replace("2025년10월_계_", ""),
        "인구수": age_totals.values.astype(int)
    })
    st.dataframe(age_df, use_container_width=True)
    st.bar_chart(age_df.set_index("연령대"))




selectedmenu = st.sidebar.selectbox("메뉴제목입니다",
                     ['HOME', '연령별 분석', '성별 분석','도시별 분석','비교하기','마무리'])
st.sidebar.image("king.jpg", width=500)
if selectedmenu == 'HOME':
    show_home()
elif selectedmenu == '연령별 분석':
    show_age()
elif selectedmenu == '성별 분석':
    show_gender()
elif selectedmenu == '도시별 분석':
    show_city()
    vs()
elif selectedmenu == '비교하기':
    choose()
elif selectedmenu == '마무리':
    finish()
