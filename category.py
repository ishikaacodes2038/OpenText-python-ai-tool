import streamlit as st
import pandas as pd
import requests
import re
import html
import json
import os 
import urllib.parse
from datetime import datetime


# --- Import UI components ---
from categoryui import (
    apply_opentext_ui,
    show_opentext_header,
    show_features_section,
    show_management_tools_header,
    show_opentext_footer,
    create_section_divider
)

# --- Apply UI ---
apply_opentext_ui()
show_opentext_header()
show_features_section()
create_section_divider()
show_management_tools_header()
st.info("""
ℹ️ **Welcome to the OTCS Category Application Tool!**

This tool allows you to:
- ✅ Apply metadata categories to multiple nodes using a structured CSV.
- 🔍 Check existing categories on any node.
- 🗑️ Delete a category from a node.
- 📁 Manage content efficiently with OpenText integrations.

**Instructions:**
1. Prepare a CSV with **FolderStructure** as the first column
2. Insert a **ApplyToSubitems** to perform inheritance
3. Insert a **GroupID** column (with value Unknown) before each new category group for visual separation. `This column is ignored during processing`.
4. Follow with columns in the format: **Category Name = Attribute = Value**.
5. Upload the file and click **Apply Categories to Nodes**.
6. Use the bottom section to **Check Existing categories on any node**.
7. Use the Delete section to **remove a category from a node** if needed.
       
Need help? Reach out to your admin or refer to the documentation.

""")

# --- Load configuration from external JSON file ---
def load_config():
    with open("otcs_config.json") as f:
        return json.load(f)

