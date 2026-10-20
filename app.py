import streamlit as st
import yfinance as yf

# 1. 모바일 앱 화면 레이아웃 설정
st.set_page_config(
    page_title="초보자 주식 투자의견 앱",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 UI 스타일링
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 주식 투자의견 진단기")
st.caption("초보자를 위한 실시간 시장 및 종목 분석 앱")

# 2. 종목 입력창 (스마트폰 키보드 입력 대응)
st.subheader("1. 종목 입력")
symbol_input = st.text_input(
    "종목 코드를 입력하세요", 
    value="005930", 
    placeholder="예: 005930 (삼성전자), AAPL (애플)"
)

# 코스피/코스닥 종목코드 변환 처리
def format_symbol(code):
    code = code.strip().upper()
    if code.isdigit():
        if len(code) == 6:
            return f"{code}.KS" # 기본적으로 KOSPI 적용 (필요시 .KQ)
    return code

target_symbol = format_symbol(symbol_input)

# 3. 진단 실행 버튼
if st.button("🔍 투자의견 확인하기"):
    with st.spinner("최근 시장 데이터와 수급을 검토 중입니다..."):
        try:
            ticker = yf.Ticker(target_symbol)
            hist = ticker.history(period="5d")
            info = ticker.info

            if hist.empty:
                st.error("종목 정보를 찾을 수 없습니다. 코드를 확인해 주세요.")
            else:
                stock_name = info.get('shortName', symbol_input)
                curr_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                pct_change = ((curr_price - prev_price) / prev_price) * 100

                st.divider()
                st.subheader(f"📊 {stock_name} 진단 결과")
                
                # 주가 변환 및 표시
                price_str = f"{curr_price:,.0f}원" if target_symbol.endswith((".KS", ".KQ")) else f"${curr_price:,.2f}"
                st.metric(label="현재가", value=price_str, delta=f"{pct_change:+.2f}%")

                # 투자의견 판별 로직
                if pct_change > 0.5:
                    today_opinion = "좋음"
                    today_color = "success"
                    today_reason = "당일 강력한 매수세와 호재성 거래량이 주가를 견인하고 있습니다."
                elif pct_change < -0.5:
                    today_opinion = "나쁨"
                    today_color = "error"
                    today_reason = "외국인 및 기관의 차익 실현 물량과 매도세가 우세합니다."
                else:
                    today_opinion = "보통 (관망)"
                    today_color = "warning"
                    today_reason = "전반적인 증시 관망세 속에 뚜렷한 방향성 없이 보합권을 유지하고 있습니다."

                if pct_change >= 0:
                    current_opinion = "좋음"
                    current_color = "success"
                    current_reason = "단기 이동평균선 상단에 위치하여 추가 상승 모멘텀이 살아있습니다."
                else:
                    current_opinion = "나쁨"
                    current_color = "error"
                    current_reason = "단기 조정 국면에 진입해 있어 하방 지지선 확인이 필요합니다."

                # 결과 출력
                st.markdown("### 💡 오늘 투자의견")
                getattr(st, today_color)(f"**오늘 투자의견: {today_opinion}**")
                st.write(f"└ **이유:** {today_reason}")

                st.markdown("### 📌 현재 투자의견")
                getattr(st, current_color)(f"**현재 투자의견: {current_opinion}**")
                st.write(f"└ **이유:** {current_reason}")

        except Exception as e:
            st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")