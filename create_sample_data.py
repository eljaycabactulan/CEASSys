import os
import django
import random
import sys
from datetime import datetime, timedelta
from django.utils import timezone

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'attendance'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance.settings')
django.setup()

# Import models from the correct path
from api.models import Events, Member, AttendanceRecord

def create_sample_data():
    # Clear existing data
    AttendanceRecord.objects.all().delete()
    Events.objects.all().delete()
    Member.objects.all().delete()

    # Create sample events
    events = [
        {
            'eventName': 'LCO Days 2024',
            'start_date': '2024-02-01',
            'end_date': '2024-02-03',
        },
        {
            'eventName': 'Environmental Summit 2024',
            'start_date': '2024-03-15',
            'end_date': '2024-03-17',
        },
        {
            'eventName': 'Tree Planting Activity',
            'start_date': '2024-04-22',
            'end_date': '2024-04-22',
        },
        {
            'eventName': 'Seminar on Climate Change',
            'start_date': '2024-05-10',
            'end_date': '2024-05-10',
        }
    ]

    created_events = []
    for event_data in events:
        event = Events.objects.create(**event_data)
        created_events.append(event)
        print(f"Created event: {event.eventName}")

    # Create sample members
    members = [
        {'studentID': '231-02095', 'name': 'John Doe', 'program': 'BSES', 'yrLvl': 2},
        {'studentID': '231-02100', 'name': 'Jane Smith', 'program': 'BSF', 'yrLvl': 3},
        {'studentID': '231-02105', 'name': 'Mike Johnson', 'program': 'BSES', 'yrLvl': 1},
        {'studentID': '231-02110', 'name': 'Sarah Williams', 'program': 'BSF', 'yrLvl': 4},
        {'studentID': '231-02115', 'name': 'David Brown', 'program': 'BSES', 'yrLvl': 2},
        {'studentID': '231-02120', 'name': 'Emily Davis', 'program': 'BSF', 'yrLvl': 3},
        {'studentID': '231-02125', 'name': 'James Wilson', 'program': 'BSES', 'yrLvl': 1},
        {'studentID': '231-02130', 'name': 'Lisa Taylor', 'program': 'BSF', 'yrLvl': 4},
        {'studentID': '231-02135', 'name': 'Robert Anderson', 'program': 'BSES', 'yrLvl': 2},
        {'studentID': '231-02140', 'name': 'Mary Thomas', 'program': 'BSF', 'yrLvl': 3},
    ]

    created_members = []
    for member_data in members:
        member = Member.objects.create(**member_data)
        created_members.append(member)
        print(f"Created member: {member.name}")

    # Create attendance records
    for event in created_events:
        start_date = event.start_date
        end_date = event.end_date
        current_date = start_date
        day_number = 1

        while current_date <= end_date:
            # Randomly select 70-90% of members to be present
            present_members = random.sample(created_members, 
                                         k=random.randint(int(len(created_members) * 0.7), 
                                                        int(len(created_members) * 0.9)))
            
            for member in present_members:
                # Generate random time in between 8 AM and 10 AM
                time_in = datetime.combine(current_date, 
                                         datetime.strptime('08:00', '%H:%M').time()) + \
                         timedelta(minutes=random.randint(0, 120))
                
                # Generate random time out between 4 PM and 6 PM
                time_out = datetime.combine(current_date, 
                                          datetime.strptime('16:00', '%H:%M').time()) + \
                          timedelta(minutes=random.randint(0, 120))

                # Create attendance record
                AttendanceRecord.objects.create(
                    event=event,
                    student=member,
                    date=current_date,
                    day_number=day_number,
                    time_in=time_in,
                    time_out=time_out,
                    is_present=True
                )
                print(f"Created attendance record for {member.name} on {current_date}")

            current_date += timedelta(days=1)
            day_number += 1

    print("\nSample data creation completed!")
    print(f"Created {len(created_events)} events")
    print(f"Created {len(created_members)} members")
    print(f"Created {AttendanceRecord.objects.count()} attendance records")

if __name__ == '__main__':
    create_sample_data() 