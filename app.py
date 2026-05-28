import streamlit as st
from google import genai
from google.genai import types
import time
import io
import random
from PIL import Image, ImageDraw, ImageFont

# 1. 網頁基礎設定
st.set_page_config(page_title="🌸 長輩專屬早安圖產生器", page_icon="🌸", layout="centered")

# ========================================================
# 📚 早安金句資料庫 (完整 88 句)
# ========================================================
quotes_list = [
    "早安世界！新的一天，帶著微笑醒來，讓生活充滿陽光和溫暖。" , # [cite: 2]
    "每天叫醒你的，不是鬧鐘，而是夢想；最美的所在，不在路上，而是在心裡，早安！" , # [cite: 3]
    "早安唷～每個醒來的早晨，都是宇宙給我們最棒的禮物。" , # [cite: 4]
    "早安！美好的一天從心開始。" , # [cite: 5]
    "晨光熹微，早安！願你擁有滿滿的正能量。" , # [cite: 6]
    "清晨的陽光已為你鋪路，早安，勇敢前行吧！" , # [cite: 7]
    "睜開眼，又是充滿可能的一天，早安，加油！" , # [cite: 8]
    "祝好心情從清晨開始，願你享受美好生活每一天！" , # [cite: 9]
    "讓每一天都充滿陽光，讓每一秒都盡情飛揚，早安。" , # [cite: 10]
    "天亮了，美妙的一天開始囉！起床吧，盡全力擁抱陽光吧！" , # [cite: 11]
    "早安，一年之計在於春，一天之計在於晨，願你起床心情好！" , # [cite: 12]
    "幸福是晨光，快樂是晨曦，夢想是晨風，把握每一個清晨，早安！" , # [cite: 13]
    "每天日出都是問候，每天的空氣都是清新，每天的心情都是舒展，每天的收穫都是充實，早安！" , # [cite: 14]
    "每個黎明都會有陽光，每個芬芳都會有清香，打開人生的窗，你會發現美麗的曙光，早安！" , # [cite: 15]
    "把每個睡醒後的早晨當成一件禮物，把每個開心後的微笑當成一個習慣；祝你微笑今天，快樂永遠！" , # [cite: 16]
    "每一個清晨都值得珍惜，每一個夢想都值得追逐，相信自己，未來可期。" , # [cite: 17]
    "告別昨日煩惱，擁抱今日美好，用積極的心態，迎接充滿希望的嶄新一天。" , # [cite: 18]
    "清晨的陽光帶來新的力量，願你放下負擔，輕裝上陣，奔赴所有美好與希望。" , # [cite: 19]
    "早安！睜開眼睛，你已經成功完成今天的第一個任務——醒來！" , # [cite: 20]
    "嘿，早安！昨晚的夢想很美，現在是時候起來把它變成現實了！" , # [cite: 21]
    "每天清晨，喚醒你的不應該是鬧鐘，應該是你的夢想。" , # [cite: 22]
    "夢想一旦被付諸行動，就會變得神聖。" , # [cite: 23]
    "不要讓你的夢想只剩下夢和想。" , # [cite: 24]
    "早晨愉快！一點點進步，也是在前進，別小看自己的努力！" , # [cite: 25]
    "早安，世界因你而精彩，今天也要元氣滿滿哦！" , # [cite: 26]
    "清晨的陽光照亮前路，願你心懷熱愛，步履不停，向著美好一路前行。" , # [cite: 27]
    "所有的好運，都藏在堅持與自律裡；默默努力，靜靜成長，你終將閃閃發光。" , # [cite: 28]
    "別讓懶惰消耗夢想，別讓猶豫錯過機會，即刻出發，你遠比想像中更強大。" , # [cite: 29]
    "人生沒有太晚的開始，只有不開始的遺憾；即刻行動，努力成為更好的人。" , # [cite: 30]
    "相信自己，從頭來過，什麼都不會晚，新的一天開始了，早安！" , # [cite: 31]
    "讓自己變優秀才是最好的反擊；新的一月，做最好的自己，早安。" , # [cite: 32]
    "雙手空空的人，才能懂得盡情奔跑的快樂，早安！" , # [cite: 33]
    "每一個新的一天都是一個改變你自己命運的機會，早安。" , # [cite: 34]
    "如果有機會，就把握吧；如果有標，就奮進吧！早安！" , # [cite: 35]
    "如果你想得到從未擁有過的東西，那麼你必須去做從未做過的事情，早安！" , # [cite: 36]
    "不要停止奔跑，不要回顧來路，來路無可眷戀，值得期待的只有前方；新的一天！加油！" , # [cite: 37]
    "當你決定堅持一件事情，全世界都會為你讓路，早安！" , # [cite: 38]
    "因為成功不在前方，而在當下，醒過來，爭取自己的夢想，早安！" , # [cite: 39]
    "從這個清晨開始努力，一點一滴的累積，迎來成功的喜悅！早安！" , # [cite: 40]
    "每一個清晨，伴著陽光上路，清新的空氣純淨著靈魂，滿天的雲霞變幻著色彩；給自己一個微笑，告訴自己今天會更美好，早安！" , # [cite: 41]
    "早安，讓微笑成為你今天的開場白。" , # [cite: 42]
    "早上好，無論今天遇見什麼，都請記得，你比自己想像得更強大！" , # [cite: 43]
    "早上好，願你的心情像晨曦一樣清新美好！" , # [cite: 44]
    "生命要有裂縫，陽光才能照的進來。" , # [cite: 45]
    "得之坦然，失之淡然，順其自然，爭其必然。" , # [cite: 46]
    "不必糾結過往，不必焦慮未來，認真活好當下，便是對自己最好的成全。" , # [cite: 47]
    "生活或許平凡，但你可以選擇熱烈；保持微笑，努力向上，日子終會發光。" , # [cite: 48]
    "把煩惱清空，把希望裝滿，新的一天，願你眼裡有光，心中有愛，萬事順遂。" , # [cite: 49]
    "生活給你壓力，你就還它奇蹟；穩住心態，踏實努力，一切美好皆可期待。" , # [cite: 50]
    "不慌不忙，靜待花開；不急不躁，默默變強；你的努力，時光終會看見。" , # [cite: 51]
    "用微笑面對生活，用努力證明自己，不負每一份熱愛，不錯過每一次機會。" , # [cite: 52]
    "活著就有希望，有希望，就有幸福的未來，早安！" , # [cite: 53]
    "只要堅信向著明媚走，活著的每一天一定是陽光的。" , # [cite: 54]
    "雨會停，心會晴，沒有什麼會永遠糟糕透頂，早安。" , # [cite: 55]
    "糟糕的日子熬過去了，剩下的就是好運氣，早安。" , # [cite: 56]
    "不管過去如何，過去的已經過去，最好的總在未來等著你，早上好！" , # [cite: 57]
    "好事情總是發生在微笑的人身上；調整心情，讓新的一天充滿笑容，早安。" , # [cite: 58]
    "早安！無論命運給你什麼，把每一個今天過好，就是人生最大的贏家！" , # [cite: 59]
    "走一步有一步的風景，進一步有一步的歡喜，說聲早安，不怕什麼路途遙遠，幸福就在前進的道路上。" , # [cite: 60]
    "向日葵說，只要你朝著陽光努力向上，生活便會因此變得單純而美好；美好的一天開始，願你能向日葵一樣，迎著陽光向上！早安！" , # [cite: 61]
    "給自己一個目標，給自己一個希望，給自己一份熱愛，給自己一份溫暖，只為今天快樂，不為昨天煩惱，照顧好自己，我的朋友，早安！" , # [cite: 62]
    "世界上只有想不通的人，沒有走不通的路。" , # [cite: 63]
    "人生沒有白走的路，每一步堅持都在鋪路，相信自己，未來終將繁花盛開。" , # [cite: 64]
    "每一次堅持都不會白費，每一份付出都有迴響，你只管向前，時光自有答案。" , # [cite: 65]
    "哪怕步伐緩慢，也絕不後退；在時光裡沉澱，在堅持中蛻變，成為更好的自己。" , # [cite: 66]
    "每一次跌倒都是成長，每一次流淚都是堅強，擦乾汗水，繼續向著光亮出發。" , # [cite: 67]
    "哪怕前路崎嶇，也要昂首前行；跌倒了就爬起來，失敗了就重新再來。" , # [cite: 68]
    "自律給你自由，堅持成就夢想；管住自己，腳踏實地，未來必定閃閃發光。" , # [cite: 69]
    "世上沒有白費的努力，更沒有碰巧的成功，成功，不過是水到渠成。" , # [cite: 70]
    "乾坤未定，你我都是黑馬。" , # [cite: 71]
    "生無捷徑，一次次逼自己完成不可能，你會成為最大的可能。" , # [cite: 72]
    "邁開腳步，再長的路也不在話下；停滯不前，再短的路也難以到達。" , # [cite: 73]
    "把握現在、就是創造未來。" , # [cite: 74]
    "努力不一定成功，但放棄一定會失敗。" , # [cite: 75]
    "曾經輸掉的東西，只要你想，就一定可以再一點一點贏回來，早安！" , # [cite: 76]
    "唯有日積月累的堅持，才會有厚積薄發的成功，早安。" , # [cite: 77]
    "成功是優點的發揮，失敗是缺點的累積。" , # [cite: 78]
    "人生最大的成就，是從失敗中站立起來。" , # [cite: 79]
    "信心、毅力、勇氣三者具備，則天下沒有做不成的事。" , # [cite: 80]
    "弱者等待時機，強者創造時機。" , # [cite: 81]
    "勇氣不可失，信心不可無，世間沒有不能與無能的事，只怕不肯。" , # [cite: 82]
    "愈能忍受艱難的花，愈能有甜蜜的果。" , # [cite: 83]
    "能善用時間的人，必能掌握自己努力的方向。" , # [cite: 84]
    "每天無所事事，是人生的消費者，積極有用，才是人生的創造者。" , # [cite: 85]
    "勤能補拙，將嘲笑視同啟發，把諷刺當作激勵。" , # [cite: 86]
    "勿輕言「挫折感」、「無力感」，縱然困難如石，也要鑽過去。" , # [cite: 87]
    "我們最強的對手不一定是別人，而可能是我們自己。" , # [cite: 88]
    "恆心就如滴水穿石，再大的困難與阻礙也能衝破。" , # [cite: 89]
]

