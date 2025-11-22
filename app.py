import streamlit as st
import requests
import math

st.set_page_config(page_title="Heat & Sun Risk Checker", layout="wide")

# -----------------------
# Districts with sample lat/long (Tamil Nadu)
# -----------------------
districts = {
    "Chennai": (13.08, 80.27),
    "Coimbatore": (11.01, 76.96),
    "Madurai": (9.93, 78.12),
    "Thoothukudi": (8.76, 78.13),
    "Erode": (11.34, 77.72),
    "Tirunelveli": (8.73, 77.71),
    "Trichy": (10.79, 78.68)
}

# Heat index calculation
def heat_index(temp_c, humidity):
    temp_f = temp_c * 9/5 + 32
    hi_f = -42.379 + 2.04901523*temp_f + 10.14333127*humidity \
           - 0.22475541*temp_f*humidity - 6.83783e-3*(temp_f**2) \
           - 5.481717e-2*(humidity**2) + 1.22874e-3*(temp_f**2)*humidity \
           + 8.5282e-4*temp_f*(humidity**2) - 1.99e-6*(temp_f**2)*(humidity**2)
    hi_c = (hi_f - 32) * 5/9
    return round(hi_c, 1)

# Risk level
def get_risk_level(hi):
    if hi < 30:
        return "Low", "🟢 Safe"
    elif hi < 40:
        return "Moderate", "🟡 Caution"
    elif hi < 54:
        return "High", "🟠 Warning"
    else:
        return "Extreme", "🔴 Danger"

# Open-Meteo API (FREE)
def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,uv_index"
    data = requests.get(url).json()
    return data["current"]

# -----------------------
# UI
# -----------------------
st.title("☀️ Heat & Sun Risk Checker")
st.subheader("Simple tool to check heat stress danger for your district")

district = st.selectbox("Select your district", list(districts.keys()))

if st.button("Check Heat Risk"):
    lat, lon = districts[district]
    weather = fetch_weather(lat, lon)

    temp = weather["temperature_2m"]
    humidity = weather["relative_humidity_2m"]
    uv = weather.get("uv_index", 0)

    hi = heat_index(temp, humidity)
    level, emoji = get_risk_level(hi)

    st.write("---")

    st.metric("Temperature", f"{temp}°C")
    st.metric("Humidity", f"{humidity}%")
    st.metric("UV Index", uv)

    st.subheader(f"Heat Index: **{hi}°C**")
    st.subheader(f"Risk Level: {emoji} **{level}**")

    st.write("---")
    st.write("### Safety Tips:")

    if level == "Low":
        st.write("- Drink 1–2L water through the day.\n- No major heat risk.")
    elif level == "Moderate":
        st.write("- Avoid direct sun 12–3 PM.\n- Drink ORS if outdoors.")
    elif level == "High":
        st.write("- Take shade every 20 mins.\n- Drink 2–3L water.\n- Avoid strenuous work.")
    else:
        st.write("- Heatstroke likely. DO NOT stay in the sun.\n- Drink ORS.\n- Cool yourself immediately.\n- Seek medical help if dizzy.")

    st.write("---")
    st.caption("This is a simplified heat risk model using Heat Index + UV. For educational purposes.")
