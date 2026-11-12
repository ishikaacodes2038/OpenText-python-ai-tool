import streamlit as st
import pandas as pd
import json
import os
import requests
import logging
import csv
from datetime import datetime
from io import BytesIO

LOGS_LOCATION = 'logs/system_logs.db'

# --- Global log_event function for all tabs ---
def log_event(username, action, status, message, details=""):
    try:
        import sqlite3
        conn = sqlite3.connect(LOGS_LOCATION)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, username TEXT, action TEXT, status TEXT, message TEXT, details TEXT)")
        c.execute("INSERT INTO logs (timestamp, username, action, status, message, details) VALUES (?, ?, ?, ?, ?, ?)",
                  (datetime.now().isoformat(), username, action, status, message, details))
        conn.commit()
        conn.close()
    except Exception as e:
        st.markdown(f"❌ Error logging event: {str(e)}", unsafe_allow_html=True)

# --- UI & CSS (from opentext_ui.py) ---
def apply_opentext_ui():
    st.set_page_config(
        page_title="OpenText Content Server Management",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
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
        /* Center the feature icon in the feature card */
        .feature-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def show_opentext_header():
    st.markdown("""
    <div class="header">
        <img src="https://companieslogo.com/img/orig/OTEX_BIG-ea374e29.png?t=1741951344" class="opentext-logo" alt="OpenText Logo">
        <p class="hero-subtext">Empowering Smarter Information Management</p>
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
    st.markdown("""
    <style>
        .feature-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .feature-icon {
            font-size: 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            margin-bottom: 0.5rem;
        }
        /* Zoom in/out animation for feature title */
        @keyframes zoomInOut {
            0% { transform: scale(1); }
            50% { transform: scale(1.15); }
            100% { transform: scale(1); }
        }
        .feature-title {
            animation: zoomInOut 2s infinite;
            transition: transform 0.3s;
        }
    </style>
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <div class="card" style="min-width: 350px; max-width: 500px; margin: 0 auto;">
            <div class="card-header">Group/SubGroup Creation</div>
            <div class="card-body">
                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <h3 class="feature-title">Group/SubGroup Creation</h3>
                    <p class="feature-description">
                        Easily create groups and subgroups in OpenText Content Server. 
                        Streamline your organization structure with a user-friendly interface and bulk operations.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 3px; background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end)); margin: 3rem 0; animation: slideLine 5s infinite;'></div>", unsafe_allow_html=True)

def show_opentext_footer():
    st.markdown("""
    <div class="footer">
        <p>OpenText Content Server Management Portal • v2.0</p>
        <p>2023 OpenText corporation. All rights reserved©.</p>
    </div>
    """, unsafe_allow_html=True)

# --- CONFIG LOADING ---
def load_config():
    config_file = 'otcs_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return (
                    config.get('otcs_url', ''),
                    config.get('username', ''),
                    config.get('password', '')
                )
        except Exception as e:
            st.error(f"Error loading config file '{config_file}': {e}. Please ensure it contains valid JSON like: {{'otcs_url': '...', 'username': '...', 'password': '...'}}")
            st.stop()
    else:
        st.error(f"Config file '{config_file}' not found. Please create it with your OpenText Content Server credentials.")
        st.stop()

base_url, username, password = load_config()

# --- LOGGING SETUP (from Group_Creation.py) ---
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f'group_creation_log_{datetime.now().strftime("%Y-%m-%d")}.log')
csv_log_filename = os.path.join(log_dir, f'group_creation_log_{datetime.now().strftime("%Y-%m-%d")}.csv')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s,%(levelname)s,%(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='a', encoding='utf-8'),
    ]
)

# --- HELPER TO CONSTRUCT API URLS ---
def get_api_url(base_url, version, path):
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    return f"{base_url}/api/{version}/{path}"

# --- OTCS API LOGIC (from Group_Creation.py) ---
def get_otcs_token(base_url, username, password):
    url = get_api_url(base_url, 'v1', 'auth')
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data, verify=False)
    if response.status_code == 200:
        return response.json().get('ticket')
    else:
        return None

