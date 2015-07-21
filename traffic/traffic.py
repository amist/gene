import matplotlib.pyplot as plt
import time

class Car(object):
    def __init__(self, lane, position, base_speed):
        self.lane = lane
        self.position = position
        self.base_speed = base_speed
        
        self.speed = 0
        self.acceleration = 1
        
    
    def run(self):
        self.position += self.speed
        
    
    def accelerate(self):
        if self.speed < self.base_speed:
            self.speed += self.acceleration
    
        
    def drive(self, car_front, car_back):
        if car_front is None or car_front.position > self.position + self.speed:
            self.run()
            self.accelerate()
        else:
            self.speed = 0
            
        
        
        
if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    plt.ion()
    plt.show()
    
    cars = [None, Car(0, 5, 5), Car(0, 4, 6), Car(0, 3, 7), Car(0, 2, 8), Car(0, 1, 7), Car(0, 0, 6), None]
    focus_car = 1
    #for r in range(30):
        #print('-- round %d --' % r)
    while True:
        for i in range(len(cars)-1, 0, -1):
            if cars[i] is not None:
                cars[i].drive(cars[i-1], cars[i+1])
            
        
        x_points = [car.position for car in cars if car is not None]
        #print(x_points)
        y_points = [car.lane for car in cars if car is not None]
        
        plt.clf()
        plt.grid()
        plt.plot(x_points, y_points, 'ro')
        #plt.axis((0,2000,-1,1))
        fcp = cars[focus_car].position
        wd = 150
        plt.axis((fcp - wd, fcp + wd, -1, 1))
        plt.draw()
        #time.sleep(0.01)
        
        #print('------------------')
    