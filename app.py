import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os
import tempfile
import playsound
#Voice Output 
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        os.system(f'start /min wmplayer "{fp.name}"')  
# Product Data
products = {
    "milk": {"price": 42, "reviews": "Fresh and good quality."},
    "bread": {"price": 35, "reviews": "Soft and tasty."},
    "sugar": {"price": 50, "reviews": "Pure and fine."},
    "detergent": {"price": 85, "reviews": "Cleans well and smells great."}
}
# Cart Initialization
if 'cart' not in st.session_state:
    st.session_state.cart = []
#  Voice Recognition 
def recognize_speech():
    r = sr.Recognizer()
    mic_index = 1  
    with sr.Microphone(device_index=mic_index) as source:
        speak("Listening")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        command = r.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t understand.")
        return ""
    except sr.RequestError:
        speak("Could not reach the service.")
        return ""
#Command Processing 
def process_command(command):
    if "add" in command:
        for item in products:
            if item in command:
                st.session_state.cart.append(item)
                speak(f"Added {item} to your cart.")
                return
        speak("Sorry, product not found.")

    elif "remove" in command:
        for item in products:
            if item in command and item in st.session_state.cart:
                st.session_state.cart.remove(item)
                speak(f"Removed {item} from your cart.")
                return
        speak("Item not in cart.")

    elif "what's in my cart" in command or "show cart" in command:
        if not st.session_state.cart:
            speak("Your cart is empty.")
        else:
            cart_items = ", ".join(st.session_state.cart)
            speak(f"Your cart has {cart_items}.")

    elif "review" in command:
        for item in products:
            if item in command:
                speak(products[item]["reviews"])
                return
        speak("Sorry, no review found.")

    elif "price" in command:
        for item in products:
            if item in command:
                speak(f"The price of {item} is {products[item]['price']} rupees.")
                return
        speak("Price not found.")

    elif "check out" in command:
        if not st.session_state.cart:
            speak("Your cart is empty.")
        else:
            total = sum(products[item]["price"] for item in st.session_state.cart)
            speak(f"Checked out. Total is {total} rupees. Thank you!")
            st.session_state.cart = []
# Streamlit UI
st.set_page_config(page_title="VocalCart", layout="centered")
st.title("🛍️ VocalCart - Voice Shopping Assistant")
st.markdown("A voice-based shopping interface designed for visually challenged users.")

if st.button("🎙️ Speak Command"):
    command = recognize_speech()
    if command:
        st.write(f"🗣️ You said: `{command}`")
        process_command(command)
    else:
        st.write("⚠️ Could not understand. Please try again.")

st.markdown("### 🛒 Cart Contents")
if st.session_state.cart:
    for item in st.session_state.cart:
        st.markdown(f"- **{item.title()}** – ₹{products[item]['price']}")
else:
    st.markdown("_Cart is empty._")
