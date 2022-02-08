import yaml
import numpy as np
import get_grib
from get_grib import Get_wave_data,Get_wind_data
class Ship_Resistance():
    def __init__(self):
        """
         Here we will load the ship model scales from a ymal file 
        when the ship not change these parameters will not change
        """
        ship_file = open("Ship_Model.yaml")
        parsed_ship_file= yaml.load(ship_file,Loader=yaml.FullLoader)
        self.Los= parsed_ship_file["Los"]
        self.TF= parsed_ship_file["TF"]
        self.TA= parsed_ship_file["TA"]
        self.Dp= parsed_ship_file["Dp"]
        self.Nrud= parsed_ship_file["Nrud"]
        self.NBrac= parsed_ship_file["NBrac"]
        self.NBoss= parsed_ship_file["NBoss"]
        self.NThr=parsed_ship_file["NThr"]
        self.L= parsed_ship_file["L"]
        self.Lwl = parsed_ship_file["Lwl"]
        self.B= parsed_ship_file["B"]
        self.CB = parsed_ship_file["CB"]
        self.S =parsed_ship_file["S"]
        self.A=parsed_ship_file["A"]
        

        
    def hollenbach(self,Vs):
        T= (self.TA+self.TF)/2
        Fi= (self.CB/self.L)*((self.B/2)*2*T)**(0.5)
        k= 0.6*Fi+145*Fi**3.5
        rho = 1025
        gravk = 9.81   
        nu = 1.1395E-6 
        self.Vs=Vs
        if self.Los/self.L<1:
            Lfn=self.Los
        elif self.Los/self.L>=1 and self.Los/self.L<1.1:
            Lfn=self.L+2/3*(self.Los-self.L)
        elif self.Los/self.L >= 1.1:
            Lfn= 1.0667*self.L
        else:print('shit')
        a =np.array([-0.3382 ,  0.8086  , -6.0258 ,-3.5632, 9.4405 ,0.0146 ,0 ,0, 0, 0])
        b =np.array([-0.57424 ,	 13.3893,	90.5960, 	   4.6614,	-39.721,	-351.483,  -1.14215	,-12.3296,	459.254]).reshape(3,3)
        #b is 3 by 3 matrix
        d = np.array([0.854 ,-1.228 ,0.497])
        e = np.array([2.1701 ,-0.1602])
        f = np.array([0.17 ,0.20, 0.60])
        g = np.array([0.642, -0.635 ,0.150])
        Fn=Vs/(gravk*Lfn)**0.5
        dd=np.array([1, self.CB ,self.CB**2]).reshape(3,1)
        Fnkrit = np.array(d).dot(dd)
        c1 = Fn/Fnkrit
        # c1_min = Fn/Fnkrit

        Rns= Vs*self.L/nu
        CFs= 0.075/(np.log10(Rns)-2)**2
        CRFnkrit = max(1.0,(Fn/Fnkrit)**(c1))
        kL=e[0]*self.L**(e[1])#1 by 1
        Fnn= np.array([1 ,Fn, Fn**2]).reshape(3,1)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # % Minimum values

        # % There is an error in the hollenbach paper and in Minsaas' 2003 textbook, which
        # % is corrected in this formula by dividing by 10
        CRstandard = np.dot(dd.T,b).dot(Fnn)/10 # a scale 
        big_array = np.array([T/self.B ,self.B/self.L ,self.Los/self.Lwl, self.Lwl/self.L,(1+(self.TA-self.TF)/self.L),self.Dp/self.TA, 1+self.Nrud,1+self.NBrac, 1+self.NBoss])
        big_array2 = (1+self.NThr)**a
        big_array_mean=np.prod(big_array)*np.prod(big_array2)#big_array.append(big_array2)#list right  now 
        CR_hollenbach= CRstandard[0]*CRFnkrit*kL*big_array_mean#*np.prod(big_array_mean)
        CR = CR_hollenbach*self.B*T/self.S#Resistance coefficient, scaled for wetted surface
        C_Ts = CFs +CR #Total resistance coeff. ship
        R_T_mean = C_Ts*rho/2*Vs*Vs*self.S#Total resistance to the ship
        return R_T_mean/1000
    def hollenbach_map(self,Vs):
        """
        for speed up the calculation time I use a map (calculate the R_T_mean offline) instead of the last function
        """
        V_map=np.array([12,12.1,12.2,12.3,12.4,12.5,12.6,12.7,12.8,12.9,13,13.1,13.2,13.3,
        13.4,13.5,13.6,13.7,13.8,13.9,14,14.1,14.2,14.3,14.4,14.5,14.6,14.7,14.8,
        14.9,15,15.1,15.2,15.3,15.4,15.5,15.6,15.7,15.8,15.9,16,16.1,16.2,16.3,
        16.4,16.5,16.6,16.7,16.8,16.9,17])
        F_map=np.array([377.726,384.201,390.786,397.483,404.294,411.223,418.271,425.443,
                432.739,440.164,447.720,455.410,463.237,471.203,479.313,487.569,
                495.974,504.530,513.243,522.114,531.146,540.3446,549.710,559.248,
                568.962,578.854,588.928,599.188,609.637,620.279,631.118,642.157,
                653.399,664.850,676.512,688.390,700.487,712.807,725.354,738.132,
                751.146,764.399,777.895,791.639,805.635,819.887,834.400,849.177,
                864.223,879.543,895.140])
        ind=np.where(V_map==Vs)
        self.Vs=Vs
        return F_map[ind]
             
    
    def Wind_resistance(self,start,goal,V_wind_x,V_wind_y):
    #  '''here we calculate the resistance of wind'''
        #we only consider the force on surge direction of a ship
        motion=np.array([goal[0]-start[0],goal[1]-start[1]])
        V_ship_vec=self.Vs*motion/np.linalg.norm(motion)
        V_wind_vec=np.array([V_wind_x,V_wind_y])*motion
        V_rel=V_ship_vec-V_wind_vec
        A=self.B*self.TA*0.8
        C_air=0.7
        R_wind= 0.5*1.29*A*C_air*(V_rel[0]*V_rel[0]+V_rel[1]*V_rel[1])
        return R_wind/1000

    def Wave_resistance(self,H_wave):
        # '''here we calculate the wave resistance'''
        R_wave = (1/16)*1025*9.8*H_wave*H_wave*self.B*np.sqrt(self.B/(self.L*0.15))
        return R_wave/1000
# for debug use
if __name__ == '__main__':
    H_wave=Get_wave_data("west_norway").data
    x, y= Get_wind_data("west_norway")
    V_wind_x=x.data
    V_wind_y=y.data
    
    shipR=Ship_Resistance()
    R_T=shipR.hollenbach(12*0.5144)# KN
    R_wind=shipR.Wind_resistance((5,5),(4,5),V_wind_x[5][5],V_wind_y[5][5])
    R_wave=shipR.Wave_resistance(H_wave[5][5])
    print(R_T)
    print(R_wind)
    print(R_wave)