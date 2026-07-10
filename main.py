import os
import time
from classroom import (
    get_all_courses, 
    get_course_work, 
    get_course_announcements,
    get_student_submissions,
    extract_submission_attachments
)
from drive import download_file

BACKUP_ROOT_DIR = "Google_Classroom_Backup"

def sanitize_folder_name(name):
    """Remove illegal characters from folder names."""
    if not name:
        return "Unnamed"
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        name = name.replace(char, '')
    name = name.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    name = name.strip('. ')
    if not name:
        return "Unnamed"
    return name

def download_materials(materials, destination_folder, label=""):
    """Downloads drive file attachments from a materials list."""
    downloaded = 0
    skipped = 0
    
    for mat in materials:
        # Use the robust extractor that handles both nesting styles
        from classroom import _extract_drive_file
        drive_file_data = _extract_drive_file(mat)
        
        if drive_file_data:
            file_id = drive_file_data.get('id')
            file_name = drive_file_data.get('title', 'UnnamedFile')
            mime_type = drive_file_data.get('mimeType', '')
            
            if 'application/vnd.google-apps.form' in mime_type:
                skipped += 1
                continue
            
            base_name = os.path.splitext(file_name)[0]
            existing = [f for f in os.listdir(destination_folder) if f.startswith(base_name)] if os.path.exists(destination_folder) else []
            if existing:
                skipped += 1
                continue
            
            success = download_file(file_id, file_name, destination_folder)
            if success:
                downloaded += 1
                print(f"        ✓ Downloaded: {file_name}")
            else:
                skipped += 1
            
            time.sleep(0.5)
    
    return downloaded, skipped

def process_all_courses():
    print("=" * 50)
    print("GOOGLE CLASSROOM ARCHIVER STARTING")
    print("=" * 50)
    print("")
    print("[1/3] Fetching all courses from Google Classroom...")
    courses = get_all_courses()
    print(f"      Found {len(courses)} courses.")
    print("")
    print("[2/3] Scanning courses for materials and submissions...")

    total_downloads = 0
    total_skipped = 0
    total_submissions = 0

    for index, course in enumerate(courses, start=1):
        course_name = course.get('name', 'Unnamed Course')
        course_id = course.get('id')
        section = course.get('section', '') or course.get('descriptionHeading', 'General')

        print("")
        print(f"[{index}/{len(courses)}] Processing: {course_name}")

        safe_course_name = sanitize_folder_name(course_name)
        safe_section = sanitize_folder_name(section)
        course_folder = os.path.join(BACKUP_ROOT_DIR, safe_section, safe_course_name)

        try:
            # ==========================================
            # PART 1: Teacher-posted course work materials
            # ==========================================
            coursework = get_course_work(course_id)
            if coursework:
                for item in coursework:
                    item_title = item.get('title', 'Untitled')
                    work_type = item.get('workType', 'MATERIAL')
                    materials = item.get('materials', [])
                    
                    if not materials:
                        # Even if no teacher materials, still check for student submissions
                        pass
                    else:
                        safe_item_title = sanitize_folder_name(item_title)
                        item_folder = os.path.join(course_folder, work_type, safe_item_title)
                        dl, sk = download_materials(materials, item_folder, "teacher")
                        total_downloads += dl
                        total_skipped += sk

                    # ==========================================
                    # PART 2: Student-submitted attachments
                    # ==========================================
                    submissions = get_student_submissions(course_id, item.get('id'))
                    
                    if submissions:
                        submission_attachments = extract_submission_attachments(submissions)
                        
                        if submission_attachments:
                            total_submissions += len(submission_attachments)
                            safe_item_title = sanitize_folder_name(item_title)
                            submission_folder = os.path.join(course_folder, "My_Submissions", safe_item_title)
                            
                            # Convert to material format for download_materials
                            mat_list = [{'driveFile': att} for att in submission_attachments]
                            dl, sk = download_materials(mat_list, submission_folder, "student")
                            total_downloads += dl
                            total_skipped += sk

            # ==========================================
            # PART 3: Announcements
            # ==========================================
            announcements = get_course_announcements(course_id)
            if announcements:
                for ann in announcements:
                    ann_text = ann.get('text', '')
                    ann_title = ann_text[:80] if ann_text else 'Announcement'
                    materials = ann.get('materials', [])
                    
                    if not materials:
                        continue
                    
                    safe_ann_title = sanitize_folder_name(ann_title)
                    ann_folder = os.path.join(course_folder, "Announcements", safe_ann_title)
                    dl, sk = download_materials(materials, ann_folder, "announcement")
                    total_downloads += dl
                    total_skipped += sk

        except Exception as e:
            print(f"      [!] Error processing course: {e}")

    print("")
    print("=" * 50)
    print("ARCHIVE COMPLETE")
    print("=" * 50)
    print(f"Total NEW Files Downloaded: {total_downloads}")
    print(f"Total Your Uploaded Files: {total_submissions}")
    print(f"Files saved to: {os.path.abspath(BACKUP_ROOT_DIR)}")

if __name__ == '__main__':
    process_all_courses()