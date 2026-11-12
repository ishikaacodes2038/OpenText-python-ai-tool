import io
import streamlit as st
import pandas as pd
import requests
import json
import configparser
import os
import sqlite3
from datetime import datetime
from io import BytesIO
import urllib.parse
import time
import re

# Set page config
st.set_page_config(
    page_title="OpenText Folder Creation",
    page_icon="📁",
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
            
        /* Hierarchy Display Styling */
    .hierarchy-display {
        background: #f8f9fa;
        border-left: 4px solid var(--primary);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Courier New', monospace;
    }

    .hierarchy-level-0 { margin-left: 0; }
    .hierarchy-level-1 { margin-left: 20px; }
    .hierarchy-level-2 { margin-left: 40px; }
    .hierarchy-level-3 { margin-left: 60px; }
    .hierarchy-level-4 { margin-left: 80px; }
    .hierarchy-level-5 { margin-left: 100px; }

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
        color:white;
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

    .warning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
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
        # Ensure logs directory exists
        os.makedirs(LOGS_LOCATION, exist_ok=True)
        
        # Create new entry
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "status": status,
            "message": message,
            "details": details
        }
        
        # Write/append to current session's log file
        if not os.path.exists(st.session_state.current_log_file):
            # Create new file with header
            pd.DataFrame([new_entry]).to_csv(st.session_state.current_log_file, index=False)
        else:
            # Append to existing file
            with open(st.session_state.current_log_file, 'a') as f:
                pd.DataFrame([new_entry]).to_csv(f, header=False, index=False)
                
    except Exception as e:
        st.markdown(f"<div class='notification error'>❌ Error logging event: {str(e)}</div>", unsafe_allow_html=True)
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
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_LOCATION, exist_ok=True)

# ---------- LOGGING SETUP ----------
def init_log_file():
    try:
        log_file = os.path.join(LOGS_LOCATION, "folder_creation_logs.csv")
        os.makedirs(LOGS_LOCATION, exist_ok=True)
        
        if not os.path.exists(log_file):
            # Create empty log file with headers
            pd.DataFrame(columns=[
                "timestamp", 
                "username", 
                "action", 
                "status", 
                "message", 
                "details"
            ]).to_csv(log_file, index=False)
            
    except Exception as e:
        st.markdown(f"<div class='notification error'>❌ Error initializing log file: {str(e)}</div>", unsafe_allow_html=True)

def read_logs():
    try:
        if not os.path.exists(LOGS_LOCATION):
            return pd.DataFrame()
            
        all_logs = []
        for filename in sorted(os.listdir(LOGS_LOCATION)):
            if filename.endswith(".csv") and filename.startswith("folder_logs_"):
                filepath = os.path.join(LOGS_LOCATION, filename)
                try:
                    df = pd.read_csv(filepath)
                    df['session'] = filename.replace("folder_logs_", "").replace(".csv", "")
                    all_logs.append(df)
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")
        
        return pd.concat(all_logs, ignore_index=True) if all_logs else pd.DataFrame()
        
    except Exception as e:
        st.markdown(f"<div class='notification error'>❌ Error reading logs: {str(e)}</div>", unsafe_allow_html=True)
        return pd.DataFrame()
    
init_log_file()
    
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
    
if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_log_file = os.path.join(
        LOGS_LOCATION, 
        f"folder_logs_{st.session_state.session_start_time}.csv"
    )    
# Initialize session state
if 'token' not in st.session_state:
    token = authenticate()
    if not token:
        st.markdown("<div class='notification error'>🔒 Authentication failed: Check OTCS URL, credentials, or network connectivity</div>", unsafe_allow_html=True)
        st.stop()
    st.session_state.token = token

def validate_folder_name(folder_name):
    """Validate folder name for invalid characters and patterns"""
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    if re.search(invalid_chars, folder_name):
        return False, f"Folder name contains invalid characters: {folder_name}"
    
    # Check for reserved names
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 
                     'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if folder_name.upper() in reserved_names:
        return False, f"Folder name is a reserved system name: {folder_name}"
    
    # Check for trailing spaces or dots
    if folder_name.endswith('.') or folder_name.endswith(' '):
        return False, f"Folder name ends with a dot or space: {folder_name}"
    
    return True, "Valid folder name"

