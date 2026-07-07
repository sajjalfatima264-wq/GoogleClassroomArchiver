🎓 Google Classroom Academic Archiver
A Python application that securely connects to your Google Classroom account using the official Google APIs, downloads your coursework, and organizes everything into a clean, searchable offline archive.

📌 The Problem
Students often lose access to course materials after a semester ends, they graduate, or a teacher deletes an old class. Google Classroom scatters assignments, announcements, and attachments across dozens of courses. Downloading hundreds of files manually takes hours.

💡 The Solution
This script automates the entire process. It communicates directly with the Google Classroom and Drive APIs to securely fetch all your enrolled courses and download every possible attachment (PDFs, Slides, Docs, Sheets, images) into a perfectly organized local folder structure.

Run it once to download everything, and run it again later to only download newly added files.

✨ Features
Secure OAuth 2.0 Login: Never asks for your password. Uses Google's official secure authentication.
Auto-Discovery: Automatically finds all your active, archived, and completed courses.
Smart Downloads: Downloads assignments, materials, questions, and announcements.
File Conversion: Automatically converts Google native files to offline formats:
Google Slides ➡️ .pdf
Google Docs ➡️ .docx
Google Sheets ➡️ .xlsx
Google Drawings ➡️ .png
Incremental Sync: Skips files you already have. Only downloads new content on future runs.
Intelligent Organization: Creates folders by Semester/Section, Course Name, and Work Type.
Duplicate Handling: Automatically renames files if there are naming conflicts.
🛠️ Tech Stack
Language: Python 3
APIs: Google Classroom API, Google Drive API, OAuth 2.0
Libraries: google-api-python-client, google-auth, google-auth-oauthlib, requests
🚀 Setup Guide (Step-by-Step)
If you want to run this script yourself, follow these exact steps.

Step 1: Clone the Repository
git clone https://github.com/YOUR_USERNAME/GoogleClassroomArchiver.gitcd GoogleClassroomArchiver
Step 2: Create a Virtual Environment
It's best practice to install Python packages in an isolated environment.
bash

python -m venv venv

# Activate it on macOS/Linux:
source venv/bin/activate

# Activate it on Windows:
venv\Scripts\activate
Step 3: Install Dependencies
bash

pip install google-api-python-client google-auth google-auth-oauthlib requests
Step 4: Get Google Cloud Credentials (Required)
The script needs permission to read your Classroom and Drive. You must generate a credentials.json file:
Go to the Google Cloud Console.
Create a new project (or select an existing one).
Go to APIs & Services > Library.
Search for and ENABLE the following:
Google Classroom API
Google Drive API
Go to APIs & Services > Credentials.
Click + CREATE CREDENTIALS > OAuth client ID.
Select Desktop app as the Application type, name it "Classroom Archiver", and click Create.
Click the Download JSON icon.
Rename the downloaded file to exactly credentials.json and place it in the root folder of this project.
🏃 How to Use
Once everything is set up, running the archiver is incredibly simple:
bash

# Make sure you are in the project folder and your venv is activated
python main.py
First Run:
Your terminal will print No valid token found. Opening browser for login...
A browser window will open asking you to log into your Google Account.
Google will warn you that the app is "not verified" (because it's a personal script). Click Advanced > Go to Classroom Archiver (unsafe).
Grant permissions to view your Google Classroom and Drive files.
The browser will say "The authentication flow has completed." You can close it.
The terminal will now start printing the courses it is processing.
A token.json file will be created automatically. Never share this file.
Future Runs:
Just run python main.py again. It will silently use your saved token, scan all courses, and only download files added since your last run.

📁 Expected Output
The script creates a folder


*(Note: Folder names are based on the "Section" or "Description Heading" set by your professors in Google Classroom).*

---

## 📊 What Gets Downloaded vs. What Gets Skipped

| File Type in Classroom | Action Taken |
|-----------------------|--------------|
| Google Slides | ✅ Exported and saved as `.pdf` |
| Google Docs | ✅ Exported and saved as `.docx` |
| Google Sheets | ✅ Exported and saved as `.xlsx` |
| Google Drawings | ✅ Exported and saved as `.png` |
| Regular PDFs, DOCX, PPTX, Images, ZIPs | ✅ Downloaded exactly as they are |
| Google Forms | ❌ Skipped (Google does not allow Forms to be exported via API) |
| YouTube Video Links | ❌ Skipped (URL only, not a downloadable file) |
| External Web Links | ❌ Skipped (URL only, not a downloadable file) |

---

## 🔍 Verification Commands

Want to check what the script did? Use these terminal commands inside the project folder:

**Count total downloaded files:**
```bash
find Google_Classroom_Backup -type f | wc -l

Count only PDF files (including converted Google Slides):
bash

find Google_Classroom_Backup -type f -name "*.pdf" | wc -l
View the folder tree structure (macOS/Linux):
bash

ls -R Google_Classroom_Backup | head -50
Open the folder in your graphical file explorer:
bash

# macOS
open Google_Classroom_Backup

# Windows
start Google_Classroom_Backup

# Linux
xdg-open Google_Classroom_Backup

⚠️ Important Notes & Limitations

API Quotas & Speed: The script includes a 0.5 second delay between downloads to prevent hitting Google's API rate limits. If you have 500+ files, the initial run will take several minutes. Let it run!
Google Forms: Unfortunately, Google's API does not provide a way to download Google Forms as files. They are completely skipped.

"Not Verified" App Warning: Because this is a personal script and not an official Google-approved app, Google will show a warning screen during login. This is completely normal for self-hosted OAuth apps. Just click "Advanced" and proceed.

Token Expiry: The script handles token expiry automatically. If your access token expires while scanning, it silently pauses, refreshes the token in the background, and continues.
File Permissions: If a teacher uploaded a file to Classroom but later restricted access to it in Google Drive, the script will safely fail and skip that file without crashing.
