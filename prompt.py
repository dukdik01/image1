import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# อัปเดตลิงก์รูปใหม่
images = {
    "หมาป่ากับปั๊ก": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/320px-Cat_poster_1.jpg",
    "นกฮูก": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Chouettes.jpg/250px-Chouettes.jpg"
}

if "selected_image_url" not in st.session_state:
    st.session_state.selected_image_url = None
if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = ""

st.title("แกลเลอรีรูปภาพ")

if not st.session_state.selected_image_url:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_container_width=True)  # ✅ แก้ use_column_width
            if st.button(f"ดูภาพ: {caption}", key=caption):
                st.session_state.selected_image_url = url
                st.session_state.selected_caption = caption
else:
    try:
        response = requests.get(st.session_state.selected_image_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=st.session_state.selected_caption + " (ภาพเต็ม)", use_container_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
    
    if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
        st.session_state.selected_image_url = None
        st.session_state.selected_caption = ""
