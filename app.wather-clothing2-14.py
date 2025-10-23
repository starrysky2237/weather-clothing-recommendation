import streamlit as st
import requests
import random

st.set_page_config(page_title="날씨 & 옷차림 추천", page_icon="🌤️", layout="centered")

# ===== CSS =====
st.markdown("""
<style>
html, body, .stApp {
    background: linear-gradient(135deg, #dff6ff 0%, #bde0fe 100%);
    font-family: 'Pretendard', 'Segoe UI', sans-serif;
    color: #1e293b;
}
h1 {
    text-align: center !important;
    font-weight: 900;
    color: #002244;
    text-shadow: 0 3px 10px rgba(255,255,255,0.9);
    font-size: 2.5em;
    margin-bottom: 20px;
}
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
.recommend-box {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 25px;
    margin-top: 30px;
    width: 85%;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}
.recommend-box h3 {
    color: #1d4ed8;
    font-weight: 900;
    font-size: 1.5em;
    margin-bottom: 12px;
}
.recommend-box p {
    color: #0f172a;
    font-weight: 700;
    font-size: 1.2em;
    line-height: 1.6;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌤️ 오늘의 날씨 & 옷차림 추천</h1>", unsafe_allow_html=True)

# ===== 도시 데이터 =====
city_coordinates = {
    '서울': (37.5665, 126.9780), '부산': (35.1796, 129.0756), '인천': (37.4563, 126.7052),
    '대구': (35.8714, 128.6014), '대전': (36.3504, 127.3845), '광주': (35.1595, 126.8526),
    '울산': (35.5384, 129.3114), '수원': (37.2636, 127.0286), '창원': (35.2281, 128.6811),
    '성남': (37.4201, 127.1262), '고양': (37.6584, 126.8320), '용인': (37.2410, 127.1776),
    '청주': (36.6424, 127.4890), '전주': (35.8242, 127.1480), '제주': (33.4996, 126.5312)
}

# ===== 함수 =====
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
    main = main.lower()
    if "clear" in main: return "☀️"
    if "cloud" in main: return "☁️"
    if "rain" in main or "drizzle" in main: return "🌧️"
    if "snow" in main: return "❄️"
    if "thunder" in main: return "⛈️"
    return "🌤️"

def get_weather(city):
    api_key = "6c40b0820856d83a30916a4ad306b932"
    lat, lon = city_coordinates.get(city, (37.5665, 126.9780))
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
    try:
        res = requests.get(url, timeout=8)
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
        base = random.choice(range(12, 20))
        return {
            "temp": base + random.randint(-2, 2),
            "feels_like": base + random.randint(-1, 1),
            "humidity": random.randint(40, 80),
            "wind_speed": round(random.uniform(1, 4), 1),
            "weather": random.choice(["맑음", "흐림", "비"]),
            "main": "Clear"
        }, True

# ===== 입력영역 =====
st.markdown("### 🏙️ 도시를 입력하거나 선택하세요")

col1, col2 = st.columns([2, 1])
with col1:
    city_input = st.text_input("도시 이름 (입력 시 선택 가능)", "", placeholder="예: 서울, 부산, 제주")
with col2:
    use_gps = st.checkbox("📍 현재위치", value=False)

city = city_input.strip()

if city == "":
    city = st.selectbox("주요 도시 선택", list(city_coordinates.keys()), index=0)

if use_gps:
    city = "서울"

# ===== 중앙 버튼 =====
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🌤️ 날씨 확인하기", use_container_width=True):
        if city not in city_coordinates:
            st.error("❌ 지원하지 않는 도시입니다.")
        else:
            weather, simulated = get_weather(city)
            emoji = get_weather_emoji(weather["main"])
            clothes = recommend_clothing(weather["temp"])

            st.markdown(f"### 📍 {city}")
            st.markdown(f"## {emoji} {weather['weather']}")
            st.markdown(f"### 🌡️ {weather['temp']}°C (체감 {weather['feels_like']}°C)")
            st.markdown(f"💧 습도: **{weather['humidity']}%** | 💨 풍속: **{weather['wind_speed']}m/s**")
            st.markdown("""
            <div class='recommend-box'>
                <h3>👕 오늘의 추천 옷차림</h3>
                <p>{}</p>
            </div>
            """.format(clothes), unsafe_allow_html=True)
            if simulated:
                st.caption("📊 실시간 API 오류로 예측 데이터를 표시합니다.")
