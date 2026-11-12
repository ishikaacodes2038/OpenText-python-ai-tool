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

def show_tabs():
    st.markdown("""
    <div class="stTabs">

    </div>
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


def show_opentext_footer():
    st.markdown("""
    <div class="footer">
        <p>OpenText Content Server Management Portal • v2.0</p>
        <p>© 2023 OpenText Corporation. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def create_section_divider():
    st.markdown("<div style='height: 3px; background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)); margin: 3rem 0; animation: slideLine 5s infinite;'></div>", unsafe_allow_html=True)

# Apply the UI at the very top of their app
apply_opentext_ui()

# Use the header components
show_opentext_header()

def show_features_section():
    st.markdown("""
    <div class="container" style="padding: 0 2rem;">
        <h2 class="section-title">Document Migration on Content Server</h2>
        <p style="margin-bottom: 1.5rem; font-size: 1.1rem; color: #555; animation: fadeInUp 1s ease-out;">
            Seamlessly move your files into the OpenText Content Server with confidence and clarity.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_document_migration_card():
    st.markdown("""
        <div class="card">
            <div class="card-header">Document Migration</div>
            <div class="card-body">
                <div class="feature-card">
                    <div class="feature-icon">📁</div>
                    <h3 class="feature-title">Document Migration</h3>
                    <p class="feature-description">
                        Allows you to migrate documents into the OpenText Content Server using a structured Excel sheet. You can upload files from local paths or public URLs.
                         The system supports both new document uploads and versioning of existing ones.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_management_tools_header():
    st.markdown("""
    <div class="container" style="padding: 0 2rem;">
        <h3 class="section-title">Migration Tools</h3>
    </div>
    """, unsafe_allow_html=True)

show_features_section()
show_document_migration_card()
show_management_tools_header()
#create_section_divider()



# respective app content goes here
import streamlit as st
import pandas as pd
import requests
import os
import json
from urllib.parse import urlparse
import datetime
import plotly.express as px

# Load config
def load_config():
    with open("otcs_config.json") as f:
        return json.load(f)
 
config = load_config()
BASE_URL = config["otcs_url"]
USERNAME = config["username"]
PASSWORD = config["password"]
DOWNLOAD_DIR = config["logs_location"]
#DOWNLOAD_DIR = config.get("download_temp_dir", "downloads")
#os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Authenticate to get ticket
def authenticate():
    url = f"{BASE_URL}/api/v1/auth"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("ticket")
    else:
        return None

# Get folder ID from TargetOT path
def resolve_folder_path(path, ticket):
    parts = path.strip("/").split("/")
    parent_id = 2000  # Enterprise workspace ID
    headers = {"OTCSTicket": ticket}

    for part in parts:
        url = f"{BASE_URL}/api/v1/nodes/{parent_id}/nodes"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            found = False
            for item in response.json().get("data", []):
                if item.get("name") == part and item.get("type") == 0:  # 0 = folder
                    parent_id = item.get("id")
                    found = True
                    break
            if not found:
                return None
        else:
            return None

    return parent_id

# Get existing document ID by name in a target folder
def get_existing_document_id(folder_id, doc_name, ticket):
    url = f"{BASE_URL}/api/v1/nodes/{folder_id}/nodes"
    headers = {"OTCSTicket": ticket}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for item in response.json().get("data", []):
            if item.get("name") == doc_name:
                return item.get("id")
    return None

# Upload document or new version
def upload_document(file_path, target_id, doc_name, version, ticket):
    headers = {"OTCSTicket": ticket}
    existing_id = get_existing_document_id(target_id, doc_name, ticket)
    with open(file_path, 'rb') as f:
        files = {
            'file': (doc_name, f),
            'name': (None, doc_name)
        }

        if existing_id:
            url = f"{BASE_URL}/api/v1/nodes/{existing_id}/versions"
            response = requests.post(url, files=files, headers=headers)
        else:
            url = f"{BASE_URL}/api/v1/nodes"
            files['parent_id'] = (None, str(target_id))
            files['type'] = (None, '144')
            response = requests.post(url, files=files, headers=headers)

    try:
        response_data = response.json()
    except:
        response_data = {}
    if response.status_code == 200:
        return True, response_data.get("id", existing_id), ""
    else:
        return False, "", response_data.get("error", f"HTTP {response.status_code}")

# Download file from URL
def download_file_from_url(url, download_dir):
    try:
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(download_dir, filename)
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return local_path
    except:
        pass
    return None

def show_instruction_box():
    st.markdown("""
    <style>
    .custom-instruction {
        background: linear-gradient(135deg, #eaf3fc, #f0f8ff);
        border: 2px solid #0077cc;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #003366;
        animation: fadeIn 0.8s ease-in-out;
    }
    .custom-instruction strong {
        font-size: 1rem;
        color: #005eb8;
    }
    .custom-instruction ul {
        margin-top: 1rem;
        padding-left: 1.2rem;
        line-height: 1.8;
    }
    .custom-instruction li {
        margin-bottom: 0.6rem;
    }
    .custom-instruction code {
        background-color: #eef6ff;
        color: #005eb8;
        padding: 2px 6px;
        border-radius: 5px;
        font-size: 0.95rem;
    }
    </style>
    <div class='custom-instruction'>
    <strong>📘 Instructions for Uploading:</strong>
    <ul>
        <li>Ensure the Excel file contains columns: <code>Source</code>, <code>Target</code>, <code>DocumentName</code>.</li>
        <li><code>Source</code>: Local path or URL to the file.</li>
        <li><code>Target</code>: Folder ID in OpenText Content Server.</li>
        <li><code>DocumentName</code>: Name of document. If it already exists, a new version will be added.</li>
        <li>Each row = one document/version upload.</li>
        <li><strong style="color:#cc0000;">Do not leave any cells blank.</strong></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
#show_instruction_box()



# Tabs: Instructions | Session Logs
tab_instructions, tab_logs, tab_help_example = st.tabs(["📘 Instructions", "📄 Session Logs", "📖 Help & Example"])

    # Tab 1: Instructions
with tab_instructions:
    st.markdown("""
    <style>
    .custom-instruction {
        background: linear-gradient(135deg, #eaf3fc, #f0f8ff);
        border: 2px solid #0077cc;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #003366;
        animation: fadeIn 0.8s ease-in-out;
    }
    .custom-instruction strong {
        font-size: 1rem;
        color: #005eb8;
    }
    .custom-instruction ul {
        margin-top: 1rem;
        padding-left: 1.2rem;
        line-height: 1.8;
    }
    .custom-instruction li {
        margin-bottom: 0.6rem;
    }
    .custom-instruction code {
        background-color: #eef6ff;
        color: #005eb8;
        padding: 2px 6px;
        border-radius: 5px;
        font-size: 0.95rem;
    }
    </style>
    <div class='custom-instruction'>
    <strong>📘 Instructions for Uploading:</strong>
    <ul>
        <li>Ensure the Excel file contains columns: <code>Source</code>, <code>Target</code>, <code>DocumentName</code>.</li>
        <li><code>Source</code>: Local path or URL to the file.</li>
        <li><code>Target</code>: Folder ID in OpenText Content Server.</li>
        <li><code>DocumentName</code>: Name of document. If it already exists, a new version will be added.</li>
        <li>Each row = one document/version upload.</li>
        <li><strong style="color:#cc0000;">Do not leave any cells blank.</strong></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)



















    uploaded_file = st.file_uploader("📤 Upload Excel File", type=[".xlsx"])

    if uploaded_file and "migration_done" not in st.session_state:
        df = pd.read_excel(uploaded_file)
        #df["Status"] = ""
        #df["OpenText Object ID"] = ""

        if not {"Source", "Target", "DocumentName"}.issubset(df.columns):
            st.error("Excel must contain 'Source', 'Target', and 'DocumentName' columns.")
        else:
            #st.subheader("📋 Preview of Entries to be Migrated")
            #st.dataframe(df)

            ticket = authenticate()
            if not ticket:
                st.error("Authentication failed. Check your config.json.")
            else:
                total_files = len(df)
                success_count = 0
                fail_count = 0

                progress_bar = st.progress(0)
                status_placeholder = st.empty()

                for index, row in df.iterrows():
                    source = str(row["Source"])
                    target_path = str(row["Target"])
                    doc_name = str(row["DocumentName"])
                    version = str(row["Version"]) if "Version" in df.columns else ""

                    target_id = resolve_folder_path(target_path, ticket)
                    if not target_id:
                        df.at[index, "Status"] = "Target path not found"
                        fail_count += 1
                        continue

                    is_url = source.lower().startswith("http")
                    local_path = download_file_from_url(source, DOWNLOAD_DIR) if is_url else source

                    if not local_path or not os.path.exists(local_path):
                        df.at[index, "Status"] = "File not found"
                        fail_count += 1
                    else:
                        try:
                            success, obj_id, error_message = upload_document(local_path, target_id, doc_name, version, ticket)
                            if success:
                                df.at[index, "Status"] = "Success"
                                df.at[index, "OpenText Object ID"] = obj_id
                                success_count += 1
                            else:
                                df.at[index, "Status"] = f"Failed: {error_message}"
                                fail_count += 1
                        except Exception as e:
                            df.at[index, "Status"] = f"Failed: {str(e)}"
                            fail_count += 1

                    completed = (index + 1) / total_files
                    progress_bar.progress(completed)
                    status_placeholder.markdown(f"**Progress:** {int(completed * 100)}% | Successfully Migrated ✅ {success_count} | Failed ❌ {fail_count} | Total: {total_files}")

                st.success("🎉 Migration complete.")

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                log_filename = f"migration_log_{timestamp}.csv"
                df["Migrated By"] = USERNAME
                df["Migration Time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                final_columns = ["Source", "Target", "DocumentName", "Version", "Status", "OpenText Object ID", "Migrated By", "Migration Time"]
                for col in final_columns:
                    if col not in df.columns:
                        df[col] = ""
                
                df["Status"] = df["Status"].apply(
                    lambda x: "Success" if str(x).lower() == "success" else f"Failed: {x}"
                )
                df = df[final_columns]
                df.to_csv(log_filename, index=False)

                st.session_state["migration_done"] = True
                st.session_state["df"] = df
                st.session_state["log_filename"] = log_filename
                st.session_state["success_count"] = success_count
                st.session_state["fail_count"] = fail_count
    
                st.session_state.update({
                    "migration_done": True,
                    "df": df,
                    "log_filename": log_filename,
                    "success_count": success_count,
                    "fail_count": fail_count
                })



    #for refresh button
    if st.session_state.get("migration_done"):    
        st.download_button("📥 Download Migration Log", data=open(st.session_state["log_filename"], "rb"), file_name=st.session_state["log_filename"])    
        #st.subheader("📊 Migration Results")
        #st.dataframe(st.session_state["df"])
        st.markdown(f"""        
                    <div class='success-box'>✅ {st.session_state["success_count"]} files successfully migrated.</div>        
                    <div class='fail-box'>❌ {st.session_state["fail_count"]} files failed to migrate.</div>    
                    """, unsafe_allow_html=True)
        # Add reset option    
        if st.button("🔁 Start New Migration"):        
            for key in ["migration_done", "df", "log_filename", "success_count", "fail_count"]:            
                if key in st.session_state:                
                    del st.session_state[key]        
                    st.rerun()


    # Tab 2: Session Logs
with tab_logs:
     if "df" in st.session_state:
        filter_option = st.selectbox(
            "Filter logs by status:",
            ["All", "Success", "Failed"]
        )

        df_logs = st.session_state["df"]

        if filter_option == "Success":
            filtered_df = df_logs[df_logs["Status"].str.lower() == "success"]
        elif filter_option == "Failed":
            filtered_df = df_logs[df_logs["Status"].str.lower().str.startswith("failed")]
        else:
            filtered_df = df_logs

        st.dataframe(filtered_df, use_container_width=True)




# --- Help & Example Tab ---
with tab_help_example:
    st.title("📘 Help & Example")

    with st.expander("❓ Frequently Asked Questions (FAQ)"):
        st.markdown("""
                    
        **Q1. What should I do if authentication fails?**  
        → Check `config.json` for correct username, password, and server URL. Also ensure server is reachable.

        **Q2. Why am I getting 'Missing Parameters' error?**  
        → Make sure the Excel file has all required columns: `Source`, `Target`, `Version` and `DocumentName`.

        **Q3. How do I handle large file uploads?**  
        → Split them into smaller files and run multiple migrations. Ensure server upload size limit is not exceeded.

        **Q4. What if a document already exists in the target folder?**  
        → If the given document already exists in the target folder, then it will be added as the next version of the previously available document.

        **Q5. Why is my Excel file not being read?**  
        → Ensure the column headers match exactly with the template provided.

        **Q6. How can I check detailed error logs?**  
        → Go to **Session Logs Tab** after migration, apply the filter as success, failed of which you want to fetch the status.

        **Q7. Why does migration stop midway?**  
        → It may be due to network interruptions. Retry after ensuring stable internet connection.
                    
        **Q8: What is this tool for?**  
        A: This tool helps migrate documents to OpenText Content Server using REST API.  

        **Q9: Can I upload multiple files at once?**  
        A: Yes, prepare them in an Excel file with correct mapping of source path and target folder ID.  

        **Q10: How do I know if my migration worked?**  
        A: Check the *Session Logs* tab or download the result Excel after migration.  
        """)

    with st.expander("✅ Good Path Examples"):
        st.markdown("""
        - Excel should have columns: **Source | Target | DocumentName | Version**
                Source:- Local file paths from which files will be migrated, 
                Target:- Opentext Context Server folder path structure, 
                DocumentName:- The name under which the files would be added on content server, if file under same given name exists, it will be added as a new version otherwise as a new node, 
                Version:- Versions of the files.
        - Example row:  
          `C:/Users/John/Documents/test.pdf | Document Migration Demo/Europe/Germany/Berlin/Assets/2024/Feb | TestOnCS.pdf | 1`  
        - Use correct target paths under column **Target** from OpenText Content Server.  
        """)

    with st.expander("⚠️ Things to Avoid"):
        st.markdown("""
        - ❌ Wrong or missing source and target folder paths  
        - ❌ Empty document names  
        - ❌ Special characters in file paths not supported by Windows/Linux 
        - ❌ Leading/trailing slashes at the end of paths, double slashes, extra spaces in names
        - ❌ Uploading without network connection  
        """)

    with st.expander("🌟 Best Practices"):
        st.markdown("""
        - Always validate the Excel file before upload  
        - Keep backup of source files  
        - Run migrations in smaller batches to avoid failures  
        - Use meaningful document names for easy searching later  
        """)

    with st.expander("🔑 Authentication Issues"):
        st.markdown("""
        - Wrong username/password → check config.json  
        - Expired OTCSTicket → refresh token  
        - Permission errors → user might not have access to target folder  
        """)

    with st.expander("📂 Migration Failures"):
        st.markdown("""
        - File not found at source path  
        - Target folder does not exist 
        - Permissions to add document in certain target folders might not be there
        - REST API timeout  
        """)

    with st.expander("📊 Excel File Issues"):
        st.markdown("""
        - Missing required columns  
        - Incorrect header names in excel (case-sensitive)  
        - Rows with empty source or folder paths
        - Non-UTF8 encoding issues in file names  
        """)

    with st.expander("🌐 Network Issues"):
        st.markdown("""
        - Timeout due to large file size → retry with smaller files  
        - Verify proper network connectivity to Content Server 
        - Proxy/firewall blocking API calls  
        """)

    with st.expander("🔗 API Endpoints Used"):
        st.markdown("""
        - **Authentication** → `POST /api/v1/auth`  
        - **Upload Document** → `POST /api/v2/nodes` 
        - **Check Node Metadata** → `GET /api/v2/nodes/{id}`  
        """)

    with st.expander("⚙️ Process Flow"):
        st.markdown("""
        1. User uploads Excel file  
        2. Tool reads each row → gets source path through "Source", folder path through "Target", document name through "DocumentName" along with Versions.
        3. API authentication (OTCSTicket generated)  
        4. Files uploaded as new or as versions to target folder  
        5. Status updated in Excel + logs written in session log  
        6. Final Excel available for download  
        """)

    with st.expander("📡 Response Code Examples"):
        st.markdown("""
        - **200 OK** → Request successful  
        - **201 Created** → Document uploaded successfully  
        - **400 Bad Request** → Wrong parameters in request  
        - **401 Unauthorized** → Invalid credentials or expired token  
        - **403 Forbidden** → User doesn’t have permission  
        - **404 Not Found** → Source path or folder not found  
        - **500 Internal Server Error** → Server issue, retry later  
        """)




# Use the footer at the bottom
show_opentext_footer()