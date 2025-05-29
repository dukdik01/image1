import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# รายการรูปภาพ (URL + caption)
images = {
    "หมาป่ากับปั๊ก": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/320px-Cat_poster_1.jpg",
    "นกฮูก": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Southern_White-Faced_Owl_%28Ptilopsis_granti%29.jpg/320px-Southern_White-Faced_Owl_%28Ptilopsis_granti%29.jpg"
}

# ตรวจสอบค่าจาก session_state
if "selected_image_url" not in st.session_state:
    st.session_state.selected_image_url = None
if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = ""

st.title("แกลเลอรีรูปภาพ")

# ถ้ายังไม่เลือกรูปภาพ
if not st.session_state.selected_image_url:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_column_width=True)
            if st.button(f"ดูภาพ: {caption}", key=caption):
                st.session_state.selected_image_url = url
                st.session_state.selected_caption = caption

# ถ้าเลือกรูปภาพแล้ว ให้แสดงเต็ม
else:
    try:
        response = requests.get(st.session_state.selected_image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=st.session_state.selected_caption + " (ภาพเต็ม)", use_column_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
    
    # ปุ่มย้อนกลับ
    if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
        st.session_state.selected_image_url = None
        st.session_state.selected_caption = ""
