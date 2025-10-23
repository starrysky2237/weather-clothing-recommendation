import streamlit as st
import requests
import random
import xml.etree.ElementTree as ET
from datetime import datetime

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

# ===== 기상청 API에서 날씨 정보 가져오기 =====
def get_weather_from_kma(city):
    # 기상청 API의 기상 정보 요청 파라미터 설정
    API_KEY = 'rP5bxYxITS2-W8WMSK0t9A'
    
    # 현재 날짜 및 시간 구하기
    today = datetime.today()
    base_date = today.strftime('%Y%m%d')  # 오늘 날짜 (YYYYMMDD)
    base_time = today.strftime('%H') + '00'  # 오늘 시간 (HH00)
    
    # 기상청의 주요 도시 NX, NY 좌표 설정
    city_coordinates = {
        '서울': ('60', '127'),
        '부산': ('98', '76'),
        '인천': ('55', '128'),
        '대구': ('89', '98'),
        '대전': ('92', '82'),
        '광주': ('85', '96'),
        '울산': ('110', '84'),
        '제주': ('65', '33')
    }

    if city not in city_coordinates:
        return None  # 기상청에서 지원하지 않는 도시 처리

    nx, ny = city_coordinates[city]
    
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': API_KEY,
        'numOfRows': 10,
        'pageNo': 1,
        'dataType': 'XML',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
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

            if category == 'T3H':  # 기온 (3시간 단위)
                weather_info['temp'] = value + '°C'
            elif category == 'SKY':  # 하늘 상태
                weather_info['sky'] = value
            elif category == 'PTY':  # 강수 형태
                weather_info['rain'] = value

        return weather_info
    else:
        return None  # API 응답이 없을 경우 None 반환

# ===== 옷차림 추천 =====
def recommend_clothing(temp):
    if temp >= 28: return "😎 민소매, 반팔, 반바지, 원피스"
    elif temp >= 23: return "👕 반팔, 얇은 셔츠, 반바지, 면바지"
    elif temp >= 20: return "👚 얇은 가디건, 긴팔, 청바지"
    elif temp >= 17: return "🧶 얇은 니트, 맨투맨, 가디건"
    elif temp >= 12: return "🧥 자켓, 야상, 청바지"
    elif temp >= 9: return "🧣 트렌치코트, 니트, 따뜻한 옷"
    elif temp >= 5: return "🧤 코트, 니트, 레깅스"
    else: return "☃️ 패딩, 목도리, 방한용품"

# UI: 도시 선택 방식 (콤보박스)
city = st.selectbox("도시 선택", ["서울", "부산", "인천", "대구", "대전", "광주", "울산", "제주"])

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

# 날씨 확인 버튼 (중앙정렬)
if st.button("🌤️ 날씨 확인하기"):
    show_weather(city)
