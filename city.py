
'''
각 도시를 의미합니다.
위치 정보를 가지고 있습니다.
'''
class City():
    def __init__(self, number, xval, yval):
        self.number = number
        self.xval = xval
        self.yval = yval
        self.dists = {}
        self.nearest_city = None

    def get(self):
        return self.number, self.xval, self.yval
    
    # 다른 점 까지의 거리의 제곱을 반환합니다. 단순 비교를 위해서 사용합니다.
    def temp_get_dist2_to(self, another_city):
        return cal_dist2(self, another_city)
    
    # 다른 점 까지의 거리를 반환합니다.
    def get_dist_to(self, another_city):
        if self == another_city:
            return 100000000
        if not another_city in self.dists:
            self.dists[another_city] = cal_dist(self, another_city)
        return self.dists[another_city]

    def copy(self):
        return City(self.number, self.xval, self.yval)
        
    def set_nearest(self, nearest_city):
        self.nearest_city = nearest_city
    
    def get_nearest(self):
        return self.nearest_city

# 두 점 사이의 거리를 계산합니다.
def cal_dist(city1, city2):
    return ((city1.xval - city2.xval) ** 2 + (city1.yval - city2.yval) ** 2) ** 0.5

# 단순 비교를 위해서
def cal_dist2(city1, city2):
    return ((city1.xval - city2.xval) ** 2 + (city1.yval - city2.yval) ** 2)
