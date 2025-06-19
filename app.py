import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

# ページ設定
st.set_page_config(page_title="InstaDish | 写真加工デモ", layout="centered")

# カスタムCSSでスタイル調整
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom right, #f8e1dc, #fbeee6);
            font-family: "Helvetica Neue", sans-serif;
        }
        .title {
            font-size: 2.2em;
            text-align: center;
            margin-bottom: 1em;
            color: #333;
        }
        .card {
            background-color: white;
            padding: 1.5em;
            border-radius: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2em;
        }
        .section-title {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 0.5em;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="title">📸 InstaDish | 写真加工デモ版</div>', unsafe_allow_html=True)

# アップロードカード
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">1. 写真をアップロード（複数可）</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)

def process_image(image):
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    return image

# 画像処理カード
if uploaded_files:
    for file in uploaded_files:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">📷 元の画像: {file.name}</div>', unsafe_allow_html=True)
        img = Image.open(file).convert("RGB")
        st.image(img, use_container_width=True)

        processed = process_image(img)
        st.markdown('<div class="section-title">✨ 加工済み画像</div>', unsafe_allow_html=True)
        st.image(processed, use_container_width=True)

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")

        st.download_button(
            label=f"📥 加工画像をダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"processed_{file.name}",
            mime="image/jpeg",
            key=str(uuid.uuid4())
        )
        st.markdown('</div>', unsafe_allow_html=True)
