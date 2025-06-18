import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

st.set_page_config(page_title="InstaDish | 写真加工デモ", layout="centered")
st.title("📸 InstaDish | 写真加工デモ版")

st.markdown("写真をアップロードすると、自動的に明るさ・コントラスト・シャープネスを補正します。")

uploaded_files = st.file_uploader(
    "画像を選択（複数可）", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

def process_image(image):
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    return image

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        st.image(img, caption=f"元の画像: {file.name}", use_container_width=True)

        processed = process_image(img)
        st.image(processed, caption="加工済み画像", use_container_width=True)

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")

        st.download_button(
            label=f"📥 加工画像をダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"processed_{file.name}",
            mime="image/jpeg",
            key=str(uuid.uuid4())
        )
