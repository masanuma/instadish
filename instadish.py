import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import torch
import clip
import uuid

st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")
st.markdown("""
<style>
section[data-testid="stFileUploader"] button { background-color: #fdd835; }
div[data-testid="stSelectbox"] { margin-bottom: 0rem; }
div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3 {
  margin-bottom: 0.5rem;
  margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; white-space: nowrap;'>InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案</h1>
<p style='text-align: center;'>by Masashi</p>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("ファイル選択", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

col1, col2 = st.columns(2)
business_type = col1.selectbox("", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"], label_visibility="collapsed")
target_audience = col2.selectbox("", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"], label_visibility="collapsed")

@st.cache_resource
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

if uploaded_files and st.button("\ud83d\udcf8 加工してハッシュタグを提案"):
    for i, file in enumerate(uploaded_files):
        unique_key = str(uuid.uuid4())
        image = Image.open(file).convert("RGB")
        st.image(image, caption=f"元の画像: {file.name}", use_container_width=True)

        processed = process_image(image)
        st.image(processed, caption="加工済み画像", use_container_width=True)

        label, conf, all_labels = classify_image_clip(image)

        if conf < 0.5:
            st.warning(f"画像分類の信頼度が低いため、内容を選んでください（信頼度 {conf:.2f}）")
            label = st.selectbox("\ud83d\udccc 内容ジャンルを選択", all_labels, index=0, key=f"select_{unique_key}")
        else:
            st.markdown(f"\ud83d\udccc 自動判定ジャンル：**{label}**（信頼度 {conf:.2f}）")

        st.subheader("\ud83d\udcdd 自動キャプション")
        st.markdown(generate_caption(label))

        st.subheader("\ud83d\udccc ハッシュタグ候補")
        st.code(" ".join(generate_hashtags(business_type, target_audience)))

        img_bytes = io.BytesIO()
        processed.save(img_bytes, format="JPEG")
        st.download_button(
            label=f"\ud83d\udc45 加工画像をダウンロード（{file.name}）",
            data=img_bytes.getvalue(),
            file_name=f"instadish_{file.name}",
            mime="image/jpeg",
            key=f"download_{unique_key}"
        )
else:
    st.info("\u753b\u50cf\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u304f\u3060\u3055\u3044\u3002")