# ========================================================
# 🎨 圖片文字處理函數 (文字自動換行與描邊)
# ========================================================
def draw_text_on_image(image_bytes, text):
    # 開啟 AI 生成的圖片
    img = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(img)
    
    # 載入字體 (請確保資料夾內有 font.ttf)，設定長輩喜歡的超大字體 (大小 60)
    try:
        font = ImageFont.truetype("font.ttf", 60)
    except:
        st.error("⚠️ 找不到字體檔 (font.ttf)！請確認檔案有放在資料夾中。")
        st.stop()

    # 自動換行邏輯：確保文字不會超出圖片邊界
    max_width = img.width - 100
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        # 使用 getbbox 計算文字寬度
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
    lines.append(current_line)

    # 計算整段文字的高度，將文字置中偏下
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines]
    total_height = sum(line_heights) + 15 * (len(lines) - 1)
    y_text = img.height - total_height - 80 # 距離底部 80 像素

    # 將每一行文字畫到圖片上 (加入黑色描邊，讓白字在任何背景都清晰)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_text = (img.width - text_width) / 2
        
        # 畫黑邊 (Stroke)
        stroke_width = 5
        draw.text((x_text, y_text), line, font=font, fill="white", 
                  stroke_width=stroke_width, stroke_fill="black")
        
        y_text += line_heights[0] + 15 # 行距

    # 將處理好的圖片轉回 bytes 以便網頁顯示與下載
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

