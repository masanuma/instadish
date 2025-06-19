# InstaDish - スマホUI修正版

import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

st.set_page_config(
    page_title="InstaDish | 写真加工デモ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- スタイル調整（背景色・カードレイアウト・余白修正） ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(160deg, #fff1e8 0%, #fde7dc 100%) !important;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        .title {
            font-size: 2.5em;
            text-align: center;
            font-weight: bold;
            color: #222;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2em;
        }
        .section {
            background-color: white;
            padding: 1.2em;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 2em;
        }
        .upload-box {
            border: 2px dashed #ccc;
            border-radius: 12px;
            padding: 2em;
            text-align: center;
            color: #333;
            font-weight: bold;
        }
        .upload-box span {
            font-size: 1.1em;
        }
        .stButton>button {
            background-color: #347EFF;
            color: white;
            font-weight: bold;
            padding: 0.6em 1.5em;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- ヘッダー ---
st.markdown("""
<div class='title'>InstaDish</div>
<div class='subtitle'>飲食店向け画像加工＋ハッシュタグ提案</div>
""", unsafe_allow_html=True)

# --- セクション 1: アップロード ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### 1 写真アップロード", unsafe_allow_html=True)
st.markdown("""
<div class='upload-box'>
    📷<br><span>画像を選んでください</span>
</div>
""", unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- セクション 2: 業態とターゲット選択 ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### 2 業態・ターゲット選択", unsafe_allow_html=True)
business_type = st.selectbox("", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
target_audience = st.selectbox("", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])
st.markdown("</div>", unsafe_allow_html=True)

# --- セクション 3: 実行ボタン＋加工結果 ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
if st.button("画像を加工"):
    if uploaded_files:
        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            processed = ImageEnhance.Brightness(img).enhance(1.2)
            processed = ImageEnhance.Contrast(processed).enhance(1.3)
            processed = ImageEnhance.Sharpness(processed).enhance(2.0)

            st.image(img, caption=f"元の画像: {file.name}", use_container_width=True)
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
st.markdown("</div>", unsafe_allow_html=True)
