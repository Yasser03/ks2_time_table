# Kumon-Style Multiplication Timetable Practice
# Yasser Mustafa WE. 13/11/2019
# Enhanced with Kumon methodology principles

from random import randint
import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Kumon Multiplication Timetable", layout="wide")

# Initialize session state for tracking progress
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'problems_correct' not in st.session_state:
    st.session_state.problems_correct = 0
if 'problems_total' not in st.session_state:
    st.session_state.problems_total = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

st.title("🎯 Kumon Multiplication Timetable")
st.markdown("*Master multiplication through consistent daily practice*")

# Sidebar for level selection and progress
with st.sidebar:
    st.header("📊 Your Progress")
    st.session_state.level = st.selectbox(
        "Select Your Level:",
        options=list(range(1, 11)),
        index=st.session_state.level - 1,
        help="Level 1: 1×1 to 1×10 | Level 10: 9×9 to 9×9"
    )
    
    if st.session_state.problems_total > 0:
        accuracy = (st.session_state.problems_correct / st.session_state.problems_total) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
        st.metric("Problems Solved", st.session_state.problems_total)
        
        if accuracy >= 90 and st.session_state.problems_total >= 10:
            st.success("🌟 Ready to advance to next level!")
    
    if st.button("Reset Progress", key="reset"):
        st.session_state.problems_correct = 0
        st.session_state.problems_total = 0
        st.rerun()

# Define level difficulty ranges
def get_level_range(level):
    ranges = {
        1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4), 5: (1, 5),
        6: (2, 6), 7: (3, 7), 8: (4, 8), 9: (5, 9), 10: (6, 10)
    }
    return ranges.get(level, (1, 10))

@st.cache_data
def get_two_random_numbers(level):
    """Generate random numbers based on Kumon level"""
    min_val, max_val = get_level_range(level)
    x = randint(min_val, max_val)
    y = randint(min_val, max_val)
    return x, y

# Display level information
min_range, max_range = get_level_range(st.session_state.level)
st.info(f"**Level {st.session_state.level}**: Multiplying numbers from {min_range} to {max_range}")

# Generate problem
x, y = get_two_random_numbers(st.session_state.level)
result = x * y

# Display problem in Kumon style (clear, simple format)
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown(f"### {x}")
with col2:
    st.markdown("### ×")
with col3:
    st.markdown(f"### {y}")

st.markdown("___________")

# Timer for speed practice
col1, col2 = st.columns([3, 1])
with col1:
    answer = st.number_input('Enter your answer:', value=0, key="answer_input")
with col2:
    st.markdown("⏱️ **Speed Practice**")

# Submit button
if st.button("✓ Submit Answer", type="primary", use_container_width=True):
    st.session_state.problems_total += 1
    
    if answer == result:
        st.session_state.problems_correct += 1
        st.success(f"✅ Correct! The answer is {result}")
        st.balloons()
        
        # Kumon encouragement
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Answer", answer)
        with col2:
            st.metric("Correct!", "👍")
            
    else:
        st.error(f"❌ Not quite right")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Answer", answer)
        with col2:
            st.metric("Correct Answer", result)
        st.info("💡 Try again! Kumon teaches us that mistakes are learning opportunities.")

# Kumon methodology tips
with st.expander("📚 Kumon Tips for Success"):
    st.markdown("""
    - **Practice Daily**: Even 15-20 minutes daily builds strong foundations
    - **Focus on Accuracy First**: Speed comes naturally with accuracy
    - **Advance Gradually**: Move to the next level only when you achieve 90%+ accuracy
    - **Review Regularly**: Revisit previous levels to maintain skills
    - **Self-Correction**: Understand why an answer is wrong, not just memorize
    ```
    )

st.markdown("---")
st.caption("Keep practicing! Each problem builds your mental math skills. 🎯")
