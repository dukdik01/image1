import streamlit as st
import requests
from PIL import Image, ImageOps
from io import BytesIO

# อัปเดตลิงก์รูปใหม่
images = {
    "หมาป่ากับปั๊ก": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/800px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg",
    "นกฮูก": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Chouettes.jpg/250px-Chouettes.jpg"
}

# เก็บสถานะ
if "selected_image_url" not in st.session_state:
    st.session_state.selected_image_url = None
if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = ""

# เก็บสถานะสำหรับ flip และขนาด (optional, เพื่อเก็บค่ารีเซต)
if "flip_image" not in st.session_state:
    st.session_state.flip_image = False
if "width" not in st.session_state:
    st.session_state.width = None
if "height" not in st.session_state:
    st.session_state.height = None

st.title("แกลเลอรีรูปภาพ")

if not st.session_state.selected_image_url:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_container_width=True)           
else:
    try:
        # โหลดรูปจาก URL
        response = requests.get(st.session_state.selected_image_url)
        img = Image.open(BytesIO(response.content))

        st.subheader(f"ภาพ: {st.session_state.selected_caption}")

        # กำหนดค่าเริ่มต้น slider ถ้ายังไม่มีค่าเก็บใน session_state
        if st.session_state.width is None:
            st.session_state.width = img.width
        if st.session_state.height is None:
            st.session_state.height = img.height

        # slider สำหรับ resize
        width = st.slider("ปรับความกว้าง (px)", 50, 1000, st.session_state.width)
        height = st.slider("ปรับความสูง (px)", 50, 1000, st.session_state.height)
        st.session_state.width = width
        st.session_state.height = height

        # checkbox flip image
        flip = st.checkbox("กลับภาพ (Flip image)", value=st.session_state.flip_image)
        st.session_state.flip_image = flip

        resized_img = img.resize((width, height))

        if flip:
            resized_img = ImageOps.mirror(resized_img)

        st.image(resized_img, caption=f"{st.session_state.selected_caption} ({width}x{height})", use_container_width=False)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
            # ล้างสถานะทั้งหมด
            st.session_state.selected_image_url = None
            st.session_state.selected_caption = ""
            st.session_state.flip_image = False
            st.session_state.width = None
            st.session_state.height = None
            st.experimental_rerun()

    with col2:
        if st.button("🔄 รีเซตการตั้งค่า"):
            # รีเซต flip และขนาด
            st.session_state.flip_image = False
            st.session_state.width = None
            st.session_state.height = None
            st.experimental_rerun()
