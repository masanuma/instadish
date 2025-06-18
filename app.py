import streamlit as st
import uuid
from processor import process_image
from config import BUSINESS_TYPES, TARGET_AUDIENCES
from PIL import Image
import io

st.set_page_config(page_title="InstaDish | 写真加工デモ版", layout="centered")

with st.container():
    st.markdown("""
    <h1 style='text-align: center;'>🍽️ InstaDish</h1>
    <p style='text-align: center; color: gray;'>飲食店向けInstagram画像加工＋ハッシュタグ提案</p>
    """, unsafe_allow_html=True)

# --- UI Section: Upload ---
st.markdown("### 1️⃣ 写真をアップロード（複数可）")
st.caption("料理・ドリンクなどの写真を選んでください")
uploaded_files = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# --- UI Section: Select ---
with st.expander("📌 業態とターゲット層を選んでください"):
    col1, col2 = st.columns(2)
    with col1:
        business_type = st.radio("業態", BUSINESS_TYPES, horizontal=True)
    with col2:
        target_audience = st.radio("", TARGET_AUDIENCES, horizontal=True)

# --- UI Section: Processing ---
if uploaded_files:
    st.markdown("### 2️⃣ アップロード画像のプレビューと加工")
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        st.image(img, caption=f"元の画像: {file.name}", use_container_width=True)

        processed = process_image(img)
        st.image(processed, caption="✨ 加工済み画像", use_container_width=True)

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")

        st.download_button(
            label=f"📥 ダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"processed_{file.name}",
            mime="image/jpeg",
            key=str(uuid.uuid4())
        )

# --- Footer ---
st.markdown("""
---
<p style='text-align: center; color: gray;'>InstaDish by Masashi ｜ ご意見・ご感想はお気軽にどうぞ</p>
""", unsafe_allow_html=True)
