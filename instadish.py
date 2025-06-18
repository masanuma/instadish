import streamlit as st
from PIL import Image, ImageEnhance
import io
import uuid

st.set_page_config(page_title="InstaDish | スマホ対応UI", layout="centered")

# スタイル調整
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 480px;
        margin: auto;
    }
    h1 {
        white-space: nowrap;
    }
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.75em 1.5em;
        border-radius: 10px;
        background-color: #ffedd5;
        color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>InstaDish 🍽️</h1>", unsafe_allow_html=True)
st.caption("飲食店向けInstagram画像加工＋ハッシュタグ提案")

# セクション1：アップロード
st.markdown("""
<div style='background-color:#fef3c7; padding: 1.5em; border-radius: 12px;'>
<h3 style='margin:0; margin-bottom:1em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>1. 📷 写真をアップロード（複数可）</h3>
""", unsafe_allow_html=True)
uploaded_files = st.file_uploader("画像を選択してください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

# セクション2：業態とターゲット
st.markdown("""
<div style='background-color:#e0f2fe; padding: 1.5em; border-radius: 12px;'>
<h3 style='margin:0; margin-bottom:1em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>2. 🏷️ 業態とターゲット層</h3>
""", unsafe_allow_html=True)
business_type = st.selectbox("業態", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
target_audience = st.selectbox("ターゲット層", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])
with st.expander("📸 撮影アドバイス"):
    st.markdown("""
    - **ドリンク**：グラスの高さを活かして斜め下から
    - **カフェメニュー**：真上から全体をきれいに
    - **バーの雰囲気**：ラベルや照明を活かしたローアングル
    - **複数皿の料理**：奥行きを出すように45度で
    - **ラベル重視**：中央配置＋明るさ重視
    """)
st.markdown("</div>", unsafe_allow_html=True)

def process_image(image):
    enhancer = ImageEnhance.Brightness(image).enhance(1.2)
    enhancer = ImageEnhance.Contrast(enhancer).enhance(1.3)
    return ImageEnhance.Sharpness(enhancer).enhance(2.0)

def generate_hashtags(business, audience):
    tags = ["#InstaFood", "#グルメ", "#食べスタグラム", "#おしゃれごはん"]
    if business == "カフェ": tags += ["#カフェ巡り", "#CafeTime"]
    if business == "居酒屋": tags += ["#居酒屋メシ", "#日本酒好き"]
    if business == "バー": tags += ["#BarTime", "#クラフトジン"]
    if business == "和食": tags += ["#和食", "#JapaneseCuisine"]
    if business == "洋食": tags += ["#洋食ランチ", "#WesternFood"]
    if business == "中華": tags += ["#中華料理", "#DimSum"]
    if audience == "インスタ好き": tags += ["#映えグルメ", "#フォトジェニック"]
    if audience == "外国人観光客": tags += ["#VisitJapan", "#TokyoFoodie"]
    if audience == "会社員": tags += ["#ランチタイム", "#お疲れ様です"]
    if audience == "シニア": tags += ["#落ち着いた時間", "#ゆっくりごはん"]
    if audience == "OL": tags += ["#女子会ごはん", "#OLランチ"]
    return sorted(set(tags))[:20]

if uploaded_files and st.button("✨ 加工してハッシュタグを提案"):
    for file in uploaded_files:
        image = Image.open(file).convert("RGB")
        st.image(image, caption="元画像", use_container_width=True)
        processed = process_image(image)
        st.image(processed, caption="加工済み画像", use_container_width=True)

        st.subheader("📌 ハッシュタグ")
        st.code(" ".join(generate_hashtags(business_type, target_audience)))

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")
        st.download_button(
            label=f"📥 {file.name} をダウンロード",
            data=img_bytes.getvalue(),
            file_name=f"instadish_{file.name}",
            mime="image/jpeg",
            key=f"dl_{uuid.uuid4()}"
        )
else:
    st.info("画像をアップロードしてください。")
