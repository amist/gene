import time
from bisect import bisect_right

class Car(object):
    def __init__(self, lane, position, base_speed):
        self.lane = lane                    # the lane's number. 0 - the rightmost
        self.position = position            # position on the road, lengthwise
        self.base_speed = base_speed        # the car's top speed
        
        self.speed = 0                      # the car's current speed
        self.acceleration = 1               # the car's top acceleration value
        self.margin = 10                    # margin kept from other cars when changing lanes
        self.last_lane_switch = 0           # keeps the position where the last lane switch occurred - for patience
        self.patience = 100                 # distance traveled before searching for other lanes
        
        self.finish_time = -1               # time of finishing the road - set at the end of the road
        self.lane_switches = 0              # counts the number of lane switches
        self.finished = False               # designates whether the car has finished the road
        
        
    def run(self):
        self.position += self.speed
        
    
    def accelerate(self):
        if self.speed < self.base_speed:
            self.speed += self.acceleration
    
    
    def switch_lane(self, lane):
        self.lane = lane
        self.lane_switches += 1
        self.last_lane_switch = self.position
        
    
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
        
        lane_back_car = None if lane_back_car_index == 0 else lane[lane_back_car_index-1]
        lane_front_car = None if lane_front_car_index > len(lane) else lane[lane_front_car_index-1]
        
        if (lane_back_car is None or lane_back_car.position + lane_back_car.speed <= self.position + self.speed - self.margin) and (lane_front_car is None or lane_front_car.position + lane_front_car.speed >= self.position + self.speed + self.margin):
            return True
        return False
            
            
    def is_eligible_to_switch_lane(self):
        return self.position - self.last_lane_switch > self.patience
            
            
    def is_front_car_far(self, front_car):
        if front_car is None or front_car.position > self.position + self.speed:
            return True
        return False
    
        
    def drive(self, front_car, back_car, right_lane, left_lane):
        if self.is_front_car_far(front_car):
            self.run()
            self.accelerate()
            if self.is_lane_available(right_lane) and self.is_eligible_to_switch_lane():
                self.switch_lane(self.lane - 1)
        else:
            if self.is_lane_available(left_lane) and self.is_eligible_to_switch_lane():
                self.switch_lane(self.lane + 1)
                
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
        
    
    def split_cars_to_lanes(self, lanes_number, cars):
        lanes = [[] for _ in range(lanes_number)]
        for i in range(lanes_number):
            lanes[i] = [car for car in cars if car.lane == i]
        return lanes
        
        
    def join_cars_from_lanes(self, lanes):
        cars = [car for lane in lanes for car in lane]
        cars.sort(key=lambda car: car.position, reverse=False)
        return cars
        
        
    def get_right_lane(self, lanes, i):
        lane = None if i == 0 else lanes[i-1]
        return lane
        
    
    def get_left_lane(self, lanes, i):
        lane = None if i == len(lanes)-1 else lanes[i+1]
        return lane
        
        
    def get_front_car(self, lane, i):
        car = None if i == len(lane)-1 else lane[i+1]
        return car
        
        
    def get_back_car(self, lane, i):
        car = None if i == 0 else lane[i-1]
        return car
        
        
    def checkout_car(self, car, lane):
        car.finish_time = self.clock
        car.finished = True
        lane.remove(car)
        self.finished_cars.append(car)
    
        
    def step(self):
        self.clock += 1
        
        self.lanes = self.split_cars_to_lanes(self.lanes_number, self.cars)
            
        for j in range(self.lanes_number):
            right_lane = self.get_right_lane(self.lanes, j)
            left_lane = self.get_left_lane(self.lanes, j)
            
            cur_lane = self.lanes[j]
                
            for i in range(len(cur_lane)):
                cur_car = cur_lane[i]
                front_car = self.get_front_car(cur_lane, i)
                back_car = self.get_back_car(cur_lane, i)
                
                cur_car.drive(front_car, back_car, right_lane, left_lane)
                if cur_car.position > self.length:
                    self.checkout_car(cur_car, cur_lane)
                    
        self.cars = self.join_cars_from_lanes(self.lanes)
                
        
        
        
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
    