import inspect
import sys
import traceback
from traffic import Car
from traffic import Road

success = True


def test_road_acceptance_test():
    road_length = 1000
    lanes_number = 2
    road = Road(lanes_number, road_length)
    road.add_car(Car(0, 5, 4))
    road.add_car(Car(0, 4, 6))
    road.add_car(Car(0, 3, 5))
    road.add_car(Car(0, 2, 5))
    road.add_car(Car(0, 1, 6))
    road.add_car(Car(0, 0, 6))
    road.add_car(Car(1, 5, 7))
    road.add_car(Car(1, 4, 8))
    road.add_car(Car(1, 3, 9))
    road.add_car(Car(1, 2, 8))
    road.add_car(Car(1, 1, 7))
    road.add_car(Car(1, 0, 9))
    
    while not road.is_empty():
        road.step()
        for car in road.cars:
            assert car.position <= road_length
            assert car.finished == False
            assert 0 <= car.lane < lanes_number
        
    assert len(road.cars) == 0
    for car in road.finished_cars:
        assert car.finished == True
        assert car.position > road_length
        assert road.finished_cars[0].position == 1004
        assert road.finished_cars[1].position == 1002
        assert road.finished_cars[2].position == 1006
        assert road.finished_cars[3].position == 1006
        assert road.finished_cars[4].position == 1009
        assert road.finished_cars[5].position == 1002
        assert road.finished_cars[6].position == 1006
        assert road.finished_cars[7].position == 1003
        assert road.finished_cars[8].position == 1002
        assert road.finished_cars[9].position == 1003
        assert road.finished_cars[10].position == 1002
        assert road.finished_cars[11].position == 1003
        assert road.finished_cars[0].lane_switches == 3
        assert road.finished_cars[1].lane_switches == 5
        assert road.finished_cars[2].lane_switches == 1
        assert road.finished_cars[3].lane_switches == 5
        assert road.finished_cars[4].lane_switches == 5
        assert road.finished_cars[5].lane_switches == 1
        assert road.finished_cars[6].lane_switches == 2
        assert road.finished_cars[7].lane_switches == 4
        assert road.finished_cars[8].lane_switches == 4
        assert road.finished_cars[9].lane_switches == 2
        assert road.finished_cars[10].lane_switches == 4
        assert road.finished_cars[11].lane_switches == 0
        
        
def test_car_run():
    car = Car(0, 0, 10)
    car.speed = 5
    car.run()
    assert car.position == 5
    
    
def test_car_accelerate():
    car = Car(0, 0, 10)
    car.speed = 5
    car.acceleration = 1
    car.accelerate()
    assert car.speed == 6
    
    car.acceleration = 5
    car.accelerate()
    assert car.speed == 11
    
    car.accelerate()
    assert car.speed == 11
    
    
def test_car_switch_lane():
    car = Car(0, 0, 10)
    car.lane_switches = 4
    car.switch_lane(8)
    
    assert car.lane_switches == 5
    assert car.lane == 8
    
    
def test_car_is_lane_available():
    lane = [Car(0, 100, 10), Car(0, 130, 10)]
    car = Car(1, 115, 10)
    car.margin = 10
    assert car.is_lane_available(lane) == True
    
    lane = [Car(0, 100, 10), Car(0, 120, 10)]
    assert car.is_lane_available(lane) == False
    
    lane = [Car(0, 106, 10), Car(0, 130, 10)]
    assert car.is_lane_available(lane) == False
    
    
def test_car_is_eligible_to_switch_lane():
    car = Car(0, 200, 10)
    car.speed = 6
    car.patience = 11
    car.switch_lane(1)
    car.run()
    assert car.is_eligible_to_switch_lane() == False
    car.run()
    assert car.is_eligible_to_switch_lane() == True
    car.patience = 12
    assert car.is_eligible_to_switch_lane() == False
    
    
def test_car_is_front_car_far():
    car = Car(0, 200, 10)
    car.speed = 10
    front_car = Car(0, 210, 10)
    assert car.is_front_car_far(front_car) == False
    front_car = Car(0, 211, 10)
    assert car.is_front_car_far(front_car) == True
    
    
def test_car_drive_no_lanes():
    car = Car(0, 200, 10)
    car.speed = 10
    front_car = Car(0, 220, 10)
    car.drive(front_car, None, None, None)
    assert car.position == 210
    car.drive(front_car, None, None, None)
    assert car.position == 210
    
    