def validate_folder_path(folder_path):
    """Validate the complete folder path"""
    if not folder_path or folder_path.strip() == '':
        return False, "Empty folder path provided"
    
    # Check for leading/trailing slashes
    if folder_path.startswith('/') or folder_path.endswith('/'):
        return False, "Folder path should not start or end with a slash"
    
    # Check for consecutive slashes
    if '//' in folder_path:
        return False, "Folder path contains consecutive slashes"
    
    # Split and validate each folder name
    path_parts = [part.strip() for part in folder_path.split('/') if part.strip()]
    
    if not path_parts:
        return False, "No valid folder names in path"
    
    for part in path_parts:
        is_valid, error_msg = validate_folder_name(part)
        if not is_valid:
            return False, f"{error_msg} in path: {folder_path}"
    
    return True, "Valid folder path"

def check_folder_exists(token, folder_name, parent_id):
    """Check if a folder exists under a parent with retries"""
    url = f"{BASE_URL}/api/v2/nodes/{parent_id}/nodes"
    headers = {"OTCSTicket": token}
    params = {"where_name": folder_name, "where_type": 0}  # 0 = folder

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    return data['results'][0]['data']['properties']['id']
            return None
        except Exception as e:
            if attempt < 2:  # Not the last attempt
                time.sleep(1)  # Wait before retrying
                continue
            log_event("system", "check_folder", "error", f"Error checking folder: {str(e)}")
            return None

def create_folder(token, folder_name, parent_id, description=""):
    """Create a single folder"""
    headers = {
        "OTCSTicket": token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "type": 0,
        "name": folder_name,
        "parent_id": parent_id,
        "description": description
    }

    url = f"{BASE_URL}/api/v2/nodes"

    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        if response.status_code == 200:
            response_data = response.json()
            node_id = response_data.get('id')
            return True, f"Folder '{folder_name}' created successfully (ID: {node_id})", node_id
        elif response.status_code == 409:
            # Folder already exists
            return False, f"Folder '{folder_name}' already exists under parent ID {parent_id}", None
        else:
            try:
                error_json = response.json()
                error_detail = error_json.get('error', {}).get('message', response.text)
            except:
                error_detail = response.text
            return False, f"Failed to create folder '{folder_name}': {response.status_code} - {error_detail}", None
    except requests.exceptions.Timeout:
        return False, f"Timeout creating folder '{folder_name}' - request took too long", None
    except Exception as e:
        return False, f"Error creating folder '{folder_name}': {str(e)}", None


