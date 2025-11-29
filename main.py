import streamlit as st
import math
import plotly.express as px
import numpy as np
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="공학 계산기 & 확률 시뮬레이터",
    page_icon="🧮",
    layout="wide"  # 그래프를 넓게 보기 위해 wide 모드 사용
)

# 사이드바 설정 (앱 모드 선택)
st.sidebar.title("메뉴")
app_mode = st.sidebar.radio(
    "사용할 앱을 선택하세요:",
    ["계산기 (Calculator)", "확률 시뮬레이터 (Probability)"]
)

st.sidebar.markdown("---")
st.sidebar.info("Created with Python & Streamlit")

# ==========================================
# 앱 1: 계산기 (기존 기능 유지)
# ==========================================
if app_mode == "계산기 (Calculator)":
    st.title("🧮 파이썬 공학 계산기")
    st.markdown("""
    이 기능은 **사칙연산, 공학용 계산** 및 **다항함수 그래프** 시각화를 지원합니다.
    """)
    st.divider()

    # 1. 연산자 선택
    operation = st.selectbox(
        "어떤 기능을 사용하시겠습니까?",
        (
            "더하기 (+)", 
            "빼기 (-)", 
            "곱하기 (*)", 
            "나누기 (/)", 
            "나머지 (%)", 
            "제곱 (**)", 
            "로그 (log)",
            "다항함수 그래프 (Graph)"
        )
    )
    st.write("")

    # --- 그래프 모드 ---
    if "그래프" in operation:
        st.subheader("📈 다항함수 그래프 설정")
        st.info("f(x) = ax^n + ... 형태의 함수를 그립니다.")

        degree = st.slider("함수의 차수 (Degree)", min_value=1, max_value=4, value=2)
        st.write("각 항의 계수를 입력하세요:")
        
        cols = st.columns(degree + 1)
        coeffs = []
        for i in range(degree, -1, -1):
            with cols[degree - i]:
                if i == 0:
                    label = "상수항 (c)"
                    val = 0.0
                else:
                    label = f"x^{i}의 계수"
                    val = 1.0 if i == degree else 0.0
                c = st.number_input(label, value=val, step=1.0, key=f"coeff_{i}")
                coeffs.append(c)

        range_col1, range_col2 = st.columns(2)
        with range_col1:
            x_min = st.number_input("X 최소값", value=-10.0, step=1.0)
        with range_col2:
            x_max = st.number_input("X 최대값", value=10.0, step=1.0)

        if st.button("그래프 그리기", type="primary", use_container_width=True):
            if x_min >= x_max:
                st.error("X 최소값은 최대값보다 작아야 합니다.")
            else:
                x = np.linspace(x_min, x_max, 500)
                y = np.zeros_like(x)
                equation_str = "f(x) = "
                for i, c in enumerate(coeffs):
                    power = degree - i
                    y += c * (x ** power)
                    if c != 0:
                        sign = " + " if c > 0 and i > 0 else " " if c > 0 else " - "
                        abs_c = abs(c)
                        c_str = "" if abs_c == 1 and power != 0 else str(abs_c)
                        if power == 0: term = f"{abs_c}"
                        elif power == 1: term = f"{c_str}x"
                        else: term = f"{c_str}x^{power}"
                        equation_str += f"{sign}{term}"

                fig = px.line(x=x, y=y, title=f"함수 그래프: {equation_str}", labels={'x': 'x', 'y': 'f(x)'})
                st.plotly_chart(fig, use_container_width=True)

    # --- 일반 계산기 모드 ---
    else:
        col1, col2 = st.columns(2)
        with col1:
            num1 = st.number_input("첫 번째 숫자", value=0.0, step=1.0, format="%.2f")
        with col2:
            if "로그" in operation:
                label_text = "밑 (Base)"
                default_val = 10.0 
            else:
                label_text = "두 번째 숫자"
                default_val = 0.0
            num2 = st.number_input(label_text, value=default_val, step=1.0, format="%.2f")

        st.write("")
        if st.button("계산하기", type="primary", use_container_width=True):
            result = None
            error_message = None
            try:
                if "더하기" in operation:
                    result = num1 + num2
                    symbol = "+"
                elif "빼기" in operation:
                    result = num1 - num2
                    symbol = "-"
                elif "곱하기" in operation:
                    result = num1 * num2
                    symbol = "*"
                elif "나누기" in operation:
                    if num2 == 0: error_message = "0으로 나눌 수 없습니다."
                    else:
                        result = num1 / num2
                        symbol = "/"
                elif "나머지" in operation:
                    if num2 == 0: error_message = "0으로 나눌 수 없습니다."
                    else:
                        result = num1 % num2
                        symbol = "%"
                elif "제곱" in operation:
                    result = num1 ** num2
                    symbol = "^"
                elif "로그" in operation:
                    if num1 <= 0: error_message = "진수는 0보다 커야 합니다."
                    elif num2 <= 0 or num2 == 1: error_message = "밑은 0보다 크고 1이 아니어야 합니다."
                    else:
                        result = math.log(num1, num2)
                        symbol = f"log base {num2} of"

                if error_message:
                    st.error(error_message)
                else:
                    st.success(f"결과: {result}")
                    if "로그" in operation:
                        st.caption(f"계산식: log_{num2}({num1}) = {result}")
                    else:
                        st.caption(f"계산식: {num1} {symbol} {num2} = {result}")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

