import streamlit as st
import requests
from geopy.geocoders import Nominatim

# OpenWeatherMap API 키
API_KEY = '6c40b0820856d83a30916a4ad306b932'  # 제공하신 API 키 사용

# 날씨 상태별 옷차림 추천 딕셔너리
weather_clothing = {
    'clear': '가벼운 옷을 입으세요. 티셔츠와 반바지가 적합합니다.',
    'clouds': '가벼운 외투를 준비하세요. 자켓이나 후드티를 추천합니다.',
    'rain': '우산을 챙기세요! 방수 자켓이나 우비를 입는 것이 좋습니다.',
    'snow': '따뜻한 옷을 입으세요. 패딩이나 두꺼운 외투를 추천합니다.',
    'drizzle': '우산을 챙기세요. 가벼운 외투와 함께 입으세요.',
    'thunderstorm': '비바람이 강하니 방수 기능이 있는 옷을 입고 우산을 챙기세요.',
    'mist': '시야가 좋지 않으니 밝은 색상의 옷을 입으세요.'
}

# 위치 정보를 통해 날씨 데이터 가져오기
def get_weather_data():
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode("Seoul, South Korea")  # 예시: 서울 위치
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
def recommend_clothing(temp, weather_conditions):
    if temp >= 28:
        return "민소매, 반팔, 반바지, 원피스"
    elif 23 <= temp < 28:
        return "반팔, 얇은 셔츠, 반바지, 면바지"
    elif 20 <= temp < 23:
        return "얇은 가디건, 긴팔, 면바지, 청바지"
    elif 17 <= temp < 20:
        return "얇은 니트, 맨투맨, 가디건, 청바지"
    elif 12 <= temp < 17:
        return "자켓, 가디건, 야상, 스타킹, 청바지, 면바지"
    elif 9 <= temp < 12:
        return "자켓, 트렌치코트, 야상, 니트, 청바지, 스타킹"
    elif 5 <= temp < 9:
        return "코트, 가족자켓, 히트텍, 니트, 레깅스"
    else:
        return "패딩, 두꺼운코트, 목도리, 기모제품"

    if 'rain' in weather_conditions.lower():
        return "우산을 챙기세요! 비가 올 수 있습니다."
    return "날씨에 맞는 옷을 준비하세요."

# Streamlit 앱
st.title("오늘의 날씨에 맞는 옷차림 추천")

# 날씨 데이터 가져오기
weather_data = get_weather_data()

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
    
    # 옷차림 추천
    clothing_recommendation = recommend_clothing(temp, description)
    st.write(f"**추천 옷차림**: {clothing_recommendation}")
    
    # 날씨 아이콘 표시
    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}.png'
    st.image(icon_url, width=100)
else:
    st.error("날씨 데이터를 가져오는 데 실패했습니다.")
