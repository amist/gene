#import time
from bisect import bisect_right

class Car(object):
    def __init__(self, lane, position, base_speed):
        self.lane = lane
        self.position = position
        self.base_speed = base_speed
        
        self.speed = 0
        self.acceleration = 1
        self.margin = 10
        
    
    def run(self):
        self.position += self.speed
        
    
    def accelerate(self):
        if self.speed < self.base_speed:
            self.speed += self.acceleration
    
        
    def drive(self, front_car, back_car, right_lane, left_lane):
        if front_car is None or front_car.position > self.position + self.speed:
            #if front_car is None:
            #    print('---> front car run. position %d, speed %d, base speed %d' % (self.position, self.speed, self.base_speed))
            #if front_car is not None:
            #    print('---> run. position %d, speed %d, front car %d' % (self.position, self.speed, front_car.position))
            self.run()
            self.accelerate()
        else:
            if left_lane is not None:
                keys = [car.position for car in left_lane]
                #print(keys, self.position)
                lane_back_car_index = bisect_right(keys, self.position)
                #print(lane_back_car_index)
                lane_front_car_index = lane_back_car_index + 1
                if lane_back_car_index == 0:
                    lane_back_car = None
                    #print('no lane back car')
                else:
                    #print(lane_back_car_index)
                    #print(left_lane)
                    #print('--')
                    lane_back_car = left_lane[lane_back_car_index-1]
                    #print('lane back car %d' % lane_back_car.position)
                    
                if lane_front_car_index > len(left_lane):
                    lane_front_car = None
                    #print('no lane front car')
                else:
                    lane_front_car = left_lane[lane_front_car_index-1]
                    #print('lane front car %d' % lane_front_car.position)
                    
                if (lane_back_car is None or lane_back_car.position + lane_back_car.speed <= self.position + self.speed - self.margin) and (lane_front_car is None or lane_front_car.position + lane_front_car.speed >= self.position + self.speed + self.margin):
                    self.lane += 1
                else:
                    self.speed = 0
            else:
                self.speed = 0
            
        
class Road(object):
    def __init__(self, lanes_number, length):
        self.lanes_number = lanes_number
        self.length = length
        self.cars = []
        
        self.lanes = [[] for _ in range(self.lanes_number)]
        self.clock = 0
        
    def step(self):
        #print([(car.lane, car.position, car.speed, car.base_speed) for car in self.cars])
        self.clock += 1
        
        self.lanes = [[] for _ in range(self.lanes_number)]
        for i in range(self.lanes_number):
            self.lanes[i] = [car for car in self.cars if car.lane == i]
            
        for j in range(self.lanes_number):
            for i in range(len(self.lanes[j])):
                front_car = None
                back_car = None
                if i != 0:
                    back_car = self.lanes[j][i-1]
                if i != len(self.lanes[j])-1:
                    front_car = self.lanes[j][i+1]
                    
                right_lane = None
                left_lane = None
                if j != 0:
                    right_lane = self.lanes[j-1]
                if j != len(self.lanes)-1:
                    left_lane = self.lanes[j+1]
                self.lanes[j][i].drive(front_car, back_car, right_lane, left_lane)
                
        #self.cars = [car for lane in self.lanes for car in lane]
        cars = []
        for lane in self.lanes:
            cars += lane
        #print(-1, [car.position for car in cars])
        cars.sort(key=lambda car: car.position, reverse=False)
        #print(0, [(car.position, car.speed) for car in cars])
        self.cars = cars
                
        #for i in range(len(self.cars)-1, -1, -1):
        #    front_car = None
        #    back_car = None
        #    if i != 0:
        #        front_car = self.cars[i-1]
        #    if i != len(self.cars)-1:
        #        back_car = self.cars[i+1]
            
            #self.cars[i].drive(front_car, back_car)
                
        
        
        
def run_animation(animate=True):
    if animate:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.ion()
        plt.show()
    
    road = Road(2, 1000)
    road.cars = [Car(0, 5, 4), Car(0, 4, 6), Car(0, 3, 5), Car(0, 2, 5), Car(0, 1, 6), Car(0, 0, 6),
                Car(1, 5, 7), Car(1, 4, 8), Car(1, 3, 9), Car(1, 2, 8), Car(1, 1, 7), Car(1, 0, 9)]
    
    while True:
        #print(road.clock)
        road.step()
        
        if animate:
            x_points = [car.position for car in road.cars]
            y_points = [car.lane for car in road.cars]
            
            plt.clf()
            plt.grid()
            plt.plot(x_points, y_points, 'ro')
            # focus position in animation
            #fcp = road.cars[-1].position
            fcp = road.lanes[0][-1].position
            wd = 150
            plt.axis((fcp - wd, fcp + wd, -0.5, 1.5))
            plt.draw()
            #time.sleep(0.01)
        
if __name__ == '__main__':
    run_animation(animate=True)
    