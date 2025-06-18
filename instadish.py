import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import uuid

st.set_page_config(page_title="InstaDish | 飲食店インスタ画像アプリ", layout="centered")
st.markdown("""
    <h1 style='text-align:center; font-size:clamp(1.5rem, 5vw, 2.2rem);'>InstaDish 🍽️ | 飲食店向けInstagram画像加工＋ハッシュタグ提案</h1>
""", unsafe_allow_html=True)
st.caption("by Masashi")

# --- セクション 1 ---
st.markdown("""
<div style='background-color:#fef3c7; padding: 1.5em; border-radius: 12px;'>
  <h3 style='margin:0; font-size:clamp(1rem, 4vw, 1.3rem);'>1. 📷 写真をアップロード（複数可）</h3>
""", unsafe_allow_html=True)
uploaded_files = st.file_uploader("ファイル選択", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="visible")
st.markdown("</div>", unsafe_allow_html=True)

if not uploaded_files:
    st.markdown("<p style='text-align:center; color:#666;'>⬆️ 上のボックスから画像を選択してください。</p>", unsafe_allow_html=True)

# --- セクション 2 ---
st.markdown("""
<div style='background-color:#e0f2fe; padding: 1.5em; border-radius: 12px;'>
  <h3 style='margin:0; font-size:clamp(1rem, 4vw, 1.3rem);'>2. 🏷️ 業態とターゲット層</h3>
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

# ここに画像処理や分類、ハッシュタグ生成処理を続けて実装
# 今後の機能追加時に差し込む位置になります
