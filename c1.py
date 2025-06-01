from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Please create .env file with GEMINI_API_KEY=your_key_here")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

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

# HTML Template with Dark Magical Theme
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chai aur Code - Hitesh Sir AI Assistant</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            overflow-x: hidden;
        }
        
        /* Magical Background Animation */
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
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
        
        /* Floating Particles */
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border-radius: 50%;
            animation: float 6s infinite ease-in-out;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 10;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .profile-img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid #ff6b6b;
            margin: 0 auto 20px;
            display: block;
            box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.5); }
            50% { box-shadow: 0 0 50px rgba(255, 107, 107, 0.8); }
            100% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.5); }
        }
        
        .title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 3s ease infinite;
            margin-bottom: 10px;
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
        
        .chat-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            height: 70vh;
            display: flex;
            flex-direction: column;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 10px;
        }
        
        .chat-messages::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-messages::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        
        .chat-messages::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border-radius: 4px;
        }
        
        .message {
            margin-bottom: 20px;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            text-align: right;
        }
        
        .user-message .message-content {
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 5px 20px;
            display: inline-block;
            max-width: 70%;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }
        
        .bot-message .message-content {
            background: linear-gradient(45deg, #4ecdc4, #45b7d1);
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 20px 5px;
            display: inline-block;
            max-width: 80%;
            box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
            white-space: pre-wrap;
        }
        
        .input-container {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .message-input {
            flex: 1;
            padding: 15px 20px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .message-input:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.15);
            border-color: #4ecdc4;
            box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
        }
        
        .message-input::placeholder {
            color: #b8b8b8;
        }
        
        .send-btn {
            padding: 15px 25px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        
        .send-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #4ecdc4;
        }
        
        .loading-dots {
            display: flex;
            gap: 5px;
        }
        
        .loading-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ecdc4;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        
        .welcome-message {
            text-align: center;
            color: #b8b8b8;
            font-style: italic;
            margin: 50px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .title {
                font-size: 2rem;
            }
            
            .chat-container {
                height: 60vh;
                padding: 20px;
            }
            
            .profile-img {
                width: 80px;
                height: 80px;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Stars Background -->
    <div class="stars"></div>
    
    <div class="container">
        <div class="header">
            <img src="https://yt3.ggpht.com/ytc/AIdro_kAkJOKtOPVIrSfZE9_PFaGiJqNEyDpXJfSL3Ow6Q=s88-c-k-c0x00ffffff-no-rj" 
                 alt="Hitesh Choudhary" class="profile-img">
            <h1 class="title">Chai aur Code</h1>
            <p class="subtitle">Ask Hitesh Sir anything about programming! ☕️💻</p>
        </div>
        
        <div class="chat-container">
            <div class="chat-messages" id="chatMessages">
                <div class="welcome-message">
                    <p>🙏 Namaste! Main Hitesh hoon, Chai aur Code se.<br>
                    Aap koi bhi programming sawal pooch sakte ho! ☕️</p>
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" class="message-input" 
                       placeholder="Apna sawal yahan type kariye..." maxlength="500">
                <button id="sendBtn" class="send-btn">Send</button>
            </div>
        </div>
    </div>

    <script>
        // Create animated stars
        function createStars() {
            const starsContainer = document.querySelector('.stars');
            for (let i = 0; i < 100; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                starsContainer.appendChild(star);
            }
        }
        
        // Create floating particles
        function createParticles() {
            const container = document.querySelector('.container');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                container.appendChild(particle);
            }
        }
        
        // Initialize animations
        createStars();
        createParticles();
        
        // Chat functionality
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function showLoading() {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message';
            loadingDiv.id = 'loading-message';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content loading';
            contentDiv.innerHTML = `
                <span>Hitesh Sir typing...</span>
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            `;
            
            loadingDiv.appendChild(contentDiv);
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function hideLoading() {
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
        }
        
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            messageInput.value = '';
            sendBtn.disabled = true;
            showLoading();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                hideLoading();
                
                if (data.error) {
                    addMessage(`Sorry bhai, kuch technical issue hai: ${data.error}`);
                } else {
                    addMessage(data.response);
                }
            } catch (error) {
                hideLoading();
                addMessage('Sorry, server se connection nahi ho pa raha. Thoda baad try kariye!');
            }
            
            sendBtn.disabled = false;
        }
        
        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus on input when page loads
        messageInput.focus();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data['message']
        
        # Create full prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser ka sawal: {user_message}\n\nHitesh Sir ke style mein jawab dijiye:"
        
        # Generate response
        chat = model.start_chat(history=[])
        response = chat.send_message(full_prompt)
        
        return jsonify({'response': response.text})
        
    except Exception as e:
        return jsonify({'error': f"Sorry bhai, technical issue! {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting Hitesh Chatbot Server...")
    print("🌐 Open: http://localhost:5000")
    print("☕ Chai aur Code chatbot is ready!")
    app.run(debug=True)