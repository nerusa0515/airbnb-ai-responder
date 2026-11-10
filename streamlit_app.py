import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests

# Page configuration
st.set_page_config(page_title="Airbnb AI Co-Host", page_icon="🏡", layout="centered")

# Custom CSS for a bright, modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input, .stSelectbox > div > div > select {
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

# Header
st.markdown("<h1 style='color: #FF385C; text-align: center;'>🏡 Personalized Airbnb AI Co-Host</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Warm, custom-tailored replies for every type of guest.</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Property & Message Setup")

# Input fields
airbnb_url = st.text_input("🔗 Airbnb Listing URL", placeholder="https://www.airbnb.com/rooms/12345678")

guest_profile = st.selectbox(
    "👤 Who is the guest?",
    [
        "General Guest",
        "Family with Kids",
        "Business Traveler / Remote Worker",
        "Couple on Vacation",
        "Pet Owner",
        "First-Time Airbnb Guest"
    ]
)

guest_message = st.text_area(
    "💬 Guest's Message", 
    placeholder="Paste the guest's message here (e.g., 'What time is check-in and is the neighborhood quiet?')"
)

openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-proj-...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Generate Personalized AI Response"):
    if not airbnb_url or not guest_message or not openai_api_key:
        st.error("⚠️ Please complete all fields above.")
    else:
        with st.spinner("🤖 Crafting a personalized, friendly reply..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(airbnb_url, headers=headers)
                
                if response.status_code != 200:
                    st.error("❌ Could not read the Airbnb URL. Make sure it's a public link.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find("h1").text if soup.find("h1") else "Airbnb Listing"
                    description_blocks = [p.text for p in soup.find_all("p")]
                    raw_content = " ".join(description_blocks)[:4000]
                    
                    client = openai.OpenAI(api_key=openai_api_key)
                    
                    system_prompt = f"""
                    You are an exceptionally warm, hospitable, and accommodating Airbnb superhost for this property: {title}.
                    
                    Here is the reference listing information:
                    {raw_content}
                    
                    Guest Profile Type: {guest_profile}
                    
                    Instructions for Tone & Personalization:
                    - **Be ultra-friendly and accommodating:** Match the guest's profile persona seamlessly.
                      * If 'Family with Kids': Emphasize safety, comfort, child-friendly amenities, or local family activities.
                      * If 'Business Traveler': Keep answers crisp, highlighting Wi-Fi reliability, quiet spaces, and smooth check-in.
                      * If 'Couple on Vacation': Add a romantic, cozy, and welcoming vibe.
                      * If 'Pet Owner': Express enthusiasm for their pet and mention any relevant pet amenities/rules gently.
                      * If 'First-Time Airbnb Guest': Be reassuring, helpful, and walk them gently through the process.
                    - **Accuracy First:** Answer their exact question using ONLY details from the listing.
                    - **Missing Info Handling:** If a detail is missing, say: "I want to make sure I give you the exact details, so I'm checking on that for you right now!"
                    - Keep it polished, natural, and delightful to read.
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
                    st.markdown("### 🚀 Personal Reply Ready to Send:")
                    st.success(reply_text)
                    st.info("💡 Copy and paste this directly into your Airbnb chat!")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
