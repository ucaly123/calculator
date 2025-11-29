import streamlit as st
import math

# 페이지 설정 (제목, 아이콘 등)
st.set_page_config(page_title="나만의 스마트 계산기", page_icon="🧮")

st.title("🧮 파이썬 스마트 계산기")
st.markdown("사칙연산뿐만 아니라 나머지, 거듭제곱, 로그 계산까지 가능한 웹앱입니다.")

# CSS로 약간의 스타일링 추가 (선택 사항)
st.markdown("""
<style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color: white;
        font-size: 20px;
        height: 3em;
        width: 100%; 
    }
</style>
""", unsafe_allow_html=True)

# 구분선
st.divider()

# 입력 레이아웃: 컬럼 2개로 나누어 숫자 입력 받기
col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("첫 번째 숫자 (또는 진수)", value=0.0, format="%.4f")

with col2:
    num2 = st.number_input("두 번째 숫자 (또는 밑)", value=0.0, format="%.4f")

# 연산 선택 박스
operation = st.selectbox(
    "연산 방식을 선택하세요",
    [
        "더하기 (+)", 
        "빼기 (-)", 
        "곱하기 (*)", 
        "나누기 (/)", 
        "나머지 연산 (%)", 
        "거듭제곱 (**)", 
        "로그 연산 (log)"
    ]
)

# 계산 버튼 및 로직
if st.button("계산하기"):
    result = None
    error_msg = None

    try:
        # 1. 더하기
        if "더하기" in operation:
            result = num1 + num2
        
        # 2. 빼기
        elif "빼기" in operation:
            result = num1 - num2
        
        # 3. 곱하기
        elif "곱하기" in operation:
            result = num1 * num2
        
        # 4. 나누기
        elif "나누기" in operation:
            if num2 == 0:
                error_msg = "❌ 0으로 나눌 수 없습니다."
            else:
                result = num1 / num2
        
        # 5. 나머지 연산
        elif "나머지" in operation:
            if num2 == 0:
                error_msg = "❌ 0으로 나눌 수 없습니다."
            else:
                result = num1 % num2
        
        # 6. 거듭제곱 (지수)
        elif "거듭제곱" in operation:
            # 결과가 너무 커지는 것을 방지하기 위한 예외처리 (선택 사항)
            if abs(num1) > 100 and num2 > 100:
                error_msg = "❌ 숫자가 너무 커서 계산할 수 없습니다."
            else:
                result = num1 ** num2
        
        # 7. 로그 연산
        elif "로그" in operation:
            # num1: 진수 (Anti-logarithm), num2: 밑 (Base)
            # 조건: 진수 > 0, 밑 > 0, 밑 != 1
            if num1 <= 0:
                error_msg = "❌ 진수(첫 번째 숫자)는 0보다 커야 합니다."
            elif num2 <= 0:
                error_msg = "❌ 밑(두 번째 숫자)은 0보다 커야 합니다."
            elif num2 == 1:
                error_msg = "❌ 밑(두 번째 숫자)은 1이 될 수 없습니다."
            else:
                result = math.log(num1, num2)

    except Exception as e:
        error_msg = f"계산 중 오류가 발생했습니다: {e}"

    # 결과 출력
    st.divider()
    if error_msg:
        st.error(error_msg)
    else:
        st.success(f"결과 값: {result}")
        # 수식으로도 보여주기 (옵션)
        if "로그" in operation:
            st.info(f"계산 식: log_{num2}({num1}) = {result}")
        elif "거듭제곱" in operation:
             st.info(f"계산 식: {num1} ^{num2} = {result}")
        else:
             # 간단한 기호 매핑
            symbol = operation.split("(")[1].replace(")", "")
            st.info(f"계산 식: {num1} {symbol} {num2} = {result}")
