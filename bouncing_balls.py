# 3D simulation of bouncing balls
#
# author: Konstantin Lübeck (Embedded Systems, Universtiy of Tuebingen)
# adapted from: Stephan Schirrecker (schirrecker) 
# https://gist.github.com/schirrecker/982847faeea703dd6f1dd8a09eab13aa

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# gravitational acceleration on Earth in m*s^-2
g = 9.80665

# acceleration vector due to g
ag = np.array((0, 0, -g))

# coefficient of restitution (ratio of velocity after and before bounce)
# see http://en.wikipedia.org/wiki/Coefficient_of_restitution
cor = 0.9

# 1 millisecond delta t
delta_t = 0.001

# number of balls to simulate
num_balls = 100

# size of the x, y, and z axis
size = 10

# colors of the balls
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# inital view angles
elev = 30
azim = 30

xlim = (0,size)
ylim = (0,size)
zlim = (0,size)

fig = plt.figure()
ax = Axes3D(fig)

ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

ax.view_init(elev, azim)

class Ball:
    def __init__(self, xyz, v, fmt):
        self.xyz = np.array(xyz)
        self.v = np.array(v)

        self.scatter, = ax.plot([], [], [], fmt, animated=True)

    def update(self):
        # ball hits lower x wall 
        if self.xyz[0] <= xlim[0]:
            self.v[0] = cor * np.abs(self.v[0])

        # ball hits upper x wall
        elif self.xyz[0] >= xlim[1]:
            self.v[0] = - cor * np.abs(self.v[0])

        # ball hits lower y wall
        if self.xyz[1] <= ylim[0]:
            self.v[1] = cor * np.abs(self.v[1])

        # ball hits upper y wall
        elif self.xyz[1] >= ylim[1]:
            self.v[1] = - cor * np.abs(self.v[1])

        # ball hits lower z wall
        if self.xyz[2] <= zlim[0]:
            self.v[2] = cor * np.abs(self.v[2])

        # ball hits upper z wall
        elif self.xyz[2] >= zlim[1]:
            self.v[2] = - cor * np.abs(self.v[2])


        delta_v = delta_t * ag
        self.v += delta_v

        self.xyz += self.v

        # make sure the balls stay inside of the canvas
        self.xyz[0] = np.clip(self.xyz[0], xlim[0], xlim[1])
        self.xyz[1] = np.clip(self.xyz[1], ylim[0], ylim[1])
        self.xyz[2] = np.clip(self.xyz[2], zlim[0], zlim[1])

        # draw ball
        self.scatter.set_xdata(self.xyz[0])
        self.scatter.set_ydata(self.xyz[1])
        self.scatter.set_3d_properties(self.xyz[2])


# generate balls with random position, velocity, and color
balls = []

for i in np.arange(0,num_balls):
    xyz = np.random.rand(1,3)[0]*size
    v = np.random.rand(1,3)[0]*0.1
    fmt = str(colors[np.random.randint(0,len(colors))] + 'o')
    balls.append(Ball(xyz, v, fmt))


def init():
    return [] 

def update(t):

    global elev, azim

    for ball in balls:
        ball.update()

    artists = [ball.scatter for ball in balls]
  
    # rotate view
    azim = azim + t/2
    ax.view_init(elev, azim)
    
    artists.append(ax)

    return artists 

ani = FuncAnimation(fig, update, frames=np.arange(0,0.5,delta_t), init_func=init, interval=10, blit=True, repeat=False)
#ani.save('animation.gif', writer='imagemagick', fps=30)
plt.show()
