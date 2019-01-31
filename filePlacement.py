
from random import randint
from random import uniform
import copy

class FilePlacement :
    def __init__(self,number_of_caches=5,number_of_files=25,
            epsilon=0.5,min_epsilon=0.01,min_cache_size=5,max_cache_size=10,remove_chance=0.5,resize_chance=0.5,log=False):
        self.caches = []
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.number_of_files = number_of_files 
        self.max_cache_size = max_cache_size
        self.min_cache_size = min_cache_size
        self.remove_chance = remove_chance
        self.resize_chance = resize_chance
        self.previouse_caches = []
        self.log = log

        for i in range(1,number_of_caches +1):
            files_in_cache = []
            current_cache_size = randint(self.min_cache_size, self.max_cache_size)
            for j in range (0,current_cache_size):
                files_in_cache.append(self.get_new_random_file(files_in_cache))
            self.caches.append(files_in_cache)

    def get_new_random_file(self,arr=[]):
        new_file_num = randint(1, self.number_of_files)
        while new_file_num in arr:
            new_file_num = randint(1, self.number_of_files)
        return new_file_num

    def my_print(self,s):
        if self.log :
            print (s)

    def mixed_up(self):

        for cache in self.caches:
            self.previouse_caches.append(cache[:])


            self.my_print( "raw cache %s" % (cache) )

            # remove phase
            for i in cache:
                should_remove = uniform(0,1)
                if should_remove < self.remove_chance:
                    self.my_print("%s removed"%(i))
                    cache.remove(i)

            self.my_print( "removed cache %s" % (cache) )

            # replace phase
            for i in range(0,len(cache)):
                should_replace = uniform(0,1)
                if should_replace < self.epsilon:
                    file_num = self.get_new_random_file(cache)
                    self.my_print("%s replaced with %s"%(cache[i],file_num))
                    cache[i] = file_num

            self.my_print( "replaced cache %s" % (cache) )

            # add new elements
            should_resize = uniform(0,1)
            if should_resize < self.resize_chance or len(cache) < self.min_cache_size:
                new_size = randint(self.min_cache_size, self.max_cache_size)
                if new_size <= len(cache):
                    while new_size != len(cache):
                        remove_candidate_index = randint(0, len(cache) -1)
                        self.my_print("removed %s"%(remove_candidate_index))
                        cache.remove(cache[remove_candidate_index])
                else:
                    while new_size != len(cache):
                        add_candidate = self.get_new_random_file(cache)
                        self.my_print("added %s"%(add_candidate))
                        cache.append(add_candidate)

            self.my_print( "resized cache %s" % (cache) )
        self.show_all()

    def ended(self):
        return self.epsilon < self.min_epsilon

    def request_cache_hits(self,req,cache_index):
        hits = 0;
        for i in req:
            if i in self.caches[cache_index]:
                hits += 1

        return hits

    def show_all(self):
        print ("************ current cache ******************")
        for cache in self.caches:
            print (cache)
        print ("************ previouse cache ******************")
        for cache in self.previouse_caches:
            print (cache)

