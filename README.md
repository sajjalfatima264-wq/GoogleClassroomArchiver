# 🎓 Google Classroom Academic Archiver

A Python application that securely connects to your Google Classroom account using the official Google APIs, downloads your coursework and learning materials, and organizes everything into a clean, searchable offline archive.

---

# 📌 The Problem

Students often lose access to their course materials after a semester ends, they graduate, or instructors remove old classes. Google Classroom stores assignments, announcements, and attachments across multiple courses, making it tedious and time-consuming to download everything manually.

---

# 💡 The Solution

This application automates the entire archiving process. Using the official Google Classroom and Google Drive APIs, it securely retrieves all of your enrolled courses and downloads every supported attachment—including PDFs, Google Docs, Google Slides, Google Sheets, images, and other course resources—into a well-structured local directory.

Run it once to create a complete offline backup of your academic history, then run it again anytime to download only newly added content.

---

# ✨ Features

### 🔐 Secure OAuth 2.0 Authentication

Authenticate using Google's official OAuth system without ever entering or storing your Google password.

### 📚 Automatic Course Discovery

Automatically detects all active, archived, and completed Google Classroom courses associated with your account.

### 📥 Intelligent Content Downloading

Downloads available:

* Assignments
* Course materials
* Questions
* Announcements
* Attachments

### 📄 Automatic File Conversion

Google-native files are automatically exported into commonly used offline formats:

| Google File     | Export Format           |
| --------------- | ----------------------- |
| Google Slides   | PDF (.pdf)              |
| Google Docs     | Microsoft Word (.docx)  |
| Google Sheets   | Microsoft Excel (.xlsx) |
| Google Drawings | PNG (.png)              |

### 🔄 Incremental Synchronization

Already downloaded files are skipped automatically. Future runs download only newly added content.

### 🗂️ Smart Organization

Creates a structured directory based on:

* Semester / Section
* Course Name
* Content Type

### 📑 Duplicate Handling

Automatically renames files whenever duplicate filenames are detected.

---

# 🛠️ Tech Stack

**Programming Language**

* Python 3

**Google Services**

* Google Classroom API
* Google Drive API
* OAuth 2.0

**Python Libraries**

* google-api-python-client
* google-auth
* google-auth-oauthlib
* requests

---

# 🚀 Setup Guide

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/GoogleClassroomArchiver.git

cd GoogleClassroomArchiver
```

---

## Step 2 — Create a Virtual Environment

Using a virtual environment keeps project dependencies isolated.

```bash
python -m venv venv
```

### Activate on macOS/Linux

```bash
source venv/bin/activate
```

### Activate on Windows

```bash
venv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```bash
pip install google-api-python-client google-auth google-auth-oauthlib requests
```

---

## Step 4 — Configure Google Cloud Credentials

To allow the application to access your Classroom and Drive content, you'll need a `credentials.json` file.

### Create Google Cloud Credentials

1. Open the Google Cloud Console.
2. Create a new project (or use an existing one).
3. Navigate to **APIs & Services → Library**.
4. Enable:

   * Google Classroom API
   * Google Drive API
5. Navigate to **APIs & Services → Credentials**.
6. Select **Create Credentials → OAuth Client ID**.
7. Choose **Desktop Application**.
8. Name it **Google Classroom Archiver**.
9. Download the generated JSON file.
10. Rename it to:

```
credentials.json
```

11. Place the file in the project's root directory.

---

# ▶️ Running the Application

After completing the setup:

```bash
python main.py
```

---

## First Run

The application will display:

```
No valid token found.
Opening browser for login...
```

A browser window will open requesting Google authentication.

Because this is a personal application, Google may display a **"This app isn't verified"** warning.

Simply select:

```
Advanced
↓

Go to Google Classroom Archiver (unsafe)
```

Grant the requested read-only permissions.

Once authentication is complete:

* the browser can be closed,
* a `token.json` file will be generated automatically,
* downloading begins immediately.

> **Important:** Never share your `token.json` file.

---

## Future Runs

Simply execute:

```bash
python main.py
```

The saved token will be reused automatically, allowing the application to synchronize only newly added course content.

---

# 📁 Output Structure

The application generates a local directory similar to:

```
Google_Classroom_Backup/

    Semester/
        Course Name/
            Assignments/
            Materials/
            Announcements/
```

Folder names are based on the Section or Description Heading configured by your instructors in Google Classroom.

---

# 📊 Supported Downloads

| Classroom Content              | Result                                     |
| ------------------------------ | ------------------------------------------ |
| Google Slides                  | ✅ Exported as PDF                          |
| Google Docs                    | ✅ Exported as DOCX                         |
| Google Sheets                  | ✅ Exported as XLSX                         |
| Google Drawings                | ✅ Exported as PNG                          |
| PDFs, DOCX, PPTX, Images, ZIPs | ✅ Downloaded directly                      |
| Google Forms                   | ❌ Skipped (not exportable through the API) |
| YouTube Links                  | ❌ Skipped                                  |
| External Website Links         | ❌ Skipped                                  |

---

# 🔍 Verification Commands

### Count downloaded files

```bash
find Google_Classroom_Backup -type f | wc -l
```

### Count PDF files

```bash
find Google_Classroom_Backup -type f -name "*.pdf" | wc -l
```

### Display folder structure

```bash
ls -R Google_Classroom_Backup | head -50
```

### Open the backup folder

**macOS**

```bash
open Google_Classroom_Backup
```

**Windows**

```bash
start Google_Classroom_Backup
```

**Linux**

```bash
xdg-open Google_Classroom_Backup
```

---

# ⚠️ Important Notes & Limitations

### API Quotas

A short delay is included between downloads to respect Google's API rate limits. Large archives containing hundreds of files may require several minutes to complete.

---

### Google Forms

Google Forms cannot be exported using the Google Classroom or Drive APIs. They are skipped automatically.

---

### "App Isn't Verified" Warning

Since this is a personal OAuth application rather than a Google-verified product, Google displays a warning during the first authentication. This is expected behavior for self-hosted applications.

---

### Automatic Token Refresh

If your access token expires during execution, the application automatically refreshes it in the background without interrupting the synchronization process.

---

### Restricted Files

If an instructor removes access to an attachment after posting it, the application safely skips the file and continues processing the remaining content without terminating.
