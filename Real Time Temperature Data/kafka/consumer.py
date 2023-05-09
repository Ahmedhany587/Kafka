from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import json

# Set up Kafka consumer
consumer = KafkaConsumer(
    "KafkaProject",
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id="consumer-group-a"
)

# Set up plot
fig, axs = plt.subplots(1, 3, figsize=(18, 6))
axs[0].set_title('Humidity Data')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Humidity (%)')
axs[0].set_ylim([0, 100])
line_humidity, = axs[0].plot([], [], lw=2)

axs[1].set_title('Temperature Data')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Temperature (C)')
line_temp, = axs[1].plot([], [], lw=2)

# Set up map
map_ax = axs[2]
map_ax.set_title('Location Data')
map_ax.set_xlabel('Longitude')
map_ax.set_ylabel('Latitude')
map_ax.set_xlim([-180, 180])
map_ax.set_ylim([-90, 90])
m = Basemap(projection='cyl', ax=map_ax)
m.drawcoastlines()

# Initialize data lists
x_data = []
y_humidity_data = []
y_temp_data = []
lons = []
lats = []

# Update plot function
def update_plot(i):
    global x_data, y_humidity_data, y_temp_data, lons, lats
    for msg in consumer:
        data = json.loads(msg.value)
        humidity = data.get('main', {}).get('humidity', None)
        temp = data.get('main', {}).get('temp', None)
        lon = data.get('coord', {}).get('lon', None)
        lat = data.get('coord', {}).get('lat', None)
        if humidity is not None and temp is not None and lon is not None and lat is not None:
            x_data.append(i)
            y_humidity_data.append(humidity)
            y_temp_data.append(temp)
            lons.append(lon)
            lats.append(lat)
            line_humidity.set_data(x_data, y_humidity_data)
            line_temp.set_data(x_data, y_temp_data)
            axs[0].relim()
            axs[0].autoscale_view(True,True,True)
            axs[1].relim()
            axs[1].autoscale_view(True,True,True)
            plt.draw()
            plt.pause(0.001)
            break
    if len(lons) > 0 and len(lats) > 0:
        x, y = m(lons, lats)
        map_ax.clear()
        m.drawcoastlines()
        m.plot(x, y, 'bo', markersize=5)

# Update plot loop
for i in range(100):
    update_plot(i)
