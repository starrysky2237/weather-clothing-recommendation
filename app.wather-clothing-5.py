import streamlit as st
import requests
import random
import xml.etree.ElementTree as ET

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

# 기상청 API 사용
def get_weather_from_kma(city):
    # 기상청 API의 기상 정보 요청 파라미터 설정
    API_KEY = 'rP5bxYxITS2-W8WMSK0t9A'
    BASE_DATE = '20251023'  # 예시 날짜 (2025년 10월 23일)
    BASE_TIME = '0600'  # 예시 시간 (06:00 시점)
    NX = '60'  # 서울의 X 좌표 (기상청 좌표)
    NY = '127'  # 서울의 Y 좌표 (기상청 좌표)

    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': API_KEY,
        'numOfRows': 10,
        'pageNo': 1,
        'dataType': 'XML',
        'base_date': BASE_DATE,
        'base_time': BASE_TIME,
        'nx': NX,
        'ny': NY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.text))
        root = tree.getroot()
        items = root.findall('.//item')

        weather_info = {}
        for item in items:
            category = item.find('category').text
            value = item.find('fcstValue').text

            if category == 'T3H':
                weather_info['temp'] = value + '°C'
            elif category == 'SKY':
                weather_info['sky'] = value
            elif category == 'PTY':
                weather_info['rain'] = value

        return weather_info
    else:
        return None

# UI
option = st.radio("도시 선택 방식", ["🏙️ 도시 직접 입력", "📍 현재 위치"], horizontal=True)

if option == "🏙️ 도시 직접 입력":
    city = st.text_input("도시 이름 입력 (예: 서울, 부산, 제주)", "서울")
    auto_search = False
else:
    city = "서울"
    auto_search = True

def show_weather(city):
    weather_data = get_weather_from_kma(city)

    if weather_data:
        st.markdown(f"### 📍 {city}")
        st.markdown(f"## 🌡️ 기온: {weather_data.get('temp', '정보 없음')}")
        st.markdown(f"### ☁️ 하늘 상태: {weather_data.get('sky', '정보 없음')}")
        st.markdown(f"### 🌧️ 강수형태: {weather_data.get('rain', '정보 없음')}")
        clothes = recommend_clothing(int(weather_data.get('temp', 0).replace('°C', '')))
        st.markdown(f"""
        <div class="recommend-box">
            <h3>👕 오늘의 추천 옷차림</h3>
            <p>{clothes}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("❌ 기상청 API에서 정보를 가져올 수 없습니다.")

# 버튼 또는 자동 실행
if st.button("🌤️ 날씨 확인하기") or auto_search:
    show_weather(city)
