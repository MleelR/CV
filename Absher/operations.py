import Traffic_Light
from Settings import MAX_TIME, MIN_TIME, OFFSET

def calculateTime(trafficLight):
    time = 0
    try:
        if isinstance(trafficLight, Traffic_Light.Traffic_Light):
            time = (trafficLight.getVehicleCount() / trafficLight.getAVGPass()) + 5
            if time < MIN_TIME:
                time = MIN_TIME
            elif time > MAX_TIME:
                time = MAX_TIME
    except:
        time = (MIN_TIME + MAX_TIME) / 2
    return int(time * OFFSET)

