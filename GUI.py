# here is the main file of this program
import PySimpleGUI as sg
import numpy as np
import plotting
from plotting import Plotting
import matplotlib
import matplotlib.pyplot as plt
import Dijkstra
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class Ship_GUI():
    "here is a GUI for the ship routing system which contain a input window of..."
    "... the start point, end point,map selection,ship velocity and step length,."
    " A output window for plotting the map and the route of the result"
    def __init__(self):
        "here a intial frame of the gui "
        print('starting node')
        layout = [[sg.T('After start the program please press Change Map first!!! or nothing shows up ')] ,[sg.T('Select Map') ,    
        sg.Combo(['oslofjord','sorlandet','skagerrak','west_norway','n-northsea','nordland','troms-finnmark'],default_value='west_norway',size=(15,1),key='map'),
                        sg.Button('Change Map'),sg.T('Velocity'),sg.Input(key='Vel',default_text=12,size=(3,1)),sg.T('knot')],
                        [sg.Text('Start Point: ',size=(15,1)),
                        sg.Text('x:',size=(1,1)),sg.Input(key='start_x',default_text=1,size=(4,1)),sg.Text('y:',size=(1,1)),sg.Input(key='start_y',default_text=1,size=(4,1)),      
                        # sg.T('',size=(6,1)),
                        sg.Text('End Point:',size=(15,1)),      
                        sg.Text('x:',size=(1,1)),sg.Input(key='end_x',default_text=2,size=(4,1)),sg.Text('y:',size=(1,1)),sg.Input(key='end_y',default_text=2,size=(4,1)),                                    
                        sg.Text('Step Length',size=(15,1)),
                        sg.Text('L:'),sg.Input(key='L',default_text=1,size=(3,1))],
                        [sg.Button('Start Calculation'),
                        sg.Text('calculate time'),sg.Output(size=(15,1),key='TT')],
                        
                        [sg.Canvas(key='controls_cv')],
                        [sg.T('Figure:')],
                        [sg.Column(
                            layout=[
                                [sg.Canvas(key='fig_cv',size=(1500,900)
                                        # it's important that you set this size
                                        #size=(400 * 2, 400)
                                        )]
                            ],
                            background_color='#DAE0E6',
                            pad=(0, 0)
                        )],
                        ]

                    
        self.window = sg.Window('Ship Routing GUI', layout,finalize=True)  
        while True:

            self.event, self.values = self.window.read()
            if self.event=='Change Map':
                self.show_map()
            if self.event=='Start Calculation':
                self.cal_route()
            if self.event==sg.WIN_CLOSED:
                break
            draw_figure_w_toolbar(self.window['fig_cv'].TKCanvas, self.fig, self.window['controls_cv'].TKCanvas)

        self.window.close
    def show_map(self):
        plt.clf()
        start=(int(self.values['start_x']),int(self.values['start_y']))
        end=(int(self.values['end_x']),int(self.values['end_y']))
        ppl=plotting.Plotting(start,end,self.values['map'])
        self.fig = plt.gcf()
        DPI = self.fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        # self.fig.set_size_inches(404 * 2/ float(DPI), 404*1.2 / float(DPI))
        self.fig.set_size_inches(1500/ float(DPI), 900 / float(DPI))
        
        ppl.plot_grid(self.values['map'])

    def cal_route(self):
        plt.clf()
        t1=time.time()
        start=(int(self.values['start_x']),int(self.values['start_y']))
        end=(int(self.values['end_x']),int(self.values['end_y']))
        location=self.values['map']
        L=int(self.values['L'])
        Vel=int(self.values['Vel'])
        dij = Dijkstra.Dijkstra(start, end,location,L,Vel)
        plot = plotting.Plotting(start, end,location)
        path, visited = dij.searching()
        t2=time.time()
        self.window['TT'].update(t2-t1)
        plot.plot_grid(location)
        fig = plt.gcf()
        DPI = fig.get_dpi()
    
        # fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        self.fig.set_size_inches(1500/ float(DPI), 900 / float(DPI))
        plot.plot_visited_in_GUI(visited)
        plot.plot_path(path)
            

def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs) 


if __name__ == '__main__':
    Ship_GUI()
    


