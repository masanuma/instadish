import streamlit as st
from PIL import Image, ImageEnhance, ImageDraw
import io
import numpy as np
import cv2
import random
import torch
import clip

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

def generate_hashtags(business, audience):
    tags = ["#InstaFood", "#グルメ", "#食べスタグラム", "#おしゃれごはん"]
    if business == "カフェ": tags += ["#カフェ巡り", "#CafeTime", "#コーヒー好き"]
    if business == "居酒屋": tags += ["#居酒屋メシ", "#日本酒好き", "#大衆酒場"]
    if business == "バー": tags += ["#BarTime", "#クラフトジン", "#隠れ家バー"]
    if business == "エスニック": tags += ["#エスニック料理", "#SpicyLovers", "#アジアごはん"]
    if business == "和食": tags += ["#和食", "#JapaneseCuisine", "#美味しい和食"]
    if business == "洋食": tags += ["#洋食ランチ", "#WesternFood", "#おしゃれディナー"]
    if business == "中華": tags += ["#中華料理", "#DimSum", "#本格中華"]
    if audience == "インスタ好き": tags += ["#映えグルメ", "#フォトジェニック", "#SNS映え"]
    if audience == "外国人観光客": tags += ["#VisitJapan", "#TokyoFoodie", "#JapaneseCulture"]
    if audience == "会社員": tags += ["#ランチタイム", "#お疲れ様です", "#仕事帰りグルメ"]
    if audience == "シニア": tags += ["#落ち着いた時間", "#大人の食事", "#ゆっくりごはん"]
    if audience == "OL": tags += ["#女子会ごはん", "#OLランチ", "#昼休みカフェ"]
    return sorted(set(tags))[:20]

@st.cache_resource
def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

def classify_image_clip(image):
    model, preprocess, device = load_clip_model()
    class_names = [
        "cocktail", "sushi", "ramen", "cake", "steak", "pizza", "bar counter", "candlelight", "bottle", "coffee"
    ]
    inputs = torch.cat([clip.tokenize(f"a photo of {c}") for c in class_names]).to(device)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(inputs)
        logits_per_image, _ = model(image_input, inputs)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
    return class_names[np.argmax(probs)], max(probs[0])

def generate_caption(label, confidence):
    phrases = {
        "cocktail": "夜の時間にぴったりな一杯を。",
        "sushi": "一貫一貫に心を込めて。",
        "ramen": "スープまで飲み干したくなる美味しさ。",
        "cake": "甘い時間をお楽しみください。",
        "steak": "ジューシーでボリュームたっぷり。",
        "pizza": "チーズたっぷりでアツアツ。",
        "bar counter": "静かな夜にしっとりと。",
        "candlelight": "灯りに包まれた癒しの空間。",
        "bottle": "こだわりのボトルがずらり。",
        "coffee": "午後の休息に、ほっとひと息。"
    }
    if confidence < 0.3:
        return "雰囲気を大切にした一枚です。ぜひチェックしてみてください。"
    return phrases.get(label, "おすすめの一品です。ぜひご賞味ください！")

def process_image(image):
    enhancer_brightness = ImageEnhance.Brightness(image)
    bright_image = enhancer_brightness.enhance(1.2)
    enhancer_contrast = ImageEnhance.Contrast(bright_image)
    contrast_image = enhancer_contrast.enhance(1.3)
    enhancer_sharpness = ImageEnhance.Sharpness(contrast_image)
    sharp_image = enhancer_sharpness.enhance(2.0)
    r, g, b = sharp_image.split()
    r = r.point(lambda i: min(255, int(i * 1.1)))
    g = g.point(lambda i: min(255, int(i * 1.05)))
    b = b.point(lambda i: int(i * 0.9))
    return Image.merge("RGB", (r, g, b))

def check_composition(pil_image):
    np_image = np.array(pil_image)
    gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    height, width = gray.shape
    center_x, center_y = width // 2, height // 2
    label = "✅ 構図チェック結果："
    if len(contours) == 0:
        return label + "被写体が検出できませんでした（画像が暗い/ぼやけている可能性あり）"
    largest = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return label + "被写体の中心を特定できません"
    cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
    offset_x = abs(cx - center_x) / width
    offset_y = abs(cy - center_y) / height
    feedback = []
    if offset_x < 0.1 and offset_y < 0.1:
        feedback.append("中心配置OK")
    else:
        feedback.append("構図を中心に近づけるとより良いです")
    if width / height > 1.2:
        feedback.append("横長構図。余白のバランスを確認しましょう")
    else:
        feedback.append("縦構図または正方形。SNS向きです")
    return label + " / ".join(feedback)

def generate_crop_preview(pil_image):
    width, height = pil_image.size
    center_x, center_y = width // 2, height // 2
    crop_size = min(width, height)
    box_1to1 = (center_x - crop_size//2, center_y - crop_size//2, center_x + crop_size//2, center_y + crop_size//2)
    box_4to5 = (center_x - crop_size//2, center_y - int(crop_size*0.4), center_x + crop_size//2, center_y + int(crop_size*0.6))
    crop_1to1 = pil_image.crop(box_1to1)
    crop_4to5 = pil_image.crop(box_4to5)
    return crop_1to1, crop_4to5

if uploaded_files:
    if st.button("📸 画像を加工してハッシュタグを提案"):
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption=f"元の画像: {uploaded_file.name}", use_container_width=True)

            st.markdown(check_composition(image))

            crop1, crop2 = generate_crop_preview(image)
            st.image(crop1, caption="トリミング候補（1:1）", use_container_width=True)
            st.image(crop2, caption="トリミング候補（4:5）", use_container_width=True)

            processed = process_image(image)
            st.image(processed, caption="加工済み画像", use_container_width=True)

            label, conf = classify_image_clip(image)
            caption = generate_caption(label, conf)
            st.subheader("📝 キャプション候補")
            st.markdown(f"{caption}（推定カテゴリ: {label}, 信頼度: {conf:.2f}）")

            hashtags = generate_hashtags(business_type, target_audience)
            st.subheader("📌 おすすめハッシュタグ")
            st.code(" ".join(hashtags), language="markdown")

            img_bytes = io.BytesIO()
            processed.save(img_bytes, format="JPEG")
            st.download_button(
                label=f"📥 加工画像をダウンロード（{uploaded_file.name}）",
                data=img_bytes.getvalue(),
                file_name=f"instadish_{uploaded_file.name}",
                mime="image/jpeg"
            )
else:
    st.info("上のフォームに画像をアップロードしてください。")
