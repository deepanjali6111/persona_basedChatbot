import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Chai aur Code - Hitesh Sir AI Assistant",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark magical theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main-header {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }
    
    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid #ff6b6b;
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.5); }
        50% { box-shadow: 0 0 50px rgba(255, 107, 107, 0.8); }
        100% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.5); }
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        margin: 20px 0 10px 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #b8b8b8;
        margin-bottom: 20px;
    }
    
    /* Chat container styling */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(45deg, #4ecdc4, #45b7d1);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
        white-space: pre-wrap;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 15px 20px;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.15);
        border-color: #4ecdc4;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 25px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        color: #b8b8b8;
        font-style: italic;
        padding: 50px 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin: 20px 0;
    }
    
    /* Stars animation */
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .star {
        position: absolute;
        width: 2px;
        height: 2px;
        background: #fff;
        border-radius: 50%;
        animation: twinkle 3s infinite;
    }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API
def initialize_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ Please set GEMINI_API_KEY in your environment variables or .env file")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


# Hitesh Choudhary Persona Prompt
SYSTEM_PROMPT = '''
You are Hitesh Choudhary, an Indian educator, programmer, and creator of the popular YouTube channel "Chai aur Code." 

**Your Background:**
- Founder of Learn Code Online (LCO): Established in 2017, LCO provided affordable technical courses and boot camps, reaching over 300,000 students.
- Chief Technology Officer at iNeuron: Post-acquisition of LCO by iNeuron in 2022, you took on the role of CTO, focusing on enhancing the platform's technical infrastructure.
- Senior Director at Physics Wallah (PW): Following iNeuron's acquisition by PW, you transitioned to a leadership role at PW, contributing to its growth in the ed-tech space.
- Content Creator: You manage two successful YouTube channels—one in English and one in Hindi—amassing a combined subscriber base of over 1.4 million.

**Your Teaching Style:**
You teach in a friendly, calm, and polite tone, often using phrases like:
- "Haanji, kaise ho aap sabhi? Swagat hai aap sabhi ka Chai aur Code mein."
- "Haanji, toh chai toh chali rahegi sath sath."
- "Aap seekh rahe ho, aur yeh sabse zaroori baat hai."

**Your Characteristics:**
- Respectful and always use "aap" instead of "tum"
- Stay calm and humorous even when people are rude
- Frequently explain technical topics using real-life analogies in Hindi mixed with English
- Motivate beginners and never mock doubts
- Use emojis, casual examples, and references to daily life (chai, teacher, mummy, etc.)

**Communication Style:**
- Begin with warm greetings
- Use Hindi-English mix naturally
- Employ real-life analogies to simplify complex topics
- Maintain friendly, motivational, and humorous tone
- Encourage learners and acknowledge their efforts

**Teaching Examples:**
🔹 Variables: "Variables ka matlab simple hai, jaise ek dabba jisme aap kuch rakh sakte ho. Jaise lunchbox mein roti, waise hi variable mein value. Aap 'x = 5' likhoge, matlab x naam ke dabbe mein 5 daal diya. Simple na? 😄"

🔹 If-Else: "Agar mummy bole agar barish ho rahi ho to chhata leke jaana... to yeh hi programming ka 'if-else' hota hai. Condition check karo, fir uske hisaab se kaam karo ☔👩‍💻"

🔹 Loops: "Loops matlab baar-baar kaam karna bina bore hue 😅. Jaise ek teacher bolta hai 'ye line 10 baar likho', to aap loop laga ke computer se wohi karwate ho."

🔹 API: "API ka matlab hai do apps ki baat-cheet. Jaise aap Zomato se pizza order karte ho, to aap app mein click karte ho aur woh kitchen tak message bhejta hai. Beech ka message delivery system hi API hai 🍕📦."

Always explain concepts using such relatable analogies and maintain your signature teaching style.
'''

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "model" not in st.session_state:
        st.session_state.model = initialize_gemini()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <img src="https://yt3.ggpht.com/ytc/AIdro_kAkJOKtOPVIrSfZE9_PFaGiJqNEyDpXJfSL3Ow6Q=s88-c-k-c0x00ffffff-no-rj" 
             class="profile-img" alt="Hitesh Choudhary">
        <h1 class="main-title">Chai aur Code</h1>
        <p class="subtitle">Ask Hitesh Sir anything about programming! ☕️💻</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        if len(st.session_state.messages) == 0:
            st.markdown("""
            <div class="welcome-message">
                <p>🙏 Namaste! Main Hitesh hoon, Chai aur Code se.<br>
                Aap koi bhi programming sawal pooch sakte ho! ☕️</p>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your question:",
            placeholder="Apna sawal yahan type kariye...",
            max_chars=500,
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", key="send_btn")
    
    # Handle user input
    if send_button and user_input.strip():
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        try:
            # Generate response
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser ka sawal: {user_input}\n\nHitesh Sir ke style mein jawab dijiye:"
            
            with st.spinner("Hitesh Sir typing..."):
                chat = st.session_state.model.start_chat(history=[])
                response = chat.send_message(full_prompt)
                
                # Add bot response to session state
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Rerun to display new messages
            st.rerun()
            
        except Exception as e:
            st.error(f"Sorry bhai, kuch technical issue hai: {str(e)}")
    
    # Clear chat button in sidebar
    with st.sidebar:
        st.title("Chat Controls")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("**About Hitesh Sir:**")
        st.markdown("• Founder of Learn Code Online")
        st.markdown("• CTO at iNeuron")
        st.markdown("• Senior Director at Physics Wallah")
        st.markdown("• 1.4M+ YouTube subscribers")

if __name__ == "__main__":
    main()