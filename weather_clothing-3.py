import streamlit as st
import requests
from geopy.geocoders import Nominatim

# OpenWeatherMap API 키
API_KEY = '6c40b0820856d83a30916a4ad306b932'  # 제공된 API 키 사용

# 귀여운 날씨 상태별 아이콘 (URL)
weather_icons = {
    'clear': 'https://cdn-icons-png.flaticon.com/128/1146/1146857.png',  # 맑은 날
    'clouds': 'https://cdn-icons-png.flaticon.com/128/1187/1187980.png',  # 흐린 날
    'rain': 'https://cdn-icons-png.flaticon.com/128/1187/1187994.png',  # 비 오는 날
    'snow': 'https://cdn-icons-png.flaticon.com/128/1187/1187974.png',  # 눈 오는 날
    'drizzle': 'https://cdn-icons-png.flaticon.com/128/1187/1187994.png',  # 가벼운 비
    'thunderstorm': 'https://cdn-icons-png.flaticon.com/128/1187/1187990.png',  # 천둥번개
    'mist': 'https://cdn-icons-png.flaticon.com/128/1187/1187982.png'  # 안개
}

# 위치 정보를 통해 날씨 데이터 가져오기
def get_weather_data(city=None):
    if city is None:
        # 사용자의 위치를 추적하여 날씨 정보를 가져오기
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode("Seoul, South Korea")  # 예시로 서울 위치
        lat = location.latitude
        lon = location.longitude
    else:
        # 사용자가 도시를 입력하면 그 도시에 대한 날씨를 가져옴
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        lat = location.latitude
        lon = location.longitude
    
    # OpenWeatherMap API 요청
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr'
    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        st.error("날씨 데이터를 가져오는 데 실패했습니다.")
        return None

    return data

# 옷차림 추천 함수
def recommend_clothing(temp):
    # 온도대별 옷차림 아이콘 및 설명 반환
    if temp >= 28:
        return "민소매, 반팔, 반바지, 원피스", 'https://cdn-icons-png.flaticon.com/128/3637/3637005.png'  # 여름 아이콘
    elif 23 <= temp < 28:
        return "반팔, 얇은 셔츠, 반바지, 면바지", 'https://cdn-icons-png.flaticon.com/128/3637/3637010.png'  # 얇은 옷
    elif 20 <= temp < 23:
        return "얇은 가디건, 긴팔, 면바지, 청바지", 'https://cdn-icons-png.flaticon.com/128/3637/3637012.png'  # 긴팔 아이콘
    elif 17 <= temp < 20:
        return "얇은 니트, 맨투맨, 가디건, 청바지", 'https://cdn-icons-png.flaticon.com/128/3637/3637009.png'  # 얇은 자켓 아이콘
    elif 12 <= temp < 17:
        return "자켓, 가디건, 야상, 스타킹, 청바지, 면바지", 'https://cdn-icons-png.flaticon.com/128/3637/3637007.png'  # 자켓 아이콘
    elif 9 <= temp < 12:
        return "자켓, 트렌치코트, 야상, 니트, 청바지, 스타킹", 'https://cdn-icons-png.flaticon.com/128/3637/3637016.png'  # 트렌치코트 아이콘
    elif 5 <= temp < 9:
        return "코트, 가족자켓, 히트텍, 니트, 레깅스", 'https://cdn-icons-png.flaticon.com/128/3637/3637005.png'  # 겨울 코트 아이콘
    else:
        return "패딩, 두꺼운코트, 목도리, 기모제품", 'https://cdn-icons-png.flaticon.com/128/3637/3637009.png'  # 패딩 아이콘

# Streamlit 앱
st.title("오늘의 날씨에 맞는 옷차림 추천")

# 도시 입력 받기 (기본값으로 서울)
city = st.text_input("도시를 입력하세요", "Seoul")

# 현재 GPS 위치로 날씨 정보 보기 버튼
use_gps = st.checkbox("현재 위치로 날씨 보기")

# 날씨 데이터 가져오기
if use_gps:
    weather_data = get_weather_data()  # GPS 위치 사용
else:
    weather_data = get_weather_data(city)  # 도시 입력

if weather_data:
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    weather_icon = weather_data['weather'][0]['icon']
    city_name = weather_data['name']
    country = weather_data['sys']['country']
    
    # 날씨 정보 출력
    st.write(f"**위치**: {city_name}, {country}")
    st.write(f"**현재 온도**: {temp}°C")
    st.write(f"**날씨 상태**: {description}")
    
    # 귀여운 날씨 아이콘 선택
    weather_condition = description.lower()
    if 'clear' in weather_condition:
        icon_url = weather_icons['clear']
    elif 'clouds' in weather_condition:
        icon_url = weather_icons['clouds']
    elif 'rain' in weather_condition:
        icon_url = weather_icons['rain']
    elif 'snow' in weather_condition:
        icon_url = weather_icons['snow']
    elif 'drizzle' in weather_condition:
        icon_url = weather_icons['drizzle']
    elif 'thunderstorm' in weather_condition:
        icon_url = weather_icons['thunderstorm']
    else:
        icon_url = weather_icons['mist']

    # 옷차림 추천 및 아이콘
    clothing_recommendation, clothing_icon_url = recommend_clothing(temp)
    st.write(f"**추천 옷차림**: {clothing_recommendation}")
    st.image(clothing_icon_url, width=100)  # 옷차림 아이콘 출력
    
    # 귀여운 날씨 아이콘 출력
    st.image(icon_url, width=100)
else:
    st.error("날씨 데이터를 가져오는 데 실패했습니다.")
