import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def test_attendance_system():
    # 1. Create a member
    member_data = {
        "studentID": 12345,
        "name": "John Doe",
        "yrLvl": 2,
        "program": "Computer Science"
    }
    member_response = requests.post(f"{BASE_URL}/members/", json=member_data)
    print("Create Member:", member_response.status_code)
    member_id = member_response.json()['id']

    # 2. Create an event
    event_data = {
        "eventID": 1,
        "eventName": "Python Workshop",
        "start_date": "2024-03-20",
        "end_date": "2024-03-22"
    }
    event_response = requests.post(f"{BASE_URL}/events/", json=event_data)
    print("Create Event:", event_response.status_code)
    event_id = event_response.json()['id']

    # 3. Register student for event
    register_response = requests.post(f"{BASE_URL}/events/{event_id}/students/{member_id}/register/")
    print("Register Student:", register_response.status_code)

    # 4. Record attendance for each day
    current_date = datetime.strptime(event_data['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(event_data['end_date'], "%Y-%m-%d")
    day_number = 1

    while current_date <= end_date:
        # Time in
        time_in = current_date.replace(hour=9, minute=0)
        attendance_data = {
            "student": member_id,
            "event": event_id,
            "date": current_date.strftime("%Y-%m-%d"),
            "day_number": day_number,
            "time_in": time_in.isoformat()
        }
        attendance_response = requests.post(f"{BASE_URL}/attendance/", json=attendance_data)
        print(f"Time In Day {day_number}:", attendance_response.status_code)
        attendance_id = attendance_response.json()['id']

        # Time out
        time_out = current_date.replace(hour=17, minute=0)
        attendance_data['time_out'] = time_out.isoformat()
        update_response = requests.put(f"{BASE_URL}/attendance/{attendance_id}/", json=attendance_data)
        print(f"Time Out Day {day_number}:", update_response.status_code)

        current_date += timedelta(days=1)
        day_number += 1

    # 5. Check event attendance report
    report_response = requests.get(f"{BASE_URL}/events/{event_id}/report/")
    print("\nEvent Report:", json.dumps(report_response.json(), indent=2))

    # 6. Check student's attendance
    student_attendance = requests.get(f"{BASE_URL}/events/{event_id}/students/{member_id}/attendance/")
    print("\nStudent Attendance:", json.dumps(student_attendance.json(), indent=2))

    # 7. Check student's complete history
    history_response = requests.get(f"{BASE_URL}/students/{member_id}/attendance-history/")
    print("\nStudent History:", json.dumps(history_response.json(), indent=2))

if __name__ == "__main__":
    test_attendance_system() 