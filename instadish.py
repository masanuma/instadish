# trigger rebuild
import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import cv2
import torch
import clip
import uuid

st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")
st.title("InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案")
st.caption("by Masashi")

st.header("1. 写真をアップロード（複数可）")
uploaded_files = st.file_uploader("料理・ドリンクなどの写真を選んでください（複数選択OK）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

st.header("2. 業態とターゲット層を選択")
business_type = st.selectbox("業態を選んでください", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
target_audience = st.selectbox("ターゲット層を選んでください", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])

with st.expander("📷 撮影アドバイスを見る"):
    st.markdown("""
    ### 📸 ジャンル別おすすめ撮影ポイント
    - **ドリンク**：グラスの高さを活かして斜め下から
    - **カフェメニュー**：真上から全体をきれいに
    - **バーの雰囲気**：ラベルや照明を活かしたローアングル
    - **複数皿の料理**：奥行きを出すように45度で
    - **パッケージやラベルが重要な場合**：中央配置＋明るさ重視
    """)

def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

def classify_image_clip(image):
    class_prompts = [
        "a bottle of gin", "a bottle of whisky", "a bottle of rum", "a bottle of sake",
        "a glass of wine", "a glass of beer", "a cocktail", "a bar counter",
        "a cup of coffee", "a slice of cake", "a bowl of ramen", "a sushi platter"
    ]
    model, preprocess, device = load_clip_model()
    inputs = torch.cat([clip.tokenize(f"{c}") for c in class_prompts]).to(device)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        logits_per_image, _ = model(image_input, inputs)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]
    best_idx = int(np.argmax(probs))
    return class_prompts[best_idx], probs[best_idx], class_prompts

def generate_caption(label):
    phrases = {
        "a bottle of gin": "こだわりのクラフトジンで夜を彩る一杯を。",
        "a bottle of whisky": "芳醇な香りが広がるウイスキーをどうぞ。",
        "a bottle of rum": "深いコクが魅力のラムで乾杯。",
        "a bottle of sake": "日本の味をそのままに、純米酒のひととき。",
        "a glass of wine": "大人の夜を演出する赤ワインとともに。",
        "a glass of beer": "仕事終わりの一杯にぴったりなビール。",
        "a cocktail": "夜の時間にぴったりな一杯を。",
        "a bar counter": "静かな夜にしっとりと。",
        "a cup of coffee": "午後の休息に、ほっとひと息。",
        "a slice of cake": "甘い時間をお楽しみください。",
        "a bowl of ramen": "スープまで飲み干したくなる美味しさ。",
        "a sushi platter": "新鮮なネタが自慢の一貫をどうぞ。"
    }
    return phrases.get(label, "おすすめの一品をぜひご賞味ください！")

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

def process_image(image):
    enhancer = ImageEnhance.Brightness(image).enhance(1.2)
    enhancer = ImageEnhance.Contrast(enhancer).enhance(1.3)
    return ImageEnhance.Sharpness(enhancer).enhance(2.0)

if uploaded_files and st.button("📸 画像を加工してハッシュタグを提案"):
    for i, file in enumerate(uploaded_files):
        unique_key = str(uuid.uuid4())
        image = Image.open(file).convert("RGB")
        st.image(image, caption=f"元の画像: {file.name}", use_container_width=True)

        processed = process_image(image)
        st.image(processed, caption="加工済み画像", use_container_width=True)

        label, conf, all_labels = classify_image_clip(image)

        if conf < 0.5:
            st.warning(f"画像分類の信頼度が低いため、内容を選んでください（信頼度 {conf:.2f}）")
            label = st.selectbox("📌 内容ジャンルを選択", all_labels, index=0, key=f"select_{unique_key}")
        else:
            st.markdown(f"📌 自動判定ジャンル：**{label}**（信頼度 {conf:.2f}）")

        st.subheader("📝 自動キャプション")
        st.markdown(generate_caption(label))

        st.subheader("📌 ハッシュタグ候補")
        st.code(" ".join(generate_hashtags(business_type, target_audience)))

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")
        st.download_button(
            label=f"📥 加工画像をダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"instadish_{file.name}",
            mime="image/jpeg",
            key=f"download_{unique_key}"
        )
else:
    st.info("画像をアップロードしてください。")
