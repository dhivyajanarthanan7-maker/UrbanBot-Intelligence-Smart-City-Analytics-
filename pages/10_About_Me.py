import streamlit as st
from PIL import Image

# Page config
st.set_page_config(
    page_title="Dhivya Janarthanan | Portfolio",
    page_icon="👩‍💻",
    layout="wide"
)

# Load profile image
profile_image = Image.open("profile.jpeg")

# ================= HEADER SECTION =================
col1, col2 = st.columns([1, 3])

with col1:
    st.image(profile_image, width=220)

with col2:
    st.markdown("<h1>Dhivya Janarthanan</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h4>Data Science Aspirant | Former Assistant Professor (ECE)</h4>",
        unsafe_allow_html=True
    )
    st.write(
        """
Postgraduate in Electronics and Communication Engineering with strong academic experience
and a purposeful transition into the IT and Data Science domain.
"""
    )

st.divider()

# ================= PROFESSIONAL SUMMARY =================
st.subheader("Professional Summary")

st.write(
    """
I am a **Postgraduate in Electronics and Communication Engineering** with over **six years of experience**
as an **Assistant Professor** at Tagore Engineering College, Chennai. During my academic career,
I taught core technical subjects including **Computer Networks and Microprocessors**,
mentored over **50+ students**, and guided academic and research-oriented projects.

After taking a planned career break, I enhanced my learning journey by completing
**Montessori Training and STEM Education**, strengthening my ability to explain complex
concepts using structured and interactive approaches.

With a strong motivation to **restart and redefine my professional career**, I chose
**Data Science at HCL–GUVI** as a strategic transition into the IT industry. I am currently
building skills in Python, data analysis, and problem-solving, with a long-term goal of
contributing to data-driven solutions in a professional environment.
"""
)

# ================= CAREER TIMELINE =================
st.subheader("Career Timeline")

st.markdown(
    """
**🎓 Education**
- ME – Communication Systems, Anna University  
- BE – Electronics and Communication Engineering, Anna University  

**🏫 Academic Experience**
- Assistant Professor – ECE Department  
  Tagore Engineering College, Chennai (2012 – 2018)

**📚 Upskilling & Transition**
- Diploma in Montessori Teaching  
- Certified STEM Educator  
- Data Science Program – HCL GUVI
"""
)

# ================= SKILLS =================
st.subheader("Skills")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
**Technical**
- Python (Beginner)
- Computer Networks
- Microprocessors
- Academic Research
"""
    )

with col2:
    st.markdown(
        """
**Professional**
- Student Mentoring
- Project Guidance
- Documentation
- Lesson Planning
"""
    )

with col3:
    st.markdown(
        """
**Soft Skills**
- Clear Communication
- Good Listener
- Quick Learner
- Organized Thinking
"""
    )

# ================= INTERESTS =================
st.subheader("Interests & Strengths")

st.write(
    """
- Reading books and continuous self-learning  
- Teaching and engaging children through interactive methods  
- Explaining complex concepts in a simple and structured way  
"""
)

# ================= CAREER OBJECTIVE =================
st.subheader("Career Objective")

st.write(
    """
To secure a role in the **IT / Data Science domain** where I can effectively combine my
**academic discipline, analytical thinking, and continuous learning mindset**
to grow professionally and contribute meaningfully to organizational goals.
"""
)

# ================= FOOTER =================
st.divider()
st.markdown(
    "<p style='text-align: center; color: grey;'>© Dhivya Janarthanan | Portfolio Homepage</p>",
    unsafe_allow_html=True
)
