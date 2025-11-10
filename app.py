# -*- coding: utf-8 -*-
"""
GAgroSmart - Pure Hindi Streamlit App with Browser Voice Input (Web Speech API)
Developed by Hemant Kumawat
"""

import streamlit as st
import pandas as pd
import time
import os
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="GAgroSmart", page_icon="🌿", layout="centered")

# Header
st.markdown(
    """
    <div style="text-align:center; padding:10px; border-radius:8px; background: linear-gradient(90deg,#e8f5e9,#fff9e6);">
        <h1 style="margin:4px 0; font-family: 'Noto Sans', sans-serif;">GAgroSmart</h1>
        <div style="font-size:16px; margin-bottom:6px;">किसान का स्मार्ट साथी — फसल एवं मिट्टी के अनुसार खाद सुझाव</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # spacing

# Left: inputs, Right: results layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("किसी भी फसल के लिए जानकारी दर्ज करें")
    crop = st.text_input("1) फसल का नाम दर्ज करें (उदा: प्याज, गेहूँ, टमाटर):")
    soil = st.selectbox("2) मिट्टी का प्रकार चुनें:", ["दोमट मिट्टी", "काली मिट्टी", "रेतीली मिट्टी", "लाल मिट्टी", "अन्य"])
    irrigation = st.selectbox("3) सिंचाई की स्थिति:", ["सिंचित", "असिंचित"])
    area = st.number_input("4) क्षेत्रफल (एकड़ में):", min_value=0.01, value=1.0, step=0.01)
    stage = st.selectbox("5) फसल का चरण:", ["बोवाई/अंकुरण", "विकास", "फूल/फल का चरण", "कटाई से पहले"])
    st.write("")


    st.markdown("**6) आवाज़ से फसल बताने के लिए नीचे बटन दबाएँ (ब्राउज़र माइक्रोफ़ोन अनुमति दें)**")
    # Voice recognition component (browser Web Speech API)
    # This HTML/JS uses the Web Speech API to recognize Hindi speech and posts the result back to Streamlit.
    voice_html = """
    <div style="text-align:center;">
      <button id="start-btn" style="font-size:16px; padding:10px 18px; border-radius:6px; background:#2e7d32; color:white; border:none;">
        🎙️ बोलकर फसल बताएं
      </button>
      <div id="status" style="margin-top:8px; font-size:14px; color:#555;"></div>
      <script>
        const btn = document.getElementById('start-btn');
        const status = document.getElementById('status');
        function sendToStreamlit(text) {
          // Post message to Streamlit's iframe parent so Streamlit component returns the value
          const payload = {event: 'speech_result', value: text};
          window.parent.postMessage(payload, "*");
        }
        btn.onclick = async function() {
          status.innerText = "माइक्रोफ़ोन के लिए अनुमति माँगी जा रही है...";
          // Check for browser support
          if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            status.innerText = "यह ब्राउज़र आवाज़ पहचान को समर्थन नहीं करता। Chrome/Edge में खोलें।";
            return;
          }
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          const recognition = new SpeechRecognition();
          recognition.lang = 'hi-IN';
          recognition.interimResults = false;
          recognition.maxAlternatives = 1;
          recognition.onstart = () => { status.innerText = "कृपया बोलें..."; }
          recognition.onerror = (e) => { status.innerText = "आवाज़ समझने में त्रुटि: " + e.error; }
          recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            status.innerText = "आपने कहा: " + text;
            // send recognized text to Streamlit
            sendToStreamlit(text);
          };
          recognition.onend = () => { /* finished */ }
          recognition.start();
        }
      </script>
    </div>
    """

    # When components.html returns, it returns the last postMessage payload if any.
    # We will capture that value below.
    voice_result = components.html(voice_html, height=150)

    # Fallback manual input
    st.markdown("---")
    st.markdown("**यदि आवाज़ का उपयोग न कर सकें तो यहाँ टाइप करें:**")
    crop_manual = st.text_input("फ़सल (टाइप करें):", value="")  # second input if user prefers typing

    # Choose final crop value (voice overrides manual if present)
    final_crop = crop  # default from earlier
    if voice_result and isinstance(voice_result, dict) and voice_result.get("event") == "speech_result":
        # Received dictionary payload from the component
        v = voice_result.get("value", "").strip()
        if v:
            final_crop = v
    elif crop_manual:
        final_crop = crop_manual

    st.write("")


with col2:
    st.subheader("सुझाव और परिणाम")
    if not final_crop:
        st.info("कृपया बाएँ तरफ फ़सल का नाम दर्ज करें या 'बोलकर फसल बताएं' दबाएँ।")
    else:
        with st.spinner("सुझाव निकाल रहे हैं..."):
            time.sleep(1.0)
            # Simple rule-based recommendation — इसे बाद में CSV/ML से बदला जाएगा
            c = final_crop.strip().lower()
            # basic mapping (expandable)
            recommendations = []
            # कुछ exemplar rules (आप अपने fertilizer CSV से replace कर सकते हैं)
            if any(x in c for x in ["गेहूँ", "गेहू", "gehun", "wheat"]):
                recommendations = [
                    {"name": "UREA (यूरिया)", "npk": "46:0:0", "qty_per_acre": 50, "note": "टिलरिंग के समय दें"},
                    {"name": "DAP", "npk": "18:46:0", "qty_per_acre": 50, "note": "बुवाई के समय आधी मात्रा"},
                    {"name": "MOP", "npk": "0:0:60", "qty_per_acre": 25, "note": "यदि पोटाश की कमी हो"}
                ]
            elif any(x in c for x in ["प्याज", "onion"]):
                recommendations = [
                    {"name": "DAP", "npk": "12:32:16", "qty_per_acre": 100, "note": "बेसल एप्लिकेशन"},
                    {"name": "UREA", "npk": "46:0:0", "qty_per_acre": 60, "note": "विकास चरण में विभाजित करो"},
                    {"name": "Zinc Sulphate", "npk": "Zn", "qty_per_acre": 10, "note": "यदि जिंक की कमी हो तो"}
                ]
            elif any(x in c for x in ["टमाटर", "tomato"]):
                recommendations = [
                    {"name": "NPK 20:20:13", "npk": "20:20:13", "qty_per_acre": 80, "note": "फलों के विकास के दौरान"},
                    {"name": "UREA", "npk": "46:0:0", "qty_per_acre": 30, "note": "लीफ़ विकास के लिए"}
                ]
            else:
                # Default general suggestion
                recommendations = [
                    {"name": "संतुलित NPK", "npk": "10:26:26", "qty_per_acre": 50, "note": "मिट्टी रिपोर्ट देखें"},
                    {"name": "जैविक खाद (गोबर/वर्मी कम्पोस्ट)", "npk": "organic", "qty_per_acre": 200, "note": "मिट्टी की संरचना सुधारने के लिए"}
                ]

        # Display final results
        st.markdown(f"### 🌾 फ़सल: **{final_crop}**")
        st.markdown(f"**मिट्टी:** {soil}  •  **सिंचाई:** {irrigation}  •  **क्षेत्रफल:** {area} एकड़  •  **चरण:** {stage}")
        st.write("")
        st.markdown("#### ✅ सुझाए गए उर्वरक (अनुशंसित मात्रा प्रति एकड़):")
        for r in recommendations:
            st.markdown(f"- **{r['name']}** ({r['npk']}) — {r['qty_per_acre']} kg/acre  •  _{r['note']}_")

        st.markdown("---")
        st.info("नोट: सटीकता बढ़ाने के लिए मिट्टी की लैब रिपोर्ट अपलोड करें।")

# Footer and developer info
st.markdown("---")
st.markdown(
    """
    <div style="font-size:13px; color:#555;">
    Developed by <b>Hemant Kumawat</b> | GAgroSmart © 2025<br>
    संपर्क: hemantkumawat204@gmail.com
    </div>
    """,
    unsafe_allow_html=True,
)