def create_folder_hierarchy(token, folder_path, root_id=2000, description=""):
    """Create complete folder hierarchy with folder verification"""
    # Validate the folder path first
    is_valid, error_msg = validate_folder_path(folder_path)
    if not is_valid:
        return False, error_msg, None, []
    
    path_parts = [part.strip() for part in folder_path.strip('/').split('/') if part.strip()]
    
    if not path_parts:
        return False, "Empty folder path provided", None, []
    
    current_parent_id = root_id
    hierarchy_details = []
    created_folders = []
    existing_folders = []
    
    log_event("system", "create_hierarchy", "info", f"Starting hierarchy creation for path: {folder_path}")

    for i, folder_name in enumerate(path_parts):
        is_final_folder = (i == len(path_parts) - 1)
        current_path = "/".join(path_parts[:i + 1])
        
        # Check if folder exists under current parent
        existing_folder_id = check_folder_exists(token, folder_name, current_parent_id)
        
        if existing_folder_id:
            # Folder exists - use as parent for next level
            current_parent_id = existing_folder_id
            existing_folders.append({
                'name': folder_name,
                'id': existing_folder_id,
                'path': current_path,
                'level': i,
            })
            hierarchy_details.append({
                'folder_name': folder_name,
                'folder_id': existing_folder_id,
                'parent_id': current_parent_id,
                'level': i,
                'status': 'existed',
                'path': current_path,
                'message': f"Folder already exists (ID: {existing_folder_id})"
            })
            log_event("system", "create_hierarchy", "info", 
                     f"Found existing folder: {folder_name} (ID: {existing_folder_id})")
            
            # If this is the final folder and it already exists, return failure
            if is_final_folder:
                error_msg = f"Final folder '{folder_name}' already exists in path: {folder_path}"
                log_event("system", "create_hierarchy", "error", error_msg)
                return False, error_msg, None, hierarchy_details
        else:
            # Create new folder under current parent
            folder_desc = description if is_final_folder else ""
            success, message, new_folder_id = create_folder(
                token, folder_name, current_parent_id, folder_desc
            )
            
            if not success:
                if "already exists" in message:
                    # Folder was created by another process, try to find it
                    time.sleep(2)  # Wait a bit for the folder to be available
                    verified_id = check_folder_exists(token, folder_name, current_parent_id)
                    
                    if verified_id:
                        current_parent_id = verified_id
                        existing_folders.append({
                            'name': folder_name,
                            'id': verified_id,
                            'path': current_path,
                            'level': i,
                        })
                        hierarchy_details.append({
                            'folder_name': folder_name,
                            'folder_id': verified_id,
                            'parent_id': current_parent_id,
                            'level': i,
                            'status': 'existed',
                            'path': current_path,
                            'message': f"Folder created by another process (ID: {verified_id})"
                        })
                        log_event("system", "create_hierarchy", "warning", 
                                 f"Folder created by another process: {folder_name} (ID: {verified_id})")
                        
                        # If this is the final folder and it already exists, return failure
                        if is_final_folder:
                            error_msg = f"Final folder '{folder_name}' already exists in path: {folder_path}"
                            log_event("system", "create_hierarchy", "error", error_msg)
                            return False, error_msg, None, hierarchy_details
                        continue
                
                error_msg = f"Failed to create '{folder_name}' at level {i}: {message}"
                log_event("system", "create_hierarchy", "error", error_msg)
                return False, error_msg, None, hierarchy_details
            
            # Verify the folder was created and is accessible
            verified = False
            for attempt in range(3):  # Try up to 3 times
                time.sleep(1)  # Wait before verification
                verified_id = check_folder_exists(token, folder_name, current_parent_id)
                
                if verified_id:
                    # Success - use this ID as parent for next level
                    current_parent_id = verified_id
                    verified = True
                    break
            
            if not verified:
                error_msg = f"Folder '{folder_name}' created but not found after creation (ID: {new_folder_id})"
                log_event("system", "create_hierarchy", "error", error_msg)
                return False, error_msg, None, hierarchy_details
            
            created_folders.append({
                'name': folder_name,
                'id': current_parent_id,  # Use verified ID
                'path': current_path,
                'level': i,
            })
            hierarchy_details.append({
                'folder_name': folder_name,
                'folder_id': current_parent_id,
                'parent_id': current_parent_id,
                'level': i,
                'status': 'created',
                'path': current_path,
                'message': f"Folder created successfully (ID: {current_parent_id})"
            })
            log_event("system", "create_hierarchy", "success", 
                     f"Created and verified folder: {folder_name} (ID: {current_parent_id})")

    success_message = (
        f"Hierarchy creation completed successfully!\n"
        f"- Path: {folder_path}\n"
        f"- Final folder ID: {current_parent_id}\n"
        f"- Created {len(created_folders)} new folders\n"
        f"- Found {len(existing_folders)} existing folders"
    )

    log_event("system", "create_hierarchy", "success", success_message)
    return True, success_message, current_parent_id, hierarchy_details

def display_hierarchy_preview(folder_paths):
    """Display a visual preview of the folder hierarchy to be created"""
    if not folder_paths:
        return

    st.markdown("### 📂 Folder Hierarchy Preview")

    # Build a tree structure
    tree = {}
    for path in folder_paths:
        parts = [part.strip() for part in path.strip('/').split('/') if part.strip()]
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def render_tree(node, level=0):
        items = []
        for name, children in sorted(node.items()):
            indent = "  " * level
            icon = "📁" if children else "📄"
            items.append(f"{indent}{icon} {name}")
            items.extend(render_tree(children, level + 1))
        return items

    tree_display = render_tree(tree)

    hierarchy_html = "<div class='hierarchy-display'>"
    for item in tree_display[:20]:  # Limit display to first 20 items
        level = (len(item) - len(item.lstrip())) // 2
        clean_item = item.strip()
        hierarchy_html += f"<div class='hierarchy-level-{min(level, 5)}'>{clean_item}</div>"

    if len(tree_display) > 20:
        hierarchy_html += f"<div class='hierarchy-level-0'>... and {len(tree_display) - 20} more items</div>"

    hierarchy_html += "</div>"

    st.markdown(hierarchy_html, unsafe_allow_html=True)


