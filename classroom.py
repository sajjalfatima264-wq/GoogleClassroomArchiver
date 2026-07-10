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
            break
            
    return announcements

def get_student_submissions(course_id, course_work_id):
    """
    Fetches student submissions for a specific assignment.
    This gets files that the STUDENT uploaded (e.g., manual solutions).
    """
    service = get_classroom_service()
    submissions = []
    page_token = None
    
    while True:
        try:
            results = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id,
                courseWorkId=course_work_id,
                pageToken=page_token
            ).execute()
            
            submissions.extend(results.get('studentSubmissions', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        except Exception as e:
            break
            
    return submissions

def _extract_drive_file(mat):
    """
    Extracts drive file data from a material/attachment dictionary.
    Handles BOTH nesting styles:
      - Teacher materials: driveFile.driveFile.{id, title}
      - Student submissions: driveFile.{id, title}
    """
    # Try double-nested first (teacher style)
    drive_file_data = mat.get('driveFile', {}).get('driveFile', {})
    if drive_file_data and 'id' in drive_file_data:
        return drive_file_data
    
    # Try single-nested (student submission style)
    drive_file_data = mat.get('driveFile', {})
    if drive_file_data and 'id' in drive_file_data:
        return drive_file_data
    
    return None

def extract_submission_attachments(submissions):
    """
    Extracts drive file attachments from student submissions.
    Checks BOTH current attachments AND submission history.
    """
    attachments = []
    
    for submission in submissions:
        # METHOD 1: Check current assignmentSubmission attachments
        assignment_submission = submission.get('assignmentSubmission', {})
        current_materials = assignment_submission.get('attachments', [])
        
        for mat in current_materials:
            drive_file_data = _extract_drive_file(mat)
            if drive_file_data:
                file_id = drive_file_data.get('id')
                if not any(a.get('id') == file_id for a in attachments):
                    attachments.append(drive_file_data)
        
        # METHOD 2: Check submissionHistory
        submission_history = submission.get('submissionHistory', [])
        
        for history_entry in submission_history:
            state_history = history_entry.get('stateHistory', {})
            submitted_attachments = state_history.get('submittedAttachments', [])
            
            for att in submitted_attachments:
                drive_file_data = _extract_drive_file(att)
                if drive_file_data:
                    file_id = drive_file_data.get('id')
                    if not any(a.get('id') == file_id for a in attachments):
                        attachments.append(drive_file_data)
    
    return attachments

if __name__ == '__main__':
    print("Connecting to Google Classroom...")
    try:
        courses = get_all_courses()
        print("Success! Found " + str(len(courses)) + " courses.")
        
        if courses:
            print("\n--- Testing with first course ---")
            test_course = courses[0]
            print(f"Course: {test_course.get('name')}")
            
            work = get_course_work(test_course['id'])
            print(f"Found {len(work)} assignments/materials")
            
            if work:
                submissions = get_student_submissions(test_course['id'], work[0]['id'])
                print(f"Found {len(submissions)} submissions for first assignment")
                
                attachments = extract_submission_attachments(submissions)
                print(f"Found {len(attachments)} attachments in submissions")
                for att in attachments:
                    print(f"  - {att.get('title', 'Untitled')}")
                    
    except Exception as e:
        print("Error: " + str(e))