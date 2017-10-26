import random

'''
경로를 관리합니다. 변경을 위한 함수가 존재합니다.
'''
class Route():
    def __init__(self, city_list = []):
        self.route = []
        self.total_dist = 0.0
        self.length = len(city_list)
        for i in range(self.length):
            self.route.append(city_list[i])
    
    # 일정 구간을 무작위로 섞습니다.
    def shuffle(self, start = 0, end = -1):
        if end == -1:
            end = self.length
        
        if end > self.length:
            one = self.route[start % self.length :] + self.route[: end % self.length]
            random.shuffle(one)
            two = self.route[end % self.length : start % self.length]
            self.route = one + two
        else:
            head = self.route[: start]
            body = self.route[start : end]
            tail = self.route[end :]
            random.shuffle(body)
            self.route = head + body + tail
    
    # 경로의 값을 새로 계산합니다.
    def dist_update(self):
        self.total_dist = 0.0
        for i in range(self.length):
            next_city = self.route[(i + 1) % self.length]
            self.total_dist += self.route[i].get_dist_to(next_city)
    
    # 새로운 객체를 만들어 값을 복사한 후 반환합니다.
    def copy(self):
        retval = Route()
        for i in range(self.length):
            retval.route.append(self.route[i])
        retval.total_dist = self.total_dist
        retval.length = self.length
        return retval
    
    # 경로 비교를 위해
    def __gt__(self, other):
        return self.total_dist > other.total_dist
    
    # 두 구간을 교체합니다.
    def swap(self, first, second, interval):
        if first > second:
            (first, second) = (second, first)
        
        if (first + interval) < second:
            for i in range(interval):
                self.route[(first + i) % self.length], self.route[(second + i) % self.length] = self.route[(second + i) % self.length], self.route[(first + i) % self.length]
        else:
            self.route = self.route[first :] + self.route[: first]
            (self.route[0 : second - first], self.route[second - first : second - first + interval]) = (self.route[interval : second - first + interval], self.route[0 : interval])
    
    # 특정 구간에서 greedy algorithm을 수행합니다.
    def greedy(self, start, end):
        checker = self.length
        self.route = self.route[start :] + self.route[: start]
        temp_route = self.route[: end - start]
        temp_city = temp_route.pop(random.randrange(len(temp_route)))
        self.route[0] = temp_city

        for i in range(end - start - 1):
            nearest_city = None
            shortest_dist = float("inf")
            for j in range(len(temp_route)):

                temp_dist = self.route[i].get_dist_to(temp_route[j])
                if temp_dist < shortest_dist:
                    nearest_city = temp_route[j]
                    shortest_dist = temp_dist
            
            temp_route.remove(nearest_city)
            self.route[i + 1] = nearest_city
        temp_route = None

    
    
    