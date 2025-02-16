# INTERSECTION
	- Attributes:
		Setup Attributes:
			
		Other Attributes:
			list TRAFFIC_LIGHTS: []
	
	- Methods:
		LoadData(Data): # Data Of INTERSECTION SETTINGS
		getTrafficLights(): list 
		addTrafficLight(title, cameraPath):
		remTrafficLight(title)
		TurnON(trafficLight, SECONDS)

# TrafficLight
	- Attributes:
		Setup Attributes:
			String Title: 
			VideoCapture camera: 
			list lines:
			tuple blurSize: (Default: (11, 11))
			int thresh_value: (Default: 15)
			int thresh_maxval: (Defualt: 255)
			int objectArea: (Default: 110)
			 
		Other Attributes:
			bool STATUS: (Default: False)
			int VEHICLE_COUNTER: (Default: 0)
			int AVG_PASS: (Default: 0)
			int AVG_LOAD: (Default: 0)
			
	- Methods:
		getTitle(): Title
		getVideo(): cv2.videoCapture(camera)
		preview(): cv2.imshow(cv2.videoCapture(camera))
		getFrame(): cv2.imread(img)
		getSTATUS(): boolean(Light_Mode)
		getLines(): list # of dimensions
		getAVGPass(): int
		turnON(seconds):
		turnOFF():
		addLine(list):
		getVehicleCount(): int
		updateVehicleCount():
		setAVGPass(AVGPass):
		isEmergencyDetected(): bool
		count_green_time(): int
		count_ranges():
		
## operations.py
	- Methods:
		calculateTime(trafficLight): int


## DetectModel.py
	- Methods:
		detectObjects(frame): list # return List of Objects
		detectVehicles(frame): list # return List of Vehicles (Cars, Truck, Bus, Motorcycles)
		cDetectVehicles(frame): int # return Number of Vehicles
		cPassVehicles(Video video, propertiesOB, lines) # return list of Passes on [ VehiclesIN, VehiclesOUT, seconds ]
		previewCamera(trafficLight): # return live video (preview)
		previewWithplt(frame): # return window to locate dimensions

### Techniques:
	- Start():
		GetVehicleCounter in TrafficLight[i]
		wait for VehicleCounter
		->
		time = calculateTime(trafficLight[i])
		wait time
		->
		Multi-Thread:
			TurnON(TrafficLight[i], time)
			TrafficLight[i].setAVGPass(TrafficLight[i].getAVGPASS())
			for every TrafficLight isEmergencyDetected() (repeat every 1 sec)
			await(time - 5)
			-> 
			GetVehicleCounter in TrafficLight[i + 1]
			wait VehicleCounter
			-> 
			time = calculateTime(trafficLight[i + 1])
			wait time
			Loop Multi-Thread (INFINITELY)




# Logs:
- Add the attributes, methods, classes, Techniques - Saleh 04/02/2021 -- 12:24 AM
- [ Any Edit Here ]