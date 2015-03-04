import cv2
import numpy as np

class Movement_Track:
    def __init__(self,color=(0,0,255),video=0):
        self.cap = cv2.VideoCapture(video)
        self.boundaries = [ ([50,30,30], [145,133,128]) ]
        self.starter = 0
        self.frame_old = []
        self.color = color
        self.prev = 0 # previous y position

        ret, frame = self.cap.read()
        frame = cv2.pyrDown(frame)
        height = frame.shape[0]

        self.maxy = height/2.0 # maximum y value reached
        self.miny = height/2.0 # minimum y value reached
        self.avg = height/2.0 # Initial average value

        self.highy = []
        self.lowy = []

    def Get_Color(self):
        ret, frame = self.cap.read()
        self.color = cv2.mean(frame)[:3]
        return self.color

    def Movement(self):
        y = self.Get_Move()
        if y == 0:
            return False

        if y > self.maxy:
            self.maxy = y
            self.avg = (self.maxy + self.miny)/2.0

        if y < self.miny:
            self.miny = y
            self.avg = (self.maxy + self.miny)/2.0

        if y > self.avg and self.prev < self.avg:
            self.prev = y
            return True
        else:
            self.prev = y
            return False

    def Get_Move(self):
        ret, frame = self.cap.read()

        if self.starter == 0:
            self.frame_old = frame
            self.starter = 1
            return 0

        diff_np = frame - self.frame_old

        for (lower, upper) in self.boundaries:
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            mask = cv2.inRange(diff_np, lower, upper)
            
        mask = cv2.pyrDown(mask)
        white_x = []
        white_y = []
        for y in xrange( mask.shape[0] ):
            for x in xrange( mask.shape[1] ):
                if mask.item(y,x) == 255:
                    white_x.append(x)
                    white_y.append(y)

        avg_y = sum(white_y) / float(len(white_y)+0.1)
        
        self.frame_old = frame
    
        return avg_y

    def destroy(self):
        cap.release()
        cv2.destroyAllWindows()
