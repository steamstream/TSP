import route
import random

'''
유전자 풀입니다.
여기서 점들의 sequence를 변형시키고 선별합니다.
'''
class Island():
    def __init__(self, population, elite_rate = 0.1, **kwargs):
        self.population = population
        self.elite_num = int(population * elite_rate) # 
        self.route_list = []
        self.best = None
        self.children = [] # mutation 실행시 임시적으로 결과를 담을 리스트입니다.
        self.immigrants = [] # 외부에서 유전자가 들어올 때 임시적으로 이를 담을 리스트입니다.
        self.route_length  = -1
        self.MUTATION_RATE = 0.4 # 각 경로가 mutation을 수행할 확률입니다.
        self.interval_rate = 0.2 # mutation 식 얼마나 변하는지에 대한 변수입니다.
        self.PRESSURE = "high" # default pressure는 high입니다. 이 경우 무조건 좋은 결과를 내는 것을 population 만큼 선별합니다.
        if kwargs:
            if kwargs["pressure"] == "low":
                self.MUTATION_RATE = 0.5
                self.interval_rate = 0.3
    
    # 전체 리스르를 받아 population 만크의 유전자를 만들고 경로를 무작위로 섞습니다.
    def initialize(self, city_list):
        self.route_length = len(city_list)
        for i in range(self.population):
            self.route_list.append(route.Route(city_list))
            self.route_list[i].shuffle()
    
    # mutation을 수행합니다.
    def evolution(self):
        self.mutation(self.MUTATION_RATE) # mutation은 정해진 확률로 발생합니다.

    # 세대에 추가된 모든 유전자를 모아 값을 비교하고 선별합니다.
    def evaluation(self):
        pool = self.route_list + self.children + self.immigrants # 기존 부모 유전자(route_list), mutation으로 만든 자식 유전자(children), 외부에서 들어온 유전자(immigrants)를 모읍니다.
        for i in range(len(pool)): # 각 경로들의 거리를 구합니다.
            pool[i].dist_update()
        pool.sort() # 짧은 순서로 정렬합니다.
        
        if (self.best == None) or (self.best > pool[0]):
            self.best = None
            self.best = pool[0].copy()
        
        # low pressure의 경우에는 Stochastic Universal Sampling으로 선별합니다.
        if self.PRESSURE == "low":
            self.route_list = pool[:self.elite_num]
            self.sampling(pool[self.elite_num:], self.population - self.elite_num)
        # high pressure의 경우는 좋은 결과만 잘라서 다음 세대로 넘깁니다.
        elif self.PRESSURE == "high":
            self.route_list = pool[:self.population]
        
        for i in range(len(pool[self.population:])):
            pool[self.population + i] = None

    # Stochastic Universal Sampling
    def sampling(self, pool, population):
        sum = 0.0
        portions = []
        for i in range(len(pool)):
            sum += pool[i].total_dist
        
        for i in range(len(pool)):
            portions.append(sum / pool[i].total_dist)
        
        sum = 0.0
        for i in range(len(pool)):
            sum += portions[i]
        
        for i in range(len(pool)):
            portions[i] = portions[i] / sum
        
        sum = 0.0
        for i in range(len(portions)):
            portions[i] = sum + portions[i]
            sum = portions[i]
        if sum > 1.0 or sum < 0.9999:
            print("Err")
        
        rand = random.random() / population
        for i in range(len(population)):
            if rand < portions[0]:
                    self.route_list.append(pool[0])
            else:
                for j in range(1, len(portions)):
                    if portions[j - 1] < rand and rand < portions[j]:
                        self.route_list.append(pool[j])
            rand += 1 / population
    
    # 외부에서 유전자를 받아 self.immigrants에 임시로 저장합니다.
    def add_routes(self, routes_list):
        self.immigrants = []
        
        for i in range(len(routes_list)):
            if len(routes_list) != self.route_length:
                print("routes_list:", len(routes_list[0].route), ", self.route_list:", self.route_length)
            immigrant = routes_list[i].copy()
            self.immigrants.append(immigrant)
    
    # 임의로 num개의 유전자를 선택해 반환합니다.
    def random_sample(self, num):
        return random.sample(self.route_list, num)
    
    # mutation을 수행하여 자식을 만듭니다.
    def mutation(self, probability):
        self.children = []
        for i in range(self.population):
            rand = random.random()
            if rand < probability: # 
                child = self.route_list[i].copy()
                dice = int(rand * 100) % 4
                start = int(self.route_length * rand)
                rand2 = (rand * 100) - int(rand * 100)
                interval = int(self.route_length * self.interval_rate * rand2) if self.route_length > 50 else 5 # 얼마나 많이 바꾸느냐를 결정합니다.
                if dice == 0: # 특정 구간을 무작위로 섞습니다.
                    child.shuffle(start, start + interval)
                elif dice == 1: # 특정 구간에서 greedy algorithm을 수행합니다.
                    if interval > 500:
                        interval = 500
                    if interval < 1:
                        interval = 1
                    child.greedy(start, start + interval)
                elif dice == 2: # 특정 두 구간을 교체합니다.
                    rand3 = (rand2 * 100) - int(rand2 * 100)
                    second = int(self.route_length * rand3)
                    child.swap(start, second, interval)
                elif dice == 3: # 두 도시 순서를 교체해서 경로를 바꿉니다.
                    child.swap(start, start + interval, 1)
                self.children.append(child)
    
    # 저장된 최고 결과를 반환합니다.
    def get_best(self):
        return self.best
    