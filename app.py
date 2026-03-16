import streamlit as st
from engine import get_layer_data
from processor import analyze_and_translate

# ... (保留原有的頁面配置與 Sidebar) ...

if st.sidebar.button("🔄 立即搜尋並更新"):
    st.cache_data.clear()
    
    # 1. 抓取原始數據
    raw_news_list = get_layer_data(layer_code, update_freq)
    
    processed_data = []
    progress_bar = st.progress(0)
    
    # 2. 進行 AI 處理 (這會花一點時間，所以加上進度條)
    for i, item in enumerate(raw_news_list):
        analysis = analyze_and_translate(item['raw_content'])
        processed_data.append({
            "analysis": analysis,
            "url": item['source_url'],
            "title": item['original_title']
        })
        progress_bar.progress((i + 1) / 10)
    
    st.session_state['current_data'] = processed_data

# 3. 渲染 UI (使用 processed_data 顯示內容)
# ... (迴圈顯示分析內容) ...
