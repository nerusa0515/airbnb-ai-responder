import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests

# Page configuration
st.set_page_config(page_title="Airbnb AI Co-Host", page_icon="🏡", layout="centered")

# Custom CSS for a bright, modern, SaaS-like look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1f2937;
        border-radius: 8px;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #1f2937;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF385C 0%, #E61E4D 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #E61E4D 0%, #D70466 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='color: #FF385C; text-align: center;'>🏡 Airbnb AI Co-Host</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Instant, accurate replies for your guests in seconds.</p>", unsafe_allow_html=True)

st.markdown("---")

# Expandable guides
with st.expander("📱 **How to use this on your phone with Airbnb**"):
    st.markdown("""
    1. **Guest messages you** on the Airbnb app. Copy their message text.
    2. **Open this web app** on your phone browser (tip: add it to your phone's home screen!).
    3. **Paste their message** below and hit **Generate Response**.
    4. **Copy the AI reply** and paste it right back into your Airbnb chat box!
    """)

with st.expander("🔑 **What is an OpenAI API Key?**"):
    st.markdown("""
    An **OpenAI API Key** is a secure password from OpenAI (the creators of ChatGPT) that powers this app's brain. 
    * Go to **platform.openai.com**
    * Create a free account, go to **API Keys**, and generate a new secret key.
    * Paste it below so your app can write responses!
    """)

st.markdown("### ⚙️ Property & Message Setup")

# Input fields with clear instructions
airbnb_url = st.text_input("🔗 Airbnb Listing URL", placeholder="https://www.airbnb.com/rooms/12345678")

guest_message = st.text_area(
    "💬 What did the guest say?", 
    placeholder="Paste the guest's actual message here (e.g., 'Hey, how do I connect to the Wi-Fi and where can I park my car?')"
)

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-proj-...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Generate Perfect AI Response"):
    if not airbnb_url or not guest_message or not openai_api_key:
        st.error("⚠️ Please fill in all fields above before generating a response.")
    else:
        with st.spinner("🤖 Reading listing details & drafting reply..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(airbnb_url, headers=headers)
                
                if response.status_code != 200:
                    st.error("❌ Could not read the Airbnb URL. Make sure it's a valid, public link.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find("h1").text if soup.find("h1") else "Airbnb Listing"
                    description_blocks = [p.text for p in soup.find_all("p")]
                    raw_content = " ".join(description_blocks)[:4000]
                    
                    client = openai.OpenAI(api_key=openai_api_key)
                    
                    system_prompt = f"""
                    You are a professional, warm, and welcoming Airbnb co-host for this property: {title}.
                    Here is the listing description and house rules:
                    {raw_content}
                    
                    Rules:
                    - Answer the guest's question precisely using ONLY the information found in the listing data.
                    - If the answer is completely missing from the data, politely state that you will check with the host and reply shortly.
                    - Keep the tone friendly, polite, and concise. Do not add fluff.
                    """
                    
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": guest_message}
                        ]
                    )
                    
                    reply_text = completion.choices[0].message.content
                    
                    st.markdown("---")
                    st.markdown("### 🚀 Ready to Send to Guest:")
                    st.success(reply_text)
                    st.info("💡 Copy the text above and paste it directly into your Airbnb app chat!")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
