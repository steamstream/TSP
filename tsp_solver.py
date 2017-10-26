import sys
from city import City
import city
import random
import argparse

import island
import route

import datetime
import os

import gc
import pump

# -p -f 옵션에 대한 설정입니다.
parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, nargs="?", help="tsp file name", default="att48.tsp")
parser.add_argument("-p", type=int, help="Population")
parser.add_argument("-f", type=int, help="Fitness evaluations")
args = parser.parse_args()

# default 옵션입니다.
tsp_file = "att48.tsp"
if args.filename and (args.filename[-4:] == ".tsp"):
    tsp_file = args.filename
path = "./tsp/" + tsp_file
population = 200
evaluation_limit = 1000
checking_step = 50

def main():
    print("path:", path)
    
    global population
    global evaluation_limit
    pumping_step = evaluation_limit / 10 # 새로운 경로를 만드는 주기입니다.
    swaping_step = evaluation_limit / 20 # 두 pool의 경로들을 교환허눈 주기입니다.
    
    # -p -f 에 대한 설정입니다.
    if args.p:
        print("Population option activated: ", args.p)
        population = args.p
    if args.f:
        print("Fitness evaluations options activated: ", args.f)
        evaluation_limit = args.f
    
    CITY_LIST = [] # 전체적인 점(도시)를 가지고 있을 리스트입니다.
    
    # 두 개의 pool에 각각 할당할 population을 정합니다. 반으로 나눕니다.
    pop_island1 = int(population / 2)
    pop_island2 = population - pop_island1
    
    # .tsp 파일을 읽어 CITY_LIST에 할당합니다.
    with open(path , "r") as fin:
        readlines = fin.readlines()
        for line in readlines[6:-1]:
            temp = line.split()
            CITY_LIST.append(City(int(temp[0]), float(temp[1]), float(temp[2])))
    
    # 두개의 pool을 만들고 초기화 합니다. 하나는 pressure에 low 옵션을 줍니다. 두 pool은 조금 다른 방식으로 자손을 선별합니다.
    pool1 = island.Island(pop_island1)
    pool2 = island.Island(pop_island2, pressure = "low")
    pool1.initialize(CITY_LIST)
    pool2.initialize(CITY_LIST)
    
    # 주기적으로 새 route를 만들어 줄 pump를 만듭니다.
    route_pump = pump.Pump1(CITY_LIST)
    
    evaluation_count = 0 # evaluation 누적 횟수입니다.
    # 각 pool에서의 best result를 비교하기 위해 선언합니다.
    best1 = None 
    best2 = None
    while evaluation_count <= evaluation_limit: # 지정된 횟수만큼 반복합니다.
        # 각 pool에서 mutation을 발생시킵니다.
        pool1.evolution()
        pool2.evolution()
        # 주기적으로 새로운 경로를 만들어 각 pool에 추가합니다.
        if (evaluation_count % pumping_step == 0):
            temp_pumped_route = route_pump.make_greedy_route(2)
            pool1.add_routes(temp_pumped_route)
            pool2.add_routes(temp_pumped_route)
        # 주기적으로 두 pool의 경로를 5개 씩 교환합니다.
        if (evaluation_count % swaping_step == 0):
            exchange1 = pool1.random_sample(5)
            exchange2 = pool2.random_sample(5)
            pool1.add_routes(exchange2)
            pool2.add_routes(exchange1)
        # mutation우로 만들어진 경로와 새로 받은 경로들의 거리를 계산하고 선별합니다.
        pool1.evaluation()
        pool2.evaluation()
        
        evaluation_count += 1
        
        # 진행 상태 확인을 위한 부분입니다.
        if (evaluation_count % checking_step == 0):
            print("count:", evaluation_count)
            best1 = pool1.get_best()
            best2 = pool2.get_best()
            
            if best2 > best1:
                best1 = best2

            print("best.total_dist:", best1.total_dist)

            gc.collect()
            with open("solution" + str(evaluation_count) + ".csv", "w") as fout:
                for i in range(best1.length):
                    fout.write(str(best1.route[i].number) + "\n")
    
    with open("solution.csv", "w") as fout:
        for i in range(best1.length):
            fout.write(str(best1.route[i].number) + "\n")
    

if __name__ == "__main__":
    main()