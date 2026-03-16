import streamlit as st
import engine
import processor
import time

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="Global Intelligence Pulse 2026", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 初始化儲存空間 (防止資料遺失) ---
if 'processed_results' not in st.session_state:
    st.session_state['processed_results'] = None
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = None

# --- 3. 側邊欄 UI 設計 ---
st.sidebar.title("🌐 決策支援系統")
st.sidebar.info("使用者：Ethan | 權限：管理員")

# ⚠️ 關鍵修正：先定義變數，再進入按鈕邏輯
selected_layer_text = st.sidebar.radio(
    "選擇情報層次",
    ["層次一：已發生 (權威新聞)", "層次二：正在發生 (社群脈動)", "層次三：將要發生 (預警分析)"]
)

# 提取層次代碼 (例如：1, 2, 3)
layer_code = "1"
if "一" in selected_layer_text: layer_code = "1"
elif "二" in selected_layer_text: layer_code = "2"
elif "三" in selected_layer_text: layer_code = "3"

update_freq = st.sidebar.selectbox(
    "更新時間區段",
    options=[1, 4, 8, 24],
    format_func=lambda x: f"最近 {x} 小時",
    index=1
)

st.sidebar.divider()

# --- 4. 搜尋與更新邏輯 ---
if st.sidebar.button("🔄 立即搜尋並更新", use_container_width=True):
    with st.status("🚀 啟動情報蒐集引擎...", expanded=True) as status:
        try:
            st.write("📡 正在存取開放式網路與社群平台...")
            # 呼叫 engine 模組抓取資料
            raw_data_list = engine.get_layer_data(layer_code, update_freq)
            
            if not raw_data_list:
                st.error("未能抓取到相關數據，請稍後再試。")
            else:
                st.write(f"🤖 已獲取 {len(raw_data_list)} 筆原始資訊，開始 AI 深度分析與翻譯...")
                final_results = []
                progress_bar = st.progress(0)
                
                for idx, item in enumerate(raw_data_list):
                    # 呼叫 processor 模組進行 200~500 字中英對照分析
                    analysis = processor.analyze_and_translate(item['raw_content'])
                    
                    final_results.append({
                        "title": item.get('original_title', '未命名消息'),
                        "url": item.get('source_url', '#'),
                        "analysis": analysis
                    })
                    
                    # 更新進度
                    progress_bar.progress((idx + 1) / len(raw_data_list))
                    # 避免 API 過快被限制
                    time.sleep(0.5)
                
                # 儲存到 session_state
                st.session_state['processed_results'] = final_results
                st.session_state['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                status.update(label="✅ 情報分析完成！", state="complete", expanded=False)
        except Exception as e:
            st.error(f"系統運行異常: {str(e)}")
            status.update(label="❌ 運行出錯", state="error")

# --- 5. 主介面內容渲染 ---
st.title("📊 全球情報脈動監控")
if st.session_state['last_update']:
    st.caption(f"最後更新時間：{st.session_state['last_update']}")

if st.session_state['processed_results']:
    # 建立頁籤分類 (僅為視覺整理，內容由 AI 生成的五大面向組成)
    st.info(f"當前顯示：{selected_layer_text}")
    
    for i, res in enumerate(st.session_state['processed_results']):
        with st.expander(f"📌 {res['title']}", expanded=(i == 0)):
            # 顯示由 processor 產出的結構化內容
            st.markdown(res['analysis'])
            st.divider()
            st.markdown(f"🔗 [查看原始來源]({res['url']})")
else:
    st.warning("目前暫無數據。請點擊左側「立即搜尋並更新」按鈕開始蒐集。")

# --- 6. 底部指標 (裝飾用) ---
st.sidebar.divider()
st.sidebar.subheader("📉 市場指標 (模擬)")
st.sidebar.metric("Brent Oil", "$86.42", "+1.2%")
st.sidebar.metric("USD Index", "104.15", "-0.05%")
