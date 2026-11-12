import streamlit as st

def apply_opentext_ui():
    # Set page config
    st.set_page_config(
        page_title="OpenText Content Server Management",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS with advanced animations and dynamic elements
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
        .card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.4s ease, box-shadow 0.4s ease;
            overflow: hidden;
            margin-bottom: 1.5rem;
            animation: slideIn 0.8s ease-out;
        }

        .card:hover {
            transform: translateY(-10px) rotate(1deg);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }

        .card-header {
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            color: white;
            padding: 1.2rem;
            font-weight: 600;
            font-size: 1.3rem;
            position: relative;
            overflow: hidden;
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
            padding: 2rem;
        }

        /* Button Styling */
        .stButton>button {
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            width: 100%;
            position: relative;
            overflow: hidden;
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
            padding: 12px 15px;
            transition: border-color 0.3s ease;
        }

        .stTextInput>div>div>input:focus, 
        .stTextArea>div>div>textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 8px rgba(0, 94, 184, 0.3);
        }

        /* Download Button */
        .stDownloadButton>button {
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stDownloadButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(0, 94, 184, 0.4);
        }

        /* Progress Bar */
        .progress-container {
            background: rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            height: 25px;
            margin: 1.5rem 0;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            border-radius: 12px;
            transition: width 0.5s ease;
            position: relative;
            overflow: hidden;
        }

        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: progressShine 2s infinite;
        }

        @keyframes progressShine {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* Feature Icon Animation */
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            color: var(--primary);
            transition: transform 0.3s ease;
        }

        .card:hover .feature-icon {
            transform: rotate(360deg);
        }

        /* Notifications */
        .notification {
            padding: 1.2rem;
            border-radius: 12px;
            margin: 1rem 0;
            font-weight: 500;
            animation: slideInRight 0.5s ease-out;
            position: relative;
            overflow: hidden;
        }

        .success {
            background-color: #d4edda;
            color: #155724;
            border-left: 5px solid #28a745;
        }

        .error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #dc3545;
        }

        .info {
            background-color: #e2e3e5;
            color: #383d41;
            border-left: 5px solid #6c757d;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #ffffff, #f8f9fa);
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
            border-radius: 0 20px 20px 0;
            animation: slideInLeft 0.8s ease-out;
        }

        /* Section Title */
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2rem;
            position: relative;
            padding-bottom: 0.8rem;
            animation: fadeIn 1s ease-out;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            border-radius: 4px;
            animation: expandLine 1.5s ease-out;
        }

        /* Animations */
        @keyframes slideIn {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes slideInRight {
            from { transform: translateX(100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes slideInLeft {
            from { transform: translateX(-100px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes expandLine {
            from { width: 0; }
            to { width: 80px; }
        }

        /* Feature Card */
        .feature-card {
            text-align: center;
            padding: 2.5rem;
            animation: fadeIn 1s ease-out;
        }

        .feature-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--dark);
        }

        .feature-description {
            color: var(--secondary);
            font-size: 1rem;
            line-height: 1.6;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 0;
            color: #eeeff2;
            background-color: #011969;
            font-size: 0.95rem;
            margin-top: 4rem;
            border-top: 1px solid #eaeaea;
            animation: fadeIn 1s ease-out;
        }

        /* Tab Styling */
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
            color: white;
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(90deg, var(--gradient-end), var(--gradient-start));
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: white;
            color: var(--primary);
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def show_opentext_header():
    st.markdown("""
    <div class="header">
        <div class="container" style="padding: 0 2rem;">
            <img src="https://companieslogo.com/img/orig/OTEX_BIG-ea374e29.png?t=1741951344" class="opentext-logo" alt="OpenText Logo">
            <p class="hero-subtext">Empowering Smarter Information Management</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_features_section():
    st.markdown("""
    <div class="container" style="padding: 0 2rem;">
        <h2 class="section-title">Content Server Management</h2>
        <p style="margin-bottom: 2rem; font-size: 1.1rem; color: #555; animation: fadeInUp 1s ease-out;">
            Discover what's new in smarter information management. Empower your organization with AI-driven content solutions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">Folder Management</div>
            <div class="card-body">
                <div class="feature-card">
                    <div class="feature-icon">📁</div>
                    <h3 class="feature-title">Bulk Folder Creation</h3>
                    <p class="feature-description">
                        Create multiple folders in OpenText Content Server with a single operation. 
                        Upload an Excel file to create folder structures efficiently.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header">Access Management</div>
            <div class="card-body">
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h3 class="feature-title">Permission Manager</h3>
                    <p class="feature-description">
                        Assign access permissions to users and groups across multiple folders. 
                        Manage security settings efficiently with bulk operations.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Divider
    st.markdown("<div style='height: 3px; background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)); margin: 3rem 0; animation: slideLine 5s infinite;'></div>", unsafe_allow_html=True)

def show_management_tools_header():
    st.markdown("""
    <div class="container" style="padding: 0 2rem;">
        <h2 class="section-title">Management Tools</h2>
    </div>
    """, unsafe_allow_html=True)

def show_opentext_footer():
    st.markdown("""
    <div class="footer">
        <p>OpenText Content Server Management Portal • v2.0</p>
        <p>© 2023 OpenText Corporation. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def create_section_divider():
    st.markdown("<div style='height: 3px; background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)); margin: 3rem 0; animation: slideLine 5s infinite;'></div>", unsafe_allow_html=True)