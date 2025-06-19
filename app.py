# このファイルは、InstaDishの新UI仕様に基づくStreamlitアプリのベースコードです。
# ユーザー提供のモックアップに忠実なデザインとモバイル最適化を実装します。

import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

st.set_page_config(
    page_title="InstaDish | 写真加工デモ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSSでスマホUI最適化
st.markdown("""
    <style>
    body {
        background-color: #f8f7f3;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton>button, .stDownloadButton>button {
        border-radius: 16px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #333333;
        margin-bottom: 0.6rem;
    }
    .upload-section, .preview-section {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📸 InstaDish</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>飲食店向けInstagram用の写真自動加工デモ</p>", unsafe_allow_html=True)

# アップロードセクション
st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
st.subheader("画像アップロード")
uploaded_files = st.file_uploader("画像を選択（複数可）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

# 加工処理関数
def process_image(image):
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    return image

# プレビューセクション
if uploaded_files:
    st.markdown("<div class='preview-section'>", unsafe_allow_html=True)
    st.subheader("加工プレビュー")
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
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("画像をアップロードしてください。")
