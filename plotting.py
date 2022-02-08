
import matplotlib.pyplot as plt
import Obstacles
import Dijkstra
from Dijkstra import Dijkstra

class Plotting:
    def __init__(self, start, end,location):
        self.start, self.end = start, end
        self.OBS = Obstacles.obstacles(location)
        self.obs = self.OBS.obs_map()

    def plot_grid(self, name):
        obs_x = [x[0] for x in self.obs]
        obs_y = [x[1] for x in self.obs]

        plt.plot(self.start[0], self.start[1], "bs")
        plt.plot(self.end[0], self.end[1], "gs")
        plt.plot(obs_x, obs_y, "sk")
        plt.title(name)
        plt.axis("equal")
    def plot_visited_in_GUI(self,visited):
        '''This function will plot the visited area directly '''
        if self.start in visited: visited.remove(self.start)
        if self.end in visited: visited.remove(self.end)
        visited_x=[visited[i][0] for i in range(len(visited))]
        visited_y=[visited[i][1] for i in range(len(visited))]
        plt.plot(visited_x,visited_y, color='yellow',marker= 'o',linestyle = 'None')
    def plot_visited(self, visited, cl='yellow'):
        if self.start in visited:
            visited.remove(self.start)

        if self.end in visited:
            visited.remove(self.end)

        count = 0

        for x in visited:
            count += 1
            plt.plot(x[0], x[1], color=cl, marker='o')
            plt.pause(0.001)
        plt.pause(0.01)

    def plot_path(self, path, cl='r'):
        path_x = [path[i][0] for i in range(len(path))]
        path_y = [path[i][1] for i in range(len(path))]

        plt.plot(path_x, path_y, linewidth='3', color=cl)

        plt.plot(self.start[0], self.start[1], "bs")
        plt.plot(self.end[0], self.end[1], "gs")
