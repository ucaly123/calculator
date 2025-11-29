import streamlit as st
import math

st.title("📘 Streamlit 계산기")

st.write("사칙연산, 모듈러, 지수, 로그 계산을 지원합니다.")

# ----------------------------
# 입력값
# ----------------------------
st.header("🔢 숫자 입력")
num1 = st.number_input("첫 번째 숫자", value=0.0, format="%.10f")
num2 = st.number_input("두 번째 숫자", value=0.0, format="%.10f")

# ----------------------------
# 연산 선택
# ----------------------------
st.header("⚙ 연산 선택")
operation = st.selectbox(
    "원하는 계산을 선택하세요",
    [
        "덧셈 (+)",
        "뺄셈 (-)",
        "곱셈 (×)",
        "나눗셈 (÷)",
        "모듈러 (%)",
        "지수 (a^b)",
        "로그 (log_a(b))"
    ]
)

# ----------------------------
# 계산 로직
# ----------------------------
st.header("📌 결과")

try:
    if operation == "덧셈 (+)":
        result = num1 + num2

    elif operation == "뺄셈 (-)":
        result = num1 - num2

    elif operation == "곱셈 (×)":
        result = num1 * num2

    elif operation == "나눗셈 (÷)":
        if num2 == 0:
            result = "❌ 0으로 나눌 수 없습니다."
        else:
            result = num1 / num2

    elif operation == "모듈러 (%)":
        if num2 == 0:
            result = "❌ 0으로 나눌 수 없습니다."
        else:
            result = num1 % num2

    elif operation == "지수 (a^b)":
        result = num1 ** num2

    elif operation == "로그 (log_a(b))":
        if num1 <= 0 or num1 == 1 or num2 <= 0:
            result = "❌ 로그의 밑은 1이 아니어야 하며 양수이어야 합니다. 로그 인수도 양수여야 합니다."
        else:
            result = math.log(num2, num1)

    st.success(f"결과: {result}")

except Exception as e:
    st.error(f"오류 발생: {e}")
