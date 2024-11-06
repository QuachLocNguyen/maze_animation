import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

n = 100
x = np.linspace(0, 2*np.pi, n)
y = np.sin(x)
fig, ax = plt.subplots()
sine_line, = ax.plot(x,y,'b')
red_circle, = ax.plot([],[],"ro",markersize = 10)

def init():
    ax.axis([0,2*np.pi,-1,1])
    ax.axes.set_ylim(-1.2, 1.2)
    return sine_line, red_circle 

def animate(i):
    red_circle.set_data(x[i:i+1], y[i:i+1])
    return sine_line, red_circle 

anim = FuncAnimation(fig, animate, frames = n, interval = 100, 
                     init_func=init, repeat = False, blit = True)

plt.show()
