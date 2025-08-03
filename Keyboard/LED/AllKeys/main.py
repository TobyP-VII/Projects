import time
import wmi
import requests
import json
import os

# This script depends on OpenHardwareMonitor (running). It is free and can be configured
# to run at Windows start.
# The SteelSeries gamesense-sdk documents can be found at https://github.com/SteelSeries/gamesense-sdk.


SENSORS_KEY_MAPPING = {
	"GPU Core|Temperature": 
		{
			"min_value": 35,
			"max_value": 90,
			"keymap": {
				"GPUTEMP0": [17, "custom-zone-keys", [79]],
				"GPUTEMP1": [17, "custom-zone-keys", [89]],
				"GPUTEMP2": [16, "custom-zone-keys", [92]],
				"GPUTEMP3": [17, "custom-zone-keys", [95]],
				"GPUTEMP4": [17, "custom-zone-keys", [83]],
				"GPUTEMP5": [16, "custom-zone-keys", [73]]
			},
			"low_colour":"green",
			"high_colour":"red"
		},
	"GPU Core|Load": 
		{
			"min_value": 0,
			"max_value": 100,
			"keymap": {
				"GPULOAD0": [17, "custom-zone-keys", [98]],
				"GPULOAD1": [17, "custom-zone-keys", [90]],
				"GPULOAD2": [16, "custom-zone-keys", [93]],
				"GPULOAD3": [17, "custom-zone-keys", [96]],
				"GPULOAD4": [17, "custom-zone-keys", [84]],
				"GPULOAD5": [16, "custom-zone-keys", [76]]
			},
			"low_colour":"green",
			"high_colour":"red"
		},
	"CPU Package|Temperature": 
		{
			"min_value": 35,
			"max_value": 95,
			"keymap": {
				"CPUTEMP0": [17, "custom-zone-keys", [99]],
				"CPUTEMP1": [17, "custom-zone-keys", [91]],
				"CPUTEMP2": [16, "custom-zone-keys", [94]],
				"CPUTEMP3": [17, "custom-zone-keys", [97]],
				"CPUTEMP4": [17, "custom-zone-keys", [85]],
				"CPUTEMP5": [16, "custom-zone-keys", [75]]
			},
			"low_colour":"blue",
			"high_colour":"red"
		},
	"CPU Total|Load": 
		{
			"min_value": 0,
			"max_value": 100,
			"keymap": {
				"CPULOAD0": [33, "custom-zone-keys", [88]],
				"CPULOAD1": [34, "custom-zone-keys", [87]],
				"CPULOAD2": [16, "custom-zone-keys", [86]],
				"CPULOAD3": [17, "custom-zone-keys", [78]],
			},
			"low_colour":"blue",
			"high_colour":"red"
		},
	}

# define sleep duration between sensor checks
sleepy_time = 3
# always posting JSON
headers = {"Content-Type":"application/json"}
# JSON colour configurations
guage_colour = {
	"red": {"red":255,"green":0,"blue":0},
	"green": {"red":0,"green":255,"blue":0},
	"blue": {"red":0,"green":0,"blue":255},
	"white": {"red":255,"green":255,"blue":255}
}

# Need to discover address:port from %ProgramData%\SteelSeries\SteelSeries Engine 3\coreProps.json
programdata = os.getenv('PROGRAMDATA')
with open(programdata + '\SteelSeries\SteelSeries Engine 3\coreProps.json') as SSEcoreProps:
	coreProps = json.load(SSEcoreProps)

# De-register the game to clear out all events
json_to_post = {"game": "HWMONITOR"}
r = requests.post('http://' + coreProps['address'] + '/remove_game', json=json_to_post, headers=headers)

# Register the app with SteelSeries
json_to_post = {"game": "HWMONITOR","game_display_name": "RGB HW Monitor","developer": "Kyle J Tuck"}
r = requests.post('http://' + coreProps['address'] + '/game_metadata', json=json_to_post, headers=headers)

# Register the event handlers
for sensor in SENSORS_KEY_MAPPING:
	for event_name in SENSORS_KEY_MAPPING[sensor]['keymap']:
		json_to_post = {"game": "HWMONITOR",
						"event":event_name,
						"handlers":[ {"device-type":"rgb-per-key-zones",
							SENSORS_KEY_MAPPING[sensor]['keymap'][event_name][1]:SENSORS_KEY_MAPPING[sensor]['keymap'][event_name][2],
							"mode":"color",
							"color":{
								"gradient":{
									"zero": guage_colour[SENSORS_KEY_MAPPING[sensor]["low_colour"]],
									"hundred": guage_colour[SENSORS_KEY_MAPPING[sensor]["high_colour"]]
								}
							}
						}]
						}
		r = requests.post('http://' + coreProps['address'] + '/bind_game_event', json=json_to_post, headers=headers)
		# reset the key colour
		json_to_post = {"game":"HWMONITOR",
						"event":event_name,
						"data": {"value":100}
						}
		r = requests.post('http://' + coreProps['address'] + '/bind_game_event', json=json_to_post, headers=headers)
		json_to_post = {"game":"HWMONITOR",
						"event":event_name,
						"data": {"value":0}
						}
		r = requests.post('http://' + coreProps['address'] + '/bind_game_event', json=json_to_post, headers=headers)


# read the sensors
while True:
	w = wmi.WMI(namespace="root\OpenHardwareMonitor")
	temperature_data = w.Sensor()
	for sensor in temperature_data:
		full_sensor_name = sensor.Name + '|' + sensor.SensorType
		if full_sensor_name in SENSORS_KEY_MAPPING.keys():
			sensor_value = float(sensor.Value) - float(SENSORS_KEY_MAPPING[full_sensor_name]['min_value'])
			min_max_delta = float(SENSORS_KEY_MAPPING[full_sensor_name]['max_value'] - SENSORS_KEY_MAPPING[full_sensor_name]['min_value'])
			if sensor_value >= 0.0:
				sensor_guage = int(sensor_value / min_max_delta * 100.0)
#				print(full_sensor_name + ' ' + str(sensor_guage))
				for event_name in SENSORS_KEY_MAPPING[full_sensor_name]['keymap']:
					if sensor_guage <= 0:
						key_value = 0
					elif SENSORS_KEY_MAPPING[full_sensor_name]['keymap'][event_name][0] > sensor_guage:
						key_value = int(sensor_guage/SENSORS_KEY_MAPPING[full_sensor_name]['keymap'][event_name][0]*100)
					else:
						key_value = 100
					json_to_post = {"game":"HWMONITOR",
									"event":event_name,
									"data": {"value":key_value}
									}
					sensor_guage -= SENSORS_KEY_MAPPING[full_sensor_name]['keymap'][event_name][0]
					r = requests.post('http://' + coreProps['address'] + '/game_event', json=json_to_post, headers=headers)
	time.sleep(sleepy_time)