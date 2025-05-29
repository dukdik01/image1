import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv5s
model = YOLO("yolov8n.pt")

st.title("🔍 ตรวจจับวัตถุในภาพ (Object Detection)")

# โหมดการเลือกภาพ
mode = st.radio("เลือกวิธีการนำเข้าภาพ", ["📤 Upload", "🌐 URL"])

image = None

# โหลดภาพจาก upload
if mode == "📤 Upload":
    uploaded_file = st.file_uploader("อัปโหลดภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# โหลดภาพจาก URL
elif mode == "🌐 URL":
    url = st.text_input("ใส่ URL ของภาพ")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {e}")

# แสดงภาพและวิเคราะห์
if image is not None:
    st.image(image, caption="ภาพที่คุณเลือก", use_column_width=True)

    # ตรวจจับวัตถุ
    st.subheader("🔍 วัตถุที่ตรวจพบ")
    results = model(image)

    # แสดงวัตถุที่ตรวจพบ
    labels = results[0].names
    detected_classes = set()
    for box in results[0].boxes:
        cls_id = int(box.cls[0].item())
        detected_classes.add(labels[cls_id])

    if detected_classes:
        st.success(f"พบวัตถุดังต่อไปนี้: {', '.join(detected_classes)}")
    else:
        st.warning("ไม่พบวัตถุใดในภาพ")

    # แสดงภาพพร้อมกล่อง object detection
    img_with_boxes = results[0].plot()
    st.image(img_with_boxes, caption="วัตถุที่ตรวจพบ", use_column_width=True)
