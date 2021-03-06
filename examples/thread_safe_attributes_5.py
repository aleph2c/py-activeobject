import math
import time
from threading import Thread
from threading import Event as ThreadEvent

from miros import ThreadSafeAttributes

def equation(a):
  return a * math.cos(0.45) + 3 * a ** 1.2

class GetLock1(ThreadSafeAttributes):

  def __init__(self, evt):
    '''running within main thread'''
    self.evt = evt
    self.thread_race_attr_1 = 0

  def thread_method_1(self):
    '''running within th1 thread'''
    while(self.evt.is_set()):
      self.thread_race_attr_1 = 0.35
      self.thread_race_attr_1 = self.thread_race_attr_1 * math.cos(0.45)
      self.thread_race_attr_1 = 3 * self.thread_race_attr_1 ** 1.2
      print("th1: ", equation(self.thread_race_attr_1))

class GetLock2():
  def __init__(self, evt, gl1):
    '''running within main thread'''
    self.evt = evt
    self.gl1 = gl1

  def thread_method_2(self):
    '''running within th2 thread'''
    while(self.evt.is_set()):
      self.gl1.thread_race_attr_1 = 0.30
      self.gl1.hread_race_attr_1 = self.gl1.thread_race_attr_1 * math.cos(0.45)
      self.gl1.hread_race_attr_1 = 3 * self.gl1.thread_race_attr_1 ** 1.2
      print("th2: ", equation(self.gl1.thread_race_attr_1))

class ThreadKiller():
  def __init__(self, evt, count_down):
    '''running within main thread'''
    self.evt = evt
    self.kill_time = count_down

  def thread_stopper(self):
    '''running within killer thread'''
    time.sleep(self.kill_time)
    self.evt.clear()

# main thread:
evt = ThreadEvent()
evt.set()

gl1 = GetLock1(evt)
gl2 = GetLock2(evt, gl1=gl1)
killer = ThreadKiller(evt, count_down=0.1)

threads = []
threads.append(Thread(target=gl1.thread_method_1, name='th1', args=()))
threads.append(Thread(target=gl2.thread_method_2, name='th2', args=()))

for thread in threads:
  thread.start()

thread_stopper = Thread(target=killer.thread_stopper, name='stopper', args=())
thread_stopper.start()
thread_stopper.join()

