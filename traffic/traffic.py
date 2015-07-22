import time
from bisect import bisect_right

class Car(object):
    def __init__(self, lane, position, base_speed):
        self.lane = lane
        self.position = position
        self.base_speed = base_speed
        
        self.speed = 0
        self.acceleration = 1
        self.margin = 10
        self.last_lane_switch = 0
        self.patience = 100
        
        self.finish_time = -1
        self.lane_switches = 0
        self.finished = False
        
        
    def run(self):
        self.position += self.speed
        
    
    def accelerate(self):
        if self.speed < self.base_speed:
            self.speed += self.acceleration
    
    
    def switch_lane(self, lane):
        self.lane = lane
        self.lane_switches += 1
        
    
    def get_report(self):
        if self.finished:
            return 'pos: %d, base speed: %d, finish time: %d, average speed: %.2f, lane switches: %d\n' % (self.position, self.base_speed, self.finish_time, self.position/float(self.finish_time), self.lane_switches)
        else:
            return 'lane: %d, pos: %d, speed: %d, base speed: %d\n' % (self.lane, self.position, self.speed, self.base_speed)
    
    def is_lane_available(self, lane):
        if lane is None:
            return False
        
        keys = [car.position for car in lane]
        lane_back_car_index = bisect_right(keys, self.position)
        lane_front_car_index = lane_back_car_index + 1
        if lane_back_car_index == 0:
            lane_back_car = None
        else:
            lane_back_car = lane[lane_back_car_index-1]
            
        if lane_front_car_index > len(lane):
            lane_front_car = None
        else:
            lane_front_car = lane[lane_front_car_index-1]
            
        if (lane_back_car is None or lane_back_car.position + lane_back_car.speed <= self.position + self.speed - self.margin) and (lane_front_car is None or lane_front_car.position + lane_front_car.speed >= self.position + self.speed + self.margin) and (self.position - self.last_lane_switch > self.patience):
            return True
            
            
    def is_front_car_far(self, front_car):
        if front_car is None or front_car.position > self.position + self.speed:
            return True
    
        
    def drive(self, front_car, back_car, right_lane, left_lane):
        if self.is_front_car_far(front_car):
            self.run()
            self.accelerate()
            if self.is_lane_available(right_lane):
                self.switch_lane(self.lane - 1)
                self.last_lane_switch = self.position
        else:
            if self.is_lane_available(left_lane):
                self.switch_lane(self.lane + 1)
                self.last_lane_switch = self.position
                
                self.run()
                self.accelerate()
            else:
                self.speed = 0
            
        
class Road(object):
    def __init__(self, lanes_number, length):
        self.lanes_number = lanes_number
        self.length = length
        self.cars = []
        self.finished_cars = []
        
        self.lanes = [[] for _ in range(self.lanes_number)]
        self.clock = 0
        
    def add_car(self, car):
        self.cars.append(car)
        
    def is_empty(self):
        return len(self.cars) == 0
        
    def get_report(self):
        ret = ''
        ret += '--- Active Cars ---\n'
        if len(self.cars) == 0:
            ret += 'No active cars\n'
        for car in self.cars:
            ret += car.get_report()
            
        ret += '--- Finished Cars ---\n'
        if len(self.finished_cars) == 0:
            ret += 'No finished cars\n'
        for car in self.finished_cars:
            ret += car.get_report()
            
        return ret
        
    def step(self):
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
                if self.lanes[j][i].position > self.length:
                    self.lanes[j][i].finish_time = self.clock
                    self.lanes[j][i].finished = True
                    self.finished_cars.append(self.lanes[j].pop(i))
                
        self.cars = [car for lane in self.lanes for car in lane]
        self.cars.sort(key=lambda car: car.position, reverse=False)
                
        
        
        
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
    
    while not road.is_empty():
        #print(road.clock)
        road.step()
        
        if animate:
            x_points = [car.position for car in road.cars]
            y_points = [car.lane for car in road.cars]
            
            plt.clf()
            plt.grid()
            plt.plot(x_points, y_points, 'ro')
            
            focus_animation = False
            if focus_animation:
                # focus position in animation
                fcp = road.cars[-1].position
                #fcp = road.lanes[0][-1].position
                wd = 350
                plt.axis((fcp - wd, fcp + wd, -0.5, 1.5))
            else:
                plt.axis((0, road.length, -0.5, 1.5))
            plt.draw()
            #time.sleep(0.1)
            
    print(road.get_report())
        
if __name__ == '__main__':
    run_animation(animate=False)
    