def create_group_otcs_v1(base_url, token, group_name, parent_id=None):
    # Use v1 for creation
    url = get_api_url(base_url, 'v1', 'members')
    headers = {'OTCSTicket': token}
    data = {'name': group_name, 'type': 1}
    if parent_id:
        data['parent_id'] = parent_id
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return True, response.json().get('id', 'N/A')
    elif response.status_code == 409:
        return False, "Group already exists"
    else:
        return False, response.text

def link_subgroup_to_group_v2(base_url, token, parent_group_id, subgroup_id):
    # Use v2 for linking
    url = get_api_url(base_url, 'v2', f'members/{parent_group_id}/members')
    headers = {
        'OTCSTicket': token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'member_id': subgroup_id,
        'type': 1
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return True, "Subgroup linked to parent group"
    else:
        return False, response.text

# --- Refactored process_excel_and_create_groups ---
def process_excel_and_create_groups(df, base_url, username, password):
    token = get_otcs_token(base_url, username, password)
    if not token:
        logging.error('Authentication failed for user: %s', username)
        with open(csv_log_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.now(), 'ERROR', username, '', '', 'Authentication failed'])
        return None, "❌ Authentication failed. Check your OTCS credentials."

    created = failed = created_sub = failed_sub = linked_sub = link_failed = 0
    progress = st.progress(0)
    counter = 0

    created_groups = {}
    report_data = []

    # --- UI: Status line below progress bar ---
    status_placeholder = st.empty()

    # --- Fetch all existing subgroups globally ---
    def fetch_all_subgroups(base_url, token):
        url = get_api_url(base_url, 'v1', 'members')
        headers = {'OTCSTicket': token}
        params = {'where_type': 1}
        all_items = []
        try:
            page = 1
            has_more = True
            while has_more:
                params['page'] = page
                response = requests.get(url, headers=headers, params=params, verify=False)
                if response.status_code == 200:
                    data = response.json().get('data', [])
                    all_items.extend(data)
                    has_more = response.json().get('has_more', False)
                    page += 1
                else:
                    has_more = False
            # Deduplicate all_items by id
            seen_ids = set()
            unique_items = [g for g in all_items if not (g.get('id') in seen_ids or seen_ids.add(g.get('id')))]
            # Only subgroups (parent_id not 0 or empty)
            subgroups = [g for g in unique_items if g.get('parent_id') and str(g.get('parent_id')) not in ('0', '')]
            return subgroups
        except Exception as e:
            st.error(f"Error fetching subgroups: {e}")
            return []

    # Build global subgroup name→ID lookup
    global_subgroups = fetch_all_subgroups(base_url, token)
    subgroup_name_to_id = {g['name']: g['id'] for g in global_subgroups if 'name' in g and 'id' in g}

    total_rows = len(df)
    total_groups = len(df['GroupName'].unique())
    total_subgroups = df['SubGroupName'].notnull().sum()

    # --- Step 1: Create groups and subgroups using v1 ---
    for idx, row in df.iterrows():
        group = str(row['GroupName']).strip()
        subgroup = str(row.get('SubGroupName', '')).strip()

        # Create Group (track by group name)
        if group not in created_groups:
            success, msg = create_group_otcs_v1(base_url, token, group)
            group_id = msg if success else None
            created += int(success)
            failed += int(not success)
            created_groups[group] = group_id
            report_data.append({
                'Group Name': group,
                'SubGroup Name': '',
                'Group ID/Message': msg,
                'Status': 'Group Created' if success else 'Group Failed'
            })
            log_status = 'SUCCESS' if success else 'FAIL'
            logging.info('Group creation: %s, Status: %s, Message: %s', group, log_status, msg)
            with open(csv_log_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.now(), log_status, username, group, '', msg])
        else:
            group_id = created_groups[group]

        # Create SubGroup (if not exists)
        if subgroup:
            if group_id:
                parent_id_int = None
                try:
                    parent_id_int = int(group_id)
                except (TypeError, ValueError):
                    parent_id_int = None
                if subgroup not in subgroup_name_to_id:
                    sub_success, sub_msg = create_group_otcs_v1(base_url, token, subgroup, parent_id=parent_id_int)
                    if sub_success:
                        created_sub += 1
                        subgroup_name_to_id[subgroup] = sub_msg
                        report_data.append({
                            'Group Name': group,
                            'SubGroup Name': subgroup,
                            'Group ID/Message': sub_msg,
                            'Status': 'SubGroup Created'
                        })
                        sub_log_status = 'SUCCESS'
                        logging.info('SubGroup creation: %s (parent: %s), Status: %s, Message: %s', subgroup, group, sub_log_status, sub_msg)
                        with open(csv_log_filename, 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([datetime.now(), sub_log_status, username, group, subgroup, sub_msg])
                    else:
                        failed_sub += 1
                        report_data.append({
                            'Group Name': group,
                            'SubGroup Name': subgroup,
                            'Group ID/Message': sub_msg,
                            'Status': f'SubGroup Failed: {sub_msg}'
                        })
                        sub_log_status = 'FAIL'
                        logging.info('SubGroup creation failed: %s (parent: %s), Status: %s, Message: %s', subgroup, group, sub_log_status, sub_msg)
                        with open(csv_log_filename, 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([datetime.now(), sub_log_status, username, group, subgroup, sub_msg])
            else:
                report_data.append({
                    'Group Name': group,
                    'SubGroup Name': subgroup,
                    'Group ID/Message': '',
                    'Status': 'SubGroup Failed: Parent group creation failed'
                })

        percent = int(((idx + 1) / total_rows) * 100)
        progress.progress(percent)
        status_html = f"""
        <div style='font-size:0.95rem; color:#005eb8; margin-top:0.5rem; text-align:left;'>
            <span style='font-weight:500;'>Processing:</span> <span style='color:#00a3e0;'>{percent}%</span>
            &nbsp;|&nbsp; <span style='font-weight:500;'>Rows:</span> {idx+1} / {total_rows}
            &nbsp;|&nbsp; <span style='font-weight:500;'>Groups Created:</span> <span style='color:#005eb8;'>{created}</span> / {total_groups}
            &nbsp;|&nbsp; <span style='font-weight:500;'>SubGroups Created:</span> <span style='color:#00a3e0;'>{created_sub}</span> / {total_subgroups}
        </div>
        """
        status_placeholder.markdown(status_html, unsafe_allow_html=True)

    # --- Step 2: Link subgroups to groups using v2 ---
    for idx, row in df.iterrows():
        group = str(row['GroupName']).strip()
        subgroup = str(row.get('SubGroupName', '')).strip()
        group_id = created_groups.get(group)
        sub_id = subgroup_name_to_id.get(subgroup)
        if group_id and sub_id and subgroup:
            link_success, link_msg = link_subgroup_to_group_v2(base_url, token, group_id, sub_id)
            linked_sub += int(link_success)
            link_failed += int(not link_success)
            report_data.append({
                'Group Name': group,
                'SubGroup Name': subgroup,
                'Group ID/Message': sub_id,
                'Status': 'SubGroup Linked' if link_success else f'SubGroup Link Failed: {link_msg}'
            })
            sub_log_status = 'SUCCESS' if link_success else 'LINK_FAIL'
            logging.info('SubGroup link: %s (parent: %s), Status: %s, Message: %s', subgroup, group, sub_log_status, link_msg)
            with open(csv_log_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.now(), sub_log_status, username, group, subgroup, link_msg])

    report_df = pd.DataFrame(report_data)
    summary = {
        'created': created,
        'failed': failed,
        'created_sub': created_sub,
        'failed_sub': failed_sub,
        'linked_sub': linked_sub,
        'link_failed': link_failed
    }

    return summary, report_df

# --- MAIN APP LOGIC (from your_main_code.py) ---
apply_opentext_ui()
show_opentext_header()
show_features_section()

# --- Add System Log Tab ---
import sqlite3

tab1, tab2, tab3, tab4 = st.tabs([
    "Group/SubGroup Creation",
    "Group/SubGroup Deletion",
    "System Logs",
    "Help & Examples"
])

with tab1:
    tab1_instructions = """
    1. Prepare an Excel file with these columns:
       - **GroupName**: Name of the group to create
       - **SubGroupName** (optional): Name of the subgroup to create and link under the group
    2. Upload the Excel file using the file uploader below
    3. Click "Create" to create all groups and subgroups
    ### Important Notes:
    - The system will create the complete group/subgroup hierarchy automatically
    - If a group already exists, it will not be recreated
    - All groups are created at the root unless a parent is specified
    - A new log file is generated each time the functionality is executed. Users can access it at the log location specified during the sign-up process.
    """
    def generate_folder_template():
        return pd.DataFrame({
            'GroupName': ['Department'],
            'SubGroupName': ['Team (optional)']
        })
    from io import BytesIO
    with st.expander("ℹ️ How to use Bulk Group/SubGroup Creation", expanded=True):
        st.markdown(tab1_instructions, unsafe_allow_html=True)
    uploaded_file = st.file_uploader('Upload Excel file with Group/SubGroup info', type=['xlsx'])
    submit = st.button('Create')
    st.markdown('''
        <style>
        /* Force the Create button to always show the gradient, even if Streamlit changes the DOM */
        div.stButton button[type="submit"], div.stButton button {
            background: linear-gradient(90deg, #005eb8, #00a3e0) !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        div.stButton button[type="submit"]:hover, div.stButton button:hover {
            background: linear-gradient(90deg, #00a3e0, #005eb8) !important;
            box-shadow: 0 8px 20px rgba(0, 94, 184, 0.4) !important;
        }
        /* Gradient blue style for download buttons */
        .stDownloadButton button {
            background: linear-gradient(90deg, #005eb8, #00a3e0) !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        .stDownloadButton button:hover {
            background: linear-gradient(90deg, #00a3e0, #005eb8) !important;
            box-shadow: 0 8px 20px rgba(0, 94, 184, 0.4) !important;
        }
        </style>
    ''', unsafe_allow_html=True)
    report_df = None
    # ...existing code...

    if submit and uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            with st.spinner('Processing...'):
                summary, report_df = process_excel_and_create_groups(df, base_url, username, password)
            if summary is None:
                st.error(report_df)
            else:
                st.success('Group/SubGroup creation completed!')
                st.write('Summary:', summary)
            # Log each row to system logs, regardless of success or failure
            if report_df is not None:
                for _, row in report_df.iterrows():
                    log_event(
                        username=username,
                        action='Group/SubGroup Creation',
                        status=row.get('Status', ''),
                        message=f"Group: {row.get('Group Name', '')}, SubGroup: {row.get('SubGroup Name', '')}",
                        details=row.get('Group ID/Message', '')
                    )
        except Exception as e:
            st.error(f'Error: {e}')
    elif submit and not uploaded_file:
        st.warning('Please upload an Excel file.')

    # Show download button for report after processing, not inside the form
    if report_df is not None:
        st.download_button('📥Download Report', report_df.to_csv(index=False), file_name='group_creation_report.csv', mime='text/csv')

with tab2:
    st.header('Group/SubGroup Deletion 🗑️')
    st.info('Select one or more groups/subgroups to delete. You can filter by type, and a confirmation dialog will appear before deletion.')

    # --- Helper functions ---____
    def get_otcs_token(base_url, username, password):
        url = get_api_url(base_url, 'v1', 'auth')
        data = {'username': username, 'password': password}
        response = requests.post(url, data=data, verify=False)
        if response.status_code == 200:
            return response.json().get('ticket')
        else:
            return None

    def fetch_all_groups_and_subgroups(base_url, token):
        url = get_api_url(base_url, 'v1', 'members')
        headers = {'OTCSTicket': token}
        params = {'where_type': 1}
        all_items = []
        try:
            page = 1
            has_more = True
            while has_more:
                params['page'] = page
                response = requests.get(url, headers=headers, params=params, verify=False)
                if response.status_code == 200:
                    data = response.json().get('data', [])
                    all_items.extend(data)
                    has_more = response.json().get('has_more', False)
                    page += 1
                else:
                    has_more = False
            # Deduplicate all_items by id
            seen_ids = set()
            unique_items = [g for g in all_items if not (g.get('id') in seen_ids or seen_ids.add(g.get('id')))]
            # Classify as group or subgroup based on parent_id
            groups = [g for g in unique_items if not g.get('parent_id') or str(g.get('parent_id')) in ('0', '')]
            subgroups = [g for g in unique_items if g.get('parent_id') and str(g.get('parent_id')) not in ('0', '')]
            return groups, subgroups
        except Exception as e:
            st.error(f"Error fetching groups: {e}")
            return [], []

    def delete_group(base_url, token, group_id):
        url = get_api_url(base_url, 'v1', f'members/{group_id}')
        headers = {'OTCSTicket': token}
        response = requests.delete(url, headers=headers, verify=False)
        return response.status_code == 200, response.text

    # --- UI ---
    token = get_otcs_token(base_url, username, password)
    if not token:
        st.error("Authentication failed. Check your OTCS credentials.")
    else:
        groups, subgroups = fetch_all_groups_and_subgroups(base_url, token)
        if not groups and not subgroups:
            st.info("No groups or subgroups found.")
        else:
            filter_type = st.radio("⏳Filter by type :", ["All", "Groups only"], horizontal=True)
            if filter_type == "All":
                display_groups = [
                    (f"👥 {g.get('name')} (ID: {g.get('id')})", g.get('id'), 'Group') for g in groups
                ]
                display_subgroups = [
                    (f"↳ {g.get('name')} (ID: {g.get('id')})", g.get('id'), 'SubGroup') for g in subgroups
                ]
                display_list = display_groups + display_subgroups
            elif filter_type == "Groups only":
                display_list = [
                    (f"👥 {g.get('name')} (ID: {g.get('id')})", g.get('id'), 'Group') for g in groups
                ]
            # Only sort if there are both groups and subgroups
            if filter_type == "All":
                display_list.sort(key=lambda x: (x[2], x[0]))
            else:
                display_list.sort(key=lambda x: x[0])
            label_to_id = {label: gid for label, gid, _ in display_list}
            selected = st.multiselect(
                "Select groups/subgroups to delete:",
                options=list(label_to_id.keys()),
                help="Groups are marked with 👥, subgroups with ↳.",
                max_selections=30
            )
            if selected:
                confirm = st.checkbox(
                    f"Are you sure you want to delete the selected {len(selected)} item(s)? This action cannot be undone.",
                    value=False, key="confirm_delete"
                )
                if confirm:
                    proceed = st.button("Proceed with Deletion", key="proceed_delete", help="Permanently delete the selected items.")
                    if proceed:
                        deleted = 0
                        failed = 0
                        failed_items = []
                        # Use global log_event function
                        for sel in selected:
                            gid = label_to_id[sel]
                            ok, msg = delete_group(base_url, token, gid)
                            # Determine type for log (Group/SubGroup)
                            item_type = 'Group' if sel.startswith('👥') else 'SubGroup'
                            log_status = 'SUCCESS' if ok else 'FAIL'
                            log_message = f"{item_type} Deletion: {sel}"
                            # Log deletion to system logs (always)
                            if log_event:
                                log_event(
                                    username=username,
                                    action='Group/SubGroup Deletion',
                                    status=log_status,
                                    message=log_message,
                                    details=msg
                                )
                            if ok:
                                deleted += 1
                            else:
                                failed += 1
                                failed_items.append(f"{sel} (Reason: {msg})")
                        if deleted:
                            st.success(f"Deleted {deleted} group(s)/subgroup(s).")
                        if failed:
                            st.error(f"Failed to delete {failed} item(s):\n" + '\n'.join(failed_items))
                elif selected:
                    st.info("Check the box above to enable deletion.")
            else:
                st.info("Select at least one group or subgroup to delete.")
# ...existing code...
with tab3:
    import sqlite3
    LOGS_LOCATION = 'logs/system_logs.db'

    def log_event(username, action, status, message, details=""):
        try:
            conn = sqlite3.connect(LOGS_LOCATION)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
            if not c.fetchone():
                c.execute('''CREATE TABLE logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    action TEXT,
                    status TEXT,
                    message TEXT,
                    details TEXT
                )''')
            c.execute("INSERT INTO logs (timestamp, username, action, status, message, details) VALUES (?, ?, ?, ?, ?, ?)",
                      (datetime.now().isoformat(), username, action, status, message, details))
            conn.commit()
            conn.close()
        except Exception as e:
            st.markdown(f"❌ Error logging event: {str(e)}", unsafe_allow_html=True)

    def read_logs():
        try:
            conn = sqlite3.connect(LOGS_LOCATION)
            c = conn.cursor()
            # Always create the logs table if it doesn't exist, so previous logs are always accessible
            c.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                action TEXT,
                status TEXT,
                message TEXT,
                details TEXT
            )''')
            df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
            conn.close()
            return df
        except Exception as e:
            st.markdown(f"❌ Error reading logs: {str(e)}", unsafe_allow_html=True)
            return pd.DataFrame()

    st.subheader("📊 System Logs")


    # --- Display all previous logs only, do not auto-generate test log ---
    logs_df = read_logs()

    if st.button("🔄 Refresh Logs"):
        st.rerun()

    st.markdown("**System Logs Table:**")
    st.dataframe(logs_df)

    # Only show filter options if logs_df has required columns
    # Show logs with filter by date and action type
    if not logs_df.empty:
        # --- Horizontal filter layout ---
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**⏳Filter by Date:**")
            date_options = [
                "None",
                "Last 1 Hour",
                "Today",
                "Last Week",
                "Last Month",
                "Last 3 Months",
                "All"
            ]
            date_filter = st.selectbox("Select Date Range 📅", date_options, index=0, key="date_filter")
        with col2:
            st.markdown("**Filter by Action Type:**")
            action_options = ["All", "Group/SubGroup Creation", "Group/SubGroup Deletion"]
            action_filter = st.selectbox("Action Type", action_options, index=0, key="action_filter")

        if date_filter != "None":
            logs_df['timestamp_dt'] = pd.to_datetime(logs_df['timestamp'], errors='coerce')
            now = pd.Timestamp.now()

            if date_filter == "Last 1 Hour":
                start = now - pd.Timedelta(hours=1)
                filtered_logs = logs_df[logs_df['timestamp_dt'] >= start]
            elif date_filter == "Today":
                start = now.normalize()
                filtered_logs = logs_df[logs_df['timestamp_dt'] >= start]
            elif date_filter == "Last Week":
                start = (now - pd.Timedelta(days=7)).normalize()
                filtered_logs = logs_df[logs_df['timestamp_dt'] >= start]
            elif date_filter == "Last Month":
                start = (now - pd.DateOffset(months=1)).normalize()
                filtered_logs = logs_df[logs_df['timestamp_dt'] >= start]
            elif date_filter == "Last 3 Months":
                start = (now - pd.DateOffset(months=3)).normalize()
                filtered_logs = logs_df[logs_df['timestamp_dt'] >= start]
            elif date_filter == "All":
                filtered_logs = logs_df.copy()
            else:
                filtered_logs = logs_df.copy()

            # Filter by action type
            if action_filter != "All":
                filtered_logs = filtered_logs[filtered_logs['action'] == action_filter]

            st.markdown("**Logs Table:**")
            st.dataframe(filtered_logs.drop(columns=['timestamp_dt']))

            excel_buffer = BytesIO()
            filtered_logs.drop(columns=['timestamp_dt']).to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)

            st.download_button(
                label="📥 Download Logs as Excel",
                data=excel_buffer,
                file_name="system_logs.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

show_opentext_footer()
with tab4:
    st.subheader("ℹ️ Help & Examples")

    # FAQ Section
    with st.expander("❓ Frequently Asked Questions", expanded=True):
        st.markdown("""
        ### Q: How do I create groups and subgroups?
        **A:** Go to the 'Group/SubGroup Creation' tab, upload an Excel file with columns 'GroupName' and optional 'SubGroupName', then click 'Create'.
        The app will process each row and create the specified groups and subgroups in OpenText Content Server. You can monitor progress and see a summary after completion.
        If there are any issues with the file or data, you will be notified immediately.

        ### Q: What happens if a group or subgroup already exists?
        **A:** The app will skip creation for existing groups/subgroups and log the result.
        This ensures no duplicate groups or subgroups are created, and you can see which items were skipped in the summary and logs.
        All actions, including skips, are recorded for transparency and troubleshooting.

        ### Q: How do I delete groups or subgroups?
        **A:** Use the 'Group/SubGroup Deletion' tab, select one or more items from the list, confirm, and click 'Proceed with Deletion'.
        The app will send a deletion request for each selected item and show you which deletions succeeded or failed. You must confirm before any deletion is performed to prevent accidental removal.
        All deletion actions are logged and can be reviewed in the System Logs tab.

        ### Q: Can I download a report of created groups/subgroups?
        **A:** Yes, after creation, use the 'Download Report' button to save a CSV file of results.
        The report contains details of all groups and subgroups processed, including their status and any error messages. This helps you keep a record and share results with others if needed.
        You can also use this report for auditing or troubleshooting purposes.

        ### Q: Where can I see logs of all actions?
        **A:** The 'System Logs' tab shows all creation and deletion events, with filters and Excel download.
        You can filter logs by date, view details of each action, and download the logs as an Excel file for further analysis. This ensures full traceability of all operations performed in the app.
        Logs include timestamps, usernames, actions, statuses, and messages for each event.

        ### Q: What if my Excel file is missing required columns?
        **A:** The app will show an error and skip processing until the file is corrected.
        Make sure your Excel file includes 'GroupName' and (optionally) 'SubGroupName' columns, with no empty required cells. If the format is incorrect, you will be prompted to fix it before proceeding.
        This helps prevent errors and ensures smooth bulk creation of groups and subgroups.
        """)

    # Examples Section
    with st.expander("📋 Group/SubGroup Examples", expanded=True):
        st.markdown("""
        ### ✅ Example Excel for Bulk Creation:
        | GroupName   | SubGroupName    |
        |-------------|-----------------|
        | HR          | Recruitment     |
        | IT          | Infrastructure  |
        | Finance     | Auditing        |
        | Marketing   | Events          |

        - Each row creates a group and (optionally) a subgroup under it.
        - You can add as many rows as needed for your organization structure.
        - Subgroups will be linked to their parent group automatically.
        - The app will skip any duplicate group/subgroup and log the result.

        ### Example: Deleting Groups/SubGroups
        - Select one or more items (e.g., 'HR', 'Recruitment', 'Finance', 'Reporting') in the deletion tab.
        - Use the filter to show only groups or all items.
        - Confirm your selection by checking the confirmation box.
        - Click 'Proceed with Deletion' to remove the selected items from OTCS.
        - The app will show which deletions succeeded and which failed, with reasons.
        - All deletion actions are logged and can be reviewed in the System Logs tab.

        ### Example: Downloading Reports
        - After group/subgroup creation, click 'Download Report' to save results as CSV.
        - The report includes all processed items, their status, and any error messages.
        - Use the report for auditing, sharing, or troubleshooting.
        """)

    # Troubleshooting Section
    with st.expander("🔧 Troubleshooting", expanded=True):
        st.markdown("""
        ### 🔐 Authentication Issues:
        - Check OTCS URL, username, and password in the config file.
        - Make sure the Content Server is reachable from your network.

        ### � Excel File Issues:
        - Ensure your file has 'GroupName' and (optionally) 'SubGroupName' columns.
        - File must be .xlsx format and not have empty required cells.

        ### 👥 Group/SubGroup Not Found:
        - If a group/subgroup is missing in the deletion tab, refresh or check if it was just created.
        - Only items fetched from OTCS will be shown for deletion.

        ### � Logging Issues:
        - All actions are logged in the 'System Logs' tab. If logs are missing, check file permissions for the logs folder.
        - If log entries are not updating, try restarting the app or check for database locks.
        - If you see errors about writing logs, ensure you have write access to the logs directory and the database file is not open elsewhere.
        """)