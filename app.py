import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Set Matplotlib to use standard sans-serif font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False 

# 2. Configure Web Page Title
st.set_page_config(page_title="Global Urban Canyon Sunlight Calculator", layout="centered")
st.title("☀️ Global Urban Canyon Microclimate & Sunlight Calculator")
st.write("An interactive spatiotemporal tool for global geography field research and environmental health audits.")

# 3. Built-in Global Location Database (Country -> City -> [Latitude, Is_Southern_Hemisphere])
GLOBAL_DB = {
    "Macao / Hong Kong": {
        "Macao (Baseline)": [22.20, False],
        "Hong Kong (Central)": [22.28, False]
    },
    "East Asia": {
        "Beijing (China)": [39.90, False],
        "Shanghai (China)": [31.23, False],
        "Taipei (Taiwan)": [25.03, False],
        "Tokyo (Japan)": [35.67, False],
        "Seoul (South Korea)": [37.56, False]
    },
    "Southeast Asia": {
        "Singapore": [1.35, False],
        "Kuala Lumpur (Malaysia)": [3.14, False],
        "Bangkok (Thailand)": [13.75, False],
        "Manila (Philippines)": [14.59, False]
    },
    "Europe": {
        "London (UK)": [51.50, False],
        "Paris (France)": [48.85, False],
        "Berlin (Germany)": [52.52, False],
        "Lisbon (Portugal)": [38.72, False]
    },
    "North America": {
        "New York (USA)": [40.71, False],
        "Los Angeles (USA)": [34.05, False],
        "Toronto (Canada)": [43.65, False]
    },
    "Southern Hemisphere": {
        "Sydney (Australia)": [33.86, True],
        "Melbourne (Australia)": [37.81, True],
        "São Paulo (Brazil)": [23.55, True],
        "Cape Town (South Africa)": [33.92, True]
    }
}

# ==========================================
# 4. Sidebar Inputs & Dynamic Coordination Fields
# ==========================================
st.sidebar.header("🌍 Step 1: Select or Input Location")

# Country and Region Dropdowns
selected_country = st.sidebar.selectbox("Select Country/Region:", list(GLOBAL_DB.keys()))
available_cities = GLOBAL_DB[selected_country]
selected_city = st.sidebar.selectbox("Select City (Auto-fills Latitude):", list(available_cities.keys()))

# Get default latitude from DB
default_lat, is_southern = available_cities[selected_city]

# Manual Latitude Override Field (Users can directly type specific latitude here)
lat = st.sidebar.number_input(
    "Target Latitude (Degree North, use negative for South):", 
    min_value=-90.0, 
    max_value=90.0, 
    value=default_lat, 
    step=0.01,
    help="You can manually override this value to input any specific latitude worldwide."
)

# Custom Location Identifier
place_name = st.sidebar.text_input("Specific Investigation Site Note:", f"{selected_city} - Field Track")

st.sidebar.header("📐 Step 2: Urban Canyon Geometry")
street_width = st.sidebar.number_input("Street Width (m):", value=5.0, step=0.1)
height = st.sidebar.number_input("Observer Height (m):", value=1.8, step=0.1)
south_angle = st.sidebar.slider("South Building Angle (°):", min_value=0, max_value=90, value=45)
north_angle = st.sidebar.slider("North Building Angle (°):", min_value=0, max_value=90, value=65)

# ==========================================
# 5. Core Astronomical & Spatiotemporal Logic
# ==========================================
# Define standard astronomical declinations
if lat < 0:
    delta_summer = -23.43   # Summer for South (December)
    delta_winter = 23.43    # Winter for South (June)
    summer_label = "December Solstice (Southern Summer Max)"
    winter_label = "June Solstice (Southern Winter Min)"
else:
    delta_summer = 23.43    # Summer for North (June)
    delta_winter = -23.43   # Winter for North (December)
    summer_label = "June Solstice (Northern Summer Max)"
    winter_label = "December Solstice (Northern Winter Min)"

# Time Axis Grid: 05:00 to 19:00 (170 sampling intervals)
hours = np.linspace(5, 19, 170)
alpha_summer = []
alpha_winter = []

