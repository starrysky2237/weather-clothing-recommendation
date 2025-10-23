import streamlit as st
import requests
import random

# ===== 기본 설정 =====
st.set_page_config(page_title="날씨 & 옷차림 추천", page_icon="🌤️", layout="centered")

# ===== CSS (배경 + 중앙정렬 + 시각 강조) =====
st.markdown("""
<style>
html, body, .stApp {
    background: linear-gradient(135deg, #dff6ff 0%, #bde0fe 100%);
    font-family: 'Pretendard', 'Segoe UI', sans-serif;
    color: #1e293b;
}

/* 제목 */
h1 {
    text-align: center !important;
    font-weight: 900;
    color: #0b2545;
    text-shadow: 0 3px 10px rgba(255,255,255,0.9);
    font-size: 2.3em;
    margin-bottom: 10px;
}

/* 중앙정렬 */
h2, h3, p, div {
    text-align: center !important;
}

/* 입력창 */
input {
    background-color: #ffffff;
    color: #1e293b !important;
    font-weight: 600;
    border-radius: 10px !important;
    border: 2px solid #bae6fd !important;
    text-align: center;
}

/* 버튼 */
.stButton > button {
    display: block;
    margin: 0 auto;
    background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    color: white;
    font-weight: 700;
    font-size: 17px;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

/* 정보 블록 */
.info-box {
    background: rgba(255,255,255,0.7);
    border-radius: 12px;
    padding: 12px 20px;
    margin: 15px auto;
    text-align: center;
    width: fit-content;
    color: #1e3a8a;
    font-weight: 600;
}

/* 오늘의 추천 옷차림 강조 박스 */
.recommend-box {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 20px;
    margin-top: 25px;
    margin-bottom: 10px;
    width: 85%;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    text-align: center;
}
.recommend-box h3 {
    color: #1d4ed8;
    font-weight: 900;
    font-size: 1.4em;
    text-shadow: 0 2px 5px rgba(173, 216, 230, 0.8);
    margin-bottom: 15px;
}
.recommend-box p {
    color: #0f172a;
    font-weight: 700;
    font-size: 1.3em;
    line-height: 1.6;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# ===== 제목 =====
st.markdown("""
<h1>
🌤️ <span style="color:#003366;">
오늘의 날씨 & 옷차림 추천
</span>
</h1>
""", unsafe_allow_html=True)

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

def get_city_coordinates_from_api(city_name):
    api_key = '6c40b0820856d83a30916a4ad306b932'  # OpenWeatherMap API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None  # 에러 발생 시 None 반환

def get_weather(city_name):
    coordinates = get_city_coordinates_from_api(city_name)
    if coordinates is None:
        st.error(f"❌ {city_name}는 지원하지 않는 도시입니다.")
        return None
    lat, lon = coordinates
    api_key = '6c40b0820856d83a30916a4ad306b932'  # OpenWeatherMap API Key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    weather_data = requests.get(weather_url).json()
    return weather_data

# ===== UI =====
option = st.radio("도시 선택 방식", ["🏙️ 도시 직접 입력", "📍 현재 위치"], horizontal=True)

if option == "🏙️ 도시 직접 입력":
    city = st.text_input("도시 이름 입력 (예: 서울, 부산, 제주)", "서울")
    auto_search = False
else:
    city = "서울"
    auto_search = True  # 현재 위치 선택 시 자동검색

def show_weather(city):
    if city not in city_coordinates:
        st.error("❌ 지원하지 않는 도시입니다.")
    else:
        weather, simulated = get_weather(city)
        emoji = get_weather_emoji(weather["main"])
        clothes = recommend_clothing(weather["temp"])

        st.markdown(f"### 📍 {city}")
        st.markdown(f"## {emoji} {weather['weather']}")
        st.markdown(f"### 🌡️ {weather['temp']}°C (체감 {weather['feels_like']}°C)")
        st.markdown(f"""
        <div class="info-box">
            💧 습도: <b>{weather['humidity']}%</b> &nbsp;&nbsp;|&nbsp;&nbsp;
            💨 풍속: <b>{weather['wind_speed']} m/s</b>
        </div>
        """, unsafe_allow_html=True)

        # 👕 오늘의 추천 옷차림 강조
        st.markdown(f"""
        <div class="recommend-box">
            <h3>👕 오늘의 추천 옷차림</h3>
            <p>{clothes}</p>
        </div>
        """, unsafe_allow_html=True)

        if simulated:
            st.caption("📊 실시간 API 오류로 예측 데이터를 표시합니다.")

# 버튼 또는 자동 실행
if st.button("🌤️ 날씨 확인하기") or auto_search:
    show_weather(city)
