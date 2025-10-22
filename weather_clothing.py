import streamlit as st
import requests
from geopy.geocoders import Nominatim

# OpenWeatherMap API Ű
API_KEY = '6c40b0820856d83a30916a4ad306b932'  # �����Ͻ� API Ű ���

# ���� ���º� ������ ��õ ��ųʸ�
weather_clothing = {
    'clear': '������ ���� ��������. Ƽ������ �ݹ����� �����մϴ�.',
    'clouds': '������ ������ �غ��ϼ���. �����̳� �ĵ�Ƽ�� ��õ�մϴ�.',
    'rain': '����� ì�⼼��! ��� �����̳� ��� �Դ� ���� �����ϴ�.',
    'snow': '������ ���� ��������. �е��̳� �β��� ������ ��õ�մϴ�.',
    'drizzle': '����� ì�⼼��. ������ ������ �Բ� ��������.',
    'thunderstorm': '��ٶ��� ���ϴ� ��� ����� �ִ� ���� �԰� ����� ì�⼼��.',
    'mist': '�þ߰� ���� ������ ���� ������ ���� ��������.'
}

# ��ġ ������ ���� ���� ������ ��������
def get_weather_data():
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode("Seoul, South Korea")  # ����: ���� ��ġ
    lat = location.latitude
    lon = location.longitude
    
    # OpenWeatherMap API ��û
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr'
    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        st.error("���� �����͸� �������� �� �����߽��ϴ�.")
        return None

    return data

# ������ ��õ �Լ�
def recommend_clothing(temp, weather_conditions):
    if temp >= 28:
        return "�μҸ�, ����, �ݹ���, ���ǽ�"
    elif 23 <= temp < 28:
        return "����, ���� ����, �ݹ���, �����"
    elif 20 <= temp < 23:
        return "���� �����, ����, �����, û����"
    elif 17 <= temp < 20:
        return "���� ��Ʈ, ������, �����, û����"
    elif 12 <= temp < 17:
        return "����, �����, �߻�, ��Ÿŷ, û����, �����"
    elif 9 <= temp < 12:
        return "����, Ʈ��ġ��Ʈ, �߻�, ��Ʈ, û����, ��Ÿŷ"
    elif 5 <= temp < 9:
        return "��Ʈ, ��������, ��Ʈ��, ��Ʈ, ���뽺"
    else:
        return "�е�, �β�����Ʈ, �񵵸�, �����ǰ"

    if 'rain' in weather_conditions.lower():
        return "����� ì�⼼��! �� �� �� �ֽ��ϴ�."
    return "������ �´� ���� �غ��ϼ���."

# Streamlit ��
st.title("������ ������ �´� ������ ��õ")

# ���� ������ ��������
weather_data = get_weather_data()

if weather_data:
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    weather_icon = weather_data['weather'][0]['icon']
    city_name = weather_data['name']
    country = weather_data['sys']['country']
    
    # ���� ���� ���
    st.write(f"**��ġ**: {city_name}, {country}")
    st.write(f"**���� �µ�**: {temp}��C")
    st.write(f"**���� ����**: {description}")
    
    # ������ ��õ
    clothing_recommendation = recommend_clothing(temp, description)
    st.write(f"**��õ ������**: {clothing_recommendation}")
    
    # ���� ������ ǥ��
    icon_url = f'http://openweathermap.org/img/wn/{weather_icon}.png'
    st.image(icon_url, width=100)
else:
    st.error("���� �����͸� �������� �� �����߽��ϴ�.")
