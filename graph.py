import json
from datetime import datetime
import matplotlib.pyplot as plt

# Step 2: Read the data from the JSON file
with open('users.json', 'r') as file:
    data = json.load(file)

# Initialize lists to store data
user_names = []
time_periods_lists = []
bmis_lists = []

# Plot the data using Matplotlib
plt.figure(figsize=(10, 6))

# Step 3: Extract data for each user
for person, info in data.items():
    if 'entry' in info:
        user_names.append(person)

        time_periods = []
        bmis = []

        for entry in info['entry']:
            if 'datetime' in entry and 'bmi' in entry:
                timestamp_ms = entry['datetime']  # Assuming datetime is in milliseconds
                datetime_obj = datetime.strptime(entry["datetime"].split(".")[0], "%Y-%m-%d %H:%M:%S")

                time_periods.append(datetime_obj)
                bmis.append(entry['bmi'])

        plt.plot(time_periods, bmis, marker='o', linestyle='-', label=person)
        # time_periods_lists.append(time_periods)
        # bmis_lists.append(bmis)

for name, time_periods, bmis in zip(user_names, time_periods_lists, bmis_lists):
    # Sort the data based on datetime
    # sorted_data = sorted(zip(time_periods, bmis))
    sorted_data = zip(time_periods, bmis)
    print(time_periods)
    sorted_time_periods, sorted_bmis = zip(*sorted_data)

    # Plot the sorted data for each user

plt.xlabel('Time')
plt.ylabel('BMI')
plt.title('BMI Over Time')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend()  # Show legend with user names
plt.tight_layout()
plt.show()