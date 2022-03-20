# The GUI of the CP468 Project
# Pathfinding
#	Filename: main_gui.py
#	Authors:
#		Abdirahman Yassin 	- 154160030
#		Gaymer Barrios 		- 171898540
#	Description:
#		Main GUI of pathfinding
#	Reference:
#		http://modelai.gettysburg.edu/2017/pathfinding/index.html
#	Run with:
#		python main_gui.py

import tkinter
from tkinter import messagebox
import os
from paths import main_backend
from tkinter.filedialog import askopenfilename
import shutil

class MainGUI:
    def __init__(self):

        # Formatting variables
        label_font = ('times', 14, 'bold')
        text_font = ('times',12)

        # ---------------------
        #   Main Window Widge
        # ---------------------
        self.main_window = tkinter.Tk()
        self.main_window.title("CP468 AI Project")
        self.menubar = tkinter.Menu(self.main_window)
        self.menubar.add_command(label="Upload", command = self.open_img)
        self.menubar.add_command(label="Clean", command = self.clean_output)

        # ---------------------
        #  Input Checkbuttons
        # ---------------------
        self.cb_road_config_tree_var = tkinter.IntVar()
        self.cb_road_config_tree_sidewalks_var = tkinter.IntVar()
        self.cb_road_config_garden_var = tkinter.IntVar()
        self.cb_road_config_aldrich_park_var = tkinter.IntVar()
        self.cb_basic_var= tkinter.IntVar()
        self.cb_basic_v2_var = tkinter.IntVar()

        # Set the intVar objects to 0
        self.cb_road_config_tree_var.set(0)
        self.cb_road_config_tree_sidewalks_var.set(0)
        self.cb_road_config_garden_var.set(0)
        self.cb_road_config_aldrich_park_var.set(0)
        self.cb_basic_var.set(0)
        self.cb_basic_v2_var.set(0)

        # --------------------------
        #  Heuristics Checkbuttons
        # --------------------------
        self.cb_best_first_var = tkinter.IntVar()
        self.cb_astar_var = tkinter.IntVar()
        self.cb_beam_var = tkinter.IntVar()
        self.cb_human_var = tkinter.IntVar()

        # Set the intVar objects to 0
        self.cb_best_first_var.set(0)
        self.cb_astar_var.set(0)
        self.cb_beam_var.set(0)
        self.cb_human_var.set(0)

        # ---------------------
        #   Loading GUI Images
        # ---------------------
        # Load title image
        script_dir = os.path.dirname(__file__)  # Absolute directory of this script
        relative_path = "../gui_images/pathfinding_title_v2.png"
        abs_file_path = os.path.join(script_dir, relative_path)
        title_img = tkinter.PhotoImage(file=abs_file_path)

        # Load run image
        relative_path = "../gui_images/run_v2.png"
        abs_file_path = os.path.join(script_dir, relative_path)
        run_img = tkinter.PhotoImage(file=abs_file_path)

        # ------------
        #   labels
        # ------------
        self.title_label = tkinter.Label(self.main_window, \
                                            #text = "PROJECT TITLE")
                                            image = title_img)
        
        self.num_iter_label = tkinter.Label(self.main_window, \
                                        text = "Number of Iterations:",
                                        font = label_font)

        self.update_terrain_label = tkinter.Label(self.main_window, \
                                        text = "Update Terrain:",
                                        font = label_font)

        self.select_input_label = tkinter.Label(self.main_window, \
                                        text = "Select Input/Upload",
                                        font = label_font)

        self.select_heuristic_label = tkinter.Label(self.main_window, \
                                        text = "Select Heuristics",
                                        font = label_font)

        # self.output_image_label = tkinter.Label(self.main_window, \
        #                                 text = "Output")

        # ------------
        #   Entries
        # ------------
        self.num_iterations_entry = tkinter.Entry(self.main_window, \
                                            width = 15)
        self.num_iterations_entry.insert(0,"1")

        self.update_terrain_entry = tkinter.Entry(self.main_window, \
                                            width = 15)
        self.update_terrain_entry.insert(0,'150')

        # ------------
        #   Buttons
        # ------------
        # A button for running the program
        self.run_buttom = tkinter.Button(self.main_window, \
                                            #text = "Run",
                                            image = run_img,
                                            border = "0", 
                                            command= self.find_path)
        
        # ----------------------
        #   Input Checkbuttons
        # ----------------------
        self.cb_road_config_tree = tkinter.Checkbutton(self.main_window, \
                                            text = "Road-Config-Treet",
                                            font = text_font,
                                            variable = self.cb_road_config_tree_var)

        self.cb_road_config_tree_sidewalks = tkinter.Checkbutton(self.main_window, \
                                            text = "Road-Config-Treet-Sidewalks",
                                            font = text_font,
                                            variable = self.cb_road_config_tree_sidewalks_var)

        self.cb_road_config_garden = tkinter.Checkbutton(self.main_window, \
                                            text = "Road-Config-Treet-Garden",
                                            font = text_font,
                                            variable = self.cb_road_config_garden_var)

        self.cb_road_config_aldrich_park = tkinter.Checkbutton(self.main_window, \
                                            text = "Road-Config-Treet-Aldrich-Park",
                                            font = text_font,
                                            variable = self.cb_road_config_aldrich_park_var)

        self.cb_basic = tkinter.Checkbutton(self.main_window, \
                                            text = "Basic",
                                            font = text_font,
                                            variable = self.cb_basic_var)

        self.cb_basic_v2 = tkinter.Checkbutton(self.main_window, \
                                            text = "Basic_v2",
                                            font = text_font,
                                            variable = self.cb_basic_v2_var)

        # ---------------------------
        #   Heuristics Checkbuttons
        # ---------------------------
        self.cb_best_first = tkinter.Checkbutton(self.main_window, \
                                            text = "Best-First",
                                            font = text_font,
                                            variable = self.cb_best_first_var)

        self.cb_astar = tkinter.Checkbutton(self.main_window, \
                                            text = "A*",
                                            font = text_font,
                                            variable = self.cb_astar_var)

        self.cb_beam = tkinter.Checkbutton(self.main_window, \
                                            text = "Beam",
                                            font = text_font,
                                            variable = self.cb_beam_var)
    
        self.cb_human = tkinter.Checkbutton(self.main_window, \
                                            text = "Human",
                                            font = text_font,
                                            variable = self.cb_human_var)

        # ------------------
        #   Creating Grid
        # ------------------
        self.title_label.grid(row = 0, column = 0, columnspan = 4)
        self.run_buttom.grid(row = 0, column = 5, padx = (0,40))

        self.num_iter_label.grid(row = 1, column = 0, padx = "5")
        self.num_iterations_entry.grid(row = 1, column = 1, sticky = "W")

        self.update_terrain_label.grid(row = 1, column = 2, sticky = "E", padx = "5")
        self.update_terrain_entry.grid(row = 1, column = 3, sticky = "W")

        self.select_input_label.grid(row = 4, column = 2, pady = (15,5))
        self.cb_road_config_tree.grid(row = 5, column = 2, sticky = "W")
        self.cb_road_config_tree_sidewalks.grid(row = 6, column = 2, sticky = "W")
        self.cb_road_config_garden.grid(row = 7, column = 2, sticky = "W")
        self.cb_road_config_aldrich_park.grid(row = 8, column = 2, sticky = "W")
        self.cb_basic.grid(row = 9, column = 2, sticky = "W")
        self.cb_basic_v2.grid(row = 10, column = 2, sticky = "W")

        self.select_heuristic_label.grid(row = 4, column = 0, pady = (15,5))
        self.cb_best_first.grid(row = 5, column = 0, sticky = "W")
        self.cb_astar.grid(row = 6, column = 0, sticky = "W")
        self.cb_beam.grid(row = 7, column = 0, sticky = "W")
        self.cb_human.grid(row = 8, column = 0, sticky = "W")

        # self.output_image_label.grid(row = 4, column = 2)

        # --------------------
        #   Display the menu
        # --------------------
        self.main_window.config(menu=self.menubar)

        # -------------------------------
        #   Enter the tkinter main loop
        # -------------------------------
        tkinter.mainloop()

    # This function will call paths.py to start finding paths
    def find_path(self):
        #road_configs = ["basic_v2"]
        #strategies = ["best-first"]

        road_configs = []
        strategies = []

        #road_configs = ["road-config-tree-sidewalks", "road-config-garden", "road-config-aldrich-park", "road-config-tree"]

        # Fill in road_configs
        if(self.cb_basic_var.get() == 1):
            road_configs.append("basic")
        if(self.cb_basic_v2_var.get() == 1):
            road_configs.append("basic_v2")
        if(self.cb_road_config_aldrich_park_var.get() == 1):
            road_configs.append("road-config-aldrich-park")
        if(self.cb_road_config_garden_var.get() == 1):
            road_configs.append("road-config-garden")
        if(self.cb_road_config_tree_sidewalks_var.get() == 1):
            road_configs.append("road-config-tree-sidewalks")
        if(self.cb_road_config_tree_var.get() == 1):
            road_configs.append("road-config-tree")

        # Fill in strategies
        if(self.cb_best_first_var.get() == 1):
            strategies.append("best-first")
        if(self.cb_astar_var.get() == 1):
            strategies.append("astar")
        if(self.cb_human_var.get() == 1):
            strategies.append("human")
        if(self.cb_beam_var.get() == 1):
            strategies.append("beam")

        iterations = int(self.num_iterations_entry.get())
        decrease_grayscale = int(self.update_terrain_entry.get())

        main_backend(strategies, road_configs, iterations, decrease_grayscale)

        tkinter.messagebox.showinfo("I'm back", "Done. Check the output images.")

    def open_img(self):
        full_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        filename = os.path.basename(full_path)
        file_no_ext = os.path.splitext(filename)[0]

        strategies = []
        road_configs = []

        # Fill in road_configs
        road_configs.append(file_no_ext)

        # Fill in strategies
        if(self.cb_best_first_var.get() == 1):
            strategies.append("best-first")
        if(self.cb_astar_var.get() == 1):
            strategies.append("astar")
        if(self.cb_human_var.get() == 1):
            strategies.append("human")
        if(self.cb_beam_var.get() == 1):
            strategies.append("beam")

        iterations = int(self.num_iterations_entry.get())
        decrease_grayscale = int(self.update_terrain_entry.get())
        
        main_backend(strategies, road_configs, iterations, decrease_grayscale)

        tkinter.messagebox.showinfo("I'm back", "Done. Check the output images.")

    def clean_output(self):
        msg_box = tkinter.messagebox.askquestion ('Cleaning output', \
                        'Are you sure you want to clean all output?',icon = 'warning')

        if msg_box == "yes":
            
            # Get the folder to delete
            script_dir = os.path.dirname(__file__)  # Absolute directory of this script
            relative_path = "../output_files/"
            abs_file_path = os.path.join(script_dir, relative_path)

            # delete
            for filename in os.listdir(abs_file_path):
                if filename.endswith('.png'):
                    os.remove(abs_file_path+filename) 

# Create an instance of the MainGUI class
main_gui = MainGUI()