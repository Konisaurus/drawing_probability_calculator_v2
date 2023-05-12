import tkinter as tk
from widgets_for_gui import *
from observer_subject import Observer
from copy import deepcopy
from model_hypgeo import *


class View(tk.Tk, Observer):
    '''
    Class that manages all visual aspects of the program.
    '''
    def __init__(self, model, controller):
        
        # Interaction with the model and the controller.
        self.model = model              # Which model should be observed.
        self.model.attach(self)         # Attach to this model.
        self.controller = controller    # Controller contains all event handlers.

        # Count/Storing variables.
        self.groups = {}
        self.group_key = 0

        # Setup a window.
        tk.Tk.__init__(self)
        self.geometry("540x520")
        self.resizable(False, True)
        self.title("Drawing Probability Master v2")      
        self.init_ui()                                  # Widgets.
        self.eval('tk::PlaceWindow . center')           # Center the window.
        self.bind("<1>", self.set_focus)                # Allways focus on the widget on left click.
        self.mainloop()

    def init_ui(self):
        '''
        Creates all widgets.
        '''
        # Widget sizes.
        self.label_width = 10
        self.text_size = 10
        self.entry_width = 5

        # Main frames: Create, configure and arragne with grid.
        self.main_frm_top = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=5, width=520, height=50)
        self.main_frm_top.grid_propagate(0)
        self.main_frm_bottom = Scrollable_Frame(master=self, relief=tk.RIDGE, borderwidth=5)

        tk.Grid.rowconfigure(self=self, index=1, weight=1)

        self.main_frm_top.grid(row=0, column=0, padx=10, pady=5, sticky="nesw")
        self.main_frm_bottom.get_frm_wrapper().grid(row=1, column=0, padx=10, pady=5, sticky="nesw")
        
        # Top labels, buttons, entries: Create, configure/bind and arrange with grid.
        self.lbl_deck_size = tk.Label(master=self.main_frm_top, text="Deck Size:", font=("Helvetica", self.text_size, "bold"), anchor="e")
        self.lbl_sample_size = tk.Label(master=self.main_frm_top, text="Sample Size:", font=("Helvetica", self.text_size, "bold"), anchor="e")

        self.btn_calculate = tk.Button(master=self.main_frm_top, text="CALCULATE", font=("Helvetica", self.text_size), anchor="center", command=self.controller.on_calculate)

        self.ent_deck_size = tk.Entry(master=self.main_frm_top, font=("Helvetica", self.text_size), width=self.entry_width, validate="key")
        self.ent_deck_size.configure(validatecommand=(self.ent_deck_size.register(self.validate),'%d', '%P'))
        self.ent_deck_size.bind('<FocusOut>', lambda event: self.controller.on_deck_size(self.ent_deck_size.get()))
        self.ent_sample_size = tk.Entry(master=self.main_frm_top, font=("Helvetica", self.text_size), width=self.entry_width, validate="key")
        self.ent_sample_size.configure(validatecommand=(self.ent_sample_size.register(self.validate),'%d', '%P'))
        self.ent_sample_size.bind('<FocusOut>', lambda event: self.controller.on_sample_size(self.ent_sample_size.get()))

        self.lbl_deck_size.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
        self.lbl_sample_size.grid(row=0, column=2, padx=5, pady=5, sticky="nesw")

        self.btn_calculate.grid(row=0, column=4, padx=20, pady=5, sticky="nesw")

        self.ent_deck_size.grid(row=0, column=1, padx=5, pady=5, sticky="nesw")
        self.ent_sample_size.grid(row=0, column=3, padx=5, pady=5, sticky="nesw")

        # Bottom widgets: Create, configure and arrange with grid
        self.lbl_group_name = tk.Label(master=self.main_frm_bottom.get_frm_container(), text="Group Name\n(optional)", font=("Helvetica", self.text_size, "bold"), anchor="center", width=self.label_width)
        self.lbl_group_success_deck = tk.Label(master=self.main_frm_bottom.get_frm_container(), text="Success in\nDeck", font=("Helvetica", self.text_size, "bold"), anchor="center", width=self.label_width)
        self.lbl_group_min_success_sample = tk.Label(master=self.main_frm_bottom.get_frm_container(), text="Min Success\nin Sample", font=("Helvetica", self.text_size, "bold"), anchor="center", width=self.label_width)
        self.lbl_group_max_success_sample = tk.Label(master=self.main_frm_bottom.get_frm_container(), text="Max Success\nin Sample", font=("Helvetica", self.text_size, "bold"), anchor="center", width=self.label_width)
        self.lbl_group_delete = tk.Label(master=self.main_frm_bottom.get_frm_container(), text="Delete\nGroup", font=("Helvetica", self.text_size, "bold"), anchor="center", width=self.label_width)

        self.btn_add_group = tk.Button(master=self.main_frm_bottom.get_frm_container(), text="ADD GROUP", font=("Helvetica", self.text_size), anchor="center", command=lambda: [self.add_group_view(), self.controller.on_add_group()])
        
        self.lbl_group_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_group_success_deck.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.lbl_group_min_success_sample.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.lbl_group_max_success_sample.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.lbl_group_delete.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        self.btn_add_group.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nesw")

    def add_group_view(self):
        '''
        Add a new group to the display.
        '''
        group_key = deepcopy(self.group_key)
        self.groups[group_key] = []
        group = self.groups[group_key]

        group.append(tk.Frame(master=self.main_frm_bottom.get_frm_container()))   # Frame for one grouo
        group.append(tk.Entry(master=group[0], font=("Helvetica", self.text_size), width=(2 * self.entry_width), validate="key"))
        group.append(tk.Entry(master=group[0], font=("Helvetica", self.text_size), width=(self.entry_width), validate="key"))
        group.append(tk.Entry(master=group[0], font=("Helvetica", self.text_size), width=(self.entry_width), validate="key"))
        group.append(tk.Entry(master=group[0], font=("Helvetica", self.text_size), width=(self.entry_width), validate="key"))
        group.append(tk.Button(master=group[0], text=" x ", font=("Helvetica", self.text_size, "bold"), anchor="center", command=lambda key=group_key: [self.del_group_view(key), self.controller.on_del_group(key)]))

        for index, command in zip([2,3,4], [self.controller.on_group_size, self.controller.on_group_min, self.controller.on_group_max]):
            entry = group[index]
            entry.configure(validatecommand=(entry.register(self.validate),'%d', '%P'))                              # Only allow integers as inputs for all entries.
            entry.bind('<FocusOut>', lambda event, key=group_key, command=command, entry=entry: command(key, entry.get()))    # Bind controller method to every entry.

        group[0].grid(row=(group_key + 1), column=0, columnspan=5)             # Arrange the group frame.
        group[1].grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        for column in range(2, 6, 1):
            group[column].grid(row=0, column=column, padx=30, pady=5, sticky="ns")  # Arrange the group widgets.

        self.btn_add_group.grid_forget()                                            # Arrange the button at the bottom of all groups
        self.btn_add_group.grid(row=(group_key + 2), column=0, columnspan=5, padx=5, pady=5, sticky="nesw")

        self.group_key += 1

    def del_group_view(self, key):
        '''
        Remove a group from the display.
        '''
        for widget in self.groups[key]:
            widget.destroy()
        self.groups.pop(key)

    def validate(self, type_of_action, entry_value):
        '''
        Validate function that only allows integers as inserts in entries.
        '''
        if type_of_action == '1':           # '1' is insert
            if not entry_value.isdigit():
                return False
            else:
                return True
        else:
            return True
        
    def set_focus(self, event=None):
        '''
        Focuses on the current widget.
        '''
        x, y = self.winfo_pointerxy()
        self.winfo_containing(x, y).focus()

    def update(self, update_event, **kwargs):
        pass
