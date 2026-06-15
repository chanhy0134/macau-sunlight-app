import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Set Matplotlib to use standard sans-serif font (Ensures no rendering issues)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # Render negative signs normally

# 2. Configure Web Page Title & Layout
st.set_page_config(page_title="Macau Sunlight Calculator", layout="centered")
st.title("☀️ Macao Urban Canyon Microclimate & Sunlight Calculator")
st.write("Welcome to the Historical Geography Study Tour Big Data Tool. Input your field data in the sidebar.")

# 3. Create Sidebar Input Fields (All English UI)
st.sidebar.header("📋 Input Investigation Parameters")
place_name = st.sidebar.text_input("Location Name:", "Toi San District / Estrada da Victoria 18")
street_width = st.sidebar.number_input("Street Width (m):", value=5.0, step=0.1)
height = st.sidebar.number_input("Observer Height (m):", value=1.8, step=0.1)
south_angle = st.sidebar.slider("South Building Angle (°):", min_value=0, max_value=90, value=45)
north_angle = st.sidebar.slider("North Building Angle (°):", min_value=0, max_value=90, value=65)

# 4. Core Spatiotemporal Calculations (Macau Baseline Latitude: 22.20° N)
lat = 22.20  
delta_summer = 23.43   # Summer Solstice Declination
delta_winter = -23.43  # Winter Solstice Declination

# Time Axis: From 05:00 to 19:00, sampled every 5 minutes (170 points total)
hours = np.linspace(5, 19, 170)
alpha_summer = []
alpha_winter = []

for hr in hours:
    # Convert local time to Hour Angle (h)
    h = (hr - 12) * 15
    h_rad = np.radians(h)
    lat_rad = np.radians(lat)
    
    # Summer Solstice Formula
    sin_alpha_s = (np.sin(lat_rad) * np.sin(np.radians(delta_summer)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_summer)) * np.cos(h_rad))
    alpha_summer.append(max(0, np.degrees(np.arcsin(sin_alpha_s))))
    
    # Winter Solstice Formula
    sin_alpha_w = (np.sin(lat_rad) * np.sin(np.radians(delta_winter)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_winter)) * np.cos(h_rad))
    alpha_winter.append(max(0, np.degrees(np.arcsin(sin_alpha_w))))
    
alpha_summer = np.array(alpha_summer)
alpha_winter = np.array(alpha_winter)

# Calculate duration above thresholds
dt = (19 - 5) / 170
summer_hours = np.sum(alpha_summer > north_angle) * dt
winter_hours = np.sum(alpha_winter > south_angle) * dt
avg_hours = (summer_hours + winter_hours) / 2

# Helper function to format time strings
def to_hr_min_str(h_val):
    hr = int(h_val)
    mn = int(round((h_val - hr) * 60))
    if hr == 0 and mn == 0: 
        return "0 hr 0 min (Permanent Shadow)"
    return f"{hr} hr {mn} min"

# 5. Plot Spatiotemporal Curve Chart
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=110)

# Plot trajectories
ax.plot(hours, alpha_summer, color='#e74c3c', linewidth=2.5, label='Summer Solstice (Max Track)')
ax.plot(hours, alpha_winter, color='#3498db', linewidth=2.5, label='Winter Solstice (Min Track)')

# Plot critical control lines
ax.axhline(y=north_angle, color='#c0392b', linestyle='--', linewidth=1.5, label=f'Summer Control Line ({north_angle}°)')
ax.axhline(y=south_angle, color='#2980b9', linestyle='--', linewidth=1.5, label=f'Winter Control Line ({south_angle}°)')

# Fill the effective window
ax.fill_between(hours, alpha_summer, north_angle, where=(alpha_summer > north_angle), color='#f1c40f', alpha=0.3, label='Summer Sunlight Window')

# Chart decorations
ax.set_title(f'Solar Altitude Angle & Daylight Window: {place_name}', fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel('Local Time (Hour, 24h Grid)', fontsize=10)
ax.set_ylabel('Solar Altitude Angle (Degree, °)', fontsize=10)
ax.set_xlim(5, 19)
ax.set_ylim(0, 95)
ax.set_xticks(range(5, 20))
ax.set_yticks(range(0, 100, 10))
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=9, frameon=True, facecolor='white')

plt.tight_layout()

# Render graph on streamlit
st.pyplot(fig)

# 6. Render Environmental Health Diagnostic Report (Ensured perfect block closure)
report_html = f"""
<div style="background-color: #f8f9fa; border-left: 5px solid #f1c40f; padding: 15px; border-radius: 4px; font-family: sans-serif;">
    <h3 style="color: #2c3e50; margin-top: 0; font-size: 16px;">🔬 Environmental Health & Urban Geometry Diagnostic Report:</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px;">
        <tr style="background-color: #eaeded;"><th style="padding: 8px; text-align: left;">Indicator / Metric</th><th style="padding: 8px; text-align: left;">Calculated Duration</th></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">☀️ <b>Max Sunlight Duration (Summer Solstice)</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #e74c3c; font-weight: bold;">{to_hr_min_str(summer_hours)}</td></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">❄️ <b>Max Sunlight Duration (Winter Solstice)</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #3498db; font-weight: bold;">{to_hr_min_str(winter_hours)}</td></tr>
        <tr style="background-color: #f2f4f4;"><td style="padding: 8px;">📊 <b>Annual Seasonal Average Duration</b></td><td style="padding: 8px; color: #27ae60; font-weight: bold;">{to_hr_min_str(avg_hours)}</td></tr>
    </table>
    <hr style="border: 0; border-top: 1px solid #ddd; margin: 15px 0;">
    <p style="font-size: 12px; color: #566573; line-height: 1.5;">
        💡 <b>Educational Note for Instructors:</b> In environmental health studies, <b>a minimum of 2 hours of direct sunlight is recognized as the biological baseline</b> required to effectively eliminate pathogens (such as Mycobacterium tuberculosis) and mitigate mold breeding cycles through absolute dehumidification.
    </p>
</div>
"""

st.markdown(report_html, unsafe_allow_html=True)
