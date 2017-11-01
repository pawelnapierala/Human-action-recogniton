import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Draw:

    JOINT_CONNECTIONS = [
        [1, 2],
        [2, 3],
        [3, 4],
        [3, 5],
        [5, 6],
        [6, 7],
        [7, 8],
        [3, 9],
        [9, 10],
        [10, 11],
        [11, 12],
        [1, 17],
        [17, 18],
        [18, 19],
        [19, 20],
        [1, 13],
        [13, 14],
        [14, 15],
        [15, 16]
        ]
    
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('z')
        self.ax.set_zlabel('y')
        self.ax.set_xlim(-0.75, 0.75)
        self.ax.set_ylim(1.5, 3.0)
        self.ax.set_zlim(-0.75, 0.75)
        self.lines = [plt.plot([], [], [])[0] for _ in range(len(self.JOINT_CONNECTIONS))]
        for line in self.lines:
            line.set_data([], [])
            line.set_3d_properties([])

    def update_plot(self, frame):
        for i, c in enumerate(self.JOINT_CONNECTIONS):
            self.lines[i].set_data([frame[0][c[0]-1], frame[0][c[1]-1]], [frame[2][c[0]-1], frame[2][c[1]-1]])
            self.lines[i].set_3d_properties([frame[1][c[0]-1], frame[1][c[1]-1]])
        return self.lines 

    def animate_skeleton(self, frames):        
        ani = animation.FuncAnimation(self.fig, self.update_plot, frames=frames, interval=40, repeat=True, blit=True) 
        plt.show()

    def draw_skeletons(self, skeleton1, skeleton2):
        fig1 = plt.figure()
        ax1 = Axes3D(fig1)
        ax1.set_xlabel('x')
        ax1.set_ylabel('z')
        ax1.set_zlabel('y')
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(1.5, 3.5)
        ax1.set_zlim(-1, 1)

        ax1.scatter(skeleton1[0,:], skeleton1[2,:], skeleton1[1,:])

        for c in self.JOINT_CONNECTIONS:
            ax1.plot([skeleton1[0][c[0]-1], skeleton1[0][c[1]-1]], [skeleton1[2][c[0]-1], skeleton1[2][c[1]-1]], [skeleton1[1][c[0]-1], skeleton1[1][c[1]-1]])

        fig2 = plt.figure()
        ax2 = Axes3D(fig2)
        ax2.set_xlabel('x')
        ax2.set_ylabel('z')
        ax2.set_zlabel('y')
        ax2.set_xlim(-1, 1)
        ax2.set_ylim(1.5, 3.5)
        ax2.set_zlim(-1, 1)

        ax2.scatter(skeleton2[0,:], skeleton2[2,:], skeleton2[1,:])

        for c in self.JOINT_CONNECTIONS:
            ax2.plot([skeleton2[0][c[0]-1], skeleton2[0][c[1]-1]], [skeleton2[2][c[0]-1], skeleton2[2][c[1]-1]], [skeleton2[1][c[0]-1], skeleton2[1][c[1]-1]])

        plt.show()

    def draw_skeleton(self, skeleton):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlabel('x')
        ax.set_ylabel('z')
        ax.set_zlabel('y')
        ax.set_xlim(-1, 1)
        ax.set_ylim(1.5, 3.5)
        ax.set_zlim(-1, 1)

        ax.scatter(skeleton[0,:], skeleton[2,:], skeleton[1,:])

        for c in self.JOINT_CONNECTIONS:
            ax.plot([skeleton[0][c[0]-1], skeleton[0][c[1]-1]], [skeleton[2][c[0]-1], skeleton[2][c[1]-1]], [skeleton[1][c[0]-1], skeleton[1][c[1]-1]])

        plt.show()