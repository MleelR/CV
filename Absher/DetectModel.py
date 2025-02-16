import cv2 as cv
import torch
import matplotlib.pyplot as plt
from lib.Sort.sort import *
from Settings import FPS_VIDEO

detect = torch.hub.load('lib/Yolov5_model', 'yolov5s6', source='local')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
detect.classes = [2, 3, 5, 7]
detect.to(device)

def getVideo(video = None):
    if isinstance(video, cv.VideoCapture):
        return video
    return cv.VideoCapture(video)

def getFrame(video = None):
    ret, frame = getVideo(video).read()
    if ret:
        return frame
    raise Exception('Frame not valid!')

def detectObjects(frame = None):
    try:
        return list(detect(frame).pandas().xyxy[0]['name'])
    except:
        return False
def detectVehicles(frame = None):
    try:
        return list(filter(lambda obj: obj in ['car', 'truck', 'bus', 'motorcycles'], detectObjects(frame)))
    except:
        return False

def cDetectVehicles(video = None):
    try:
        return len(detectVehicles(getFrame(video)))
    except:
        return 0

def isEmergencyDetected(video = None):
    try: 
        if len(list(filter(lambda obj: obj in 'Emergency', detectObjects(getFrame(video))))) > 0: 
            return True
        else: 
            return False
    except:
        return False

def vehiclesPass(trafficLight):
    assert len(trafficLight.getLines()) == 2, "Bottleneck not found!"

    capture = trafficLight.getVideo()
    vehiclesIN = vehiclesOUT = frames = 0
    tracker = Sort()
    ids = {}
    dim1, dim2 = trafficLight.getLines()
    while trafficLight.getSTATUS():
        ret, frame = capture.read()
        if ret:
            predects = detect(frame)
            detectObj = predects.pred[0].numpy()
            track_ids = tracker.update(detectObj).tolist()
            for j in range(len(track_ids)):
                coordinates = track_ids[j]
                xmin, ymin, xmax, ymax = int(coordinates[0]), int(coordinates[1]), int(coordinates[2]), int(coordinates[3])
                name_idx = int(coordinates[4])
                if xmin >= dim1[0][0] and ymin >= dim1[0][1]: # Line 1
                    if ids.get(name_idx) != None and ids.get(name_idx) >= 1:
                        ids.pop(name_idx)
                        vehiclesOUT += 1

                elif xmax > dim2[0][0] and ymax > dim2[0][1] and xmin <= dim2[1][0] and ymin <= dim1[1][1]: # Line 2
                    if ids.get(name_idx) == None:
                        ids.update({name_idx: 1})
                        vehiclesIN += 1
    
            if(frames >= FPS_VIDEO and frames % FPS_VIDEO == 0 and (vehiclesIN - vehiclesOUT) > 0):
                AVGPASS = vehiclesOUT / (frames / FPS_VIDEO)

            frames += 1
            if cv.waitKey(20) & 0xFF == ord('q'):
                break

    trafficLight.setRanges(vehiclesIN, vehiclesOUT)
    trafficLight.setAVGPass(AVGPASS)
    capture.release()

def preiewCamera(trafficLight):
    while True:
        isExist, frame = trafficLight.getVideo().read()
        if isExist:
            for dim1, dim2 in trafficLight.getLines():
                cv.line(frame, (dim1[0], dim1[1]), (dim2[0], dim2[1]), (0, 0, 255), thickness=4)
            cv.imshow('{}'.format(trafficLight.getTitle()), frame)
            if cv.waitKey(20) & 0xFF == ord('E'): # E to end preview
                break

def previewWithplt(video = None):
    frame = getFrame(video)
    plt.style.use('ggplot')
    matplotlib.use( 'tkagg' )
    plt.imshow(frame)
    plt.show()