import math
import heapq
import numpy as np
import plotting, Obstacles
import Resistance_Forces

import matplotlib.pyplot as plt
import get_grib
from get_grib import Get_wave_data,Get_wind_data
class Dijkstra():
    """
    Here is the Dijkstra program 
    """
    def __init__(self, start, goal,location,L,Vel):
        self.s_start = start#start point 
        self.s_goal = goal#  destination 
        self.Obs = Obstacles.obstacles(location)  
        self.Vel=Vel
        self.motion = [(-L, 0), (-L, L), (0, L), (L, L),
                        (L, 0), (L, -L), (0, -L), (-L, -L)] 
        self.obs = self.Obs.obs  # position of obstacles
        self.wave_data=Get_wave_data(location).data
        self.wind_x,self.wind_y=Get_wind_data(location)
        self.range_x=np.size(self.wave_data,0)#import the data range from Obs
        self.range_y=np.size(self.wave_data,1)#
        self.OPEN = []  # priority queue / OPEN set
        self.Visited = []  # / VISITED order
        self.PARENT = dict()  # recorded parent
        self.g = dict()  # cost of the nodes
    def searching(self):
        """
        Here is the main loop of the Dijkstra program
        """

        self.PARENT[self.s_start] = self.s_start
        self.g[self.s_start] = 0
        self.g[self.s_goal] = math.inf
        heapq.heappush(self.OPEN,
                       (0, self.s_start))

        while self.OPEN:
            c, s = heapq.heappop(self.OPEN)
            self.Visited.append(s)

            if s == self.s_goal:
                break

            for s_n in self.get_neighbor(s):
                new_cost = self.g[s] + self.cost(s, s_n)

                if s_n not in self.g:
                    self.g[s_n] = math.inf

                if new_cost < self.g[s_n]: 
                    self.g[s_n] = new_cost
                    self.PARENT[s_n] = s
                    heapq.heappush(self.OPEN, (new_cost, s_n))

        return self.extract_path(self.PARENT), self.Visited
    def get_neighbor(self, s):
        """ 
        find all the neighbor of current point
        """
        Neighbors=[]
        for i in self.motion:
            Neighbors.append((s[0] + i[0], s[1] + i[1]))
        return Neighbors

    def cost(self, s_start, s_goal):
        """
        Calculate Cost for this motion
        """
        if self.is_collision(s_start, s_goal):
            return math.inf
        if self.out_of_range(s_start,s_goal):
            return math.inf
        R_S=Resistance_Forces.Ship_Resistance()
        R1=R_S.hollenbach(self.Vel*0.5144)
        # R1=R_S.hollenbach_map(self.Vel)
        R2= R_S.Wave_resistance(self.wave_data[s_start[0]][s_start[1]])
        R3=R_S.Wind_resistance(s_start,s_goal,self.wind_x[s_start[0]][s_start[1]],
                                self.wind_y[s_start[0]][s_start[1]])
        R=R1+R2+R3
        W=R*math.hypot(s_goal[0] - s_start[0], s_goal[1] - s_start[1])
        return W
    def is_collision(self, start, end):
        """
        check if the start or end points are is collision with obstacles.
        """

        if start in self.obs or end in self.obs:
            return True
        return False
    def out_of_range(self,start,end):
        """
        check if the start or end points are getting out of the data range 
        """
        if start[0]<0 or start[1]<0:
            return True
        if end[0]<0 or end[1]<0:
            return True
        if start[0]>self.range_x-1 or start[1]>self.range_y-1:
            return True
        if end[0]>self.range_x-1 or end[1]>self.range_y-1:
            return True
        return False        
   
    def extract_path(self, PARENT):
        """
        from the end point getting back to the start point
        with parent set
        """
        path = [self.s_goal]
        s = self.s_goal
        while True:
            s = PARENT[s]#
            path.append(s)
            if s == self.s_start:
                break
        return list(path)

# for debug

if __name__ == '__main__':
  
    s_start = (1,1)
    s_goal = (35,5)

    dijkstra = Dijkstra(s_start, s_goal,"west_norway",1,12)
    plot = plotting.Plotting(s_start, s_goal,"west_norway")
    path, visited = dijkstra.searching()
    plot.plot_grid("West Norway")
    plot.plot_visited(visited)
    plot.plot_path(path)
    plt.show()
  