config = load_config()
BASE_URL = config["otcs_url"]
USERNAME = config["username"]
PASSWORD = config["password"]
DOWNLOAD_DIR = config.get("download_temp_dir", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --- Authenticate and get token ---
def authenticate():
    url = f"{BASE_URL}/api/v1/auth"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("ticket")
    else:
        return None

# --- API Endpoints ---
CATEGORY_APPLY_URL = f"{BASE_URL}/api/v2/nodes/{{node_id}}/categories"
CATEGORY_LIST_URL = f"{BASE_URL}/api/v1/nodes/{{node_id}}/categories"
CATEGORY_DELETE_URL = f"{BASE_URL}/api/v1/nodes/{{node_id}}/categories/{{category_id}}"
WEBREPORT_ID = 997497
WEBREPORT_URL = f"{BASE_URL}/api/v1/nodes/{WEBREPORT_ID}/output"

# --- Get Category ID from WebReport ---
def get_category_id(category_name, token):
    headers = {"OTCSTicket": token, "Accept": "application/json"}
    params = {"CategoryName": category_name, "format": "webreport"}

    try:
        response = requests.get(WEBREPORT_URL, headers=headers, params=params)
        response.raise_for_status()
        raw_output = html.unescape(response.text)
        rows = re.findall(r"<TR.*?>.*?</TR>", raw_output, re.DOTALL)

        for row in rows:
            cells = re.findall(r"<TD>(.*?)</TD>", row)
            if len(cells) >= 2:
                data_id = cells[0].strip().replace('\xa0', '')
                name = cells[1].strip().replace('\xa0', '')
                if name.lower() == category_name.lower():
                    return int(data_id)
        return None
    except Exception as e:
        st.warning(f"⚠️ Failed to fetch Category ID for '{category_name}': {e}")
        return None

# --- Type inference from value ---
def infer_type_from_value(value):
    if pd.isna(value) or str(value).strip().lower() == "unknown":
        return None
    value_str = str(value).strip()
    if re.match(r"\d{1,2}[-/]\d{1,2}[-/]\d{4}", value_str):
        return "date"
    elif value_str.lower() in ["yes", "no", "true", "false", "1", "0"]:
        return "flag"
    elif re.match(r"^\d+(\.0+)?$", value_str):  # matches 1245 or 1245.0
       return "integer"
    elif value_str.isdigit():
       if len(value_str) > 6:
        return "text"
       return "integer"

    else:
        return "text"


# --- Format value based on type ---
def format_value_by_type(value, detected_type):
    if detected_type.lower() == "date":
        for fmt in ("%m-%d-%Y", "%m/%d/%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                parsed_date = datetime.strptime(value, fmt)
                return parsed_date.strftime("%Y-%m-%dT00:00:00")
            except ValueError:
                continue
        return None
    elif detected_type.lower() == "flag":
        return "1" if value.lower() in ["yes", "true", "1"] else "0"
    elif detected_type.lower() == "integer":
       try:
         value_float = float(value)
         if value_float.is_integer():
             return str(int(value_float))  # convert 1245.0 → 1245
         else:
              return None  # not a valid integer
       except ValueError:
          return None

    else:
        return value
    


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

# --- Apply or update category ---
def apply_or_update_category(node_id, category_id, fields, token, debug=False):
    update_url = CATEGORY_APPLY_URL.format(node_id=node_id)
    headers = {
        "OTCSTicket": token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    formatted_fields = {}
    for index, (attr_name, value) in enumerate(fields.items(), start=2):
        key = f"{category_id}_{index}"
        formatted_fields[key] = value

    formatted_fields["category_id"] = category_id
    payload = {"body": json.dumps(formatted_fields)}
    print(f"DEBUG → Sending to API: {formatted_fields}")
    response = requests.post(update_url, headers=headers, data=payload)

    if debug:
        if response.status_code != 200 or "error" in response.text.lower():
            try:
                st.text("Response:")
                st.json(response.json())
            except Exception:
                st.text(response.text)

    return response.status_code, response.text


# --- Get existing categories on a node ---
def get_existing_categories(node_id, token):
    url = CATEGORY_LIST_URL.format(node_id=node_id)
    headers = {"OTCSTicket": token, "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    categories = data.get("data", [])
    if not categories:
        st.warning(f"No categories found on Node {node_id}.")
        return []

    st.success(f"✅ Categories found on Node {node_id}:")
    for cat in categories:
        name = cat.get("name", "Unnamed Category")
        st.markdown(f"- **{name}**")

    return [cat.get("name") for cat in categories]

# -- Delete Category from node --
def delete_category_from_node(node_id, category_id, token):
    url = CATEGORY_DELETE_URL.format(node_id=node_id, category_id=category_id)
    headers = {"OTCSTicket": token, "Accept": "application/json"}
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return 500, str(e)

# --- Streamlit UI ---
# --- Streamlit UI ---
tab1, tab2, tab3 = st.tabs(["Main Application", "System Log", "Help & Examples"])


with tab1:
    st.title("📂 OTCS Category Application Tool")

    # No CSV uploader here — it's handled in Main App section
    # No logging of CSV upload status
    # Category application logic should be in Main App block


with tab2:
    st.subheader("📋 System Log Viewer")

    # Load logs from session or file
    session_logs = st.session_state.get("recent_logs", [])
    file_logs = []
    if os.path.exists("system_log.txt"):
        with open("system_log.txt", "r", encoding="utf-8") as f:
            file_logs = f.readlines()

    # Combine logs
    all_logs = session_logs + file_logs

    # Let user choose view
    log_view = st.radio("Select Log View", ["Recent Logs", "Full History"])
    selected_logs = session_logs if log_view == "Recent Logs" else all_logs

    if selected_logs:
        log_data = []
        for line in selected_logs:
            line_lower = line.lower()
            if "successfully" in line_lower or "✅ success" in line_lower:
                status = "SUCCESS"
            elif "[error]" in line_lower:
                status = "ERROR"
            else:
                continue  # Skip INFO and OTHER logs

            match = re.search(r"category '(.+?)'", line, re.IGNORECASE)
            category = match.group(1) if match else "Unknown"
            log_data.append({
                "Status": status,
                "Category": category,
                "Message": line.strip()
            })


        log_df = pd.DataFrame(log_data)

        # Filters
        status_filter = st.multiselect(
            "Filter by Status", options=["SUCCESS", "ERROR"], default=["SUCCESS", "ERROR"]
        )
        category_filter = st.text_input("Search by Category Name")

        # Apply filters
        filtered_df = log_df[log_df["Status"].isin(status_filter)]
        if category_filter:
            filtered_df = filtered_df[filtered_df["Category"].str.contains(category_filter, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("ℹ️ No logs to display.")


with tab3:
    st.subheader("ℹ️ Help & Examples")

    # FAQ Section
    with st.expander("❓ Frequently Asked Questions", expanded=True):
        st.markdown("""
        ### Q: What does this tool do?
        **A:** It applies metadata categories to multiple nodes in OpenText Content Server using a structured CSV file. You can also check existing categories or delete them from nodes.

        ### Q: What is a 'GroupID' column and why is it needed?
        **A:** 'GroupID' is used for visual separation in the CSV. It should be placed before each new category group and set to 'Unknown'. It is ignored during processing.
        
        ### Q: What is a 'ApplyToSubitem' column ?
        **A:** 'ApplyToSubitem' is used to perform inheritance if it is 'Yes' then it will apply Category to the Sub Folders or Files present in Parent Folder.
        
        ### Q: How should I format the CSV file?
        **A:** The first column must be `FolderStructure`, followed by columns in the format `Category Name = Attribute = Value`. Blank cells are treated as valid (clear attribute), but values like 'NA', 'Unknown', and 'N/A' are ignored.

        ### Q: What happens if a category already exists on a node?
        **A:** The tool checks for existing categories and skips reapplying them. It logs the result for each node and category.

        ### Q: Can I apply multiple categories to the same node?
        **A:** Yes, as long as each category is defined correctly in the CSV and the node path resolves successfully.

        ### Q: What is the root folder ID 2000?
        **A:** In OpenText Content Server, folder ID 2000 typically refers to the "Enterprise" root folder.
        """)

    # Examples Section
    with st.expander("📋 CSV Format & Best Practices", expanded=True):
        st.markdown("""
        ### ✅ Good CSV Structure:
        ```
        FolderStructure, HR = EmployeeStatus = Active, HR = JoinDate = 01/15/2024
        Projects/ClientA, Project = Status = Active, Project = StartDate = 03/01/2024
        Finance/Reports/2024, Finance = Approved = Yes, Finance = Month = January
        ```

        ### ❌ Avoid These:
        ```
        /HR/Employees/, HR = Status = Active       (Leading slash)
        Projects//ClientA, Project = Status = Active (Double slashes)
        Finance/Reports with spaces, Finance = Month = Jan (Spaces in folder names)
        ```

        ### 📏 Best Practices:
        - Use `FolderStructure` as the first column
        - Use `Category = Attribute = Value` format for metadata
        - Avoid 'NA', 'Unknown', 'N/A' values—they are ignored
        - Use hyphens or underscores instead of spaces in folder names
        - Keep folder names under 50 characters
        - Maintain consistent naming conventions
        """)

    # Troubleshooting Section
    with st.expander("🔧 Troubleshooting Common Issues", expanded=True):
        st.markdown("""
        ### 🔐 Authentication Issues:
        - Check `otcs_config.json` for correct OTCS URL, username, and password
        - Ensure Content Server is running and accessible

        ### 📁 Folder Path Resolution Failures:
        - Ensure folder path exists under Enterprise (ID 2000)
        - Avoid leading/trailing slashes or double slashes
        - Check for typos or invalid characters

        ### 📊 CSV File Issues:
        - Ensure 'FolderStructure' column exists
        - Remove empty rows or cells with invalid data
        - Ensure file format is `.csv` (not `.xls` or `.xlsx`)
        - Avoid using 'NA', 'Unknown', or 'N/A' as values

        ### 🧠 Category Application Failures:
        - Ensure category name matches exactly with OTCS
        - Check if category ID is retrievable via WebReport
        - Ensure attribute values are valid and formatted correctly

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
        - **Apply Category:** `{BASE_URL}/api/v2/nodes/{{node_id}}/categories`
        - **List Categories:** `{BASE_URL}/api/v1/nodes/{{node_id}}/categories`
        - **Delete Category:** `{BASE_URL}/api/v1/nodes/{{node_id}}/categories/{{category_id}}`

        ### 🔄 Process Flow:
        1. **Authentication:** Get OTCSTicket token
        2. **CSV Parsing:** Read structured CSV with FolderStructure and Category=Attribute=Value columns
        3. **Path Resolution:** Resolve folder path to Node ID
        4. **Category Mapping:** Get Category ID via WebReport
        5. **Smart Application:** Apply only valid attributes, skipping 'NA', 'Unknown', 'N/A'
        6. **Logging:** Store results and errors in `system_log.txt`

        ### 📊 Response Codes:
        - **200:** Success - Category applied
        - **400:** Bad Request - Invalid parameters
        - **401:** Unauthorized - Authentication failed
        - **403:** Forbidden - No permission
        - **409:** Conflict - Category already exists
        """)



# --- Authenticate once ---
if "token" not in st.session_state:
    try:
        st.session_state.token = authenticate()
    except Exception as e:
        st.error(f"Authentication failed: {e}")

# --- Main App ---
if "token" in st.session_state:
    token = st.session_state.token

    # --- Upload and Apply CSV ---
    structured_file = st.file_uploader("📄 Upload Structured Category CSV", type=["csv"])
    if structured_file:
        st.info("ℹ️ Please ensure your CSV format is: `NodeID`, followed by columns like `Category = Attribute = Value`.")

    if structured_file and st.button("🚀 Apply Categories to Nodes"):
        df = pd.read_csv(structured_file)
        # Clean NodeID column
        df.rename(columns={"FolderStructure": "FolderStructure"}, inplace=True)
        df["FolderStructure"] = df["FolderStructure"].fillna("").astype(str)
        results = []
        for idx, row in df.iterrows():
         node_id = str(row["FolderStructure"]).strip()

        
        # Create progress bar and status text once
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0
        failure_count = 0
        total_rows = len(df)

       # Loop through rows
        for idx, row in df.iterrows():
            folder_path = str(row["FolderStructure"]).strip()
            apply_to_subitems = str(row.get("ApplyToSubItems", "")).strip().lower()

            node_id, error = get_node_id_from_path(BASE_URL, token, folder_path)
            if error:
                st.error(f"❌ Failed to resolve folder path '{folder_path}': {error}")
                failure_count += 1
                continue

            # Your category application logic here...
            # If successful:
            success_count += 1
            # If failed:
            # failure_count += 1
            # Update progress bar and status
            percent_complete = int(((idx + 1) / total_rows) * 100)
            progress_bar.progress((idx + 1) / total_rows)
            status_text.text(
                f"Progress: {percent_complete}% | Total: {total_rows} | ✅ Success: {success_count} | ❌ Failed: {failure_count}"
            )



            categories = {}

            for col in df.columns:
                if "=" in col:
                    try:
                        parts = [p.strip() for p in col.split("=")]
                        if len(parts) >= 3:
                            category_name, attribute_name, detected_type = parts
                            raw_value = str(row[col]).strip()
                            raw_value_clean = raw_value.lower()
                            # Treat blank as valid clear
                            if raw_value_clean == "":
                                categories.setdefault(category_name, {})[attribute_name] = ""
                                continue

                            # Infer type if needed
                            if detected_type.lower() in ["value", "type"]:
                                inferred = infer_type_from_value(raw_value)
                                if inferred:
                                   detected_type = inferred
                            # Handle special values
                            if raw_value_clean in {"na", "unknown", "n/a"}:
                                categories.setdefault(category_name, {})[attribute_name] = raw_value
                            else:
                                formatted = format_value_by_type(raw_value, detected_type)
                                if formatted is not None:
                                   categories.setdefault(category_name, {})[attribute_name] = formatted


                                        
                        print(f"DEBUG → Category: {category_name}, Attribute: {attribute_name}, Raw: '{raw_value}', Type: {detected_type}, Formatted: '{formatted}'")


                    except Exception:
                        continue

            for category_name, fields in categories.items():
                # Keep blank values, exclude only NA/Unknown/N/A/null
                valid_fields = {
                    k: v for k, v in fields.items()
                    if str(v).strip().lower() not in {"na", "unknown", "n/a", "null", "nan"}
                }
                if not valid_fields:
                    results.append((folder_path, category_name, "❌ Category is not Applied"))
                    continue

                # Apply category with valid (including blank) values
                category_id = get_category_id(category_name, token)
                if category_id:
                    status_code, response_text = apply_or_update_category(node_id, category_id, valid_fields, token)
                    if status_code == 200:
                        results.append((folder_path, category_name, "✅ Category Applied to Folder"))
                        # ✅ Log cleared attributes
                        for attr, val in valid_fields.items():
                            if val == "":
                                with open("system_log.txt", "a") as log_file:
                                    log_file.write(f"[CLEAR] Cleared attribute '{attr}' in category '{category_name}' on Node {node_id}\n")
                            else:
                                results.append((folder_path, category_name, f"❌ Failed to apply category to folder: {response_text}"))

                    csv_paths = set(df["FolderStructure"].str.strip())
                    if apply_to_subitems == "yes":
                        # Enable inheritance for future items
                        inheritance_url = f"{BASE_URL}/api/v2/nodes/{node_id}/categories/{category_id}/inheritance"
                        inheritance_response = requests.post(inheritance_url, headers={"OTCSTicket": token, "Accept": "application/json"})
                        results.append((folder_path, category_name, f"🔄 Inheritance Enabled (Status: {inheritance_response.status_code})"))

                        # Apply category to existing child nodes
                        child_url = f"{BASE_URL}/api/v2/nodes/{node_id}/nodes"
                        child_response = requests.get(child_url, headers={"OTCSTicket": token, "Accept": "application/json"})
                        
                        if child_response.status_code == 200:
                            child_data = child_response.json().get("results", [])
                            for child in child_data:
                                child_id = child["data"]["properties"]["id"]
                                child_name = child["data"]["properties"]["name"]
                                child_path = f"{folder_path.strip()}/{child_name}".strip()

                                # ✅ Skip child if it has its own row in the CSV
                                if child_path in csv_paths:
                                    continue

                                child_status, child_response_text = apply_or_update_category(child_id, category_id, valid_fields, token)
                                if child_status == 200:
                                    results.append((child_path, category_name, "✅ Category Applied to Child"))
                                    with open("system_log.txt", "a") as log_file:
                                        log_file.write(f"[SUCCESS] Applied category '{category_name}' to Child Node {child_id} successfully\n")
                                else:
                                    results.append((child_path, category_name, f"❌ Failed to apply to child: {child_response_text}"))
                                    with open("system_log.txt", "a") as log_file:
                                        log_file.write(f"[ERROR] Failed to apply category '{category_name}' to Child Node {child_id}\n")

                             

                    if status_code == 200 and "error" not in response_text.lower():
                        results.append((folder_path, category_name, "✅ Success"))
                        with open("system_log.txt", "a") as log_file:
                            log_file.write(f"[SUCCESS] Applied category '{category_name}' to Node {node_id} successfully\n")
                        with open("system_log.txt", "a") as log_file:
                            log_file.write(f"[SUCCESS] Applied category '{category_name}' to Child Node {child_id} successfully\n")
                        with open("system_log.txt", "a") as log_file:
                            log_file.write(f"[ERROR] Failed to apply category '{category_name}' to Child Node {child_id}\n")



                            if "recent_logs" not in st.session_state:
                                st.session_state.recent_logs = []
                            st.session_state.recent_logs.append(f"[SUCCESS] Applied category '{category_name}' to Node {node_id} successfully\n")
                    else:
                        results.append((folder_path, category_name, "❌ Failed:NO Category Applied"))
                        with open("system_log.txt", "a") as log_file:
                            log_file.write(f"[ERROR] Failed to apply category '{category_name}' to Node {node_id}\n")
                            if "recent_logs" not in st.session_state:
                                st.session_state.recent_logs = []
                            st.session_state.recent_logs.append(f"[ERROR] Failed to apply category '{category_name}' to Node {node_id}\n")


                else:
                    results.append((folder_path, category_name, "❌ Failed: Category ID not found"))

        st.success("✅ Processing complete.")
        # Convert results to DataFrame
        results_df = pd.DataFrame(results, columns=["Folder/Item", "Category", "Status"])
        st.session_state.results_df = results_df  # Store in session state
        # Save to CSV for download
        results_df.to_csv("category_update_report.csv", index=False) 

        # Show summary
        st.write(f"Total processed: {len(results_df)}")
        st.write(f"Failures: {results_df['Status'].str.contains('Failed').sum()}")

        
  # Show results only when user clicks 'View Results'
if "results_df" in st.session_state:
    df = st.session_state.results_df
    rows_per_page = 10
    total_pages = (len(df) + rows_per_page - 1) // rows_per_page

    if total_pages > 0:
        if "page_number" not in st.session_state or st.session_state.page_number > total_pages:
            st.session_state.page_number = 1

        st.session_state.page_number = st.number_input(
            "Page", min_value=1, max_value=total_pages,
            value=st.session_state.page_number, step=1
        )

        start_idx = (st.session_state.page_number - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        st.dataframe(df.iloc[start_idx:end_idx])

        # ✅ Provide download button here
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download Full Report", csv, "category_update_report.csv", "text/csv")
    else:
        st.info("ℹ️ No results to display.")


# --- Check existing categories on a node ---
st.markdown("---")
st.subheader("🔍 Check Existing Categories on a Node")
check_node_id = st.text_input("Enter Node ID to check categories")

if st.button("Check Categories") and check_node_id:
        try:
            get_existing_categories(check_node_id.strip(), token)
        except Exception as e:
            st.error(f"Failed to fetch categories: {e}")


# --- Delete category from node ---
st.markdown("---")
st.subheader("🗑️ Delete Category from Node")

del_node_id = st.text_input("Enter Node ID for deletion")
del_category_id = st.text_input("Enter Category ID to delete")

if st.button("Delete Category") and del_node_id and del_category_id:
    try:
        status_code, response_text = delete_category_from_node(del_node_id.strip(), del_category_id.strip(), token)
        if status_code in [200, 204]:
            st.success(f"✅ Category {del_category_id} successfully deleted from Node {del_node_id}.")
        else:
            st.error(f"❌ Failed to delete category. Status: {status_code}, Response: {response_text}")
    except Exception as e:
        st.error(f"Error occurred during deletion: {e}")


# --- Footer ---
create_section_divider()
show_opentext_footer()
