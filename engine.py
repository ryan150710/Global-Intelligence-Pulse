import requests
from bs4 import BeautifulSoup

def get_layer_data(layer_type, hours):
    """
    根據層次與時間抓取資料
    layer_type: 1(新聞), 2(社群), 3(預警)
    """
    results = []
    
    if layer_type == "1":
        # 範例：抓取 Reuters 國際新聞 RSS (這只是模擬路徑)
        # 實際開發建議使用 NewsAPI 或特定新聞網 RSS
        rss_url = "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best"
        # 這裡簡化處理，先回傳結構化資料供介面測試
        results = [
            {
                "raw_content": "Trump signals new tariffs on energy imports...",
                "source_url": "https://reuters.com/example1",
                "original_title": "Trump's New Energy Policy"
            }
            # ... 這裡會循環產出 10 筆
        ]
        
    elif layer_type == "2":
        # 層次二：模擬社群平台 (X/Reddit) 的即時趨勢
        results = [
            {
                "raw_content": "Trending on X: #MiddleEastWar update - Iran mobilization detected near borders.",
                "source_url": "https://x.com/trend",
                "original_title": "Social Media Pulse: Middle East"
            }
        ]
        
    else:
        # 層次三：預警 (論壇與非對稱資訊)
        results = [
            {
                "raw_content": "Deep Web Intel: Unusual silicon inventory movements in South Asia.",
                "source_url": "https://reddit.com/r/osint",
                "original_title": "Early Warning: Semiconductor Supply Chain"
            }
        ]
        
    return results[:10] # 確保回傳 10 筆
