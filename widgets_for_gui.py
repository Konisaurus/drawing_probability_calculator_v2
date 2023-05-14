'''
tkinter widget: Frame with a scrollbar.
'''

# Imports
import tkinter as tk

# Classes
class Scrollable_Frame(tk.Frame):
    '''
    Frame with a scrollbar for the y-axis.
    Access the container with self.get_frm_container().
    '''
    def __init__(self, master, **kwargs):
        # The wrapper frame inherited tk.Frame. It contains the scrollbar an the container frame.
        super().__init__(master, **kwargs)

        # Create a canvas which will be scrollable.
        self.cnv_scrollbar = tk.Canvas(master=self)
        self.cnv_scrollbar.pack(side="left", fill="both",expand=1)

        # Add a scrollbar to the canvas.
        self.scb_yaxis = tk.Scrollbar(master=self, orient="vertical", command=self.cnv_scrollbar.yview)
        self.scb_yaxis.pack(side="right",fill="y")

        # Configure the canvas.
        self.cnv_scrollbar.configure(yscrollcommand=self.scb_yaxis.set)
        self.cnv_scrollbar.bind("<Configure>", lambda e: self.cnv_scrollbar.config(scrollregion= self.cnv_scrollbar.bbox(tk.ALL))) 

        # Create another frame inside the canvas which will contain all widgets and add it to the canvas.
        self.frm_container = tk.Frame(master=self.cnv_scrollbar)
        self.cnv_scrollbar.create_window((0,0), window=self.frm_container, anchor="nw")  

        # Bind the scrollwheel to the scrollbar.
        self.frm_container.bind("<Enter>", self.bind_mousewheel)
        self.frm_container.bind("<Leave>", self.unbind_mousewheel)
        self.frm_container.bind("<Configure>", self.adjust_scrollregion)

    def get_frm_container(self):
        '''
        Access/add all widgets in this frame.
        '''
        return self.frm_container
        
    def bind_mousewheel(self, event):
        '''
        Binds mousewheel when inside of the frame.
        '''
        self.cnv_scrollbar.bind_all("<MouseWheel>", self.handle_mousewheel)

    def unbind_mousewheel(self, event):
        '''
        Unbinds mousewheel when outside of the frame.
        '''
        self.cnv_scrollbar.unbind_all("<MouseWheel>")

    def handle_mousewheel(self, event):
        '''
        Configures the mousewheel with the scorllbar.
        '''
        self.cnv_scrollbar.yview_scroll(int(-1*(event.delta/120)), "units")

    def adjust_scrollregion(self, event):
        '''
        Adjusts the scrollbarregion when the frame gets bigger.
        '''
        self.cnv_scrollbar.configure(scrollregion=self.cnv_scrollbar.bbox("all"))