# ==========================================
# 앱 2: 확률 시뮬레이터 (신규 기능)
# ==========================================
elif app_mode == "확률 시뮬레이터 (Probability)":
    st.title("🎲 확률 시뮬레이터")
    st.markdown("""
    동전 던지기나 주사위 굴리기를 시뮬레이션하고, **대수의 법칙**을 눈으로 확인해보세요.
    시행 횟수가 늘어날수록 이론적 확률에 가까워지는지 확인해봅시다.
    """)
    st.divider()

    # 설정 영역
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        sim_type = st.radio("시뮬레이션 유형 선택", ["동전 던지기 (Coin)", "주사위 굴리기 (Dice)"])
    
    with col_sim2:
        trials = st.number_input("시행 횟수 (Trials)", min_value=10, max_value=100000, value=100, step=10)
        st.caption("최소 10회, 최대 100,000회까지 가능합니다.")

    if st.button("시뮬레이션 시작 (Start)", type="primary", use_container_width=True):
        with st.spinner('시뮬레이션 중...'):
            # 데이터 생성 로직
            if "동전" in sim_type:
                outcomes = ["앞면", "뒷면"]
                # numpy를 사용하여 빠르게 랜덤 추출
                data = np.random.choice(outcomes, size=trials)
                color_seq = ["#FF9999", "#9999FF"] # 빨강, 파랑 계열
                title_text = f"동전 던지기 {trials}회 결과"
            else:
                outcomes = [1, 2, 3, 4, 5, 6]
                data = np.random.randint(1, 7, size=trials)
                color_seq = px.colors.qualitative.Pastel
                title_text = f"주사위 굴리기 {trials}회 결과"

            # 데이터프레임으로 변환하여 집계
            df = pd.DataFrame(data, columns=["Result"])
            count_df = df["Result"].value_counts().reset_index()
            count_df.columns = ["Result", "Count"]
            
            # 주사위의 경우 순서대로 정렬 (1,2,3,4,5,6)
            if "주사위" in sim_type:
                count_df = count_df.sort_values("Result")

            # 비율 계산
            count_df["Ratio"] = count_df["Count"] / trials
            
            # 결과 표시 (레이아웃 분할)
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                st.subheader("📊 결과 요약")
                st.dataframe(count_df, hide_index=True, use_container_width=True)
                
                # 이론적 확률과 비교 멘트
                if "동전" in sim_type:
                    st.info(f"이론적 확률: 각 0.5 (50%)")
                else:
                    st.info(f"이론적 확률: 각 1/6 (약 16.7%)")

            with res_col2:
                st.subheader("📈 결과 시각화")
                # Plotly Bar Chart
                fig = px.bar(
                    count_df, 
                    x="Result", 
                    y="Count", 
                    text="Count",
                    title=title_text,
                    color="Result",
                    color_discrete_sequence=color_seq
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False)
                
                # 주사위일 경우 X축을 카테고리형으로 강제하여 1.5 같은 중간값 표시 방지
                if "주사위" in sim_type:
                    fig.update_xaxes(type='category')
                    
                st.plotly_chart(fig, use_container_width=True)
