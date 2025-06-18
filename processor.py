# processor.py
from PIL import ImageEnhance
import numpy as np
import torch
import clip
from config import CAPTION_PHRASES

def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

def classify_image_clip(image):
    class_prompts = list(CAPTION_PHRASES.keys())
    model, preprocess, device = load_clip_model()
    inputs = torch.cat([clip.tokenize(f"{c}") for c in class_prompts]).to(device)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        logits_per_image, _ = model(image_input, inputs)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]
    best_idx = int(np.argmax(probs))
    return class_prompts[best_idx], probs[best_idx], class_prompts

def generate_caption(label):
    return CAPTION_PHRASES.get(label, "おすすめの一品をぜひご賞味ください！")

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

def process_and_classify_image(image, business_type, target_audience, key):
    processed_image = process_image(image)
    label, confidence, all_labels = classify_image_clip(image)
    caption = generate_caption(label)
    hashtags = generate_hashtags(business_type, target_audience)

    return {
        "processed_image": processed_image,
        "label": label,
        "confidence": confidence,
        "all_labels": all_labels,
        "caption": caption,
        "hashtags": hashtags
    }
