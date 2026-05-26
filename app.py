import streamlit as st
from google import genai
from google.genai import types
import time
import io

# 1. 網頁基礎設定 (這行必須在程式碼的最上方)
st.set_page_config(page_title="AI 早安圖產生器", page_icon="🌅", layout="centered")

st.title("🌅 AI 專屬早安圖產生器")
st.markdown("歡迎來到 AI 繪圖體驗！請在下方輸入你想看到的畫面，AI 會幫你畫出專屬的早安圖。")

# 2. 安全地取得 API Key
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("系統尚未設定 API 金鑰，請通知老師處理！")
    st.stop() # 如果沒抓到金鑰，就停止執行下面的程式

# 3. 初始化 Gemini 客戶端
client = genai.Client(api_key=api_key)

# 4. 使用者輸入區
prompt_input = st.text_input(
    "請描述你的早安圖畫面：", 
    placeholder="例如：一位可愛的日系二次元精靈少女，在陽光灑落的森林中微笑喝著咖啡"
)

# 5. 生成圖片按鈕與邏輯
if st.button("✨ 開始生成早安圖"):
    if not prompt_input:
        st.warning("請先輸入你想畫的內容喔！")
    else:
        # 設定最高重試次數，這就是保護全班同時按下按鈕的防禦機制
        max_retries = 3
        
        # st.spinner 會在畫面上顯示一個旋轉的等待動畫
        with st.spinner("AI 畫家正在努力揮灑畫筆，請稍候約 10-15 秒..."):
            for attempt in range(max_retries):
                try:
                    # 組合提示詞：確保生成的圖片符合早安圖的溫馨氛圍
                    full_prompt = f"一張適合做為長輩圖或早安圖的插畫。畫面內容：{prompt_input}。風格溫馨、明亮，請確保圖片看起來充滿朝氣。"
                    
                    # 呼叫 Imagen 3 模型生成圖片
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=full_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,       # 每次產生 1 張
                            aspect_ratio="1:1",       # 圖片比例 (方形)
                            output_mime_type="image/jpeg",
                            # 安全過濾機制，避免生成不適當的內容
                            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE" 
                        )
                    )
                    
                    # 顯示生成的圖片
                    for generated_image in result.generated_images:
                        img = generated_image.image # 取得圖片物件
                        st.image(img, caption="你的專屬早安圖！", use_column_width=True)
                        
                        # 將圖片轉換為可以下載的格式
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='JPEG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        st.download_button(
                            label="📥 下載圖片",
                            data=img_byte_arr,
                            file_name="my_good_morning.jpg",
                            mime="image/jpeg"
                        )
                    
                    # 成功生成圖片後，跳出重試的迴圈
                    break 
                    
                except Exception as e:
                    # 捕捉 429 速率限制錯誤 (Too Many Requests)
                    if "429" in str(e) or "exhausted" in str(e).lower():
                        if attempt < max_retries - 1:
                            wait_time = 2 ** (attempt + 1) # 指數退避：分別等待 2秒、4秒
                            st.warning(f"目前同時使用的人數較多，系統將在 {wait_time} 秒後自動重試...")
                            time.sleep(wait_time)
                        else:
                            st.error("現在太多人同時生成啦！請大家稍微等個 10 秒再按一次喔！")
                    else:
                        # 如果是其他未知的錯誤，直接顯示出來方便除錯
                        st.error(f"發生未知的錯誤，請重新嘗試。詳細資訊：{e}")
                        break