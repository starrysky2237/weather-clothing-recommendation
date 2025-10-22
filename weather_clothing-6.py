import streamlit as st
import requests
from geopy.geocoders import Nominatim

# OpenWeatherMap API 키
API_KEY = '6c40b0820856d83a30916a4ad306b932'  # 제공된 API 키 사용

# 💖 귀여운 날씨 상태별 아이콘 URL (Flaticon에서 가져온 URL)
cute_icons = {
    'clear': 'https://cdn-icons-png.flaticon.com/512/1146/1146857.png',  # 맑은 날
    'clouds': 'https://cdn-icons-png.flaticon.com/512/1187/1187980.png',  # 흐린 날
    'rain': 'https://cdn-icons-png.flaticon.com/512/1187/1187994.png',  # 비 오는 날
    'snow': 'https://cdn-icons-png.flaticon.com/512/1187/1187974.png',  # 눈 오는 날
    'drizzle': 'https://cdn-icons-png.flaticon.com/512/1187/1187994.png',  # 이슬비
    'thunderstorm': 'https://cdn-icons-png.flaticon.com/512/1187/1187990.png',  # 천둥번개
    'mist': 'https://cdn-icons-png.flaticon.com/512/1187/1187982.png'  # 안개
}

# 위치 정보를 통해 날씨 데이터 가져오기
def get_weather_data(city=None):
    if city is None:
        # 사용자의 위치를 추적하여 날씨 정보를 가져오기
        geolocator = Nominatim(user_agent="cute_weather_app")
        location = geolocator.geocode("Seoul, South Korea")  # 기본값: 서울
        if not location:
            st.error("위치를 찾을 수 없습니다. 도시 이름을 다시 확인해 주세요.")
            return None
    else:
        # 사용자가 도시를 입력하면 그 도시에 대한 날씨를 가져옴
        geolocator = Nominatim(user_agent="cute_weather_app")
        location = geolocator.geocode(city)
        if not location:
            st.error(f"'{city}' 도시에 대한 정보를 찾을 수 없습니다. 도시 이름을 다시 확인해 주세요.")
            return None

    lat, lon = location.latitude, location.longitude
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    return response.json()

# 옷차림 추천 함수
def recommend_clothing(temp):
    if temp >= 28:
        return "민소매, 반팔, 반바지, 원피스", "https://cdn-icons-png.flaticon.com/512/3075/3075977.png"
    elif 23 <= temp < 28:
        return "반팔, 얇은 셔츠, 반바지, 면바지", "https://cdn-icons-png.flaticon.com/512/3075/3075955.png"
    elif 20 <= temp < 23:
        return "얇은 가디건, 긴팔, 면바지, 청바지", "https://cdn-icons-png.flaticon.com/512/3075/3075942.png"
    elif 17 <= temp < 20:
        return "얇은 니트, 맨투맨, 가디건, 청바지", "https://cdn-icons-png.flaticon.com/512/3075/3075962.png"
    elif 12 <= temp < 17:
        return "자켓, 가디건, 야상, 스타킹, 청바지, 면바지", "https://cdn-icons-png.flaticon.com/512/3075/3075945.png"
    elif 9 <= temp < 12:
        return "트렌치코트, 니트, 청바지, 스타킹", "https://cdn-icons-png.flaticon.com/512/3075/3075948.png"
    elif 5 <= temp < 9:
        return "코트, 가죽자켓, 니트, 레깅스", "https://cdn-icons-png.flaticon.com/512/3075/3075960.png"
    else:
        return "패딩, 두꺼운 코트, 목도리, 기모제품", "https://cdn-icons-png.flaticon.com/512/3075/3075965.png"

# Streamlit 앱
st.title("🌤️ 오늘의 귀여운 날씨 & 옷차림 추천")

option = st.radio("날씨 정보를 가져올 방법을 선택하세요:", ("도시 직접 입력", "현재 위치 (기본: 서울)"))

if option == "도시 직접 입력":
    city = st.text_input("도시 이름을 입력하세요:", "Seoul")
    weather_data = get_weather_data(city)
else:
    weather_data = get_weather_data()

# 날씨 데이터 표시
if weather_data and weather_data.get('cod') == 200:
    temp = weather_data['main']['temp']
    weather_desc = weather_data['weather'][0]['main'].lower()
    city_name = weather_data['name']
    country = weather_data['sys']['country']

    st.markdown(f"### 📍 위치: {city_name}, {country}")
    st.markdown(f"**🌡️ 현재 온도:** {temp}°C")

    # 귀여운 날씨 아이콘 선택
    icon_url = cute_icons.get(weather_desc, cute_icons['clear'])
    
    # 옷차림 추천
    clothing, clothing_icon = recommend_clothing(temp)
    
    # 날씨 아이콘과 옷차림 아이콘을 나란히 출력
    col1, col2 = st.columns(2)
    with col1:
        st.image(icon_url, width=100, caption=f"날씨: {weather_desc.capitalize()}")
    with col2:
        st.image(clothing_icon, width=100, caption=clothing)
    st.success(f"**추천 옷차림**: {clothing}")

else:
    st.error("날씨 데이터를 불러오는 데 실패했습니다. 도시 이름이나 네트워크를 확인하세요.")
