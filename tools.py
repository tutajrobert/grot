import time

class timer():
  def __init__(self):
    self.t = time.time()
    
  def stop(self):
    return time.time() - self.t
    
  def check(self):
    return str(round(self.stop() * 1e3, 2)) + " ms"
    