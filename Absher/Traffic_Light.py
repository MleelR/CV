from Settings import MAX_TIME, MIN_TIME
from time import sleep
import operations
import DetectModel
import multiprocessing

class Traffic_Light:
    
    # Setup Attributes
    title = None
    __input = None
    lines = [] 

    __em=""
    em_p=None
    issue_p=None
    __traffic_light_status = False
    __light_mode = False # STATUS
    __green_time = (MAX_TIME + MIN_TIME) / 2 # Time
    __vehiclesCount = 0
    __inside_range = 0
    __vehiclesIn = 0
    __vehiclesOUT = 0
    __avg_pass = 0

    def __init__(self, title, input):
        self.title = title
        self.__input = DetectModel.getVideo(input)
        self.__traffic_light_status=True
        self.em_p = multiprocessing.Process(target=self.isEmergencyDetected)
        #self.issue_p = multiprocessing.Process(target=self.is_issue)
        #self.em_p.start()
        #self.issue_p.start()

    def getTitle(_):
        return _.title

    def getVideo(self):
        return DetectModel.getVideo(self.__input)

    def preview(self):
        DetectModel.previewCamera(self)
    
    def previewWithCoor(self):
        DetectModel.previewWithplt(self.getVideo())

    def getSTATUS(self):
        return self.__light_mode

    def getLines(self):
        return self.lines

    def getAVGPass(self):
        return self.__avg_pass

    def turnON(self, seconds):
        self.__light_mode = True
        print(self.title, f"is turned on for {seconds} sec.\n")
        sleep(seconds)
        self.__light_mode = False
        print(self.title, "is turned off.\n")

    def turnOFF(self):
        self.__light_mode = False
        print(self.title,"is turned off.\n")

    def addLine(self, line = [[0, 0], [0, 0]]):
        if len(self.lines) < 2:
            if line[0][0] > line[1][0]:
                temp = line
                line[0] = temp[1]
                line[1] = temp[0]
            self.lines.append(line)

    def getVehicleCount(self):
        return self.__vehiclesCount

    def updateVehicleCount(self):
        self.__vehiclesCount = DetectModel.cDetectVehicles(self.getVideo())

    def setAVGPass(self, AVGPASS):
        self.__avg_pass = AVGPASS

    def isEmergencyDetected(self):
        while self.__traffic_light_status==True:
            if DetectModel.isEmergencyDetected(self.getVideo()):
                self.em = "emergency"
            else:
                self.em = None
            sleep(10)

    def count_green_time(self): # Calculate Time of Traffic Light
        self.__green_time = operations.calculateTime(self)

    def setRanges(self, vehiclesIN, vehiclesOut):
            self.__vehiclesIn, self.__vehiclesOUT = vehiclesIN, vehiclesOut
            self.__inside_range = vehiclesIN - vehiclesOut

    def count_ranges(self):
        DetectModel.vehiclesPass(self)

    #def is_issue(self): 

    def main(self):
        print(self.title," invoked")
        self.updateVehicleCount()
        print(self.getVehicleCount())
        self.addLine([[0, 600], [480, 600]])
        self.addLine([[170, 350], [300, 350]])
        self.turnON(10)
        self.count_ranges()
        print("vehiclesIn: ", self.__vehiclesIn)
        print("vehiclesOUT: ", self.__vehiclesOUT)
        print("inside_range: ", self.__inside_range)
        print(self.title, " invoked")
        print("avg_pass: ", self.__avg_pass)
        self.count_green_time()
        print("time: ", self.__green_time)
        #if not self.em=="None":
        #return self.em
        #em_p=multiprocessing.Process(target=self.isEmergencyDetected)
