import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. 設定 Matplotlib 使用標準 sans-serif 字型（確保英文網頁渲染無亂碼）
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 正常顯示負號

# 2. 設定網頁標題與佈局
st.set_page_config(page_title="Macau Sunlight Calculator", layout="centered")
st.title("☀️ Macao Urban Canyon Microclimate & Sunlight Calculator")
st.write("Welcome to the Historical Geography Study Tour Big Data Tool. Input your field data in the sidebar.")

# 3. 建立網頁側邊欄輸入欄位 (All English UI)
st.sidebar.header("📋 Input Investigation Parameters")
place_name = st.sidebar.text_input("Location Name:", "Toi San District / Estrada da Victoria 18")
street_width = st.sidebar.number_input("Street Width (m):", value=5.0, step=0.1)
height = st.sidebar.number_input("Observer Height (m):", value=1.8, step=0.1)
south_angle = st.sidebar.slider("South Building Angle (°):", min_value=0, max_value=90, value=45)
north_angle = st.sidebar.slider("North Building Angle (°):", min_value=0, max_value=90, value=65)

# 4. 核心天文地理學幾何計算 (澳門基準緯度: 北緯 22.20°)
lat = 22.20  
delta_summer = 23.43   # 夏至赤緯
delta_winter = -23.43  # 冬至赤緯

# 時間軸：清晨 05:00 到晚上 19:00，每 5 分鐘採樣一個點 (共 170 個點)
hours = np.linspace(5, 19, 170)
alpha_summer = []
alpha_winter = []

for hr in hours:
    # 將地方時轉換為地方時角 h
    h = (hr - 12) * 15
    h_rad = np.radians(h)
    lat_rad = np.radians(lat)
    
    # 夏至太陽高度角公式
    sin_alpha_s = (np.sin(lat_rad) * np.sin(np.radians(delta_summer)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_summer)) * np.cos(h_rad))
    alpha_summer.append(max(0, np.degrees(np.arcsin(sin_alpha_s))))
    
    # 冬至太陽高度角公式
    sin_alpha_w = (np.sin(lat_rad) * np.sin(np.radians(delta_winter)) + 
                   np.cos(lat_rad) * np.cos(np.radians(delta_winter)) * np.cos(h_rad))
    alpha_winter.append(max(0, np.degrees(np.arcsin(sin_alpha_w))))
    
alpha_summer = np.array(alpha_summer)
alpha_winter = np.array(alpha_winter)

# 計算高於大廈阻擋控制線的有效日照時數 (點數乘以時間間隔)
dt = (19 - 5) / 170
summer_hours = np.sum(alpha_summer > north_angle) * dt
winter_hours = np.sum(alpha_winter > south_angle) * dt
avg_hours = (summer_hours + winter_hours) / 2

# 格式化時間為英文字串的輔助函數
def to_hr_min_str(h_val):
    hr = int(h_val)
    mn = int(round((h_val - hr) * 60))
    if hr == 0 and mn == 0: 
        return "0 hr 0 min (Permanent Shadow)"
    return f"{hr} hr {mn} min"

# 5. 繪製精美時空幾何曲線圖
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=110)

# 畫出夏至與冬至拋物線
ax.plot(hours, alpha_summer, color='#e74c3c', linewidth=2.5, label='Summer Solstice (Max Track)')
ax.plot(hours, alpha_winter, color='#3498db', linewidth=2.5, label='Winter Solstice (Min Track)')

# 畫出採光臨界控制線
ax.axhline(y=north_angle, color='#c0392b', linestyle='--', linewidth=1.5, label=f'Summer Control Line ({north_angle}°)')
ax.axhline(y=south_angle, color='#2980b9', linestyle='--', linewidth=1.5, label=f'Winter Control Line ({south_angle}°)')

# 填滿夏季有效日照的黃金窗口
ax.fill_between(hours, alpha_summer, north_angle, where=(alpha_summer > north_angle), color='#f1c40f', alpha=0.3, label='Summer Sunlight Window')

# 圖表外觀美化
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

# 在網頁上渲染圖表
st.pyplot(fig)

# 6. 在網頁下方顯示環境衛生學診斷報告
st.markdown(f"""
<div style="background-color: #f8f9fa; border-left: 5px solid #f1c40f; padding: 15px; border-radius: 4px; font-family: sans-serif;">
    <h3 style="color: #2c3e50; margin-top: 0; font-size: 16px;">🔬 Environmental Health & Urban Geometry Diagnostic Report:</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px;">
        <tr style="background-color: #eaeded;"><th style="padding: 8px; text-align: left;">Indicator / Metric</th><th style="padding: 8px; text-align: left;">Calculated Duration</th></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">☀️ <b>Max Sunlight Duration (Summer Solstice)</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #e74c3c; font-weight: bold;">{to_hr_min_str(summer_hours)}</td></tr>
        <tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">❄️ <b>Max Sunlight Duration (Winter Solstice)</b></td><td style="padding: 8px; border-bottom: 1px solid #ddd; color: #3498db; font-weight: bold;">{to_hr_min_str(winter_hours)}</td></tr>
        <tr style="background-color: #f2
