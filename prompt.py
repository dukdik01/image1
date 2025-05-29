import streamlit as st
import requests
from PIL import Image
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

st.title("แกลเลอรีรูปภาพ")

if not st.session_state.selected_image_url:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_container_width=True)
            if st.button(f"ดูภาพ: {caption}", key=caption):
                st.session_state.selected_image_url = url
                st.session_state.selected_caption = caption
                st.experimental_rerun()
else:
    try:
        # โหลดรูปจาก URL
        response = requests.get(st.session_state.selected_image_url)
        img = Image.open(BytesIO(response.content))

        st.subheader(f"ภาพ: {st.session_state.selected_caption}")

        # slider สำหรับ resize
        width = st.slider("ปรับความกว้าง (px)", 50, 1000, img.width)
        height = st.slider("ปรับความสูง (px)", 50, 1000, img.height)

        # Checkbox flip image
        flip = st.checkbox("กลับภาพ (Flip image)")

        resized_img = img.resize((width, height))

        if flip:
            resized_img = ImageOps.mirror(resized_img)  # กลับภาพแนวนอน

        st.image(resized_img, caption=f"{st.session_state.selected_caption} ({width}x{height})", use_container_width=False)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
            st.session_state.selected_image_url = None
            st.session_state.selected_caption = ""
            st.experimental_rerun()
    with col2:
        if st.button("🔄 รีเซตการตั้งค่า"):
            # รีเซตขนาดและ flip
            # เนื่องจาก slider กับ checkbox ไม่ได้เก็บใน session_state โดยตรง
            # ให้ rerun หน้าโดยไม่เปลี่ยนสถานะภาพ
            st.experimental_rerun()
