import streamlit as st
import engine      # 確保 engine.py 在同目錄
import processor   # 確保 processor.py 在同目錄
import time

# --- 初始化 Session State (防止重新整理時資料消失) ---
if 'processed_results' not in st.session_state:
    st.session_state['processed_results'] = None

# ... (Sidebar 配置) ...

if st.sidebar.button("🔄 立即搜尋並更新"):
    with st.status("🚀 正在執行全球情報抓取與 AI 分析...", expanded=True) as status:
        st.write("1. 正在從開放網路與社群獲取原始數據...")
        # 呼叫 engine 模組的函數 (假設函數名為 get_layer_data)
        raw_data = engine.get_layer_data(layer_code, update_freq)
        
        st.write("2. 正在調用 Gemini 進行深度分析與中英翻譯 (共 10 項)...")
        final_list = []
        progress_bar = st.progress(0)
        
        for i, item in enumerate(raw_data):
            # 呼叫 processor 模組進行 AI 處理
            try:
                # 傳入原始文本進行分析
                analysis_result = processor.analyze_and_translate(item['raw_content'])
                
                final_list.append({
                    "title": item['original_title'],
                    "url": item['source_url'],
                    "analysis": analysis_result
                })
                # 加入微小延遲避免觸發 Gemini API 的 Rate Limit
                time.sleep(1) 
            except Exception as e:
                st.error(f"第 {i+1} 項分析失敗: {e}")
            
            progress_bar.progress((i + 1) / len(raw_data))
        
        # 存入 Session State
        st.session_state['processed_results'] = final_list
        status.update(label="✅ 分析完成！", state="complete", expanded=False)

# --- 渲染結果 (這部分要放在 Button 之外) ---
if st.session_state['processed_results']:
    for idx, res in enumerate(st.session_state['processed_results']):
        with st.expander(f"📌 項目 {idx+1}: {res['title']}", expanded=(idx==0)):
            st.markdown(res['analysis']) # 顯示 processor 產出的 200~500 字內容
            st.caption(f"🔗 [來源連結]({res['url']})")
else:
    st.info("請點擊左側「立即搜尋並更新」按鈕獲取最新情報。")
