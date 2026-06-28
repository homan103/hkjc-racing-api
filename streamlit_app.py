import streamlit as st
from openai import AzureOpenAI
import json

st.set_page_config(page_title="馬場通 AI 大腦", page_icon="🐎", layout="centered")

st.title("🐎 馬場通 AI 預測大腦")
st.write("基於 Microsoft Azure OpenAI GPT-4o 的智能賽馬數據分析看板")

# 內置模擬數據，免除手機輸入困難
mock_data = {
    "race_info": {
        "race_number": 6,
        "venue": "Sha Tin",
        "course": "Turf - C Course",
        "distance": 1400,
        "track_condition": "Good to Yielding"
    },
    "horses": [
        {"number": 1, "name": "閃電馬王", "draw": 1, "weight": 133, "jockey": "潘頓", "recent_forms": [1, 2, 4, 1, 5], "track_notes": "上場田草一放到底贏馬。今場有1檔黃金內欄優勢，預計依然會主動放頭。"},
        {"number": 2, "name": "金牌秘書", "draw": 11, "weight": 128, "jockey": "布文", "recent_forms": [5, 3, 11, 2, 4], "track_notes": "上場轉跑泥地不合發揮。前場草地同程外疊衝刺極強奪亞。唯獨11檔起步流於被動。"},
        {"number": 3, "name": "運財福星", "draw": 4, "weight": 122, "jockey": "艾兆禮", "recent_forms": [6, 7, 5, 1, 9], "track_notes": "過去兩場因慢步速落敗。晨操火氣極旺。今場4檔有利，場地稍軟對其腳法有幫助。"}
    ]
}

st.subheader("📋 本場測試賽事數據 (沙田草地1400米)")
st.json(mock_data)

# 撳鈕出發
if st.button("🚀 啟動 GPT-4o 綜合分析"):
    with st.spinner("AI 正在深度解讀人馬數據、檔位、場地及馬評隱藏訊息..."):
        try:
            # 讀取 Streamlit 後台秘密設定的環境變數
            client = AzureOpenAI(
                api_key=st.secrets["AZURE_OPENAI_API_KEY"],
                api_version="2024-06-01",
                azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
            )

            # 呼叫微軟的 gpt-4o 部署
            response = client.chat.completions.create(
                model=st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"],
                messages=[
                    {"role": "system", "content": "你是一位精通香港賽馬的頂級評馬大師。請分析用戶傳入的賽事JSON數據，綜合權衡『檔位、負磅、騎師、近況、場地狀況（好至黏地）』以及『馬評評語中的隱藏訊息』。請為每匹馬進行精準的實力評分（0-100），給出前三名名次預測，並用幽默、專業的繁體中文廣東話（香港評馬口吻）輸出深度報告。"},
                    {"role": "user", "content": json.dumps(mock_data, ensure_ascii=False)}
                ]
            )

            st.success("📊 AI 運算分析完成！")
            st.markdown("---")
            st.markdown("### 🔮 GPT-4o 專家預測報告")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"❌ 連線失敗！請確保一陣間在 Streamlit 後台有填妥 Secrets。")
            st.code(str(e))
