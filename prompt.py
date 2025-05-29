import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ตั้งค่าหัวข้อ
st.title("แสดงรูปภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png"

# ดาวน์โหลดรูปภาพ
response = requests.get(image_url)
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    st.image(img, caption="หมาป่ากับปั๊ก", use_column_width=True)
else:
    st.error("ไม่สามารถดาวน์โหลดรูปภาพได้")
