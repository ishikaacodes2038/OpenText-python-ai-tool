import io
import streamlit as st
import pandas as pd
import requests
import json
import configparser
import os
import sqlite3
from datetime import datetime
from io import BytesIO, StringIO
import urllib.parse

# Set page config
st.set_page_config(
    page_title="OpenText Access Permission Manager",
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
        color: white;
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        color: white;
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
        color : white;
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

def log_event(username, action, status, message, details=""):
    try:
        # Only log significant events (modify these as needed)
        significant_actions = {
            'session_start', 'session_end', 
            'permission_batch', 'error',
            'config_load', 'authentication'
        }
        
        if action not in significant_actions:
            return
            
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "status": status,
            "message": message,
            "details": details
        }
        
        # Append to log file
        with open(st.session_state.current_log_file, 'a') as f:
            pd.DataFrame([new_entry]).to_csv(f, header=False, index=False)
            
    except Exception as e:
        st.error(f"❌ Logging failed: {str(e)}")

# ---------- CONFIGURATION SETUP ----------
def load_config():
    json_config_file = "otcs_config.json"
    ini_config_file = "config.ini"
    
    if os.path.exists(json_config_file):
        try:
            with open(json_config_file, 'r') as f:
                config = json.load(f)
                return config
        except Exception as e:
            st.markdown(f"<div class='notification error'>❌ Error reading otcs_config.json: {str(e)}</div>", unsafe_allow_html=True)
            log_event("system", "config_load", "error", f"Failed to read otcs_config.json: {str(e)}")
    
    # Fallback to config.ini
    config = configparser.ConfigParser()
    config['OTCS'] = {
        'otcs_url': 'http://10.100.253.32/otcs/cs.exe',
        'username': 'your_username',
        'password': 'your_password',
        'logs_location': 'logs.db',
        'download_temp_dir': 'downloads',
        'report_location': 'reports'
    }
    with open(ini_config_file, 'w') as f:
        config.write(f)
    log_event("system", "config_load", "warning", "otcs_config.json not found, created config.ini with defaults")
    return config['OTCS']

config = load_config()
BASE_URL = config["otcs_url"]
USERNAME = config["username"]
PASSWORD = config["password"]
LOGS_LOCATION = config.get("logs_location", "logs")
DOWNLOAD_DIR = config.get("download_temp_dir", "downloads")
REPORT_LOCATION = config.get("report_location", "reports")

# Validate base_url
try:
    parsed_url = urllib.parse.urlparse(BASE_URL)
    if not parsed_url.scheme or not parsed_url.netloc:
        st.markdown("<div class='notification error'>❌ Invalid OTCS URL in configuration</div>", unsafe_allow_html=True)
        log_event("system", "config_validation", "error", f"Invalid OTCS URL: {BASE_URL}")
        st.stop()
except Exception as e:
    st.markdown(f"<div class='notification error'>❌ Error parsing OTCS URL: {str(e)}</div>", unsafe_allow_html=True)
    log_event("system", "config_validation", "error", f"Error parsing OTCS URL: {str(e)}")
    st.stop()

# Ensure directories exist
os.makedirs(LOGS_LOCATION, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_LOCATION, exist_ok=True)

# ---------- LOGGING SETUP ----------
def init_logging():
    try:
        os.makedirs(LOGS_LOCATION, exist_ok=True)
        
        # Initialize session log file only once
        if 'logging_initialized' not in st.session_state:
            st.session_state.logging_initialized = True
            st.session_state.current_log_file = os.path.join(
                LOGS_LOCATION, 
                f"permission_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            # Create empty log file with headers
            pd.DataFrame(columns=[
                "timestamp", "username", "action", 
                "status", "message", "details"
            ]).to_csv(st.session_state.current_log_file, index=False)
            
    except Exception as e:
        st.error(f"❌ Logging initialization failed: {str(e)}")

init_logging()

def log_event(username, action, status, message, details=""):
    try:
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "status": status,
            "message": message,
            "details": details
        }
        
        # Append to current session's log file
        if not os.path.exists(st.session_state.current_log_file):
            pd.DataFrame([new_entry]).to_csv(st.session_state.current_log_file, index=False)
        else:
            with open(st.session_state.current_log_file, 'a') as f:
                pd.DataFrame([new_entry]).to_csv(f, header=False, index=False)
                
    except Exception as e:
        st.error(f"❌ Logging failed: {str(e)}")
