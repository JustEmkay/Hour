import datetime
import time

from datetime import datetime


current_datetime = datetime.now()
print("Current Date and Time:", current_datetime) #current date time
timestamp = datetime.timestamp(current_datetime) #timestamp

print("Timestamp:", timestamp, "\nDate time:",current_datetime)
time.sleep(3)

ts_to_date=datetime.fromtimestamp(timestamp)
print("from timestamp:",ts_to_date)