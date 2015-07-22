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
    
        
    def drive(self, front_car, back_car, right_lane, left_lane):
        if front_car is None or front_car.position > self.position + self.speed:
            #if front_car is None:
            #    print('---> front car run. position %d, speed %d, base speed %d' % (self.position, self.speed, self.base_speed))
            #if front_car is not None:
            #    print('---> run. position %d, speed %d, front car %d' % (self.position, self.speed, front_car.position))
            self.run()
            self.accelerate()
            if right_lane is not None:
                keys = [car.position for car in right_lane]
                lane_back_car_index = bisect_right(keys, self.position)
                lane_front_car_index = lane_back_car_index + 1
                if lane_back_car_index == 0:
                    lane_back_car = None
                else:
                    lane_back_car = right_lane[lane_back_car_index-1]
                    
                if lane_front_car_index > len(right_lane):
                    lane_front_car = None
                else:
                    lane_front_car = right_lane[lane_front_car_index-1]
                    #print('lane front car %d' % lane_front_car.position)
                if (lane_back_car is None or lane_back_car.position + lane_back_car.speed <= self.position + self.speed - self.margin) and (lane_front_car is None or lane_front_car.position + lane_front_car.speed >= self.position + self.speed + self.margin) and (self.position - self.last_lane_switch > self.patience):
                    #self.lane -= 1
                    self.switch_lane(self.lane - 1)
                    self.last_lane_switch = self.position
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
                    
                if (lane_back_car is None or lane_back_car.position + lane_back_car.speed <= self.position + self.speed - self.margin) and (lane_front_car is None or lane_front_car.position + lane_front_car.speed >= self.position + self.speed + self.margin) and (self.position - self.last_lane_switch > self.patience):
                    #self.lane += 1
                    self.switch_lane(self.lane + 1)
                    self.last_lane_switch = self.position
                    self.run()
                    self.accelerate()
                else:
                    self.speed = 0
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
                if self.lanes[j][i].position > self.length:
                    print('finished in position %d in time %d, base speed %d, average speed %.2f' % (self.lanes[j][i].position, self.clock, self.lanes[j][i].base_speed, (self.lanes[j][i].position/float(self.clock))))
                    self.lanes[j][i].finish_time = self.clock
                    self.lanes[j][i].finished = True
                    self.finished_cars.append(self.lanes[j].pop(i))
                
        self.cars = [car for lane in self.lanes for car in lane]
        #cars = []
        #for lane in self.lanes:
        #    cars += lane
        #print(-1, [car.position for car in cars])
        self.cars.sort(key=lambda car: car.position, reverse=False)
        #print(0, [(car.position, car.speed) for car in cars])
        #self.cars = cars
                
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
    