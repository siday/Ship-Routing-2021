import csv
import numpy as np
import get_grib
from get_grib import Get_wave_data
class obstacles:
    def __init__(self,location):
        self.Wave= Get_wave_data(location).mask
        self.x_range = np.size(self.Wave,0)  # size of background
        self.y_range = np.size(self.Wave,1)
        self.obs = self.obs_map()

    def obs_map(self):
        """
        Here is a map of land and data boundary
        """
        x = self.x_range
        y = self.y_range
        obs = set()

        for i in range(x):#left boundary
            obs.add((i, 0))
        for i in range(x):#right boundary
            obs.add((i, y - 1))

        for i in range(y):#up boundary
            obs.add((0, i))
        for i in range(y):#down boundary
            obs.add((x - 1, i))
        land=np.where(self.Wave==1.0 )# detect where is the land
        for m in range(np.size(land,1)):
            obs.add((land[0][m],land[1][m]))
     
        return obs
# for test use here
if __name__=='__main__':
    obstacles("west_norway").obs_map()