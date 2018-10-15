import threading 

class MyTimer:

    def __init__(self, interval=5):
        self.interval= interval
        self.stop = False


    def stop_intervals(self):
        self.stop = True

    def set_interval(self,func, args=None):
        if self.stop :
            return None
        def func_wrapper():
            self.set_interval(func, args)
            if args :
                func(args)
            else:
                func()


        threading.Timer(self.interval,func_wrapper).start()
