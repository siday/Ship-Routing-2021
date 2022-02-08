import pupygrib
import yaml
import os
def Get_wave_data(location):
    """
    Get the wave signficant height
    location: map name
    """
    nowdic=os.getcwd()#+'/'
    ship_file = open("Ship_Model.yaml")
    parsed_ship_file= yaml.load(ship_file,Loader=yaml.FullLoader)
    F=parsed_ship_file[location]
    Fname=os.path.join(nowdic,F[0])
    with open(Fname, 'rb') as stream:# signaficate wave hight
        for i, msg in enumerate(pupygrib.read(stream), 1):
            lons, lats = msg.get_coordinates()
            time = msg.get_time()
            values = msg.get_values()
            if i==63 : wave=values
            # print("Message {}: {} {:.3f} {}".format(i, time, values.mean(), values.shape))
    return wave

def Get_wind_data(location):
    """
    Get the wind velocity along x and y 
    location: map name
    """
    nowdic=os.getcwd()
    ship_file = open("Ship_Model.yaml")
    parsed_ship_file= yaml.load(ship_file,Loader=yaml.FullLoader)
    F=parsed_ship_file[location]
    Fname=os.path.join(nowdic,F[1])
    with open(Fname, 'rb') as stream:# signaficate wave hight
        for i, msg in enumerate(pupygrib.read(stream), 1):
            lons, lats = msg.get_coordinates()
            time = msg.get_time()
            values = msg.get_values()
            if i==112: wind_u=values
            if i==113: wind_v=values
            #next row for debug
            # print("M/essage {}: {} {:.3f} {}".format(i, time, values.mean(), values.shape))
    return wind_u,wind_v
if __name__=='__main__':
    # F,M=Get_wind_data("nordland")
    # Get_wave_data("west_norway")
    Get_wind_data("oslofjord")