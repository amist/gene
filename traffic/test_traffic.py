from traffic import Car
from traffic import Road

if __name__ == '__main__':
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