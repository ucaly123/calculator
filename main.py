import streamlit as st
import math

# 페이지 기본 설정
st.set_page_config(
    page_title="나만의 공학 계산기",
    page_icon="🧮",
    layout="centered"
)

# 제목 및 설명
st.title("🧮 파이썬 스트림릿 계산기")
st.markdown("""
이 웹앱은 **사칙연산**뿐만 아니라 **나머지, 제곱, 로그** 연산도 지원합니다.
숫자를 입력하고 연산자를 선택하세요.
""")

st.divider()

# 입력 레이아웃 (컬럼으로 나누어 배치)
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    num1 = st.number_input("첫 번째 숫자", value=0.0, step=1.0, format="%.2f")

with col2:
    operation = st.selectbox(
        "연산자",
        (
            "더하기 (+)", 
            "빼기 (-)", 
            "곱하기 (*)", 
            "나누기 (/)", 
            "나머지 (%)", 
            "제곱 (**)", 
            "로그 (log)"
        )
    )

with col3:
    # 로그 연산일 경우 두 번째 숫자의 라벨을 '밑(Base)'로 변경하여 직관성 높임
    if "로그" in operation:
        label_text = "밑 (Base)"
        default_val = 10.0 # 상용로그 기본값
    else:
        label_text = "두 번째 숫자"
        default_val = 0.0
        
    num2 = st.number_input(label_text, value=default_val, step=1.0, format="%.2f")

# 계산 실행 버튼
if st.button("계산하기", type="primary", use_container_width=True):
    result = None
    error_message = None

    try:
        # 연산 로직
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
            if num2 == 0:
                error_message = "0으로 나눌 수 없습니다."
            else:
                result = num1 / num2
                symbol = "/"
                
        elif "나머지" in operation:
            if num2 == 0:
                error_message = "0으로 나눌 수 없습니다."
            else:
                result = num1 % num2
                symbol = "%"
                
        elif "제곱" in operation:
            result = num1 ** num2
            symbol = "^"
            
        elif "로그" in operation:
            # 로그의 진수 조건(num1 > 0)과 밑 조건(num2 > 0, num2 != 1) 체크
            if num1 <= 0:
                error_message = "로그의 진수(첫 번째 숫자)는 0보다 커야 합니다."
            elif num2 <= 0 or num2 == 1:
                error_message = "로그의 밑(두 번째 숫자)은 0보다 크고 1이 아니어야 합니다."
            else:
                result = math.log(num1, num2)
                symbol = f"log base {num2} of"

        # 결과 출력
        if error_message:
            st.error(error_message)
        else:
            st.success(f"결과: {result}")
            # 수식 보여주기
            if "로그" in operation:
                 st.caption(f"계산식: log_{num2}({num1}) = {result}")
            else:
                 st.caption(f"계산식: {num1} {symbol} {num2} = {result}")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.divider()
st.markdown("Created with Python & Streamlit")
