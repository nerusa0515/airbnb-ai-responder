import streamlit as st

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
st.markdown("<h1 style='color: #FF385C; text-align: center;'>🏡 Personalized Airbnb Co-Host</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Smart template replies tailored for every type of guest (No API Key Required).</p>", unsafe_allow_html=True)

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
    placeholder="Type or paste the guest's message here (e.g., 'What time is check-in?')"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Generate Custom Reply"):
    if not airbnb_url or not guest_message:
        st.error("⚠️ Please fill in both the Airbnb Listing URL and the guest message.")
    else:
        with st.spinner("🏡 Crafting your tailored host response..."):
            
            # Smart profile-based response builder (No API Key needed)
            message_lower = guest_message.lower()
            
            # Base response depending on the core question
            if "check-in" in message_lower or "arrive" in message_lower:
                core_answer = "Standard check-in is at 3:00 PM or anytime after using our self-check-in keypad lock. I will send you the door code on the morning of your arrival!"
            elif "wifi" in message_lower or "internet" in message_lower:
                core_answer = "Our high-speed Wi-Fi network details and password are conveniently located on the welcome sign right inside the front door."
            elif "parking" in message_lower or "car" in message_lower:
                core_answer = "Free parking is available right on the premises for your convenience."
            else:
                core_answer = f"Thank you so much for reaching out! Regarding your question about '{guest_message}', everything is set up and ready for your stay."

            # Customize greeting/tone based on guest profile
            if guest_profile == "Family with Kids":
                intro = "Hi there! We are so excited to host you and your family."
                extra = " We've made sure the space is cozy, safe, and family-friendly for everyone."
            elif guest_profile == "Business Traveler / Remote Worker":
                intro = "Hello! Thanks for choosing our space for your trip."
                extra = " We know how important reliable Wi-Fi and a quiet environment are for productivity."
            elif guest_profile == "Couple on Vacation":
                intro = "Hi! We are thrilled to host your getaway."
                extra = " We hope you have a wonderfully relaxing and memorable time together."
            elif guest_profile == "Pet Owner":
                intro = "Hello! We are delighted to welcome you and your furry friend."
                extra = " We love hosting pets and hope they enjoy the stay just as much as you do."
            elif guest_profile == "First-Time Airbnb Guest":
                intro = "Hi there! A special welcome to Airbnb—we are honored to be your first stay!"
                extra = " If you have any questions about how anything works during your stay, please don't hesitate to ask."
            else:
                intro = "Hi there! Thanks so much for reaching out."
                extra = " We are looking forward to hosting you."

            # Final composed response
            reply_text = f"{intro} {core_answer}{extra} Let me know if you need anything else before you arrive!"

            st.markdown("---")
            st.markdown("### 🚀 Personal Reply Ready to Send:")
            st.success(reply_text)
            st.info("💡 Copy and paste this directly into your Airbnb chat!")
