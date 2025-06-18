import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import uuid

st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")

# カスタムスタイル
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 480px;
        margin: auto;
    }
    h1 {
        font-size: clamp(1.5rem, 5vw, 2.2rem);
        text-align: center;
    }
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.75em 1.5em;
        border-radius: 10px;
        background-color: #ffedd5;
        color: #111827;
    }
    /* D&D領域非表示 */
    [data-testid="stFileUploader"] > div:first-child {
        display: none !important;
    }
    /* アップロードボタンの日本語化 */
    [data-testid="stFileUploader"] button {
        font-size: 1.1rem;
    }
    [data-testid="stFileUploader"] button:after {
        content: "ファイル選択";
        visibility: visible;
        display: inline;
    }
    [data-testid="stFileUploader"] button > div {
        visibility: hidden;
    }
    /* セレクタの上下余白を縮める */
    div[data-testid="stSelectbox"] {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案</h1>", unsafe_allow_html=True)
st.caption("by Masashi")

# --- セクション 1 ---
st.markdown("""
<div style='background-color:#fef3c7; padding: 1.5em; border-radius: 12px;'>
  <h3 style='margin:0; font-size:clamp(1rem, 4vw, 1.3rem); white-space: nowrap;'>1. 📷 写真をアップロード（複数可）</h3>
""", unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

if not uploaded_files:
    st.markdown("<p style='text-align:center; color:#666;'>⬆️ 上のボタンから画像を選択してください。</p>", unsafe_allow_html=True)

# --- セクション 2 ---
st.markdown("""
<div style='background-color:#e0f2fe; padding: 1.5em; border-radius: 12px;'>
  <h3 style='margin:0; font-size:clamp(1rem, 4vw, 1.3rem); white-space: nowrap;'>2. 🏷️ 業態とターゲット層</h3>
""", unsafe_allow_html=True)
business_type = st.selectbox("", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
target_audience = st.selectbox("", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])
st.markdown("</div>", unsafe_allow_html=True)

# --- 撮影アドバイス ---
if uploaded_files:
    with st.expander("📸 撮影アドバイス"):
        st.markdown("""
        ### 📸 ジャンル別おすすめ撮影ポイント
        - **ドリンク**：グラスの高さを活かして斜め下から
        - **カフェメニュー**：真上から全体をきれいに
        - **バーの雰囲気**：ラベルや照明を活かしたローアングル
        - **複数皿の料理**：奥行きを出すように45度で
        - **パッケージやラベルが重要な場合**：中央配置＋明るさ重視
        """)

# --- 加工ボタンとアップロード処理 ---
if uploaded_files:
    if st.button("🎨 加工してハッシュタグを提案"):
        for file in uploaded_files:
            image = Image.open(file).convert("RGB")
            st.image(image, caption=f"元画像: {file.name}", use_container_width=True)
            enhancer = ImageEnhance.Brightness(image).enhance(1.2)
            enhancer = ImageEnhance.Contrast(enhancer).enhance(1.3)
            processed = ImageEnhance.Sharpness(enhancer).enhance(2.0)
            st.image(processed, caption="加工済み画像", use_container_width=True)

            img_bytes = io.BytesIO()
            processed.save(img_bytes, format="JPEG")
            st.download_button(
                label=f"📅 加工画像をダウンロード（{file.name}）",
                data=img_bytes.getvalue(),
                file_name=f"instadish_{file.name}",
                mime="image/jpeg",
                key=f"dl_{uuid.uuid4()}"
            )
