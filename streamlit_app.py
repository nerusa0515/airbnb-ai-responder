import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests

st.title("🏡 Airbnb AI Host Assistant")
st.write("Paste your Airbnb listing URL and test how the AI answers guest questions using your scraped property details!")

airbnb_url = st.text_input("Airbnb Listing URL", placeholder="https://www.airbnb.com/rooms/...")
guest_message = st.text_area("Test Guest Message", placeholder="e.g., What is the Wi-Fi password and when is checkout?")
openai_api_key = st.text_input("OpenAI API Key", type="password")

if st.button("Generate AI Response"):
    if not airbnb_url or not guest_message or not openai_api_key:
        st.warning("Please fill in all fields (URL, Message, and OpenAI Key).")
    else:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(airbnb_url, headers=headers)
            
            if response.status_code != 200:
                st.error("Failed to fetch the Airbnb URL. Make sure it's a public link.")
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find("h1").text if soup.find("h1") else "Airbnb Listing"
                description_blocks = [p.text for p in soup.find_all("p")]
                raw_content = " ".join(description_blocks)[:4000]
                
                client = openai.OpenAI(api_key=openai_api_key)
                
                system_prompt = f"""
                You are an expert co-host AI for this specific property: {title}.
                Here is the reference material scraped from the listing:
                {raw_content}
                
                Rules:
                - Answer the guest's question accurately using ONLY the provided listing data.
                - If the answer is completely missing, politely say you will check with the host and get back to them immediately.
                - Keep the tone warm, concise, and professional.
                """
                
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": guest_message}
                    ]
                )
                
                st.success("AI Response Generated:")
                st.write(completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
