import streamlit as st
import google.generativeai as genai

# 正確讀取方式
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("找不到 GEMINI_API_KEY，請在 Streamlit Cloud Settings -> Secrets 中設定。")

# 從 Streamlit 的秘密管理中讀取
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 請替換為你的 API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def analyze_and_translate(raw_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    請針對以下國際新聞或社群內容進行深度分析與彙整：
    
    內容：{raw_text}
    
    要求：
    1. 提供 200~500 字的詳細分析。
    2. 必須細分為以下五個面向：
       - 美國川普政府政策 (Trump Admin Policies)
       - 金融體系影響 (利率、通膨/通縮)
       - 資訊科技 (半導體、AI)
       - 能源與原物料 (油價、金屬)
       - 地緣政治風向 (烏克蘭、中東戰局意見)
    3. 全文採「中英對照」格式，每一段中文後緊跟著對應的英文。
    4. 語氣需專業且具備決策參考價值。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"分析生成失敗: {str(e)}"
