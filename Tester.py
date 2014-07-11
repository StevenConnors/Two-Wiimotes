import pymouse
import time

m = pymouse.PyMouse()
m.move(30, 550)
#print m.position()
#time.sleep(2)

m.press(30, 550)
time.sleep(0.3)

m.move(30, 500)
print m.position()

m.move(30, 400)
print m.position()

m.move(30, 300)
print m.position()

m.move(30, 200)
m.release(30, 200)