def generate_folder_template():
    """Generate a sample Excel template with more comprehensive examples"""
    data = {
        "Folder Path": [
            "Projects/2024/Client-ABC/Documents",
            "Projects/2024/Client-ABC/Contracts",
            "Projects/2024/Client-XYZ/Financial",
            "HR/Employee-Records/2024/January",
            "HR/Employee-Records/2024/February",
            "Marketing/Campaigns/Q1-2024/Social-Media",
            "Marketing/Campaigns/Q1-2024/Email-Marketing",
            "IT/Software/Licenses/2024",
            "Legal/Contracts/Vendor-Agreements",
            "Finance/Reports/Monthly/2024"
        ],
        "Description": [
            "Project documents for Client ABC",
            "Contract files for Client ABC",
            "Financial documents for Client XYZ",
            "Employee records for January 2024",
            "Employee records for February 2024",
            "Social media campaign materials Q1 2024",
            "Email marketing campaign files Q1 2024",
            "Software license documentation for 2024",
            "Vendor agreement contracts",
            "Monthly financial reports for 2024"
        ]
    }
    return pd.DataFrame(data)


# ---------- STREAMLIT UI ----------
# Header
st.markdown("""
<div class="header">
    <div class="container" style="padding: 0 2rem;">
        <img src="https://companieslogo.com/img/orig/OTEX_BIG-ea374e29.png?t=1741951344" class="opentext-logo" alt="OpenText Logo">
        <p class="hero-subtext">Bulk Folder Creation</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="container" style="padding: 0 2rem;">
    <h2 class="section-title">Folder Management</h2>
    <p style="margin-bottom: 2rem; font-size: 1.1rem; color: #555; animation: fadeInUp 1s ease-out;">
        Efficiently create folder structures in OpenText Content Server.
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Card
with st.container():
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
# Divider
st.markdown(
    "<div style='height: 3px; background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)); margin: 3rem 0; animation: slideLine 5s infinite;'></div>",
    unsafe_allow_html=True
)

# Tabs
tab1, tab2, tab3 = st.tabs(["📁 Folder Creation", "📊 System Logs", "ℹ️ Help & Examples"])

with tab1:
    st.subheader("🏗️ Hierarchical Folder Creation")

    with st.expander("🚀 Quick Start Guide", expanded=True):
        st.markdown("""
        ### How to Create Nested Folder Hierarchies:

        **1. Prepare Your Excel File:**
        - **Folder Path**: Complete path like `Department/Team/Project/SubProject`
        - **Description** (optional): Description for the final folder in each path

        **2. Examples of Valid Paths:**
        ```
        Projects/2024/Client-ABC/Documents/Contracts
        HR/Employees/2024/January/Performance-Reviews
        Marketing/Campaigns/Q1/Social-Media/Images
        IT/Infrastructure/Servers/Production/Logs
        ```

        **3. What the System Does:**
        - ✅ Creates `Projects` folder under root (Enterprise)
        - ✅ Creates `2024` folder under `Projects`
        - ✅ Creates `Client-ABC` folder under `2024`
        - ✅ Creates `Documents` folder under `Client-ABC`
        - ✅ Creates `Contracts` folder under `Documents` with your description
        
        **4. Important Note:**
        - ❌ If the final folder in any path already exists, the entire path will be marked as failed
        - ✅ Intermediate existing folders are fine and will be used
        - 🔄 The system will create only the missing folders in the hierarchy
        """)


    # Display template and download option
    col1, col2 = st.columns([2, 1])
    # Prepare the Excel template buffer
    template_df = generate_folder_template()
    excel_buffer = BytesIO()
    template_df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    with col1:
        st.download_button(
            label="📥 Download Excel Template",
            data=excel_buffer.getvalue(),
            file_name="folder_hierarchy_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download a sample Excel file with hierarchy examples"
        )

    with col2:
        root_folder_id = st.number_input(
            "Root Folder ID",
            value=2000,
            min_value=1,
            help="Parent folder ID where hierarchy will be created (2000 = Enterprise)"
        )

# File Upload
    uploaded_file = st.file_uploader(
        "📤 Upload Excel File for Hierarchical Folder Creation",
        type=["xlsx"],
        help="Upload Excel file with 'Folder Path' column containing nested paths"
    )

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        required_columns = ["Folder Path"]
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.markdown(
                f"<div class='notification error'>❌ Missing required columns: {', '.join(missing_cols)}</div>",
                unsafe_allow_html=True
            )
            log_event("admin", "folder_upload", "error", f"Missing columns: {missing_cols}")
        else:
            # Clean the data
            df = df.dropna(subset=['Folder Path'])
            df['Folder Path'] = df['Folder Path'].astype(str).str.strip()
            df = df[df['Folder Path'] != '']

            if len(df) == 0:
                st.markdown(
                    "<div class='notification error'>❌ No valid folder paths found in the file</div>",
                    unsafe_allow_html=True
                )
            else:
                with st.expander("📄 Preview Uploaded Data", expanded=True):
                    st.dataframe(df, use_container_width=True)
                    st.markdown(
                        f"<div class='notification info'>📊 Found {len(df)} folder hierarchies to create</div>",
                        unsafe_allow_html=True
                    )

                # Display hierarchy preview
                folder_paths = df['Folder Path'].tolist()
                display_hierarchy_preview(folder_paths)

                # Validation warnings
                long_paths = df[df['Folder Path'].str.len() > 200]
                if not long_paths.empty:
                    st.markdown(
                        f"<div class='notification error'>⚠️ {len(long_paths)} paths are longer than 200 characters and may cause issues</div>",
                        unsafe_allow_html=True
                    )

                deep_paths = df[df['Folder Path'].str.count('/') > 10]
                if not deep_paths.empty:
                    st.markdown(
                        f"<div class='notification error'>⚠️ {len(deep_paths)} paths have more than 10 levels deep - consider simplifying</div>",
                        unsafe_allow_html=True
                    )

                if st.button("🚀 Create Folder Hierarchies", key="create_hierarchies", type="primary"):
                    total = len(df)
                    success_count = 0
                    failure_count = 0
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    results = []

                    # Start timing here
                    start_time = datetime.now()

                    for i, row in df.iterrows():
                        folder_path = str(row.get("Folder Path", "")).strip()
                        description = str(row.get("Description", "")).strip() if "Description" in df.columns else ""

                        status_text.markdown(f"""
                            <div class='notification info'>
                                🔄 Processing {i+1}/{total}: <strong>{folder_path}</strong>
                                <br><small>Creating nested folder structure...</small>
                            </div>
                        """, unsafe_allow_html=True)

                        if folder_path and folder_path.lower() not in ['nan', 'none']:
                            success, message, final_folder_id, hierarchy_details = create_folder_hierarchy(
                                st.session_state.token,
                                folder_path,
                                root_id=root_folder_id,
                                description=description
                            )

                            if success:
                                success_count += 1
                                created_count = sum(1 for detail in hierarchy_details if detail['status'] == 'created')
                                existing_count = sum(1 for detail in hierarchy_details if detail['status'] == 'existed')

                                log_event("admin", "create_hierarchy", "success",
                                        f"Created hierarchy: {folder_path} (Final ID: {final_folder_id})")

                                results.append({
                                    "Folder Path": folder_path,
                                    "Status": "✅ Success",
                                    "Final Folder ID": final_folder_id,
                                    "Created Folders": created_count,
                                    "Existing Folders": existing_count,
                                    "Total Levels": len(hierarchy_details),
                                    "Description": description or "N/A",
                                    "Message": f"Created {created_count} new, found {existing_count} existing"
                                })
                            else:
                                failure_count += 1
                                log_event("admin", "create_hierarchy", "error",
                                        f"Failed to create hierarchy: {folder_path} - {message}")

                                results.append({
                                    "Folder Path": folder_path,
                                    "Status": "❌ Failed",
                                    "Final Folder ID": "N/A",
                                    "Created Folders": 0,
                                    "Existing Folders": 0,
                                    "Total Levels": 0,
                                    "Description": description or "N/A",
                                    "Message": message
                                })
                        else:
                            failure_count += 1
                            error_msg = f"Invalid folder path at row {i+2}"
                            log_event("admin", "create_hierarchy", "error", error_msg)

                            results.append({
                                "Folder Path": f"Row {i+2}",
                                "Status": "❌ Failed",
                                "Final Folder ID": "N/A",
                                "Created Folders": 0,
                                "Existing Folders": 0,
                                "Total Levels": 0,
                                "Description": "N/A",
                                "Message": "Invalid or empty folder path"
                            })

                        progress = int(((i + 1) / total) * 100)
                        progress_bar.progress(progress)

                    # Completion summary - properly indented inside the button block
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()

                    status_text.markdown(f"""
                        <div class='notification success'>
                            ✅ <strong>Hierarchy Creation Complete!</strong>
                            <br>⏱️ Duration: {duration:.1f} seconds
                            <br>📊 Success: {success_count} | Failed: {failure_count}
                        </div>
                    """, unsafe_allow_html=True)

                    progress_bar.empty()

                    # Results summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("✅ Successful", success_count)
                    with col2:
                        st.metric("❌ Failed", failure_count)
                    with col3:
                        st.metric("⏱️ Duration", f"{duration:.1f}s")

                    # Detailed results
                    with st.expander("📊 Detailed Hierarchy Creation Results", expanded=True):
                        result_df = pd.DataFrame(results)
                        st.dataframe(result_df, use_container_width=True)

                    # Export results
                    excel_buffer = BytesIO()
                    result_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)

                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    report_filename = f"folder_hierarchy_results_{timestamp}.xlsx"
                    report_file = os.path.join(REPORT_LOCATION, report_filename)

                    with open(report_file, 'wb') as f:
                        f.write(excel_buffer.getvalue())

                    st.download_button(
                        label="📥 Download Detailed Results",
                        data=excel_buffer,
                        file_name=report_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download complete results with hierarchy details"
                    )
    except Exception as e:
        st.markdown(
            f"<div class='notification error'>❌ Error processing Excel file: {str(e)}</div>",
            unsafe_allow_html=True
        )
        log_event("admin", "folder_upload", "error", f"Excel processing error: {str(e)}")


with tab2:
    st.subheader("📊 System Logs & Activity")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Refresh Logs"):
            st.rerun()

    logs_df = read_logs()

    if logs_df.empty:
        st.markdown(
            "<div class='notification info'>📝 No system logs available yet.</div>",
            unsafe_allow_html=True
        )
    else:
        # Log filters
        st.markdown("**🔍 Filter Options:**")
        col1, col2, col3 = st.columns(3)

        with col1:
            action_filter = st.selectbox(
                "Action Type",
                ["All"] + sorted(logs_df['action'].unique().tolist()),
                help="Filter logs by action type"
            )
        with col2:
            status_filter = st.selectbox(
                "Status",
                ["All"] + sorted(logs_df['status'].unique().tolist()),
                help="Filter logs by status"
            )
        with col3:
            username_filter = st.selectbox(
                "User",
                ["All"] + sorted(logs_df['username'].unique().tolist()),
                help="Filter logs by username"
            )

        # Apply filters
        filtered_logs = logs_df.copy()
        if action_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['action'] == action_filter]
        if status_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['status'] == status_filter]
        if username_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['username'] == username_filter]

        # Log statistics
        if not filtered_logs.empty:
            st.markdown("**📈 Log Statistics:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Logs", len(filtered_logs))
            with col2:
                success_logs = len(filtered_logs[filtered_logs['status'] == 'success'])
                st.metric("Success", success_logs)
            with col3:
                error_logs = len(filtered_logs[filtered_logs['status'] == 'error'])
                st.metric("Errors", error_logs)
            with col4:
                unique_actions = filtered_logs['action'].nunique()
                st.metric("Action Types", unique_actions)

        # Display logs
        st.dataframe(filtered_logs, use_container_width=True, height=400)

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
    st.subheader("ℹ️ Help & Examples")

    # FAQ Section
    with st.expander("❓ Frequently Asked Questions", expanded=True):
        st.markdown("""
        ### Q: What is hierarchical folder creation?
        **A:** It automatically creates nested folder structures like `Projects/2024/ClientA/Documents` in a single operation, creating all intermediate folders if they don't exist.

        ### Q: What happens if a folder already exists?
        **A:** The system intelligently skips existing folders and continues creating the missing parts of the hierarchy.

        ### Q: What's the maximum folder depth supported?
        **A:** While there's no hard limit, we recommend keeping hierarchies under 10 levels deep for better performance and usability.

        ### Q: Can I use special characters in folder names?
        **A:** Avoid special characters like `< > : " | ? *` and control characters. Use hyphens or underscores instead of spaces.

        ### Q: What is the root folder ID 2000?
        **A:** In OpenText Content Server, 2000 typically represents the "Enterprise" root folder where all content is stored.
        """)

    # Examples Section
    with st.expander("📋 Path Examples & Best Practices", expanded=True):
        st.markdown("""
        ### ✅ Good Path Examples:
        ```
        HR/Employees/2024/Performance-Reviews
        Projects/Web-Development/Client-ABC/Source-Code
        Finance/Reports/Monthly/2024/January
        Marketing/Campaigns/Q1-2024/Email/Templates
        IT/Documentation/Systems/Production/Monitoring
        ```

        ### ❌ Avoid These:
        ```
        /HR/Employees/                     (Leading/trailing slashes)
        Projects//Client-ABC               (Double slashes)
        Finance/Reports with spaces        (Spaces in names)
        Marketing/Campaigns/<Special>      (Special characters)
        ```

        ### 📏 Best Practices:
        - Use descriptive but concise folder names
        - Use hyphens or underscores instead of spaces
        - Keep folder names under 50 characters
        - Use consistent naming conventions
        - Organize by category, then by time/project
        """)

    # Troubleshooting Section
    with st.expander("🔧 Troubleshooting Common Issues", expanded=True):
        st.markdown("""
        ### 🔐 Authentication Issues:
        - Verify OTCS URL is correct and accessible
        - Check username and password in configuration
        - Ensure Content Server is running and accessible

        ### 📁 Folder Creation Failures:
        - Check if you have permission to create folders in the target location
        - Verify the root folder ID exists and is accessible
        - Ensure folder names don't contain invalid characters

        ### 📊 Excel File Issues:
        - Ensure 'Folder Path' column exists and contains valid paths
        - Remove empty rows or cells with invalid data
        - Check file format is .xlsx (not .xls)

        ### 🌐 Network Issues:
        - Verify network connectivity to Content Server
        - Check if firewall is blocking the connection
        - Increase timeout if requests are timing out
        """)

    # API Reference
    with st.expander("🔗 API Reference & Technical Details", expanded=True):
        st.markdown(f"""
        ### 🛠️ Current Configuration:
        - **OTCS URL:** `{BASE_URL}`
        - **API Version:** v2
        - **Root Folder ID:** Enterprise (2000)
        - **Authentication:** OTCSTicket based

        ### 📡 API Endpoints Used:
        - **Auth:** `{BASE_URL}/api/v1/auth`
        - **Create Node:** `{BASE_URL}/api/v2/nodes`
        - **List Nodes:** `{BASE_URL}/api/v2/nodes/{{parent_id}}/nodes`

        ### 🔄 Process Flow:
        1. **Authentication:** Get OTCSTicket token
        2. **Path Parsing:** Split folder path into individual components
        3. **Hierarchy Check:** For each level, check if folder exists
        4. **Smart Creation:** Create only missing folders in correct order
        5. **Final Verification:** Return final folder ID and creation details

        ### 📊 Response Codes:
        - **200:** Success - Folder created or found
        - **400:** Bad Request - Invalid parameters
        - **401:** Unauthorized - Authentication failed
        - **403:** Forbidden - No permission
        - **409:** Conflict - Folder name already exists
        """)
# Footer
st.markdown("""
<div class="footer">
    <p>OpenText Content Server Bulk Folder Creation Tool</p>
    <p>Version 2.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)