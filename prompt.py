import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# รายการ URL รูปภาพ (เปลี่ยนลิงก์นกฮูกให้ใช้ได้)
images = {
    "หมาป่ากับปั๊ก": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/320px-Cat_poster_1.jpg",
    "นกฮูก": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Southern_White-Faced_Owl_%28Ptilopsis_granti%29.jpg/320px-Southern_White-Faced_Owl_%28Ptilopsis_granti%29.jpg"
}

# ตรวจสอบว่ามีการเลือกภาพหรือยัง
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

st.title("แกลเลอรีรูปภาพ")

if st.session_state.selected_image is None:
    # แสดงรูปภาพ 3 รูป
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_column_width=True)
            if st.button(f"ดูภาพ: {caption}", key=caption):
                st.session_state.selected_image = url
                st.experimental_rerun()
else:
    # แสดงรูปภาพเต็ม
    try:
        response = requests.get(st.session_state.selected_image)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption="ภาพแบบเต็ม", use_column_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
    
    if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
        st.session_state.selected_image = None
        st.experimental_rerun()
