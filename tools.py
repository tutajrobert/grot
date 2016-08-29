import time

class timer():
		def __init__(self):
				self.t = time.time()
    
		def stop(self):
				return time.time() - self.t
    
		def check(self):
				return str(round(self.stop() * 1e3, 2)) + " ms"

def max_search(value, max):
		if value > max:
				max = value
		else:
				pass
		return max
    
def min_search(value, min):
		if value < min:
				min = value
		else:
				pass
		return min
		