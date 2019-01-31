
from random import randint

class Requests :
    def __init__(self,number_of_cars=10,min_req_size=5,max_req_size=10,number_of_files=25):
        self.cars_req = []
        self.number_of_cars= number_of_cars
        self.min_req_size = min_req_size
        self.max_req_size = max_req_size
        self.number_of_files = number_of_files

        for i in range(1,self.number_of_cars +1):
            req = []
            number_of_reqs = randint(self.min_req_size, self.max_req_size)

            for j in range(0,number_of_reqs):
                req.append(self.get_new_random_req(req))
            self.cars_req.append(req)

    def get_new_random_req(self,arr=[]):
        new_file_num = randint(1, self.number_of_files)
        while new_file_num in arr:
            new_file_num = randint(1, self.number_of_files)
        return new_file_num

    def update_req(self):
        for i in range(1,self.number_of_cars +1):
            req = []
            number_of_reqs = randint(self.min_req_size, self.max_req_size)

            for j in range(0,number_of_reqs):
                req.append(self.get_new_random_req(req))
            self.cars_req[i-1] = req

    def get_car_req(self,car_index):
        if car_index < len(self.cars_req):
            return self.cars_req[car_index]
        return None

    def show_all(self):
        for car_req in self.cars_req:
            print (car_req)

