import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Set page config
st.set_page_config(
    page_title="Virtual Assistant Selector",
    page_icon="🤖",
    layout="centered"  # Changed to centered for better mobile experience
)

# Custom CSS for styling
st.markdown("""
<style>
    .birthday-text {
        font-size: 28px;
        color: #FF69B4;
        font-weight: bold;
        text-align: center;
        animation: rainbow 5s infinite;
    }
    @keyframes rainbow {
        0% {color: #FF69B4;}
        20% {color: #FF6347;}
        40% {color: #FFD700;}
        60% {color: #7CFC00;}
        80% {color: #1E90FF;}
        100% {color: #FF69B4;}
    }
    .hidden {
        display: none;
    }
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f00;
        animation: fall 5s ease-in infinite;
    }
    @keyframes fall {
        0% {transform: translateY(0) rotate(0deg);}
        100% {transform: translateY(100vh) rotate(360deg);}
    }
    /* Mobile-friendly styling */
    .assistant-option {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .assistant-option:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .assistant-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 15px;
    }
    /* Make buttons more mobile-friendly */
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 18px;
    }
    /* Mobile-optimized charts */
    .st-emotion-cache-1v0mbdj.e115fcil1 {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'assistant_selected' not in st.session_state:
    st.session_state.assistant_selected = False
if 'show_birthday' not in st.session_state:
    st.session_state.show_birthday = False

# Function to create assistant cards
def create_assistant_card(name, description, icon):
    return f"""
    <div class="assistant-option" onclick="this.style.backgroundColor='#f0f0f0';">
        <h3>{icon} {name}</h3>
        <p>{description}</p>
    </div>
    """

# Dictionary of assistants
assistants = {
    "claude": {
        "name": "Claude",
        "description": "An AI assistant with a focus on helpful, harmless, and honest interactions.",
        "icon": "🧠"
    },
    "gpt": {
        "name": "ChatGPT",
        "description": "A conversational AI model that can discuss a wide range of topics.",
        "icon": "💬"
    },
    "alexa": {
        "name": "Alexa",
        "description": "A virtual assistant that can help with smart home control and everyday questions.",
        "icon": "🔊"
    },
    "siri": {
        "name": "Siri",
        "description": "A personal assistant designed to help with tasks on your devices.",
        "icon": "🍎"
    },
    "gemini": {
        "name": "Gemini",
        "description": "An AI assistant that combines various learning capabilities.",
        "icon": "♊"
    },
    "bard": {
        "name": "Bard",
        "description": "A creative AI assistant with language capabilities.",
        "icon": "📝"
    }
}

# Function to create a birthday card image
def create_birthday_card(name):
    # Create a new image with a white background
    width, height = 600, 400
    background_color = (255, 255, 255)
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, or use default if not available
    try:
        font = ImageFont.truetype("Arial.ttf", 36)
        small_font = ImageFont.truetype("Arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw a decorative border
    border_width = 20
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=(255, 105, 180),
        width=5
    )
    
    # Add some decorative elements
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 15)
        color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
        draw.ellipse([(x, y), (x + size, y + size)], fill=color)
    
    # Add birthday message
    message = f"Happy Birthday!"
    w, h = draw.textsize(message, font=font) if hasattr(draw, 'textsize') else (300, 40)
    draw.text(
        ((width - w) // 2, height // 3),
        message,
        fill=(255, 20, 147),
        font=font
    )
    
    # Add personalized message
    personal_message = f"To {name}, Have a wonderful day!"
    w2, h2 = draw.textsize(personal_message, font=small_font) if hasattr(draw, 'textsize') else (200, 30)
    draw.text(
        ((width - w2) // 2, height // 2 + 20),
        personal_message,
        fill=(70, 130, 180),
        font=small_font
    )
    
    # Convert to bytes for display in Streamlit
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()

# Main app logic
if not st.session_state.assistant_selected and not st.session_state.show_birthday:
    # First page - Assistant selection
    st.title("Choose Your Virtual Assistant")
    st.write("Select the virtual assistant you'd like to use:")
    
    # Display assistant options in a grid
    cols = st.columns(2)
    
    assistant_keys = list(assistants.keys())
    for i in range(0, len(assistant_keys), 2):
        for j in range(2):
            if i + j < len(assistant_keys):
                key = assistant_keys[i + j]
                assistant = assistants[key]
                with cols[j]:
                    if st.button(f"{assistant['icon']} {assistant['name']}", key=key, help=assistant['description']):
                        st.session_state.assistant_selected = key
                        st.session_state.show_birthday = True
                        st.rerun()
                    st.markdown(f"<p>{assistant['description']}</p>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add a "More Options" button at the bottom
    if st.button("More Options...", key="more_options"):
        st.session_state.show_birthday = True
        st.rerun()
elif st.session_state.show_birthday:
    # Create confetti effect
    confetti_html = ""
    for i in range(100):
        x = random.randint(0, 100)
        delay = random.random() * 5
        color = f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"
        confetti_html += f"""
        <div class="confetti" style="left: {x}vw; background-color: {color}; animation-delay: {delay}s;"></div>
        """
    
    st.markdown(confetti_html, unsafe_allow_html=True)
    
    # Display the birthday message with improved styling
    st.markdown("""
    <div style="text-align: center; padding: 10px; margin: 20px 0;">
        <h1 style="font-size: 32px; background: linear-gradient(90deg, #ff69b4, #ff6347, #ffd700, #7cfc00, #1e90ff); 
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: bold; padding: 10px; animation: shimmer 3s infinite linear;">
        🎉 HAPPY BIRTHDAY! 🎂
        </h1>
    </div>
    <style>
    @keyframes shimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 100% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Personal message - Updated with last year's sentiment
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: rgb(255, 105, 180); border-radius: 10px; margin: 20px 0;'>
        <h2>To my amazing friend and mentor,</h2>
        <p style='font-size: 18px;'>
            Last year, I wrote about our journey together - how your guidance became foundational to my way of thinking.
            How without your guidance, I wouldn't be where I am today.
        </p>
        <p style='font-size: 18px;'>
            A year later, and my gratitude has only grown. You're still the most amazing person I've ever met!
            Despite all my questions, mistakes, and probably annoying moments through the years, 
            your big heart and wonderful soul took it all without annoyance.
        </p>
        <p style='font-size: 18px; font-weight: bold;'>
            I am grateful that you exist. I am grateful to have had the honor of learning from you - 
            a great manager, wonderful human, amazing friend and guide. Someone I respect from the core of my heart.
        </p>
        <p style='font-size: 18px;'>
            Language can't capture what I want to say, but I wish you all the happiness and success in the world.
            This year, I wanted to surprise you with something different - but the sentiment remains the same!
        </p>
        <p style='font-style: italic; margin-top: 20px;'>
            With deep admiration and birthday wishes,
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate and display a birthday card
    st.subheader("Your Birthday Card")
    card_image = create_birthday_card("My Wonderful Mentor")  # Updated the name
    st.image(card_image, use_column_width=True)
    
    # Add personalized meaningful content instead of generic charts
    st.subheader("Our Journey Together")
    
    # Create a timeline of your professional relationship
    timeline_data = [
        {"year": "First Meeting", "event": "When you became my manager and I was just starting out, unsure and a bit lost"},
        {"year": "Early Days", "event": "You guided me through the intricacies of field work, explaining planning methodologies"},
        {"year": "Growing", "event": "You showed patience with my endless questions and mistakes"},
        {"year": "Evolving", "event": "Your guidance became foundational to my way of thinking"},
        {"year": "Today", "event": "Even as a former manager, you remain a wonderful friend and mentor"}
    ]
    
    # Create a DataFrame for the timeline
    timeline_df = pd.DataFrame(timeline_data)
    
    # Display the timeline in a more meaningful way with better colors
    st.markdown("""
    <div style="background-color: #FF69B4; border-radius: 10px; padding: 20px; margin-bottom: 20px; color: white;">
        <h3 style="text-align: center; color: white;">Our Professional Journey</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for i, row in enumerate(timeline_data):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="background-color: #FF69B4; color: white; padding: 10px; border-radius: 50%; width: 50px; height: 50px; 
            display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold;">
                {i+1}
            </div>
            <div style="text-align: center; font-weight: bold; margin-top: 10px; color: #FF69B4;">
                {row['year']}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background-color: #FFB6C1; color: #333; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                {row['event']}
            </div>
            """, unsafe_allow_html=True)
    
    # Add a section for qualities you appreciate about your mentor
    st.markdown("""
    <div style="background-color: #FF69B4; border-radius: 10px; padding: 20px; margin: 30px 0 20px 0; color: white;">
        <h3 style="text-align: center; color: white;">What Makes You Amazing</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for qualities
    qualities = [
        {"quality": "Guidance", "description": "Your ability to guide without dictating, allowing room for growth"},
        {"quality": "Patience", "description": "Your endless patience with my questions and mistakes"},
        {"quality": "Wisdom", "description": "Your insightful approach to challenges and problem-solving"},
        {"quality": "Support", "description": "Your unwavering support during difficult times"},
        {"quality": "Friendship", "description": "Your ability to be both a respected mentor and a cherished friend"}
    ]
    
    # Display qualities in an attractive format with better contrast
    for i, quality in enumerate(qualities):
        if i % 2 == 0:
            cols = st.columns(2)
        
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FF69B4 0%, #FF6347 100%); 
                 border-radius: 10px; padding: 20px; margin-bottom: 15px; color: white;">
                <h4 style="color: white; text-align: center; margin-bottom: 10px;">{quality['quality']}</h4>
                <p style="color: white; text-align: center;">{quality['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Add a meaningful section header with better contrast
    st.markdown("""
    <div style="background-color: #FF69B4; border-radius: 10px; padding: 20px; margin: 30px 0 20px 0; color: white;">
        <h3 style="text-align: center; color: white;">From My Heart To Yours</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Fixed personal message without visible tags - More compact version
    st.markdown("""
    <style>
    .personal-message {
        background-color: #FFB6C1;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #FF69B4;
        margin-bottom: 20px;
        text-align: center;
        color: #333;
    }
    .personal-message p {
        font-size: 17px;
        line-height: 1.5;
        margin-bottom: 10px;
        color: #333;
    }
    .personal-message .bold {
        font-weight: bold;
    }
    .personal-message .italic {
        font-style: italic;
        margin-top: 10px;
    }
    </style>
    
    <div class="personal-message">
        <p>As I reflect on our professional journey, there's a hope that burns bright in my heart - that someday, our paths will cross again in work. The thought of collaborating with you once more brings a smile to my face and excitement for what we could accomplish together.</p>
        <p>I'm deeply grateful that you exist in this world. Your presence has made a difference not just in my career, but in how I see myself and my potential. You occupy a special place in my mind - a corner reserved for those rare individuals who truly impact our lives.</p>
        <p>What makes you different is not just your professional brilliance, but the humanity you bring to everything you do. Where others might have seen just another team member, you saw potential. Where others might have grown impatient with questions, you saw curiosity worth nurturing.</p>
        <p class="bold">You are truly one of a kind, and on your birthday, I want you to know that your impact continues to ripple through my life. Whether we work together again or our paths remain separate, the lessons you've taught me and the confidence you've helped me build will always be part of who I am.</p>
        <p class="italic">Thank you for being you - the extraordinary person who made all the difference.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a special YouTube music embed with better header
    st.markdown("""
    <div style="background-color: #FF69B4; border-radius: 10px; padding: 20px; margin: 30px 0 20px 0; color: white;">
        <h3 style="text-align: center; color: white;">A Birthday Song Just For You</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Use a reliable YouTube embed instead of SoundCloud
    st.markdown("""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <iframe width="100%" height="315" src="https://www.youtube.com/embed/nl62hhiBMOM" 
        title="YouTube video player" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>
    </div>
    <p style="text-align: center; font-style: italic;">A special song to brighten your day!</p>
    """, unsafe_allow_html=True)

    # Add a fun button at the end
    if st.button("Send More Birthday Wishes! 🎉"):
        st.balloons()
        st.snow()
        st.success("More birthday wishes sent! Have an amazing day! 🎂")

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ for your special day!*")