# ========================================================
# 🔒 防護機制與記憶體設定
# ========================================================
class ClassTracker:
    def __init__(self):
        self.total_images_generated = 0
    def increase(self):
        self.total_images_generated += 1
    def get_total(self):
        return self.total_images_generated

@st.cache_resource
def get_class_tracker():
    return ClassTracker()

class_tracker = get_class_tracker()
MAX_CLASS_IMAGES = 100 

if "student_image_count" not in st.session_state:
    st.session_state.student_image_count = 0
MAX_STUDENT_IMAGES = 3 

if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# ========================================================
# 網頁介面
# ========================================================
st.title("🌸 數位機會中心：AI 早安圖產生器")
st.markdown("各位大哥大姐早安！請在下方隨便輸入一個字、一個數字，或是一句話，AI 就會幫您配上一張漂亮的風景照跟金句喔！")

st.info(f"📊 您的今日體驗額度：已經生成 {st.session_state.student_image_count} / {MAX_STUDENT_IMAGES} 張")

api_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 長輩輸入區
prompt_input = st.text_input("請在這裡輸入 (隨便打什麼都可以)：", placeholder="例如：1、好、蓮花、開心")

if st.button("✨ 點我製作早安圖"):
    if class_tracker.get_total() >= MAX_CLASS_IMAGES:
        st.error("🚫 今日全班額度已滿，請通知講師。")
        st.stop()
        
    if st.session_state.student_image_count >= MAX_STUDENT_IMAGES:
        st.error("🚫 您已經做完 3 張囉！把機會讓給其他同學吧。")
        st.stop()
        
    if not prompt_input:
        st.warning("大哥大姐，請先在上面框框隨便打個字喔！")
    else:
        # 🎲 隨機抽取一句金句
        selected_quote = random.choice(quotes_list)
        
        # 🎲 隨機百變圖庫：融合長輩們最喜歡的多元場景與元素
        subjects = [
            "可愛的貓咪", "活潑的小狗", "毛茸茸的兔子", "朝氣的小雞", 
            "純真快樂的小孩", "笑容滿面的男生", "溫柔優雅的女生", 
            "一杯冒著熱氣的茶", "一張放著盆栽的精緻咖啡桌", "盛開的蓮花"
        ]
        backgrounds = [
            "寧靜的湖畔", "溫馨的咖啡廳裡面", "翠綠的茶園中", 
            "寬廣的綠草地", "藍天白雲的風景", "陽光灑落的海岸邊", 
            "壯闊的蔚藍大海", "雲霧繚繞的山水畫場景"
        ]
        
        # 每次按下按鈕，都隨機抽一個主體和一個背景
        random_subject = random.choice(subjects)
        random_bg = random.choice(backgrounds)
        
        with st.spinner("電腦畫家中，請稍候約 15 秒..."):
            for attempt in range(3):
                try:
                    # 🖼️ 進階防呆提示詞：組合長輩的輸入與我們的隨機題庫
                    full_prompt = (
                        f"一張極度美麗的溫馨攝影照片，風格明亮、充滿朝氣，非常適合長輩作為早安圖。 "
                        f"畫面主要靈感來自：'{prompt_input}'。 "
                        f"【重要指示】如果前面的靈感內容只是無意義的符號、注音、單一數字字母，或是難以直接畫出具體物品，"
                        f"請自動忽略它，改為畫這個主題：『{random_subject}，場景搭配{random_bg}』。 "
                        f"畫面中心偏下方請稍微留白。絕對不要在圖片中生成任何文字、浮水印或字母。"
                    )
                    
                    result = client.models.generate_images(
                        model='imagen-4.0-generate-001',
                        prompt=full_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio="1:1",
                            output_mime_type="image/jpeg",
                            safety_filter_level="BLOCK_LOW_AND_ABOVE"
                        )
                    )
                    
                    # 取得原始圖片
                    raw_image_bytes = result.generated_images[0].image.image_bytes
                    
                    # 🖋️ 呼叫我們寫好的函數，把金句寫上去！
                    final_image_bytes = draw_text_on_image(raw_image_bytes, selected_quote)
                    
                    # 存入記憶體
                    st.session_state.generated_image = final_image_bytes
                    class_tracker.increase()
                    st.session_state.student_image_count += 1
                    
                    st.rerun()
                    break 
                    
                except Exception as e:
                    if "429" in str(e) or "exhausted" in str(e).lower():
                        if attempt < 2:
                            time.sleep(2 ** (attempt + 1))
                        else:
                            st.error("現在太多人同時生成啦！請稍微等個 10 秒再按一次喔！")
                    else:
                        st.error(f"發生未知的錯誤：{e}")
                        break

# ========================================================
# 🖼️ 顯示最終成果與下載按鈕
# ========================================================
if st.session_state.generated_image:
    st.markdown("---")
    st.markdown("### 🎉 您的專屬早安圖完成啦！")
    st.image(st.session_state.generated_image, use_container_width=True)
    
    st.download_button(
        label="📥 點我下載早安圖到手機/電腦",
        data=st.session_state.generated_image,
        file_name="my_good_morning_card.jpg",
        mime="image/jpeg"
    )
