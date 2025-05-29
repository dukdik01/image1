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
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "resized_image" not in st.session_state:
    st.session_state.resized_image = None

st.title("แกลเลอรีรูปภาพ")

if not st.session_state.selected_image_url:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_container_width=True)
            if st.button(f"ดูภาพ: {caption}", key=caption):
                st.session_state.selected_image_url = url
                st.session_state.selected_caption = caption
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                st.session_state.original_image = img
                st.session_state.resized_image = img
else:
    st.subheader(f"ภาพ: {st.session_state.selected_caption}")
    img = st.session_state.resized_image

    width = st.slider("ปรับความกว้าง (px)", 50, 1000, img.width)
    height = st.slider("ปรับความสูง (px)", 50, 1000, img.height)
    resized_img = st.session_state.original_image.resize((width, height))
    st.session_state.resized_image = resized_img

    # ตัวเลือกการกลับภาพ
    flip_option = st.selectbox("เลือกการกลับภาพ", ["None", "Horizontal", "Vertical"])
    if flip_option == "Horizontal":
        flipped_img = ImageOps.mirror(resized_img)
    elif flip_option == "Vertical":
        flipped_img = ImageOps.flip(resized_img)
    else:
        flipped_img = resized_img

    st.image(flipped_img, caption=f"{st.session_state.selected_caption} ({width}x{height})", use_container_width=False)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 รีเซตรูปภาพ"):
            st.session_state.resized_image = st.session_state.original_image
    with col2:
        if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
            st.session_state.selected_image_url = None
            st.session_state.selected_caption = ""
            st.session_state.original_image = None
            st.session_state.resized_image = None

st.header("🖼️ ผสมภาพ (Blending Images)")

# เลือกภาพที่ 1 และภาพที่ 2 จากรายการ
col1, col2 = st.columns(2)
with col1:
    img1_caption = st.selectbox("เลือกรูปภาพที่ 1", list(images.keys()), key="blend1")
with col2:
    img2_caption = st.selectbox("เลือกรูปภาพที่ 2", list(images.keys()), index=1, key="blend2")

# ความเด่น (ค่าผสม)
alpha = st.slider("ระดับความเด่น (0.0 - 1.0)", 0.0, 1.0, 0.7, step=0.01)

# โหลดภาพทั้งสอง
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGBA")

img1 = load_image(images[img1_caption])
img2 = load_image(images[img2_caption])

# ปรับขนาดให้เท่ากัน
common_size = (min(img1.width, img2.width), min(img1.height, img2.height))
img1 = img1.resize(common_size)
img2 = img2.resize(common_size)

# ผสมภาพ
if dominant_caption == img1_caption:
    blended = Image.blend(img2, img1, alpha)  # img1 เด่น
else:
    blended = Image.blend(img1, img2, alpha)  # img2 เด่น

# แสดงภาพที่ผสม
st.subheader("ภาพที่ผสมแล้ว")
st.image(blended, use_container_width=False)

with st.expander("ดูภาพต้นฉบับ"):
    st.image(img1, caption=f"ภาพที่ 1: {img1_caption}", use_container_width=True)
    st.image(img2, caption=f"ภาพที่ 2: {img2_caption}", use_container_width=True)

