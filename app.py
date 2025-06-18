# app.py
import streamlit as st
from PIL import Image
import io
import uuid
from config import BUSINESS_TYPES, TARGET_AUDIENCES
from layout import show_photo_advice
from processor import process_and_classify_image

st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")
st.title("InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案")
st.caption("by Masashi")

st.header("1. 写真をアップロード（複数可）")
uploaded_files = st.file_uploader(
    "料理・ドリンクなどの写真を選んでください（複数選択OK）",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

st.header("2. 業態とターゲット層を選択")
business_type = st.selectbox("業態を選んでください", BUSINESS_TYPES)
target_audience = st.selectbox("ターゲット層を選んでください", TARGET_AUDIENCES)

show_photo_advice()

if uploaded_files and st.button("📸 画像を加工してハッシュタグを提案"):
    for i, file in enumerate(uploaded_files):
        key = str(uuid.uuid4())
        image = Image.open(file).convert("RGB")
        st.image(image, caption=f"元の画像: {file.name}", use_container_width=True)

        result = process_and_classify_image(image, business_type, target_audience, key)
        st.image(result["processed_image"], caption="加工済み画像", use_container_width=True)

        if result["confidence"] < 0.5:
            st.warning(f"画像分類の信頼度が低いため、内容を選んでください（信頼度 {result['confidence']:.2f}）")
            result["label"] = st.selectbox("📌 内容ジャンルを選択", result["all_labels"], index=0, key=f"select_{key}")
        else:
            st.markdown(f"📌 自動判定ジャンル：**{result['label']}**（信頼度 {result['confidence']:.2f}）")

        st.subheader("📝 自動キャプション")
        st.markdown(result["caption"])

        st.subheader("📌 ハッシュタグ候補")
        st.code(" ".join(result["hashtags"]))

        img_bytes = io.BytesIO()
        result["processed_image"].save(img_bytes, format="JPEG")
        st.download_button(
            label=f"📥 加工画像をダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"instadish_{file.name}",
            mime="image/jpeg",
            key=f"download_{key}"
        )
else:
    st.info("画像をアップロードしてください。")