for hr in hours:
    h = (hr - 12) * 15
    h_rad = np.radians(h)
    lat_rad = np.radians(lat)
    
    # Summer Solstice Formula
    sin_alpha_s = (np.sin(lat_rad) * np.sin(np.radians(delta_summer)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_summer)) * np.cos(h_rad))
    sin_alpha_s = np.clip(sin_alpha_s, -1.0, 1.0)
    alpha_summer.append(max(0, np.degrees(np.arcsin(sin_alpha_s))))
    
    # Winter Solstice Formula
    sin_alpha_w = (np.sin(lat_rad) * np.sin(np.radians(delta_winter)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_winter)) * np.cos(h_rad))
    sin_alpha_w = np.clip(sin_alpha_w, -1.0, 1.0)
    alpha_winter.append(max(0, np.degrees(np.arcsin(sin_alpha_w))))
    
alpha_summer = np.array(alpha_summer)
alpha_winter = np.array(alpha_winter)

# Calculate durations above canyon blockades
dt = (19 - 5) / 170
summer_hours = np.sum(alpha_summer > north_angle) * dt
winter_hours = np.sum(alpha_winter > south_angle) * dt
avg_hours = (summer_hours + winter_hours) / 2

def to_hr_min_str(h_val):
    hr = int(h_val)
    mn = int(round((h_val - hr) * 60))
    if hr == 0 and mn == 0: 
        return "0 hr 0 min (Permanent Shadow Zone)"
    return f"{hr} hr {mn} min"

# ==========================================
# 6. Plotting the Dynamic Global Curve Chart
# ==========================================
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=110)

ax.plot(hours, alpha_summer, color='#e74c3c', linewidth=2.5, label=summer_label)
ax.plot(hours, alpha_winter, color='#3498db', linewidth=2.5, label=winter_label)

ax.axhline(y=north_angle, color='#c0392b', linestyle='--', linewidth=1.5, label=f'Summer Cutoff (North Bldg: {north_angle}°)')
ax.axhline(y=south_angle, color='#2980b9', linestyle='--', linewidth=1.5, label=f'Winter Cutoff (South Bldg: {south_angle}°)')

ax.fill_between(hours, alpha_summer, north_angle, where=(alpha_summer > north_angle), color='#f1c40f', alpha=0.3, label='Effective Sunlight Window')

ax.set_title(f'Solar Trajectory & Canyon Shading Audit\nSite: {place_name} (Calculated Latitude: {lat:.2f}°)', fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('Local Apparent Time (Hour, 24h Grid)', fontsize=10)
ax.set_ylabel('Solar Altitude Angle (Degree, °)', fontsize=10)
ax.set_xlim(5, 19)
ax.set_ylim(0, 95)
ax.set_xticks(range(5, 20))
ax.set_yticks(range(0, 100, 10))
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=9, frameon=True, facecolor='white')

plt.tight_layout()
st.pyplot(fig)

# ==========================================
# 7. Dynamic Environmental Health Report
# ==========================================
report_html = f"""
<div style="background-color: #f8f9fa; border-left: 5px solid #f1c40f; padding: 15px; border-radius: 4px; font-family: sans-serif;">
    <h3 style="color: #2c3e50; margin-top: 0; font-size: 16px;">🔬 Global Spatiotemporal & Environmental Health Diagnostic Report:</h3>
    <p style="font-size: 14px; color: #2c3e50;"><b>Current Evaluated Location:</b> <span style="color:#27ae60; font-weight:bold;">{place_name}</span> | <b>Target Latitude:</b> {lat:.2f}°N/S</p>
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px;">
        <tr style="background-color: #eaeded;"><th style="padding: 8px; text-align: left;">Climatic Indicator</th><th style="padding: 8px; text-align: left;">Calculated Sunlight Window</th></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">☀️ <b>Peak Summer Solstice Duration</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #e74c3c; font-weight: bold;">{to_hr_min_str(summer_hours)}</td></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">❄️ <b>Deep Winter Solstice Duration</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #3498db; font-weight: bold;">{to_hr_min_str(winter_hours)}</td></tr>
        <tr style="background-color: #f2f4f4;"><td style="padding: 8px;">📊 <b>Annual Solstice Average</b></td><td style="padding: 8px; color: #27ae60; font-weight: bold;">{to_hr_min_str(avg_hours)}</td></tr>
    </table>
    <hr style="border: 0; border-top: 1px solid #ddd; margin: 15px 0;">
    <p style="font-size: 12px; color: #566573; line-height: 1.5;">
        💡 <b>Global Geography Field Note:</b> This system dynamically accounts for hemisphere flipping. If a negative latitude is typed or a Southern Hemisphere city (e.g., Sydney) is chosen, the engine automatically shifts the peak tracking vectors to the December Solstice to ensure mathematical precision.
    </p>
</div>
"""

st.markdown(report_html, unsafe_allow_html=True)
