import streamlit as st
from PIL import Image, ImageEnhance
import io

# ---------------------------
# 設定
st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")
st.title("InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案")
st.caption("by Masashi")

# ---------------------------
# 入力フォーム
st.header("1. 写真をアップロード（複数可）")
uploaded_files = st.file_uploader("料理・ドリンクなどの写真を選んでください（複数選択OK）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

st.header("2. 業態とターゲット層を選択")
business_type = st.selectbox("業態を選んでください", ["和食", "洋食", "中華", "居酒屋", "バー", "エスニック", "カフェ"])
target_audience = st.selectbox("ターゲット層を選んでください", ["インスタ好き", "外国人観光客", "会社員", "シニア", "OL"])

# 撮影アドバイス
with st.expander("📷 撮影アドバイスを見る"):
    st.markdown("""
    ### 📸 ジャンル別おすすめ撮影ポイント
    - **ドリンク**：グラスの高さを活かして斜め下から
    - **カフェメニュー**：真上から全体をきれいに
    - **バーの雰囲気**：ラベルや照明を活かしたローアングル
    - **複数皿の料理**：奥行きを出すように45度で
    - **パッケージやラベルが重要な場合**：中央配置＋明るさ重視
    """)

# ---------------------------
# ハッシュタグ生成関数

def generate_hashtags(business, audience):
    tags = []
    base_tags = ["#InstaFood", "#グルメ", "#食べスタグラム", "#おしゃれごはん"]
    tags.extend(base_tags)

    if business == "カフェ":
        tags += ["#カフェ巡り", "#CafeTime", "#コーヒー好き"]
    elif business == "居酒屋":
        tags += ["#居酒屋メシ", "#日本酒好き", "#大衆酒場"]
    elif business == "バー":
        tags += ["#BarTime", "#クラフトジン", "#隠れ家バー"]
    elif business == "エスニック":
        tags += ["#エスニック料理", "#SpicyLovers", "#アジアごはん"]
    elif business == "和食":
        tags += ["#和食", "#JapaneseCuisine", "#美味しい和食"]
    elif business == "洋食":
        tags += ["#洋食ランチ", "#WesternFood", "#おしゃれディナー"]
    elif business == "中華":
        tags += ["#中華料理", "#DimSum", "#本格中華"]

    if audience == "インスタ好き":
        tags += ["#映えグルメ", "#フォトジェニック", "#SNS映え"]
    elif audience == "外国人観光客":
        tags += ["#VisitJapan", "#TokyoFoodie", "#JapaneseCulture"]
    elif audience == "会社員":
        tags += ["#ランチタイム", "#お疲れ様です", "#仕事帰りグルメ"]
    elif audience == "シニア":
        tags += ["#落ち着いた時間", "#大人の食事", "#ゆっくりごはん"]
    elif audience == "OL":
        tags += ["#女子会ごはん", "#OLランチ", "#昼休みカフェ"]

    return sorted(set(tags))[:20]

# ---------------------------
# 画像加工関数

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
    warm_image = Image.merge("RGB", (r, g, b))
    return warm_image

# ---------------------------
# 加工開始ボタン
if uploaded_files:
    if st.button("📸 画像を加工してハッシュタグを提案"):
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption=f"元の画像: {uploaded_file.name}", use_column_width=True)
            processed = process_image(image)
            st.image(processed, caption="加工済み画像", use_column_width=True)
            hashtags = generate_hashtags(business_type, target_audience)
            st.subheader("📌 おすすめハッシュタグ")
            st.code(" ".join(hashtags), language="markdown")
            img_bytes = io.BytesIO()
            processed.save(img_bytes, format="JPEG")
            st.download_button("📥 加工画像をダウンロード", data=img_bytes.getvalue(), file_name="instadish_processed.jpg", mime="image/jpeg")
else:
    st.info("上のフォームに画像をアップロードしてください。")