def test_car_drive_blocked():
    car = Car(0, 200, 10)
    car.speed = 10
    front_car = Car(0, 201, 10)
    car.drive(front_car, None, None, None)
    assert car.position == 200
    
    
def test_car_drive_and_bypass():
    car = Car(0, 200, 10)
    car.speed = 10
    front_car = Car(0, 205, 10)
    car.drive(front_car, None, None, [])
    assert car.lane == 1
    assert car.position == 210
    
    
def test_car_drive_back_to_right_lane():
    car = Car(1, 200, 10)
    car.speed = 10
    car.last_lane_switch = 190
    car.patience = 25
    car.drive(None, None, [], None)
    assert car.lane == 1
    car.drive(None, None, [], None)
    assert car.lane == 0
    
    
def test_road_add_car():
    road = Road(2, 1000)
    road.add_car(Car(0, 42, 10))
    road.add_car(Car(0, 84, 10))
    assert road.cars[0].position == 42
    assert len(road.cars) == 2
    
    
def test_road_is_empty():
    road = Road(2, 1000)
    assert road.is_empty()
    road.add_car(Car(0, 42, 10))
    assert not road.is_empty()
    
    
def test_road_split_cars_to_lanes():
    road = Road(2, 1000)
    cars = [Car(0, 42, 10), Car(1, 43, 10), Car(0, 44, 10)]
    lanes = road.split_cars_to_lanes(2, cars)
    assert lanes[0][0].position == 42
    assert lanes[0][1].position == 44
    assert lanes[1][0].position == 43
    
    
def test_road_join_cars_from_lanes():
    road = Road(2, 1000)
    lanes = [[Car(0, 42, 10), Car(0, 44, 10)], [Car(1, 43, 10)]]
    cars = road.join_cars_from_lanes(lanes)
    assert cars[0].lane == 0
    assert cars[1].lane == 1
    assert cars[2].lane == 0
    assert cars[0].position == 42
    assert cars[1].position == 43
    assert cars[2].position == 44
    
    
def test_road_get_right_lane():
    road = Road(2, 1000)
    lanes = [[Car(0, 42, 10), Car(0, 44, 10)], [Car(1, 43, 10)]]
    lane = road.get_right_lane(lanes, 1)
    assert lane[0].position == 42
    lane = road.get_right_lane(lanes, 0)
    assert lane is None
    
    
def test_road_get_left_lane():
    road = Road(2, 1000)
    lanes = [[Car(0, 42, 10), Car(0, 44, 10)], [Car(1, 43, 10)]]
    lane = road.get_left_lane(lanes, 0)
    assert lane[0].position == 43
    lane = road.get_left_lane(lanes, 1)
    assert lane is None
    
    
def test_road_get_front_car():
    road = Road(2, 1000)
    lane = [Car(0, 42, 10), Car(0, 43, 10), Car(0, 44, 10)]
    car = road.get_front_car(lane, 1)
    assert car.position == 44
    car = road.get_front_car(lane, 2)
    assert car is None
    
    
def test_road_get_back_car():
    road = Road(2, 1000)
    lane = [Car(0, 42, 10), Car(0, 43, 10), Car(0, 44, 10)]
    car = road.get_back_car(lane, 1)
    assert car.position == 42
    car = road.get_back_car(lane, 0)
    assert car is None
    
    
def test_road_checkout_car():
    road = Road(2, 1000)
    fin_car = Car(0, 1001, 10)
    lane = [Car(0, 42, 10), Car(0, 43, 10), Car(0, 44, 10), fin_car]
    road.checkout_car(fin_car, lane)
    assert fin_car.finished == True
    assert fin_car not in lane
    assert fin_car in road.finished_cars
    
    
def test_road_step():
    pass
    
    
def run_test(f):
    global success
    try:
        f()
    except AssertionError:
        print('[FAIL] %s has failed.' % f.__name__)
        traceback.print_exc()
        success = False
    print('[PASS] %s has finished successfully.' % f.__name__)
    
        
def testall():
    testfunctions = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) 
                     if (inspect.isfunction(obj) and name.startswith('test_'))]
    for f in testfunctions:
        run_test(f)
    
    
if __name__ == '__main__':
    testall()
    if success:
        print('[SUCCESS] All tests have finished successfully.')
    else:
        print('[FAILURE] Some tests have failed.')