import os
from googleapiclient.discovery import build
from auth import get_credentials

_service_instance = None

def get_classroom_service():
    global _service_instance
    if _service_instance is None:
        creds = get_credentials()
        _service_instance = build('classroom', 'v1', credentials=creds)
    return _service_instance

def get_all_courses():
    service = get_classroom_service()
    courses = []
    page_token = None
    
    while True:
        results = service.courses().list(
            pageToken=page_token, 
            pageSize=100
        ).execute()
        
        courses.extend(results.get('courses', []))
        page_token = results.get('nextPageToken')
        
        if not page_token:
            break
            
    return courses

def get_course_work(course_id):
    service = get_classroom_service()
    coursework_list = []
    page_token = None
    
    while True:
        results = service.courses().courseWork().list(
            courseId=course_id,
            pageSize=100,
            pageToken=page_token
        ).execute()
        
        coursework_list.extend(results.get('courseWork', []))
        page_token = results.get('nextPageToken')
        
        if not page_token:
            break
            
    return coursework_list

def get_course_announcements(course_id):
    """Fetches all announcements for a specific course."""
    service = get_classroom_service()
    announcements = []
    page_token = None
    
    while True:
        try:
            results = service.courses().announcements().list(
                courseId=course_id,
                pageSize=100,
                pageToken=page_token
            ).execute()
            
            announcements.extend(results.get('announcements', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        except Exception as e:
            # Some courses might have announcements disabled, so we silently pass
            break
            
    return announcements

if __name__ == '__main__':
    print("Connecting to Google Classroom...")
    try:
        courses = get_all_courses()
        print("Success! Found " + str(len(courses)) + " courses.")
        
        # CHANGED: Looking for "Applied Machine Learning" instead of "Machine Learning"
        target_course = next((c for c in courses if "Applied Machine Learning" in c.get('name', '')), None)
        
        if target_course:
            print("\n--- Inspecting: " + target_course['name'] + " ---")
            work = get_course_work(target_course['id'])
            
            print("Found " + str(len(work)) + " assignments/materials:\n")
            
            for item in work[:5]:
                title = item.get('title', 'Untitled')
                work_type = item.get('workType', 'UNKNOWN')
                due_date = item.get('dueDate', {})
                materials = item.get('materials', [])
                attachment_count = len(materials)
                
                print("- [" + work_type + "] " + title)
                if due_date and due_date.get('year'):
                    print("  Due: " + str(due_date.get('month')) + "/" + str(due_date.get('day')) + "/" + str(due_date.get('year')))
                else:
                    print("  Due: No due date")
                print("  Attachments: " + str(attachment_count))
                
                for mat in materials:
                    drive_file = mat.get('driveFile', {}).get('driveFile', {})
                    if drive_file:
                        print("    -> Drive File: " + drive_file.get('title', 'Untitled'))
                    elif 'link' in mat:
                        print("    -> Web Link: " + mat['link'].get('url', 'No URL'))
                    elif 'youtubeVideo' in mat:
                        print("    -> YouTube Video")
                print()
        else:
            print("Applied Machine Learning course not found.")
            
    except Exception as e:
        print("Error: " + str(e))