import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# ------------------ DARK MODE ------------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    h1,h2,h3,h4,h5,h6,p,div {color: white !important;}
    .card {background-color: #1e1e1e !important;}
    .stButton>button {background-color: #262730; color: white;}
    section[data-testid="stSidebar"] {background-color: #111 !important;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {background-color: #f4f6f9;}
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align: center; color:#4CAF50;'>📄 AI Resume Analyzer Pro</h1>", unsafe_allow_html=True)
st.caption("Analyze your resume with AI insights 🚀")

# ------------------ FUNCTIONS ------------------

def extract_text(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# 🔥 MULTI-DOMAIN SKILLS
skills_list = [
    "python","sql","power bi","excel","machine learning","data analysis","pandas","numpy",
    "civil","construction","autocad","site",
    "mechanical","cad","manufacturing",
    "teaching","education","subject",
    "cooking","food","kitchen","menu","chef",
    "design","photoshop","illustrator",
    "finance","accounting","banking",
    "management","leadership","project"
]

def extract_skills(text):
    text = text.lower()
    return list(set([skill for skill in skills_list if skill in text]))

def calculate_score(skills):
    return round((len(skills) / len(skills_list)) * 100, 2)

# ------------------ ROLE DATABASE ------------------

job_roles = {
    "Data Analyst": ["python","sql","excel","data analysis"],
    "Data Scientist": ["python","machine learning","pandas","numpy"],
    "Software Developer": ["java","python","c++","programming"],
    "Civil Engineer": ["civil","construction","autocad","site"],
    "Mechanical Engineer": ["mechanical","cad","manufacturing"],
    "Teacher": ["teaching","education","subject"],
    "Chef": ["cooking","food","kitchen","menu"],
    "Graphic Designer": ["design","photoshop","illustrator"],
    "Accountant": ["finance","accounting","excel"],
    "Project Manager": ["management","leadership","project"]
}

# 🔥 ROLE MATCHING
def get_best_roles(skills):
    scores = {}
    for role, req in job_roles.items():
        match = len(set(skills) & set(req))
        scores[role] = match

    filtered = {r: s for r, s in scores.items() if s >= 2}
    sorted_roles = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return sorted_roles[:3]

# 🔥 ROLE-BASED GAP (FIXED)
def get_role_based_gap(skills, roles):
    gap = []
    for role, _ in roles:
        missing = list(set(job_roles[role]) - set(skills))
        gap.extend(missing)
    return list(set(gap))

def suggest_improvements(gap):
    return [f"Learn {skill}" for skill in gap]

# ------------------ CHATBOT ------------------

def simple_chatbot(query, skills, gap, roles):
    query = query.lower()

    if "role" in query:
        return f"Best roles: {', '.join([r for r,_ in roles])}"

    if "skills" in query:
        return f"Your skills: {', '.join(skills)}"

    if "improve" in query:
        return f"Learn: {', '.join(gap)}"

    return "Ask about roles, skills, or improvements."

# ------------------ SIDEBAR ------------------

st.sidebar.header("📌 Navigation")
section = st.sidebar.radio("Go to", ["Upload Resume","About"])

# ------------------ MAIN ------------------

if section == "Upload Resume":

    uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")
    analyze = st.button("🚀 Analyze Resume")

    if uploaded_file and analyze:

        text = extract_text(uploaded_file)
        skills = extract_skills(text)
        score = calculate_score(skills)
        roles = get_best_roles(skills)
        gap = get_role_based_gap(skills, roles)
        suggestions = suggest_improvements(gap)

        # SCORE
        st.subheader("⭐ Resume Score")
        st.progress(int(score))
        st.metric("Score", f"{score}/100")

        # SKILLS + GAP
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Skills")
            for s in skills:
                st.markdown(f"✔️ {s}")

        with col2:
            st.subheader("📉 Missing Skills")
            for g in gap:
                st.markdown(f"❌ {g}")

            # GRAPH
            labels = ["Skills","Missing"]
            values = [len(skills), len(gap)]
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            st.pyplot(fig)

        # SUGGESTIONS
        st.subheader("📈 Suggestions")
        for s in suggestions:
            st.markdown(f"💡 {s}")

        # ROLES
        st.subheader("🤖 Career Suggestions")
        if roles:
            for role, val in roles:
                percent = int((val / len(job_roles[role])) * 100)
                st.markdown(f"👉 **{role}** ({percent}%)")
        else:
            st.warning("No strong match found")

        # CHATBOT
        st.subheader("💬 Chatbot")
        user_input = st.text_input("Ask something...")
        if user_input:
            st.success(simple_chatbot(user_input, skills, gap, roles))

        # TEXT
        with st.expander("📄 Resume Text"):
            st.write(text)

# ------------------ ABOUT ------------------

elif section == "About":
    st.write("AI Resume Analyzer with hybrid role matching system.")