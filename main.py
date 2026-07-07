import os
import time
from classroom import get_all_courses, get_course_work, get_course_announcements
from drive import download_file

BACKUP_ROOT_DIR = "Google_Classroom_Backup"

def sanitize_folder_name(name):
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        name = name.replace(char, '')
    return name.strip()

def download_materials(materials, destination_folder):
    downloaded = 0
    for mat in materials:
        drive_file_data = mat.get('driveFile', {}).get('driveFile', {})
        if drive_file_data:
            file_id = drive_file_data.get('id')
            file_name = drive_file_data.get('title', 'UnnamedFile')
            mime_type = drive_file_data.get('mimeType', '')
            if 'application/vnd.google-apps.form' in mime_type:
                continue
            if not os.path.exists(os.path.join(destination_folder, file_name)):
                success = download_file(file_id, file_name, destination_folder)
                if success:
                    downloaded += 1
                time.sleep(0.5)
    return downloaded

def process_all_courses():
    print("=" * 50)
    print("GOOGLE CLASSROOM ARCHIVER STARTING")
    print("=" * 50)
    print("")
    print("[1/3] Fetching all courses from Google Classroom...")
    courses = get_all_courses()
    print("      Found " + str(len(courses)) + " courses.")
    print("")
    print("[2/3] Scanning courses, assignments, AND announcements...")

    total_downloads = 0

    for index, course in enumerate(courses, start=1):
        course_name = course.get('name', 'Unnamed Course')
        course_id = course.get('id')
        section = course.get('section', '') or course.get('descriptionHeading', 'General')

        print("")
        print("[" + str(index) + "/" + str(len(courses)) + "] Processing: " + course_name)

        safe_course_name = sanitize_folder_name(course_name)
        safe_section = sanitize_folder_name(section)
        course_folder = os.path.join(BACKUP_ROOT_DIR, safe_section, safe_course_name)

        try:
            coursework = get_course_work(course_id)
            if coursework:
                for item in coursework:
                    item_title = item.get('title', 'Untitled')
                    work_type = item.get('workType', 'MATERIAL')
                    materials = item.get('materials', [])
                    if not materials:
                        continue
                    safe_item_title = sanitize_folder_name(item_title)
                    item_folder = os.path.join(course_folder, work_type, safe_item_title)
                    total_downloads += download_materials(materials, item_folder)

            announcements = get_course_announcements(course_id)
            if announcements:
                for ann in announcements:
                    ann_title = ann.get('text', 'Untitled Announcement')[:50]
                    materials = ann.get('materials', [])
                    if not materials:
                        continue
                    safe_ann_title = sanitize_folder_name(ann_title)
                    ann_folder = os.path.join(course_folder, "Announcements", safe_ann_title)
                    total_downloads += download_materials(materials, ann_folder)

        except Exception as e:
            print("      [!] Error processing course: " + str(e))

    print("")
    print("=" * 50)
    print("ARCHIVE COMPLETE")
    print("=" * 50)
    print("Total NEW Files Downloaded: " + str(total_downloads))
    print("Files saved to: " + os.path.abspath(BACKUP_ROOT_DIR))

if __name__ == '__main__':
    process_all_courses()