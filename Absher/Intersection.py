import multiprocessing
import threading
from Traffic_Light import *

class Intersection:

    __list = [] 
    __process = []
    __IS = True
    __emg = False       

    def getTrafficLights(_):
        return _.__list

    def addTrafficLight(self, title, input):
        self.__list.append(Traffic_Light(title, input))

    def turnON(self, trafficLight, time):
        for e in range(len(self.getTrafficLights())):
            self.getTrafficLights()[e].turnOFF()
        self.IS_status()
        trafficLight.turnON(time)

    def IS_status(self):
        for t in range(len(self.getTrafficLights())):
            print(f"Traffic Light: {self.getTrafficLights()[t].getTitle()}\tstatus: {self.getTrafficLights()[t].getSTATUS()}\n\n")

    def intersection_LC(self):
        while True:
            for t in range(len(self.getTrafficLights())):
                self.turnON(self.getTrafficLights()[t],Traffic_Light.count_green_time(self.getTrafficLights()[t]))
                #while self.emg==True:
                #time.sleep(10)
                
    def sendNotifcation(self, reason = "", trafficLight = None):
        # Connection to control center
        print('{} traffic light has issue {}.'.format(trafficLight.getTitle(), reason))

    def do(self,traffic_Light):
        p= multiprocessing.Process(target=traffic_Light.main)
        p.start()
        print(traffic_Light.getTitle(), "proccess started.\n")

    def oper(self):
        print("----------")
        for n in range(len(self.getTrafficLights())):
            print("for invoke",n)
            self.do(self.getTrafficLights()[n])

    def main(self):
        self.addTrafficLight('One', '1.mp4')
        self.addTrafficLight('Two', '1.mp4')
        self.addTrafficLight('Three', '1.mp4')
        if __name__ == '__main__':
            self.getTrafficLights()[0].main()
            p=multiprocessing.Process(target=self.intersection_LC)
            p.start()
            po = multiprocessing.Process(target=self.oper)
            po.start()

Intersection().main()