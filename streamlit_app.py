import streamlit as st
from datetime import datetime
import random

# --- Custom Wellness Functions ---
def generate_workout_plan(fitness_level="beginner", focus_area="full body"):
    workouts = {
        "beginner": {
            "full body": ["Bodyweight squats: 3x10", "Push-ups (knees): 3x8", "Plank: 30 sec"],
            "upper body": ["Wall push-ups: 3x10", "Arm circles: 3x15", "Shoulder taps: 3x10"],
            "lower body": ["Chair squats: 3x10", "Standing calf raises: 3x12", "Glute bridges: 3x8"]
        },
        "intermediate": {
            "full body": ["Jump squats: 3x12", "Push-ups: 3x10", "Mountain climbers: 3x15"],
            "upper body": ["Diamond push-ups: 3x8", "Superman holds: 3x20 sec", "Tricep dips: 3x10"],
            "lower body": ["Lunges: 3x10 each", "Single-leg deadlifts: 3x8", "Wall sit: 1 min"]
        }
    }
    return workouts.get(fitness_level, {}).get(focus_area, ["No plan available"])

def create_meditation_guide(duration=5):
    techniques = [
        "Focus on your breath: Inhale for 4 counts, hold for 4, exhale for 6",
        "Body scan: Gradually relax each body part from toes to head",
        "Mantra repetition: Silently repeat 'peace' or 'calm' with each exhale"
    ]
    return f"""
🧘 {random.choice(techniques)}
⏰ Duration: {duration} minutes
🌿 Environment: Quiet space, comfortable position
"""

def analyze_sleep_pattern(bedtime, wake_time):
    bed = datetime.strptime(bedtime, "%H:%M")
    wake = datetime.strptime(wake_time, "%H:%M")
    duration = (wake - bed).seconds / 3600
    if duration >= 8: return "😊 Excellent sleep duration!"
    elif duration >= 7: return "🙂 Good, but could use 30-60 more minutes"
    else: return "😴 Consider extending your sleep by 1-2 hours"

# --- Streamlit UI ---
st.set_page_config(
    page_title="🌿 Health Wellness Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for unique styling
st.markdown("""
<style>
.header {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
}
.pill-button {
    border-radius: 20px;
    padding: 0.5rem 1rem;
    margin: 0.3rem;
    border: none;
    background-color: #f0f2f6;
    color: #2575fc;
    font-weight: 500;
}
.pill-button:hover {
    background-color: #2575fc;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Header with gradient
st.markdown("""
<div class="header">
<h1 style='text-align: center; margin: 0;'>🌿 Fitness Journey</h1>
<p style='text-align: center; margin: 0; font-size: 1.1rem;'>Your personalized guide to healthy LifeStyle</p>
</div>
""", unsafe_allow_html=True)

# Three-column layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 🏋️‍♂️ Quick Tools")
    tool = st.radio("Select a tool:", 
                   ["Workout Generator", "Meditation Guide", "Sleep Analyzer"])
    
    if tool == "Workout Generator":
        fitness_level = st.selectbox("Your level:", ["beginner", "intermediate"])
        focus_area = st.selectbox("Focus area:", ["full body", "upper body", "lower body"])
        if st.button("Generate Workout"):
            workout = generate_workout_plan(fitness_level, focus_area)
            st.session_state.workout_result = workout
    
    elif tool == "Meditation Guide":
        duration = st.slider("Minutes:", 1, 20, 5)
        if st.button("Create Guide"):
            st.session_state.meditation_guide = create_meditation_guide(duration)
    
    elif tool == "Sleep Analyzer":
        bedtime = st.text_input("Bedtime (HH:MM)", "22:30")
        wake_time = st.text_input("Wake time (HH:MM)", "06:30")
        if st.button("Analyze Sleep"):
            st.session_state.sleep_analysis = analyze_sleep_pattern(bedtime, wake_time)

with col2:
    st.markdown("### 📝 Your Fitness Coach")
    journal_entry = st.text_area("How are you feeling today?", height=150)
    
    if st.button("Save Entry", key="journal_save"):
        if 'journal' not in st.session_state:
            st.session_state.journal = []
        st.session_state.journal.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "entry": journal_entry
        })
        st.success("Journal saved!")
    
    if 'journal' in st.session_state and st.session_state.journal:
        st.markdown("### 📖 Previous Entries")
        for entry in reversed(st.session_state.journal[-3:]):
            st.markdown(f"**{entry['date']}**\n{entry['entry']}\n---")

with col3:
    st.markdown("### 🌟 Today's Healthy Tip")
    daily_tips = [
        "Drink a glass of water first thing in the morning",
        "inhale deeply and exhale slowly for 5 minutes",
        "Stretch for 2 minutes every hour",
        "Write down 3 things you're grateful for today",
        "Try the 20-20-20 rule: Every 20 mins, look 20 feet away for 20 sec"
        "Take a 5-minute walk outside to refresh your mind",
        "take a healthy snack like fruits or nuts for yur appetite",
        "Practice deep breathing for 2 minutes to reduce stress",
        "Spend 10 minutes in nature to boost your mood",
    ]
    st.markdown(f'<div style="background-color:#f0f2f6; padding:1rem; border-radius:10px;">✨ {random.choice(daily_tips)}</div>', 
                unsafe_allow_html=True)
    
    st.markdown("### 📊 Activity Results")
    if tool == "Workout Generator" and 'workout_result' in st.session_state:
        st.markdown("**Your Custom Workout:**")
        for exercise in st.session_state.workout_result:
            st.markdown(f"- {exercise}")
    
    elif tool == "Meditation Guide" and 'meditation_guide' in st.session_state:
        st.markdown(st.session_state.meditation_guide)
    elif tool == "Sleep Analyzer" and 'sleep_analysis' in st.session_state:
        st.markdown(f"**Sleep Analysis:** {st.session_state.sleep_analysis}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>🌱 Nourish your mind, body, and soul</p>", 
            unsafe_allow_html=True)
