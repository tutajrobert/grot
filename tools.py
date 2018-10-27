import time

class timer():
    
    """
    Just timer class for nice looking solving time printing
    Can be used like a timer for measuring midtimes
    """

    def __init__(self):
        self.t = time.time()
    
    def stop(self):
        return time.time() - self.t
    
    def check(self):
        return str(round(self.stop() * 1e0, 2)) + " s"

def max_search(value, max):
#For iterative search of maximum value
    if value > max:
        max = value
    else:
        pass
    return max
    
def min_search(value, min):
#For iterative search of minimum value
    if value < min:
        min = value
    else:
        pass
    return min