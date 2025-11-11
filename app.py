# -*- coding: utf-8 -*-
import streamlit as st
import time
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="GAgroSmart", page_icon="🌿", layout="centered")

# 🌈 Custom CSS for Attractive Farmer UI
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #e8f5e9 0%, #ffffff 100%);
    font-family: 'Noto Sans Devanagari', sans-serif;
}
h1, h2, h3, h4 {
    color: #1b5e20;
    text-align: center;
}
.stButton>button {
    background: linear-gradient(90deg, #43a047, #1b5e20);
    color: white;
    border-radius: 12px;
    padding: 10px 18px;
    font-size: 18px;
    border: none;
    width: 100%;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #66bb6a, #2e7d32);
    transform: scale(1.03);
}
.card {
    background-color: #ffffff;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 15px;
}
.recommend {
    background-color: #f1f8e9;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 8px;
}
.footer {
    text-align: center;
    font-size: 14px;
    color: #555;
    margin-top: 40px;
}
.loader {
    text-align: center;
    font-size: 24px;
    color: #2e7d32;
    padding: 50px;
}
.notification {
    background: #e8f5e9;
    padding: 10px;
    border-left: 5px solid #43a047;
    border-radius: 8px;
    margin-bottom: 10px;
    animation: fadeIn 1s;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# 🌾 Loading Animation
with st.spinner("🌿 AgroSmart लोड हो रहा है..."):
    time.sleep(1.5)
st.markdown("""
<div class='loader'>
🌾 <b>GAgroSmart</b><br>
<b>किसान का स्मार्ट साथी</b><br>
<small>AI आधारित खाद एवं फसल सुझाव प्रणाली</small>
</div>
""", unsafe_allow_html=True)
time.sleep(1)

# 🔔 Random Smart Notifications
notifications = [
    "🌦️ बारिश के आसार हैं — सिंचाई रोक दें!",
    "🌱 मिट्टी में नमी अच्छी है — आज यूरिया डालना सही रहेगा।",
    "⚠️ तापमान गिरने की संभावना — पाले से बचाव करें।",
    "🐛 फसल पर कीट दिखे तो नीम आधारित जैविक कीटनाशक उपयोग करें।",
]
st.markdown(f"<div class='notification'>{random.choice(notifications)}</div>", unsafe_allow_html=True)

# 🪴 Input Section
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📋 फसल की जानकारी दर्ज करें")
crop = st.text_input("1️⃣ फसल का नाम (उदा: गेहूँ, प्याज, टमाटर):")
soil = st.selectbox("2️⃣ मिट्टी का प्रकार:", ["दोमट मिट्टी", "काली मिट्टी", "रेतीली मिट्टी", "लाल मिट्टी"])
irrigation = st.selectbox("3️⃣ सिंचाई की स्थिति:", ["सिंचित", "असिंचित"])
area = st.number_input("4️⃣ क्षेत्रफल (एकड़ में):", min_value=0.01, value=1.0)
stage = st.selectbox("5️⃣ फसल का चरण:", ["बोवाई/अंकुरण", "विकास", "फूल/फल का चरण", "कटाई से पहले"])
st.markdown("</div>", unsafe_allow_html=True)

# 🎧 Voice Input Button
st.markdown("""
<div class='card' style='text-align:center;'>
    <h4>🎙️ बोलकर फसल बताएं</h4>
    <button onclick="startVoice()" style="font-size:18px; padding:10px 20px; border-radius:10px; background:#43a047; color:white; border:none;">🎧 बोलें</button>
    <div id='result' style='margin-top:10px; font-size:18px; color:#1b5e20;'></div>
    <script>
    function startVoice(){
        const status=document.getElementById('result');
        if(!('webkitSpeechRecognition' in window)){
            status.innerText="⚠️ कृपया Chrome ब्राउज़र का उपयोग करें।";
            return;
        }
        const rec=new webkitSpeechRecognition();
        rec.lang='hi-IN';
        rec.start();
        rec.onresult=function(event){
            status.innerText="आपने कहा: " + event.results[0][0].transcript;
        };
    }
    </script>
</div>
""", unsafe_allow_html=True)

# 💧 Recommendation Logic
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧪 खाद सुझाव परिणाम")

if crop:
    crop_lower = crop.strip().lower()
    recs = []
    if "गेहूँ" in crop_lower or "wheat" in crop_lower:
        recs = [
            ("UREA", "46:0:0", 50, "टिलरिंग के समय दें"),
            ("DAP", "18:46:0", 50, "बुवाई के समय आधी मात्रा"),
            ("MOP", "0:0:60", 25, "यदि पोटाश की कमी हो"),
        ]
    elif "लहसुन" in crop_lower or "garlic" in crop_lower:
        recs = [
            ("NPK 12:32:16", "12:32:16", 70, "बुवाई के समय डालें"),
            ("UREA", "46:0:0", 40, "विकास के दौरान दो बार में दें"),
            ("वर्मी कम्पोस्ट", "organic", 150, "मिट्टी की उर्वरता के लिए"),
        ]
    elif "प्याज" in crop_lower or "onion" in crop_lower:
        recs = [
            ("DAP", "12:32:16", 100, "बेसल एप्लिकेशन"),
            ("UREA", "46:0:0", 60, "विकास चरण में विभाजित करें"),
            ("Zinc Sulphate", "Zn", 10, "यदि जिंक की कमी हो तो"),
        ]
    else:
        recs = [
            ("संतुलित NPK", "10:26:26", 50, "मिट्टी रिपोर्ट देखें"),
            ("जैविक खाद", "organic", 200, "मिट्टी की संरचना सुधारने के लिए"),
        ]

    st.markdown(f"<h4>🌿 फसल: {crop}</h4>", unsafe_allow_html=True)
    for name, npk, qty, note in recs:
        st.markdown(f"<div class='recommend'><b>{name}</b> ({npk}) — {qty} kg/acre<br><i>{note}</i></div>", unsafe_allow_html=True)
else:
    st.info("कृपया ऊपर फसल का नाम दर्ज करें।")

st.markdown("</div>", unsafe_allow_html=True)

# 🧾 Footer
st.markdown("""
<div class='footer'>
Developed by <b>Hemant Kumawat</b> | GAgroSmart © 2025<br>
📧 hemantkumawat204@gmail.com<br>
<b>🌿 किसान का स्मार्ट साथी</b>
</div>
""", unsafe_allow_html=True)