def read_logs():
    try:
        if not os.path.exists(LOGS_LOCATION):
            return pd.DataFrame()
            
        all_logs = []
        for filename in sorted(os.listdir(LOGS_LOCATION)):
            if filename.endswith(".csv") and filename.startswith("permission_logs_"):
                filepath = os.path.join(LOGS_LOCATION, filename)
                try:
                    df = pd.read_csv(filepath)
                    df['session'] = filename.replace("permission_logs_", "").replace(".csv", "")
                    all_logs.append(df)
                except Exception as e:
                    print(f"Skipping corrupt log file {filename}: {str(e)}")
        
        return pd.concat(all_logs, ignore_index=True) if all_logs else pd.DataFrame()
        
    except Exception as e:
        st.error(f"❌ Error reading logs: {str(e)}")
        return pd.DataFrame()

# ---------- AUTHENTICATION SETUP ----------
def authenticate():
    url = f"{BASE_URL}/api/v1/auth"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("ticket")
        else:
            error_msg = f"Authentication failed: HTTP {response.status_code} - {response.text}"
            log_event("system", "authentication", "error", error_msg, f"URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error during authentication: {str(e)}"
        log_event("system", "authentication", "error", error_msg, f"URL: {url}")
        return None

# Initialize session state
if 'token' not in st.session_state:
    token = authenticate()
    if not token:
        st.markdown("<div class='notification error'>🔒 Authentication failed: Check OTCS URL, credentials, or network connectivity</div>", unsafe_allow_html=True)
        st.stop()
    st.session_state.token = token

# ---------- PERMISSION MANAGEMENT FUNCTIONS ----------
def get_node_id_from_path(base_url, token, folder_path):
    try:
        path_parts = folder_path.strip('/').split('/')
        current_node_id = 2000
        
        for part in path_parts:
            if not part:
                continue
                
            url = f"{base_url}/api/v2/nodes/{current_node_id}/nodes"
            headers = {"OTCSTicket": token}
            params = {"where_name": part}
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                return None, f"Failed to access path part '{part}': {response.text}"
            
            data = response.json()
            
            if not data.get('results') or len(data['results']) == 0:
                return None, f"Path part '{part}' not found in current location"
            
            current_node_id = data['results'][0]['data']['properties']['id']
        
        return current_node_id, None
    except Exception as e:
        return None, f"Error resolving path: {str(e)}"

def get_user_group_id(base_url, token, name):
    try:
        url = f"{base_url}/api/v2/members"
        headers = {"OTCSTicket": token}
        params = {"where_name": name.strip(), "where_type": 0}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                return data['results'][0]['data']['properties']['id'], None
        
        params = {"where_name": name.strip(), "where_type": 1}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                return data['results'][0]['data']['properties']['id'], None
        
        return None, f"User/Group '{name}' not found"
    except Exception as e:
        return None, f"Error finding user/group: {str(e)}"

# Function to assign permissions
def assign_permissions(base_url, token, node_id, right_id, permissions, apply_to=2, include_sub_types=None):
    """
    Assign permissions to a node using POST /permissions/custom with multipart/form-data
    """
    url = f"{base_url}/api/v2/nodes/{node_id}/permissions/custom"

    headers = {
        "OTCSTicket": token
        # Do not set Content-Type manually; requests handles it when using `files`
    }

    # Clean and validate permissions
    permissions_list = [perm.strip().lower() for perm in str(permissions).split(",")]
    valid_permissions = {
        'see', 'see_contents', 'modify', 'add_items', 'delete', 
        'edit_permissions', 'add_major_version', 'add_minor_version',
        'reserve', 'view_audit_trail', 'view_annotations', 'add_annotations',
        'edit_attributes', 'delete_versions'
    }
    filtered_permissions = [perm for perm in permissions_list if perm in valid_permissions]

    if not filtered_permissions:
        return 400, "No valid permissions provided"

    # Build the JSON body
    body_dict = {
        "permissions": filtered_permissions,
        "right_id": right_id,
        "apply_to": apply_to
    }
    if include_sub_types:
        body_dict["include_sub_types"] = include_sub_types

    # Send as multipart/form-data using `files`
    files = {
        "body": (None, json.dumps(body_dict))
    }

    try:
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 207:
            try:
                multi_data = response.json()
                if 'results' in multi_data:
                    for result in multi_data['results']:
                        if result.get('status') != 200:
                            return 207, f"Partial success: {multi_data}"
                return 200, "All permissions applied successfully"
            except Exception:
                return 207, f"Multi-status response: {response.text}"

        return response.status_code, response.text
    except Exception as e:
        return 500, f"Error assigning permissions: {str(e)}"

def generate_permission_template():
    data = {
        "folder_path": ["/Enterprise/Projects/MyFolder", "/Enterprise/Documents/Reports"],
        "user_group_name": ["john.doe", "Project Managers,IT Team"],
        "permissions": ["see,see_contents,modify", "see,see_contents"],
        "apply_to": [0, 2],
        "description": ["Project folder access", "Read-only access to reports"]
    }
    return pd.DataFrame(data)

# ---------- STREAMLIT UI ----------
# Header
st.markdown("""
<div class="header">
    <div class="container" style="padding: 0 2rem;">
        <img src="https://companieslogo.com/img/orig/OTEX_BIG-ea374e29.png?t=1741951344" class="opentext-logo" alt="OpenText Logo">
        <p class="hero-subtext">Access Permission Manager</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="container" style="padding: 0 2rem;">
    <h2 class="section-title">Access Management</h2>
    <p style="margin-bottom: 2rem; font-size: 1.1rem; color: #555; animation: fadeInUp 1s ease-out;">
        Efficiently manage access permissions in OpenText Content Server.
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Card
with st.container():
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

# Tabs
tab1, tab2, tab3 = st.tabs(["🔐 Access Permission Manager", "📊 System Logs", "ℹ️ Help & Examples"])
with tab1:
    st.subheader("🔐 Access Permission Manager")
    
    with st.expander("ℹ️ Instructions", expanded=True):
        st.markdown("""
        Upload an Excel file with the following columns:
        - **folder_path**: Full path of the folder/document (e.g., `/Enterprise/Projects/MyFolder`)
        - **user_group_name**: Name of the user or group (comma-separated for multiple)
        - **permissions**: Comma-separated permissions (e.g., `see,see_contents,modify`)
        - **apply_to** (optional): Inheritance level (0=this item only, 1=direct children, 2=all descendants)
        - **description** (optional): Description of the permission assignment
        ### Permission Reference:
        - Basic: `see`, `see_contents`, `modify`, `add_items`, `delete`
        - Advanced: `edit_permissions`, `add_major_version`, `add_minor_version`
        - Special: `reserve`, `view_audit_trail`, `view_annotations`, `add_annotations`, `edit_attributes`, `delete_versions`
                    
         **Note:** A new log file is generated each time the session is refreshed. Users can access it at the log location specified during the sign-up process.
        """, unsafe_allow_html=True)
        
        template_df = generate_permission_template()
        excel_buffer = BytesIO()
        template_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Excel Template",
            data=excel_buffer,
            file_name="permission_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    uploaded_file = st.file_uploader("Upload Excel File for Permissions", type=["xlsx", "xls"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        if 'apply_to' not in df.columns:
            df['apply_to'] = 0
        
        with st.expander("📄 Preview Uploaded Data", expanded=True):
            st.dataframe(df)
            st.markdown(f"<div class='notification info'>Found {len(df)} records to process</div>", unsafe_allow_html=True)
        
        required_columns = ["folder_path", "user_group_name", "permissions"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.markdown(f"<div class='notification error'>❌ Missing required columns: {', '.join(missing_columns)}</div>", unsafe_allow_html=True)
            log_event("admin", "permission_upload", "error", f"Missing columns: {missing_columns}")
        else:
            if st.button("🚀 Apply Permissions", key="apply_permissions"):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                notification_container = st.empty()
                total_operations = 0
                
                for index, row in df.iterrows():
                    user_groups = [ug.strip() for ug in str(row["user_group_name"]).split(",") if str(row["user_group_name"]).strip()]
                    total_operations += len(user_groups)
                
                current_operation = 0
                
                for index, row in df.iterrows():
                    folder_path = str(row["folder_path"]).strip()
                    user_group_names = [ug.strip() for ug in str(row["user_group_name"]).split(",") if str(row["user_group_name"]).strip()]
                    permissions = str(row["permissions"]).strip()
                    apply_to = int(row.get("apply_to", 0))
                    description = str(row.get("description", "")).strip()
                    
                    if apply_to not in [0, 1, 2]:
                        apply_to = 0
                        log_event("admin", "apply_permissions", "warning", 
                                  f"Invalid apply_to value for {folder_path}, defaulting to 0", 
                                  f"Value: {row.get('apply_to')}")
                    
                    node_id, node_error = get_node_id_from_path(BASE_URL, st.session_state.token, folder_path)
                    if node_error:
                        for user_group_name in user_group_names:
                            results.append({
                                "Folder Path": folder_path,
                                "User/Group": user_group_name,
                                "Status": "Failed",
                                "Node ID": "N/A",
                                "Message": node_error,
                                "Permissions": permissions,
                                "Apply To": apply_to
                            })
                            log_event("admin", "apply_permissions", "error", node_error, 
                                      f"Path: {folder_path}, User/Group: {user_group_name}")
                            current_operation += 1
                            progress = min(100,int((current_operation / total_operations) * 100))
                            progress_bar.progress(progress)
                            status_text.markdown(f"<div class='notification info'>Progress: {progress}% | Processing {current_operation} of {total_operations}</div>", unsafe_allow_html=True)
                            continue
                    
                    for user_group_name in user_group_names:
                        status_text.markdown(f"<div class='notification info'>Progress: {int((current_operation / total_operations) * 100)}% | Processing {current_operation + 1} of {total_operations}: {folder_path} for {user_group_name}</div>", unsafe_allow_html=True)
                        
                        right_id, user_error = get_user_group_id(BASE_URL, st.session_state.token, user_group_name)
                        if user_error:
                            results.append({
                                "Folder Path": folder_path,
                                "User/Group": user_group_name,
                                "Status": "Failed",
                                "Node ID": node_id,
                                "Message": user_error,
                                "Permissions": permissions,
                                "Apply To": apply_to
                            })
                            log_event("admin", "apply_permissions", "error", user_error, 
                                      f"Path: {folder_path}, User/Group: {user_group_name}")
                            current_operation += 1
                            progress = min(100,int((current_operation / total_operations) * 100))
                            progress_bar.progress(progress)
                            status_text.markdown(f"<div class='notification info'>Progress: {progress}% | Processing {current_operation} of {total_operations}</div>", unsafe_allow_html=True)
                            continue
                        
                        status_code, response_text = assign_permissions(
                            BASE_URL, 
                            st.session_state.token, 
                            node_id, 
                            right_id, 
                            permissions,
                            apply_to
                        )
                        
                        status = "Success" if status_code in [200, 207] else "Failed"
                        response_msg = "Permissions applied successfully" if status_code in [200, 207] else response_text
                        
                        results.append({
                            "Folder Path": folder_path,
                            "User/Group": user_group_name,
                            "Status": status,
                            "Node ID": node_id,
                            "Message": response_msg,
                            "Permissions": permissions,
                            "Apply To": apply_to
                        })
                        
                        log_event("admin", "apply_permissions", status.lower(), response_msg, 
                                  f"Path: {folder_path}, User/Group: {user_group_name}, Node ID: {node_id}, Right ID: {right_id}, Apply To: {apply_to}")
                        
                        current_operation += 1
                        progress = min(100,int((current_operation / total_operations) * 100))
                        progress_bar.progress(progress)
                        status_text.markdown(f"<div class='notification info'>Progress: {progress}% | Processing {current_operation} of {total_operations}</div>", unsafe_allow_html=True)
                
                status_text.markdown("<div class='notification success'>✅ Processing complete!</div>", unsafe_allow_html=True)
                progress_bar.empty()
                
                result_df = pd.DataFrame(results)
                success_count = len(result_df[result_df["Status"] == "Success"])
                failed_count = len(result_df[result_df["Status"] == "Failed"])
                
                if success_count > 0:
                    notification_container.markdown(
                        f"<div class='notification success'>✅ {success_count} permissions applied successfully!</div>", 
                        unsafe_allow_html=True
                    )
                if failed_count > 0:
                    notification_container.markdown(
                        f"<div class='notification error'>❌ {failed_count} permissions failed to apply</div>", 
                        unsafe_allow_html=True
                    )
                
                with st.expander("📊 Detailed Results", expanded=True):
                    st.dataframe(result_df)
                
                excel_buffer = BytesIO()
                result_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                
                report_file = os.path.join(REPORT_LOCATION, f"permission_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                with open(report_file, 'wb') as f:
                    f.write(excel_buffer.getvalue())
                
                st.download_button(
                    label="📥 Download Results as Excel",
                    data=excel_buffer,
                    file_name=os.path.basename(report_file),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

with tab2:
    st.subheader("📊 System Logs")
    
    if st.button("🔄 Refresh Logs"):
        st.rerun()
    
    logs_df = read_logs()
    
    if logs_df.empty:
        st.markdown("<div class='notification info'>No logs available yet.</div>", unsafe_allow_html=True)
    else:
        st.markdown("**Filter Options:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            action_filter = st.selectbox(
                "Action Type",
                ["All"] + sorted(logs_df['action'].unique().tolist())
            )
        with col2:
            status_filter = st.selectbox(
                "Status",
                ["All"] + sorted(logs_df['status'].unique().tolist())
            )
        with col3:
            user_filter = st.selectbox(
                "User",
                ["All"] + sorted(logs_df['username'].unique().tolist())
            )
        # Apply filters
        filtered_logs = logs_df.copy()
        if action_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['action'] == action_filter]
        if status_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['status'] == status_filter]
        if user_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['username'] == user_filter]
        
        # Display stats
        success_count = len(filtered_logs[filtered_logs['status'] == 'success'])
        error_count = len(filtered_logs[filtered_logs['status'] == 'error'])
        
        col1, col2 = st.columns(2)
        col1.metric("✅ Successes", success_count)
        col2.metric("❌ Errors", error_count)
        
        st.dataframe(filtered_logs)
        
 # Export logs
                # Replace the Excel export code with this:
        if not filtered_logs.empty:
            csv_buffer = io.StringIO()
            filtered_logs.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            
            st.download_button(
                label="📥 Download Filtered Logs",
                data=csv_buffer.getvalue().encode('utf-8'),  # Convert to bytes
                file_name=f"system_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download current filtered logs as CSV file"
            )
            
            # Also provide Excel download option
            excel_buffer = BytesIO()
            filtered_logs.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            
            st.download_button(
                label="📥 Download as Excel",
                data=csv_buffer.getvalue().encode('utf-8'),  # Convert to bytes,
                file_name=f"system_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download current filtered logs as Excel file"
            )
with tab3:
    st.subheader("ℹ️ Permission Management Guide")
    
    # FAQ Section
    with st.expander("❓ Frequently Asked Questions", expanded=True):
        st.markdown("""
        ### Q: What permissions can I assign?
        **A:** You can assign these common permissions:
        - **Basic Access**: `see`, `see_contents`, `modify`
        - **Content Management**: `add_items`, `delete`, `reserve`
        - **Version Control**: `add_major_version`, `add_minor_version`, `delete_versions`
        - **Administrative**: `edit_permissions`, `view_audit_trail`

        ### Q: What does 'apply_to' mean?
        **A:** It controls permission inheritance:
        - `0`: Apply to this item only
        - `1`: Apply to direct children only
        - `2`: Apply to all descendants (full inheritance)

        ### Q: How do I specify multiple users/groups?
        **A:** Separate them with commas in the Excel file:
        ```csv
        user_group_name
        "john.doe,project_managers"
        ```

        ### Q: What if a folder path doesn't exist?
        **A:** The operation will fail for that path but continue with others.
        """)

    # Examples Section
    with st.expander("📋 Template Examples", expanded=True):
        st.markdown("""
        ### Sample Excel Structure:
        ```csv
        folder_path,user_group_name,permissions,apply_to,description
        "/Enterprise/Projects", "project_team", "see,see_contents,modify", 2, "Full project access"
        "/Enterprise/Finance", "audit_team", "see,see_contents", 0, "Read-only access"
        ```

        ### Complete Example File:
        | folder_path            | user_group_name       | permissions                 | apply_to | description               |
        |------------------------|-----------------------|-----------------------------|----------|---------------------------|
        | /Enterprise/Projects   | project_managers      | see,see_contents,modify     | 2        | Full project access       |
        | /Enterprise/HR         | hr_staff              | see,see_contents,add_items  | 1        | HR document management    |
        | /Enterprise/IT         | it_admin              | see,edit_permissions        | 2        | IT administrator access   |
        """)
        
        # Generate and show template download
        template_df = pd.DataFrame({
            "folder_path": ["/Enterprise/Projects", "/Enterprise/Finance"],
            "user_group_name": ["project_team,managers", "audit_team"],
            "permissions": ["see,see_contents,modify", "see,see_contents"],
            "apply_to": [2, 0],
            "description": ["Full project access", "Read-only financial reports"]
        })
        
        excel_buffer = BytesIO()
        template_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        st.download_button(
            label="📥 Download Complete Template",
            data=excel_buffer,
            file_name="permission_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Troubleshooting Section
    with st.expander("🔧 Troubleshooting", expanded=True):
        st.markdown("""
        ### Common Issues and Solutions:
        
        🔴 **Permission assignments failing**
        - Verify the folder path exists exactly as typed
        - Check user/group names are correct
        - Ensure your account has permission to modify permissions

        🔴 "User/Group not found" errors
        - Names are case-sensitive
        - Groups must be prefixed with `#` (e.g., `#project_managers`)
        - Check for extra spaces in names

        🔴 Partial success (207 status)
        - Some permissions were applied but not all
        - Check the detailed results for specific failures

        ### Best Practices:
        1. Test with small batches first
        2. Use `apply_to=0` for precise control
        3. Document changes in the description field
        4. Review system logs after bulk operations
        """)

    # API Reference
    with st.expander("🔗 Technical Reference", expanded=True):
        st.markdown(f"""
        ### API Endpoints Used:
        - **Permission Assignment**: `{BASE_URL}/api/v2/nodes/{{node_id}}/permissions/custom`
        - **Node Lookup**: `{BASE_URL}/api/v2/nodes/{{parent_id}}/nodes`
        - **User/Group Search**: `{BASE_URL}/api/v2/members`

        ### Permission Reference Table:
        | Permission          | Description                          |
        |---------------------|--------------------------------------|
        | `see`               | See item in listings                 |
        | `see_contents`      | Open and view content                |
        | `modify`            | Edit existing content                |
        | `add_items`         | Add new files/folders                |
        | `delete`            | Delete items                         |
        | `edit_permissions`  | Change permissions                   |
        | `view_audit_trail`  | Access audit history                 |
        """)

# Footer
st.markdown("""
<div class="footer">
    <p>OpenText Access Permission Manager Portal • v2.0</p>
    <p>© 2023 OpenText Corporation. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)