# InstaDish - コンパクトUIレイアウト調整版

import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

st.set_page_config(
    page_title="InstaDish | 写真加工デモ",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- スタイル修正：余白最小化・レイアウト詰め調整 ---
st.markdown("""
    <style>
        .stApp {
            background-color: #fde7dc !important;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .title {
            font-size: 2.2em;
            text-align: center;
            font-weight: bold;
            color: #222;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 1.5em;
        }
        .upload-box {
            border: 2px dashed #ccc;
            border-radius: 12px;
            padding: 1.2em;
            text-align: center;
            color: #333;
            font-weight: bold;
            margin-bottom: 0.5em;
            background-color: #fff;
        }
        .stButton>button {
            background-color: #347EFF;
            color: white;
            font-weight: bold;
            padding: 0.4em 1.2em;
            border-radius: 10px;
            margin-top: 0.5em;
            margin-bottom: 0.5em;
        }
        label, .stSelectbox label {
            font-size: 0.9em !important;
            margin-bottom: 0.3em !important;
        }
        .stSelectbox, .stFileUploader, .stButton {
            margin-bottom: 0.8em !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- ヘッダー ---
st.markdown("""
<div class='title'>InstaDish</div>
<div class='subtitle'>飲食店向け画像加工＋ハッシュタグ提案</div>
""", unsafe_allow_html=True)

# --- セクション 1: アップロード ---
with st.container():
    st.markdown("### 1 写真アップロード")
    st.markdown("""
    <div class='upload-box'>📷<br><span>画像を選んでください</span></div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# --- セクション 2: 業態とターゲット選択 ---
with st.container():
    st.markdown("### 2 業態・ターゲット選択")
    business_type = st.selectbox("", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
    target_audience = st.selectbox("", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])

# --- セクション 3: 実行・結果 ---
with st.container():
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
