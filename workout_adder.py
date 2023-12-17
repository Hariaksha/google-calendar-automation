import datetime
import pytz 
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def three_or_six():
  inp = input("Rest days are important to remain consistent and allow your muscles to grow! With this in mind, would you like to workout 3 (MWF) or 6 (all days except Saturday) times a week?")
  if inp == "3":
    print("You chose to work out 3 days per week.")
    return 3
  elif inp == "6":
    print("You chose to work out 6 days per week.")
    return 6
  else:
    print("You entered an invalid input. You will be redirected to the question.")
    return three_or_six()  

def add_workouts(muscle, group):
  cur_len = len(group)
  while len(group) is cur_len:
    for exercise in muscle:
      add = input(f"Would you like {exercise} to be included in your workout? Enter 'Y' or 'y' for yes and any other character(s) for no.")
      if add.upper() == 'Y':
        group.append(exercise)
    if len(group) is cur_len:
      print("You have not included any exercises. You will be reprompted now.")

def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          'credentials.json', SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    print("Welcome to the Workout Adder Program! Through this program, you will create your own customized push-pull-leg (PPL) workout routine.")
    days_in_week = three_or_six()

    # Create push day routine
    triceps = ["Skull Crushers", "Standing Tricep Push Down",]
    shoulders = ["Dumbbell Lateral Raises", "Shoulder Press"]
    pecs = ["Standing Cable Crossovers", "Seated Machine Fly"]
    chest = ["Incline DB Bench Press", "Flat DB Bench Press"]
    push = []
    print("To begin, you will now choose exercises for push day, which typically targets chest, shoulders, and triceps.")
    print("You will first choose tricep exercises.You are required to include at least one tricep exercise.")
    add_workouts(triceps, push)
    print("You will now choose shoulder exercises.You are required to include at least one shoulder exercise.")
    add_workouts(shoulders, push)
    print("You will now choose pecs exercises.You are required to include at least one pecs exercise.")
    add_workouts(pecs, push)
    print("You will now choose chest exercises.You are required to include at least one chest exercise.")
    add_workouts(chest, push)
    
    # Create pull day routine
    vertical_rows = ["Pull-Ups", "Lat Pulldowns", "Shrugs DB"]
    horizontal_rows = ["Iso-Lateral Low Row", "Cable Rows",]
    biceps = ["Bicep Curls", "Reverse Bicep Curls"]
    rear_delts = ["Seated Machine Reverse Fly", "Standing Cable Reverse Fly"]
    pull = []
    print("You will now choose exercises for pull day, which typically targets back and biceps.")
    print("First, choose at least one vertical row exercise.")
    add_workouts(vertical_rows, pull)
    print("Next, choose at least one horizontal row exercise.")
    add_workouts(horizontal_rows, pull)
    print("Next, choose at least one biceps exercise.")
    add_workouts(biceps, pull)
    print("Lastly, choose at least one rear delt exercise.")
    add_workouts(rear_delts, pull)

    # Create leg day routine
    squats = ["Barbell Back Squat", "Pendulum Squat"]
    hamstrings = ["Leg Curl (lying)", "Hamstring Curl"]
    calves = ["Standing Calf Raise", "Seated Calf Raise"]
    hips = ["Hip Abduction", "Barbell Hip Thrusts"]
    quads = ["Leg Press", "Seated Leg Extensions"]
    legs = []
    print("You will now choose exercises for leg day.")
    print("First, choose at least one squatting exercise.")
    add_workouts(squats, legs)
    print("Next, choose at least one hamstring exercise.")
    add_workouts(hamstrings, legs)
    print("Next, choose at least one calf exercise.")
    add_workouts(calves, legs)
    print("Lastly, choose at least one hip exercise.")
    add_workouts(hips, legs)
    print("Lastly, choose at least one quadriceps exercise.")
    add_workouts(quads, legs)

    # Call the Calendar API
    timezone = pytz.timezone("America/Indiana/Knox") # This indicates Central Standard Time. Full list of timezones available at https://mljar.com/blog/list-pytz-timezones/.
    now = datetime.datetime.now(timezone).isoformat()

    #Create a new calendar
    new_calendar = {
        'summary': 'PPL Exercise Calendar',
        'timeZone': 'America/Indiana/Knox'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    print(f"Created calendar: {created_calendar['id']}")

    push_description = ""
    pull_description = ""
    legs_description = ""
    for exercise in push:
      push_description += (exercise + "\n")
    for exercise in pull:
      pull_description += (exercise + "\n")
    for exercise in legs:
      legs_description += (exercise + "\n")

    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday()) % 7
    next_sunday = today + datetime.timedelta(days=days_until_sunday)
    next_monday = next_sunday + datetime.timedelta(days=1)
    next_tuesday = next_sunday + datetime.timedelta(days=2)

    sunday_start_time = datetime.datetime(next_sunday.year, next_sunday.month, next_sunday.day, 6, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
    sunday_end_time = datetime.datetime(next_sunday.year, next_sunday.month, next_sunday.day, 7, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
    monday_start_time = datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 6, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
    monday_end_time = datetime.datetime(next_monday.year, next_monday.month, next_monday.day, 7, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
    tuesday_start_time = datetime.datetime(next_tuesday.year, next_tuesday.month, next_tuesday.day, 6, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))
    tuesday_end_time = datetime.datetime(next_tuesday.year, next_tuesday.month, next_tuesday.day, 7, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=0)))

    push_event = {
      'summary': 'Push Day',
      'description': push_description,
      'recurrence': ['RRULE:FREQ=WEEKLY;BYDAY=SU, WE'],
      'start': {
        'dateTime': sunday_start_time.isoformat(),
        'timeZone': timezone
      },
      'end': {
        'dateTime': sunday_end_time.isoformat(),
        'timeZone': timezone
      }
    }

    pull_event = {
      'summary': 'Pull Day',
      'description': pull_description,
      'recurrence': ['RRULE:FREQ=WEEKLY;BYDAY=MO, TH'],
      'start': {
        'dateTime': monday_start_time.isoformat(),
        'timeZone': timezone
      },
      'end': {
        'dateTime': monday_end_time.isoformat(),
        'timeZone': timezone
      }
    }

    legs_event = {
      'summary': 'Legs Day',
      'description': legs_description,
      'recurrence': ['RRULE:FREQ=WEEKLY;BYDAY=TU, FR'],
      'start': {
        'dateTime': tuesday_start_time.isoformat(),
        'timeZone': timezone
      },
      'end': {
        'dateTime': tuesday_end_time.isoformat(),
        'timeZone': timezone
      }
    }

    recurring_push_event = service.events().insert(calendarId='PPL Exercise Calendar', body=push_event).execute()
    recurring_pull_event = service.events().insert(calendarId='PPL Exercise Calendar', body=pull_event).execute()
    recurring_legs_event = service.events().insert(calendarId='PPL Exercise Calendar', body=legs_event).execute()

  except HttpError as error:
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()
