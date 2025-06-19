import streamlit as st
import uuid
from processor import process_image
from config import BUSINESS_TYPES, TARGET_AUDIENCES
from PIL import Image
import io

st.set_page_config(page_title="InstaDish | スマホ対応画像加工", layout="centered")

st.markdown("""
<style>
    .insta-header {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 0;
    }
    .insta-subtitle {
        text-align: center;
        font-size: 14px;
        color: gray;
        margin-top: 0;
    }
    .upload-box {
        border: 2px dashed #ccc;
        padding: 20px;
        text-align: center;
        border-radius: 12px;
        background-color: #fffdfc;
        margin-bottom: 16px;
    }
    .section-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
</style>
<div class='insta-header'>InstaDish</div>
<div class='insta-subtitle'>飲食店向け画像加工＋ハッシュタグ提案</div>
""", unsafe_allow_html=True)

# --- セクション1: 写真アップロード ---
st.markdown("<div class='section-title'>① 写真アップロード</div>", unsafe_allow_html=True)
st.markdown("""
<div class='upload-box'>📷<br><span style='color:gray;'>画像を選んでください</span></div>
""", unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# --- セクション2: 業態とターゲット層選択 ---
st.markdown("<div class='section-title'>② 業態・ターゲット選択</div>", unsafe_allow_html=True)
business_type = st.selectbox("", BUSINESS_TYPES)
target_audience = st.selectbox("", TARGET_AUDIENCES)

# --- 実行ボタン ---
if st.button("📸 画像を加工"):
    if uploaded_files:
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
    else:
        st.warning("画像をアップロードしてください。")

# --- フッター ---
st.markdown("""
---
<p style='text-align: center; color: gray;'>InstaDish by Masashi ｜ ご意見・ご感想はお気軽にどうぞ</p>
""", unsafe_allow_html=True)
