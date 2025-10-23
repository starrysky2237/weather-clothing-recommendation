import streamlit as st
import requests
import random
from datetime import datetime

# ===== 기본 설정 =====
st.set_page_config(page_title="날씨 & 옷차림 추천", page_icon="🌤️", layout="centered")

# ===== 계절별 배경 설정 =====
def get_season_background():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%)"  # 겨울: 푸른빛
    elif month in [3, 4, 5]:
        return "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)"  # 봄: 핑크+라벤더
    elif month in [6, 7, 8]:
        return "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"  # 여름: 시원한 파랑
    else:
        return "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"  # 가을: 주황빛

# ===== CSS (가독성 + 중앙 정렬 + 반투명 블록) =====
background_color = get_season_background()
st.markdown(f"""
<style>
html, body, .stApp {{
    background: {background_color};
    font-family: 'Pretendard', 'Segoe UI', sans-serif;
    color: #ffffff;
}}

/* 제목 영역 */
.title-container {{
    text-align: center;
    background: rgba(0,0,0,0.3);
    border-radius: 16px;
    padding: 15px 25px;
    margin-bottom: 25px;
    backdrop-filter: blur(10px);
}}
.title-container h1 {{
    font-size: 2.2em;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.5px;
    text-shadow: 0 3px 10px rgba(0,0,0,0.7);
}}
.title-gradient {{
    background: linear-gradient(135deg, #ffffff 0%, #cce5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
/* 버튼 */
.stButton > button {{
    display: block;
    margin: 0 auto;
    background: rgba(255,255,255,0.2);
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 12px;
    color: white;
    font-weight: 700;
    font-size: 17px;
    padding: 10px 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}}
.stButton > button:hover {{
    transform: translateY(-3px);
    background: rgba(255,255,255,0.35);
}}
/* 입력창 */
input {{
    background-color: rgba(255,255,255,0.95);
    color: #1e293b !important;
    font-weight: 600;
    border-radius: 10px !important;
    border: 2px solid #dbeafe !important;
    text-align: center;
}}
/* 정보 박스 */
.info-box {{
    background: rgba(255,255,255,0.25);
    border-radius: 15px;
    padding: 12px 25px;
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}
/* 섹션 텍스트 */
.section {{
    text-align: center;
    background: rgba(0,0,0,0.25);
    border-radius: 16px;
    padding: 15px;
    margin-top: 15px;
    color: #ffffff;
    backdrop-filter: blur(6px);
    text-shadow: 0 2px 6px rgba(0,0,0,0.6);
}}
.section h3 {{
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 5px;
}}
.section p {{
    font-size: 20px;
    font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)

# ===== 제목 =====
st.markdown("""
<div class="title-container">
    <h1>🌤️ <span class="title-gradient">오늘의 날씨 & 옷차림 추천</span></h1>
</div>
""", unsafe_allow_html=True)

# ===== 도시 데이터 =====
city_coordinates = {
    '서울': (37.5665, 126.9780), '부산': (35.1796, 129.0756), '인천': (37.4563, 126.7052),
    '대구': (35.8714, 128.6014), '대전': (36.3504, 127.3845), '광주': (35.1595, 126.8526),
    '울산': (35.5384, 129.3114), '수원': (37.2636, 127.0286), '창원': (35.2281, 128.6811),
    '성남': (37.4201, 127.1262), '고양': (37.6584, 126.8320), '용인': (37.2410, 127.1776),
    '청주': (36.6424, 127.4890), '전주': (35.8242, 127.1480), '안산': (37.3219, 126.8309),
    '천안': (36.8151, 127.1139), '제주': (33.4996, 126.5312), '포항': (36.0190, 129.3435),
    '강릉': (37.7519, 128.8761), '춘천': (37.8813, 127.7298), '원주': (37.3422, 127.9202),
    '속초': (38.2070, 128.5918), '경주': (35.8562, 129.2247), '안동': (36.5684, 128.7294),
    '목포': (34.8118, 126.3922), '여수': (34.7604, 127.6622), '순천': (34.9506, 127.4872)
}

# ===== 함수 정의 =====
def recommend_clothing(temp):
    if temp >= 28: return "😎 민소매, 반팔, 반바지, 원피스"
    elif temp >= 23: return "👕 반팔, 얇은 셔츠, 반바지, 면바지"
    elif temp >= 20: return "👚 얇은 가디건, 긴팔, 청바지"
    elif temp >= 17: return "🧶 얇은 니트, 맨투맨, 가디건"
    elif temp >= 12: return "🧥 자켓, 야상, 청바지"
    elif temp >= 9: return "🧣 트렌치코트, 니트, 따뜻한 옷"
    elif temp >= 5: return "🧤 코트, 니트, 레깅스"
    else: return "☃️ 패딩, 목도리, 방한용품"

def get_weather_emoji(main):
    desc = main.lower()
    if "clear" in desc: return "☀️"
    if "cloud" in desc: return "☁️"
    if "rain" in desc or "drizzle" in desc: return "🌧️"
    if "snow" in desc: return "❄️"
    if "thunder" in desc: return "⛈️"
    if "mist" in desc or "fog" in desc: return "🌫️"
    return "🌤️"

def get_simulated_weather(city):
    base_temp = random.choice(range(12, 20))
    return {
        "temp": base_temp + random.randint(-2, 2),
        "feels_like": base_temp + random.randint(-1, 1),
        "humidity": random.randint(40, 80),
        "wind_speed": round(random.uniform(1, 4), 1),
        "weather": random.choice(["맑음", "구름 많음", "흐림"]),
        "main": "Clear"
    }

def get_weather(city):
    api_key = "6c40b0820856d83a30916a4ad306b932"
    lat, lon = city_coordinates[city]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    try:
        res = requests.get(url, timeout=8)
        res.raise_for_status()
        data = res.json()
        return {
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"],
            "main": data["weather"][0]["main"]
        }, False
    except:
        return get_simulated_weather(city), True

# ===== 입력 영역 =====
option = st.radio("도시 선택 방식", ["🏙️ 도시 직접 입력", "📍 현재 위치"], horizontal=True)
if option == "🏙️ 도시 직접 입력":
    city = st.text_input("도시 이름 입력 (예: 서울, 부산, 제주)", "서울")
else:
    city = "서울"

# ===== 실행 버튼 =====
if st.button("🌤️ 날씨 확인하기"):
    if city not in city_coordinates:
        st.error("❌ 지원하지 않는 도시입니다.")
    else:
        weather, simulated = get_weather(city)
        emoji = get_weather_emoji(weather["main"])
        clothes = recommend_clothing(weather["temp"])

        # ===== 결과 출력 =====
        st.markdown(f"""
        <div class="section">
            <h3>📍 {city}</h3>
            <p style="font-size:26px;">{emoji} {weather['weather']}</p>
            <p style="font-size:28px;">🌡️ {weather['temp']}°C (체감 {weather['feels_like']}°C)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-box">
            💧 습도: <b>{weather['humidity']}%</b> &nbsp;&nbsp;|&nbsp;&nbsp;
            💨 풍속: <b>{weather['wind_speed']} m/s</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="section">
            <h3>👕 오늘의 추천 옷차림</h3>
            <p>{clothes}</p>
        </div>
        """, unsafe_allow_html=True)

        if simulated:
            st.caption("📊 실시간 API 오류로 예측 데이터를 표시합니다.")
