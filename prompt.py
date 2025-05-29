import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# รายการ URL รูปภาพ
images = {
    "หมาป่ากับปั๊ก": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/250px-Comparison_of_a_wolf_and_a_pug.png",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/VAN_CAT.png/220px-VAN_CAT.png",
    "นกฮูก": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Owl_on_branch02.jpg/220px-Owl_on_branch02.jpg"
}

st.title("แกลเลอรีรูปภาพ")

# เลือกรูปภาพที่จะแสดงแบบเต็ม
selected_image = st.session_state.get("selected_image", None)

# ถ้ายังไม่มีการเลือกรูปภาพ ให้แสดงตัวอย่าง 3 รูป
if selected_image is None:
    cols = st.columns(3)
    for idx, (caption, url) in enumerate(images.items()):
        with cols[idx]:
            st.image(url, caption=caption, use_column_width=True)
            if st.button(f"ดูภาพ: {caption}"):
                st.session_state.selected_image = url
                st.experimental_rerun()

# ถ้ามีการเลือกรูปภาพ ให้แสดงรูปใหญ่พร้อมปุ่มย้อนกลับ
else:
    response = requests.get(selected_image)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        st.image(img, caption="ภาพแบบเต็ม", use_column_width=True)
        if st.button("🔙 กลับไปหน้ารูปทั้งหมด"):
            st.session_state.selected_image = None
            st.experimental_rerun()
    else:
        st.error("ไม่สามารถโหลดรูปภาพได้")
