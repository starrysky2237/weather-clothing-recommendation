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

/* 버튼 중앙 정렬 */
.stButton {
    display: flex;
    justify-content: center;
}
.stButton > button {
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

def get_weather(city):
    api_key = "6c40b0820856d83a30916a4ad306b932"
    lat, lon = city_coordinates.get(city, (37.5665, 126.9780))
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
        base = random.choice(range(12, 20))
        return {
            "temp": base + random.randint(-2, 2),
            "feels_like": base + random.randint(-1, 1),
            "humidity": random.randint(40, 80),
            "wind_speed": round(random.uniform(1, 4), 1),
            "weather": random.choice(["맑음", "흐림", "비"]),
            "main": "Clear"
        }, True

# ===== 입력 =====
option = st.radio("도시 선택 방식", ["🏙️ 도시 직접 입력", "📍 현재 위치"], horizontal=True)

# 입력 초기화용 상태
if "city_input" not in st.session_state:
    st.session_state.city_input = ""

# 입력창 (클릭 시 빈칸으로)
city = st.text_input(
    "도시 이름 입력 (예: 서울, 부산, 제주)",
    value=st.session_state.city_input,
    key="city_input_box",
    placeholder="도시를 입력 후 Enter ⏎"
)
if city == "":
    st.session_state.city_input = city

auto_search = (option == "📍 현재 위치")

# ===== 날씨 표시 =====
def show_weather(city):
    if city not in city_coordinates:
        st.error("❌ 지원하지 않는 도시입니다.")
        return
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

    # ✅ 단순한 형태로 복원된 추천 칸
    st.markdown("---")
    st.markdown(f"### 👕 오늘의 추천 옷차림")
    st.markdown(f"**{clothes}**")

    if simulated:
        st.caption("📊 실시간 API 오류로 예측 데이터를 표시합니다.")

# ===== 중앙 버튼 =====
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🌤️ 날씨 확인하기", use_container_width=True) or auto_search or st.session_state.get("city_input_box"):
        if city.strip():
            show_weather(city.strip())
