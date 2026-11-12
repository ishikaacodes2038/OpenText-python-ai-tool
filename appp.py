from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json
import os
from dotenv import load_dotenv
from functools import lru_cache
from googletrans import Translator  # Free translation library

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Initialize Bedrock client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Initialize translator
translator = Translator()

# Language mapping including regional languages
LANGUAGE_MAP = {
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'ru': 'Russian',
    'ar': 'Arabic'
}


# Comprehensive OTCS context
OTCS_CONTEXT = """
OpenText Content Server (OTCS) is an enterprise content management platform designed to manage documents, workflows, compliance, and security for organizations. It provides a centralized repository for content with features like document versioning, access control, and automated workflows. Below are key features and tools:

1. Folder Creation Tool
Purpose: Streamlines folder setup in OTCS workspaces.
Functionality: Enables users to create folders and organize content.
Usage:
Navigate to a workspace.
Click “New Folder”.
Enter a folder name.
Save to create the folder.
🔗 Access it here: http://localhost:8503

2. Access Permission Manager
Purpose: Manages secure access to folders via ACL (Access Control List).
Functionality: Assigns read, write, or administer rights to users or groups.
Usage:
Open the folder.
Go to the Permissions tab.
Add users/groups to the ACL.
Set appropriate rights (e.g., read-only, full control).
🔗 Access it here: http://localhost:8504


3. **Migration Through Excel**:
   - Purpose: Supports document migration into OTCS using Excel spreadsheets.
   - Functionality: Users can upload Excel files with columns specifying document paths (local or public URLs), metadata (e.g., title, category), and target OTCS locations. Supports versioning to track changes during migration.
   - Usage: Access the tool at http://localhost:8506, upload an Excel file, map columns to OTCS fields, and initiate migration. Errors are logged for invalid paths or metadata.

4. **Category Application Tool**:
   - Purpose: Manages metadata categories on OTCS nodes for efficient content organization.
   - Functionality: Allows users to define and apply metadata categories (e.g., project ID, department) to documents or folders, improving searchability and compliance.
   - Usage: Open the tool at http://localhost:8505, select a node, and assign or edit categories via a user-friendly interface.

5. **Group & SubGroup Creation**:
   - Purpose: Enables bulk creation and linking of groups and subgroups in OTCS.
   - Functionality: Simplifies user management by allowing administrators to create groups, add subgroups, and assign members in bulk. Supports integration with OTCS permissions.
   - Usage: Access the tool at http://localhost:8502, input group details, and link subgroups or users. Supports CSV imports for bulk operations.

7. **General OTCS Features**:
   - **Document Versioning**: OTCS tracks document changes, maintaining historical versions accessible via the Version Control tab. Users can revert to previous versions or compare changes.
   - **Workflows**: Automates business processes by defining steps, assignees, and actions (e.g., approval, review). Create workflows in the OTCS Workflow Designer, assigning tasks to users or groups.
   - **Permissions**: Managed via the ACL, accessible in folder or document properties. Permissions include See, See Contents, Modify, Edit Attributes, and Administer. For example, to restrict a folder to a specific user, add them to the ACL with limited rights.
   - **Search**: OTCS supports full-text and metadata-based search. Use the Search bar to query documents by keywords, categories, or attributes.
   - **Compliance**: Ensures regulatory compliance with audit trails, retention policies, and secure access controls.

8. **Common Tasks**:
   - To create a folder: In a workspace, click 'New Folder,' enter a name, and set permissions in the ACL.
   - To set permissions for a specific user: Open the folder’s properties, go to Permissions, add the user to the ACL, and select rights (e.g., read, write).
   - To migrate documents: Use the Migration Through Excel tool or OTCS’s native import feature, specifying document paths and metadata.
   - To manage categories: Use the Category Application Tool or OTCS’s metadata interface to assign categories to nodes.
   - To automate processes: Create a workflow in the Workflow Designer, defining steps and assignees.

If a query is unclear or not covered, respond with: 'I need more details to answer this query. Please specify, e.g., "How do I create a folder in OTCS?" or contact OpenText support.'
"""

@lru_cache(maxsize=100)
def generate_bedrock_response(query, language):
    try:
        # Translate query to English for better understanding by the model
        if language != 'en':
            translated_query = translator.translate(query, src=language, dest='en').text
        else:
            translated_query = query

        # Prepare prompt for Titan
        body = json.dumps({
            "inputText": f"""
You are an expert assistant for OpenText Content Server (OTCS) and its tools. Use the following context to provide a concise, accurate, and conversational answer to the user's query. If the query is unclear or not covered, respond with: 'I need more details to answer this query. Please specify, e.g., "How do I create a folder in OTCS?" or contact OpenText support.' Do not make up information.

Context: {OTCS_CONTEXT}

Query: {translated_query}
""",
            "textGenerationConfig": {
                "maxTokenCount": 500,
                "temperature": 0.5,
                "topP": 0.9
            }
        })

        # Invoke Bedrock model
        response = bedrock_client.invoke_model(
            body=body,
            modelId="amazon.titan-text-express-v1",
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response['body'].read())
        answer = response_body["results"][0]["outputText"].strip()

        # Translate answer back to the requested language
        if language != 'en':
            answer = translator.translate(answer, src='en', dest=language).text

        return answer

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query")
        language = data.get("language", "en")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Validate language
        if language not in LANGUAGE_MAP:
            language = 'en'

        # Get response from Bedrock (cached if identical query)
        answer = generate_bedrock_response(query, language)

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)