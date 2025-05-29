st.header("🖼️ ผสมภาพ (Blending Images)")

# เลือกภาพที่ 1 และภาพที่ 2 จากรายการ
col1, col2 = st.columns(2)
with col1:
    img1_caption = st.selectbox("เลือกรูปภาพที่ 1", list(images.keys()), key="blend1")
with col2:
    img2_caption = st.selectbox("เลือกรูปภาพที่ 2", list(images.keys()), index=1, key="blend2")

# เลือกภาพที่เด่น
dominant_caption = st.radio("เลือกรูปที่ต้องการให้เด่น", [img1_caption, img2_caption], index=0)

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
