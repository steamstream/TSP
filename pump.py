import random
import route

'''
Pump1()은 임의의 방식으로 route를 생성하는 역할을 합니다.
주기적으로 Pump1은 새로운 route를 만들고 기존의 루트들과 경쟁합니다.
'''
class Pump1():
    def __init__(self, CITY_LIST):
        self.city_list = CITY_LIST
    
    # 전체적으로 greedy algorithm을 이용한 루트 생성
    def make_greedy_route(self, num):
        ret_route_list = []
        for i in range(num):
            temp_route = self.city_list[:]
            temp_ret_route = []
            temp_city = temp_route.pop(random.randrange(len(temp_route)))
            temp_ret_route.append(temp_city)
            for i in range(len(self.city_list) - 1):
                nearest_city = None
                shortest_dist = float("inf")
                for j in range(len(temp_route)):
                    temp_dist = temp_ret_route[-1].temp_get_dist2_to(temp_route[j])
                    if temp_dist < shortest_dist:
                        nearest_city = temp_route[j]
                        shortest_dist = temp_dist
                temp_route.remove(nearest_city)
                temp_ret_route.append(nearest_city)
            ret_route_list.append(route.Route(temp_ret_route))
        
        return ret_route_list
