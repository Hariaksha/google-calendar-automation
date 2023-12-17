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
  inp = input("Rest days are important to remain consistent and allow your muscles to grow! With this in mind, would you like to workout 3 or 6 times a week?")
  if inp == "3":
    print("You chose to work out 3 days per week.")
    return 3
  elif inp == "6":
    print("You chose to work out 6 days per week.")
    return 6
  else:
    print("You entered an invalid input. You will be redirected to the question.")
    return three_or_six()  

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
    minutes = input("First, how many minutes should each workout last? ")
    days_in_week = three_or_six()

    # Create push day routine
    triceps = ["Skull Crushers", 
               "Standing Tricep Push Down",]
    shoulders = ["Dumbbell Lateral Raises", 
                 "Shoulder Press"]
    pecs = ["Standing Cable Crossovers",
            "Seated Machine Fly"]
    chest = ["Incline DB Bench Press", 
            "Flat DB Bench Press"]
    print("You will first choose exercises for your triceps.")
    while triceps:
      add = input(f"Would you like {triceps[0]} to be included in your workout")
    push = []

    

    vertical_rows = ["Pull-Ups", 
                     "Lat Pulldowns",
                     "Shrugs DB"]
    horizontal_rows = ["Iso-Lateral Low Row",
                       "Cable Rows",]
    biceps = ["DB Bicep Curls"]
    rear_delts = ["Seated Machine Reverse Fly"]
    pull = []
    legs = ["Barbell Back Squat",
            "Leg Press",
            "Leg Curl (lying)",
            "Standing Calf Raise",
            "Hip Abduction",
            "Barbell Hip Thrusts",
            "Seated Leg Extensions"]
    
    # Call the Calendar API
    timezone = pytz.timezone("America/Indiana/Knox") # This indicates Central Standard Time. Full list of timezones available at https://mljar.com/blog/list-pytz-timezones/.
    now = datetime.datetime.now(timezone).isoformat()
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
