

 
import streamlit as st
import json
from datetime import datetime
import urllib.parse
import os
 
HISTORY_FILE = "history.json"
 
# Load history from file
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = {"url": [], "username": [], "logs": [], "reports": []}
 
# Function to update history
def update_history(field, value):
    if value and value not in history[field]:
        history[field].insert(0, value)  # add to top
        history[field] = history[field][:1]  # keep only last 4
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
 
 
# --- Page Config ---
st.set_page_config(
    page_title="OTCS Config Form",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
#--- Custom CSS Theme ---
#(Your existing CSS remains unchanged)
st.markdown("""
<style>
    :root {
        --primary: #005eb8;
        --primary-dark: #004a93;
        --secondary: #6c757d;
        --success: #28a745;
        --danger: #dc3545;
        --light: #f8f9fa;
        --dark: #212529;
        --gradient-start: #005eb8;
        --gradient-end: #00a3e0;
    }
    /* ... rest of your CSS remains unchanged ... */
             
    .stApp {
        background: linear-gradient(45deg, #e4edf5 0%, #f5f7fa 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-x: hidden;
    }
 
    /* Animated Header with Logo */
    .header {
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
        padding: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        border-radius: 0 0 30px 30px;
        position: relative;
        overflow: hidden;
        margin-bottom: 3rem;
    }
 
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shine 4s infinite;
    }
 
    @keyframes shine {
        0% { left: -100%; }
        50% { left: 100%; }
        100% { left: 100%; }
    }
 
    .opentext-logo {
        width: 200px;
        animation: logo-pulse 3s ease-in-out infinite;
    }
 
    @keyframes logo-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
 
    .hero-subtext {
        font-size: 1.2rem;
        color: #ffffff;
        margin-top: 1rem;
        opacity: 0;
        animation: fadeInUp 1s ease-out forwards;
        animation-delay: 0.5s;
    }
 
    /* Card Styling with Animation */
    .form-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
        overflow: hidden;
        margin: 0 auto 3rem;
        max-width: 700px;
        animation: slideIn 0.8s ease-out;
    }
 
    .form-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
 
    .card-header {
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
        color: white;
        padding: 1.5rem;
        font-weight: 600;
        font-size: 1.5rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }
 
    .card-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: slideLine 3s infinite;
    }
 
    @keyframes slideLine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
 
    .card-body {
        padding: 2.5rem;
    }
 
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
        color: white;
        border-radius: 10px;
        padding: 14px 28px;
        border: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        position: relative;
        overflow: hidden;
        margin-top: 1.5rem;
    }
 
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 94, 184, 0.4);
        background: linear-gradient(90deg, var(--gradient-end), var(--gradient-start));
    }
 
    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
 
    .stButton>button:hover::after {
        left: 100%;
    }
 
    /* Input and Textarea Styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #d1d5db;
        padding: 14px 16px;
        transition: border-color 0.3s ease;
        font-size: 1rem;
    }
 
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 10px rgba(0, 94, 184, 0.3);
    }
 
    /* Section Title */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 1.5rem;
        position: relative;
        padding-bottom: 0.8rem;
        text-align: center;
        animation: fadeIn 1s ease-out;
    }
 
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
        border-radius: 4px;
        animation: expandLine 1.5s ease-out;
    }
 
    @keyframes expandLine {
        from { width: 0; }
        to { width: 100px; }
    }
 
    /* Animations */
    @keyframes slideIn {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
 
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
 
    @keyframes fadeInUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
 
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #eeeff2;
        background-color: #011969;
        font-size: 0.95rem;
        margin-top: 3rem;
        border-top: 1px solid #eaeaea;
        animation: fadeIn 1s ease-out;
        border-radius: -2px 30px 0 0;
    }
 
    /* Input Icons */
    .input-icon {
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.2rem;
        color: var(--primary);
        z-index: 2;
    }
 
    .input-container {
        position: relative;
        margin-bottom: 1.8rem;
    }
 
    .input-container input {
        padding-left: 45px !important;
    }
 
    /* Success Message */
    .success-box {
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        border-left: 5px solid #00a3e0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem auto;
        max-width: 700px;
        animation: slideIn 0.6s ease-out;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
 
    .success-icon {
        font-size: 3rem;
        color: #28a745;
        margin-bottom: 1rem;
        animation: logo-pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)
 
# --- Header with Logo ---
st.markdown("""
<div class="header">
    <div class="container" style="padding: 0 2rem;">
        <img src="https://cdn.1min30.com/wp-content/uploads/2018/05/Embl%C3%A8me-Capgemini.jpg" class="opentext-logo" alt="OpenText Logo">
        <p class="hero-subtext">Configuration Management Portal</p>
    </div>
</div>
""", unsafe_allow_html=True)
 
# --- Section Title ---
st.markdown("""
<div class="container">
    <h2 class="section-title">OTCS Configuration Form</h2>
    <p style="text-align: center; margin-bottom: 2rem; font-size: 1.1rem; color: #555; animation: fadeInUp 1s ease-out;">
        Fill out the required configuration details below to generate your OTCS setup file
    </p>
</div>
""", unsafe_allow_html=True)
 
# --- Initialize Session State ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "last_submission" not in st.session_state:
    st.session_state.last_submission = {}
 
# --- Get return_url from query parameters ---
query_params = st.query_params
return_url = query_params.get("return_url", [""])[0]
 
# --- Validate and decode return_url ---
try:
    return_url = urllib.parse.unquote(return_url)
    # Check if return_url is a file:// URL or empty; provide fallback if needed
    if not return_url or not return_url.startswith("file://"):
        return_url = "http://localhost:8000/ui3.html"
except Exception:
    return_url = "http://localhost:8000/ui3.html"
 
# --- Form Card ---
with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">System Configuration</div>', unsafe_allow_html=True)
 
   
    with st.form("otcs_form"):
     st.markdown('<div class="card-body">', unsafe_allow_html=True)
 
     value_from_history = history["url"][0] if history["url"] else ""
     st.markdown(f"""
       <div style="margin-bottom: 0.2rem;">
       🔗 OTCS URL <span style="color:red;">*</span>
      </div>
       """, unsafe_allow_html=True)
 
     url = st.text_input("", value=value_from_history, placeholder="https://your-opentext-server.com", label_visibility="collapsed", key="url_input")
 
     value_from_histor = history["username"][0] if history["username"] else ""
     st.markdown(f"""
       <div style="margin-bottom: 0.2rem;">
       👤 OTCS Username <span style="color:red;">*</span>
      </div>
       """, unsafe_allow_html=True)
 
     username = st.text_input("", value=value_from_histor, placeholder="Enter your username", label_visibility="collapsed", key="username_input")
 
 
     password_html = """
      <div style="margin-bottom: 0.2rem;">
       👤 OTCS password <span style="color:red;">*</span>
       </div>
       """
     st.markdown(password_html, unsafe_allow_html=True)
 
     password = st.text_input(
     label="",
     type="password",
     placeholder="Enter your password",
     label_visibility="collapsed",
     key="password_input"
     )
 
         
     value_from_histo = history["logs"][0] if history["logs"] else ""
     st.markdown(f"""
       <div style="margin-bottom: 0.2rem;">
       📁 Logs Location
      </div>
       """, unsafe_allow_html=True)
 
     logs_location = st.text_input("", value=value_from_histo, placeholder="Enter your username", label_visibility="collapsed", key="logs_input")
 
 
     value_from_hist = history["reports"][0] if history["reports"] else ""
     st.markdown(f"""
       <div style="margin-bottom: 0.2rem;">
       📂 Reports Location
      </div>
       """, unsafe_allow_html=True)
 
     reports_location = st.text_input("", value=value_from_hist, placeholder="Enter your username", label_visibility="collapsed", key="reports_input")
 
     submitted = st.form_submit_button("🚀 Submit Configuration")
 
     if submitted:
        update_history("url", url)
        update_history("username", username)
        update_history("logs", logs_location)
        update_history("reports", reports_location)
        st.success("Configuration saved successfully!")
       
        if not url or not username or not password:
            st.error("❌ Please fill in all required fields (URL, Username, Password)")
        else:
            form_data = {
                "otcs_url": url,
                "username": username,
                "password": password,
                "logs_location": logs_location,
                "reports_location": reports_location,
                "submitted_at": datetime.now().isoformat()
            }
 
            # Save to JSON
            try:
                with open("otcs_config.json", "w") as f:
                    json.dump(form_data, f, indent=4)
 
                # Store in session state (excluding password)
                st.session_state.submitted = True
                st.session_state.last_submission = {
                    "otcs_url": url,
                    "username": username,
                    "logs_location": logs_location,
                    "reports_location": reports_location,
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
 
                  # Attempt redirect to file:// URL with login_success parameter
                redirect_url = f"{return_url}?login_success=true"
                st.markdown(
                    f"""
                    <p>Configuration saved successfully! Redirecting...</p>
                    <p>If you are not redirected, <a href="{redirect_url}" target="_self">click here to return to the main page</a>.</p>
                    <meta http-equiv="refresh" content="2;url={redirect_url}">
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"❌ Error saving configuration: {str(e)}")
 
# --- Success Message ---
if st.session_state.submitted:
    st.markdown("""
    <div class="success-box">
        <div class="success-icon">✅</div>
        <h3 style="color: #555; margin-bottom: 0.5rem;">Configuration Submitted Successfully!</h3>
        <p style="color: #555; margin-bottom: 0;">Your OTCS settings have been saved to <code style="color: #00a3e0;" >otcs_config.json</code></p>
    </div>
    """, unsafe_allow_html=True)
 
# --- Show Submitted Credentials (excluding password) ---
if st.session_state.last_submission:
    creds = st.session_state.last_submission
   
# --- Footer ---
st.markdown("""
<div class="footer">
    <p>OpenText Configuration Manager • v2.0</p>
    <p>© 2023 OpenText Corporation. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
 