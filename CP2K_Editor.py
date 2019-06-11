#Made by Andreas Vishart
#Python 2 or 3 can be used for the script, if an input file is given after the script
#the parameters of the input file is loaded into CP2K_Editor interface
#---------------Package----------------
import os
import sys

#PROGRAM SETTINGS
PROGRAM={}
#The name of the program
PROGRAM["Program_name"]="CP2K Editor"
PROGRAM["Script_name"]="CP2K_Editor.py"

#Python 3
if str(sys.version)[0]=="3":
    import tkinter as tk
    from tkinter import filedialog
    import scr.coord_file_info as coord_file_info
    import scr.program_to_input as program_to_input
    import scr.default_parameters as default_parameters
    import scr.program_to_input_cdft as program_to_input_cdft
#Python 2
elif str(sys.version)[0]=="2":
    sys.path.insert(0, str(os.path.realpath(__file__))[:-len(PROGRAM["Script_name"])]+'scr/')
    import Tkinter as tk
    import tkFileDialog as filedialog
    import coord_file_info as coord_file_info
    import program_to_input as program_to_input
    import default_parameters as default_parameters
    import program_to_input_cdft as program_to_input_cdft
                
#---------------Parameters----------------
#Path to Script
PROGRAM["Path"]=str(os.path.realpath(__file__))[:-len(PROGRAM["Script_name"])]
#Size of the windows
PROGRAM["size_of_window_width"]=800
PROGRAM["size_of_window_height"]=750
PROGRAM["size_of_window_height_top_bottom"]=50
PROGRAM["size_of_window_height_middle"]=PROGRAM["size_of_window_width"]-2*PROGRAM["size_of_window_height_top_bottom"]
PROGRAM["pady_section_size"]=30
PROGRAM["pady_line_size"]=5
PROGRAM["padx_section_size"]=0.05*PROGRAM["size_of_window_width"]

#Load default parameters
GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION,BASIS_SET,POTENTIAL=default_parameters.default_parameters(PROGRAM)

#If an input file is given after the program the parameters from the input file is used
if len(sys.argv)>1:
    if str(sys.version)[0]=="3":
        import scr.import_output as import_output
    elif str(sys.version)[0]=="2":
        import import_output as import_output
    GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION=import_output.load_parameters(sys.argv[1],PROGRAM)

class Window_Frame:
    def __init__(self,master):
        #self.master=master
        master.geometry(str(PROGRAM["size_of_window_width"])+"x"+str(PROGRAM["size_of_window_height"])+"+0+0")
        #Window can not change size
        master.resizable(width=False, height=False)
        #Title of window
        master.title(PROGRAM["Program_name"])
        
        #Menubar
        master.Menubar_Top=Menubar(master)

        #Top Frame
        self.Top_Frame=tk.Frame(master,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_top_bottom"]),relief=tk.SUNKEN)
        self.Top_Frame.pack(side=tk.TOP)
        
        #Bottom Frame
        self.Bottom_Frame=tk.Frame(master,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_top_bottom"]),relief=tk.SUNKEN)
        self.Bottom_Frame.pack(side=tk.BOTTOM,pady=PROGRAM["pady_section_size"])
        #Execute Bottom frame part
        

        #Middle Frame
        self.Middle_Frame=tk.Frame(master,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_middle"]),relief=tk.SUNKEN)
        self.Middle_Frame.pack(pady=(PROGRAM["pady_section_size"],0),padx=PROGRAM["padx_section_size"],fill="both",expand=True)

        #Execute Top frame part and all frames of the middle frame
        self.Top_F=Top_Frame_part(self.Top_Frame,self.Middle_Frame)
        self.Bottom_F=Bottom_Frame_part(self.Bottom_Frame,self.Top_F)



#Setting up the Menu------
class Menubar:
    def __init__(self,master):  
        self.menubar=tk.Menu(master)
        master.config(menu=self.menubar)
        #Filemenu
        self.filemenu=tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="New", command=self.new_input)
        self.filemenu.add_command(label="Open", command=lambda: self.open_input(master))
        self.filemenu.add_command(label="Save", command=Bottom_Frame_part.Save)
        self.filemenu.add_command(label="About", command=self.popup_About)
        self.filemenu.add_command(label="Exit", command=Bottom_Frame_part.popup_exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        #Function
        self.functionmenu=tk.Menu(self.menubar,tearoff=0)
        self.functionmenu.add_command(label="Cutoff test", command=lambda: self.Generate_cutoff_test(master))
        self.menubar.add_cascade(label="Function", menu=self.functionmenu)
        #Analyse
        self.analysemenu=tk.Menu(self.menubar,tearoff=0)
        self.analysemenu.add_command(label="CDFT charge", command=self.CDFT_charge_function)
        self.analysemenu.add_command(label="CDFT coupling", command=self.CDFT_details_function)
        self.analysemenu.add_command(label="Convergence", command=lambda: self.Convergence_function(master))
        self.analysemenu.add_command(label="Cutoff test", command=lambda: self.Analyse_cutoff_test_function(master))
        self.analysemenu.add_command(label="Geometry", command=lambda: self.Analyse_geometry_function(master))
        self.analysemenu.add_command(label="MD energy", command=lambda: self.MD_energy_temp_function(master))
        self.analysemenu.add_command(label="Optimization", command=lambda: self.Optimization_function(master))
        self.analysemenu.add_command(label="UV-Vis", command=lambda: self.UV_Vis_function(master))
        self.analysemenu.add_command(label="Vibrations", command=lambda: self.Vib_function(master))
        self.menubar.add_cascade(label="Analyse", menu=self.analysemenu)
        #Helpmenu
        self.helpmenu=tk.Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.Help)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
    
    #File

    #New input file window
    def new_input(self):
        os.system(str(sys.executable)+" "+PROGRAM["Path"]+PROGRAM["Script_name"])

    #Open an input file
    def open_input(self,master):
        if str(sys.version)[0]=="3":
            import scr.import_output as import_output
        elif str(sys.version)[0]=="2":
            import import_output as import_output
        inputfile=filedialog.askopenfilename(initialdir="./",title = "Select Input file",filetypes = (("Inp files","*.inp"),("all files","*")))
        master.update()
        if inputfile!="":
            os.system(str(sys.executable)+" "+PROGRAM["Path"]+PROGRAM["Script_name"]+" "+str(inputfile))

    #About pop up window
    def popup_About(self):
        popup=tk.Tk()
        popup.title("About")
        popup.geometry("500x"+str(int(PROGRAM["size_of_window_height"]*0.2))+"+0+0")
        B_Okay=tk.Button(popup, text="  Okay  ", command = popup.destroy)
        B_Okay.pack(side=tk.BOTTOM)
        with open(PROGRAM["Path"]+"scr/ABOUT.txt") as about_file:
            About_content=about_file.read()
        label=tk.Text(popup, height=int(PROGRAM["size_of_window_height"]*0.8), width=500)
        label.pack(side=tk.LEFT, fill=tk.Y)
        label.insert(tk.END, About_content)
        label.config(state=tk.DISABLED,wrap=tk.WORD)
        popup.mainloop()

    #Help

    #Open the Help 
    def Help(self):
        popup=tk.Tk()
        popup.title("Help")
        popup.geometry("500x"+str(int(PROGRAM["size_of_window_height"]*0.85))+"+0+0")
        B_Close=tk.Button(popup, text="  Close  ", command = popup.destroy)
        B_Close.pack(side=tk.BOTTOM)
        with open(PROGRAM["Path"]+"scr/HELP.txt") as help_file:
            Help_content=help_file.read()
        scrollbar=tk.Scrollbar(popup)
        label=tk.Text(popup, height=int(PROGRAM["size_of_window_height"]*0.8), width=500)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        label.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.config(command=label.yview)
        label.config(yscrollcommand=scrollbar.set)
        label.insert(tk.END, Help_content)
        label.config(state=tk.DISABLED,wrap=tk.WORD)
        popup.mainloop()

    #Function
    #Generate Cutoff test
    def Generate_cutoff_test(self,master):
        generate_cutoff_file=filedialog.askopenfilename(initialdir="./",title = "Select input file",filetypes = (("INP files","*.inp"),("all files","*")))
        master.update()
        if str(generate_cutoff_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Function_generate_cutoff_test as Function_generate_cutoff_test
            elif str(sys.version)[0]=="2":
                import Function_generate_cutoff_test as Function_generate_cutoff_test
            Function_generate_cutoff_test.popup_generate_cutoff(generate_cutoff_file)        


    #Analyse 

    #CDFT charge on fragments details
    def CDFT_charge_function(self):
        if str(sys.version)[0]=="3":
            import scr.Analyse_CDFT_charge as Analyse_CDFT_charge
        elif str(sys.version)[0]=="2":
            import Analyse_CDFT_charge as Analyse_CDFT_charge
        try:
            popup_cdft_start=Analyse_CDFT_charge.CDFT_start_popup()
        except:
            popup_cdft_start=Bottom_Frame_part.popup_error_file(self,cdft_detail_file)
        popup_cdft_start.mainloop()

    #CDFT electronic coupling details
    def CDFT_details_function(self):
        cdft_detail_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
        if str(cdft_detail_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_CDFT as Analyse_CDFT
            elif str(sys.version)[0]=="2":
                import Analyse_CDFT as Analyse_CDFT
            try:
                popup_cdft=Analyse_CDFT.CDFT_popup(cdft_detail_file)
            except:
                popup_cdft=Bottom_Frame_part.popup_error_file(self,cdft_detail_file)
            popup_cdft.mainloop()

    #Convergence (Is the file converged properly)
    def Convergence_function(self,master):
        convergence_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
        master.update()
        if str(convergence_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_Convergence as Analyse_Convergence
            elif str(sys.version)[0]=="2":
                import Analyse_Convergence as Analyse_Convergence
            try:
                popup_conv=Analyse_Convergence.Convergence_popup(convergence_file)
            except:
                popup_conv=Bottom_Frame_part.popup_error_file(self,convergence_file)
            popup_conv.mainloop()

    #Analyse Cutoff test
    def Analyse_cutoff_test_function(self,master):
        cutoff_folder=filedialog.askdirectory(initialdir="./",title = "Select cutoff test folder")
        master.update()
        if str(cutoff_folder)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_cutoff_test as Analyse_cutoff_test
            elif str(sys.version)[0]=="2":
                import Analyse_cutoff_test as Analyse_cutoff_test
            try:
                cutoff_analyse_data=Analyse_cutoff_test.Cutoff_test(cutoff_folder)
            except:
                popup=tk.Tk()
                popup.title("No such folder")
                tk.Label(popup, text="Could not find or use the folder called "+str(cutoff_folder)).pack()
                tk.Button(popup, text="  Okay  ", command = popup.destroy).pack()
                popup.mainloop()
            else:
                Analyse_cutoff_test.plot_cutoff_test(cutoff_analyse_data)

    #Geometry Optimization
    def Analyse_geometry_function(self,master):
        geometry_file=filedialog.askopenfilename(initialdir="./",title = "Select position file",filetypes = (("XYZ files","*.xyz"),("all files","*")))
        master.update()
        if str(geometry_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_Geometry as Analyse_Geometry
            elif str(sys.version)[0]=="2":
                import Analyse_Geometry as Analyse_Geometry
            try:
                Geometry_analyse_data=Analyse_Geometry.coord_file_extract(geometry_file)
            except:
                Bottom_Frame_part.popup_error_file(self,geometry_file)
            else:
                Analyse_Geometry.plot_Geometry(Geometry_analyse_data)

    #Energy and Temperature plot for MD
    def MD_energy_temp_function(self,master):
        md_e_t_file=filedialog.askopenfilename(initialdir="./",title = "Select energy file",filetypes = (("ENER files","*.ener"),("all files","*")))
        master.update()
        if str(md_e_t_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_MD_Ener as Analyse_MD_Ener
            elif str(sys.version)[0]=="2":
                import Analyse_MD_Ener as Analyse_MD_Ener
            try:
                MD_analyse_data=Analyse_MD_Ener.MD_Ener(md_e_t_file)
            except:
                Bottom_Frame_part.popup_error_file(self,md_e_t_file)
            else:
                Analyse_MD_Ener.plot_MD_Ener(MD_analyse_data)

    #Geometry Optimization
    def Optimization_function(self,master):
        optimization_file=filedialog.askopenfilename(initialdir="./",title = "Select position file",filetypes = (("XYZ files","*.xyz"),("all files","*")))
        master.update()
        if str(optimization_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_Optimization as Analyse_Optimization
            elif str(sys.version)[0]=="2":
                import Analyse_Optimization as Analyse_Optimization
            try:
                Optimization_analyse_data=Analyse_Optimization.Optimization(optimization_file)
            except:
                Bottom_Frame_part.popup_error_file(self,optimization_file)
            else:
                Analyse_Optimization.plot_Optimization(Optimization_analyse_data)

    #UV-Vis spectrum
    def UV_Vis_function(self,master):
        uvvis_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
        master.update()
        if str(uvvis_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_UV_Vis as Analyse_UV_Vis
            elif str(sys.version)[0]=="2":
                import Analyse_UV_Vis as Analyse_UV_Vis
            try:
                popup_uv_vis=Analyse_UV_Vis.UV_Vis_pop_up(uvvis_file)
            except:
                popup_uv_vis=Bottom_Frame_part.popup_error_file(self,uvvis_file)
            popup_uv_vis.mainloop()

    #Vibrational spectrum
    def Vib_function(self,master):
        vib_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
        master.update()
        if str(vib_file)!="":
            if str(sys.version)[0]=="3":
                import scr.Analyse_Vib as Analyse_Vib
            elif str(sys.version)[0]=="2":
                import Analyse_Vib as Analyse_Vib
            try:
                popup_vib=Analyse_Vib.Vibration_popup(vib_file)
            except:
                popup_vib=Bottom_Frame_part.popup_error_file(self,vib_file)
            popup_vib.mainloop()



#Make the Bottom-----
class Bottom_Frame_part:
    def __init__(self,Bot_F,Top_F):
        #Rows and Columns
        i=0;j=0
        #The button for save to input file
        self.save_btn=tk.Button(Bot_F,text="SAVE",width=10,command=lambda type=type: self.Save(Top_F))
        self.save_btn.grid(row=i,column=j)
        j+=1
        #The button for Preview to input file
        self.preview_btn=tk.Button(Bot_F,text="PREVIEW",width=10,command=lambda type=type: self.Preview(Top_F))
        self.preview_btn.grid(row=i,column=j)
        j+=1
        #The button for cancel program
        self.cancel_btn=tk.Button(Bot_F,text="CANCEL",width=10,command=self.popup_exit)
        self.cancel_btn.grid(row=i,column=j)
        j+=1

    #Exit the program
    def Exit(self,popup):
        popup.destroy()
        CP2K_Editor.destroy()

    #Exit pop up window
    def popup_exit(self):
        popup=tk.Tk()
        popup.title("Exit")
        self.label=tk.Label(popup, text="Do you want to exit "+PROGRAM["Program_name"]+"?")
        self.label.grid(row=0,column=1)
        self.B1=tk.Button(popup, text="Yes",width=5, command=lambda popup=popup: self.Exit(popup))
        self.B1.grid(row=1,column=0,)
        self.B2=tk.Button(popup, text="No",width=5, command=popup.destroy)
        self.B2.grid(row=1,column=2)
        popup.mainloop()

    #Save the input file
    def Save(self,Top_F):
        global GLOBAL
        global FORCE_EVAL
        global SUBSYS
        global EXT_RESTART
        global MOTION
        self.save_entries(Top_F)
        self.popup_save_file()
    
    #Save the input file as 
    def popup_save_file(self):
        global GLOBAL
        input_filename=filedialog.asksaveasfilename(initialdir = "./",initialfile=GLOBAL["FILE_NAME"],title = "Save input file as",filetypes = (("INP files","*.inp"),("all files","*")))
        if input_filename!="":
            GLOBAL["FILE_NAME"]=input_filename
            if GLOBAL["PROPERTIES"]=="CDFT":
                inputfile_content=program_to_input_cdft.Save_cdft_files(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
            else:
                inputfile_content=program_to_input.Save_to_input(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
            the_inputfile=open(input_filename,"w")
            the_inputfile.write(inputfile_content)
            the_inputfile.close()
            self.popup_save()

        #Save the input file
    def Save_Edit(self,Top_F):
        global GLOBAL
        global FORCE_EVAL
        global SUBSYS
        global EXT_RESTART
        global MOTION
        self.save_entries(Top_F)
        self.inputfile_content=self.label.get(1.0,tk.END)
        self.popup_save_file_edit(self.inputfile_content)

    #Save the input file as 
    def popup_save_file_edit(self,inputfile_content):
        global GLOBAL
        input_filename=filedialog.asksaveasfilename(initialdir = "./",initialfile=GLOBAL["FILE_NAME"],title = "Save input file as",filetypes = (("INP files","*.inp"),("all files","*")))
        if input_filename!="":
            GLOBAL["FILE_NAME"]=input_filename
            the_inputfile=open(input_filename,"w")
            the_inputfile.write(inputfile_content)
            the_inputfile.close()
            self.popup_save()

    #The input file is saved pop up window
    def popup_save(self):
        popup=tk.Tk()
        popup.title("Saved")
        self.label=tk.Label(popup, text="The input file is saved as "+GLOBAL["FILE_NAME"])
        self.label.grid(row=0)
        self.B1=tk.Button(popup, text="  Okay  ", command=popup.destroy)
        self.B1.grid(row=1)
        popup.mainloop()

    #Error could not find such file
    def popup_error_file(self,filename):
        popup_error=tk.Tk()
        popup_error.title("No such file")
        tk.Label(popup_error, text="Could not find or use the file called "+str(filename)).pack()
        tk.Button(popup_error, text="  Okay  ", command=popup_error.destroy).pack()
        return popup_error

    #Preview input file
    def Preview(self,Top_F):
        global GLOBAL
        global FORCE_EVAL
        global SUBSYS
        global EXT_RESTART
        global MOTION
        self.save_entries(Top_F)
        popup=tk.Tk()
        popup.title("Preview")
        popup.geometry("500x"+str(int(PROGRAM["size_of_window_height"]*0.85))+"+0+0")
        if GLOBAL["PROPERTIES"]=="CDFT":
            self.inputfile_content=program_to_input_cdft.Save_cdft_files(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
        else:
            self.inputfile_content=program_to_input.Save_to_input(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
        self.B_Close=tk.Button(popup, text="  Close  ", command = popup.destroy)
        self.B_Close.pack(side=tk.BOTTOM)
        self.B_Save=tk.Button(popup, text="  Save  ",command=lambda: self.Save_Edit(Top_F))
        self.B_Save.pack(side=tk.BOTTOM)
        scrollbar=tk.Scrollbar(popup)
        self.label=tk.Text(popup, height=int(PROGRAM["size_of_window_height"]*0.8), width=500)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.label.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.config(command=self.label.yview)
        self.label.config(yscrollcommand=scrollbar.set)
        self.label.insert(tk.END, self.inputfile_content)
        #self.label.config(state=tk.DISABLED)
        popup.mainloop()

    #Save all the entries
    def save_entries(self,Top_F):
        global GLOBAL
        global FORCE_EVAL
        global SUBSYS
        global EXT_RESTART
        global MOTION
        GLOBAL["PROJECT_NAME"]=Top_F.Global_sec.project_name_entry.get()
        GLOBAL["NSTATES"]=Top_F.Global_sec.properties_info_nstates_entry.get()
        GLOBAL["FILE_NAME"]=GLOBAL["PROJECT_NAME"]+".inp"
        FORCE_EVAL["EACH"]=Top_F.Global_sec.each_entry.get()
        if FORCE_EVAL["BASIS_SET"]=="Custom":
            FORCE_EVAL["BASIS_SET"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_basis_set_entry.get()
        if FORCE_EVAL["POTENTIAL"]=="Custom":
            FORCE_EVAL["POTENTIAL"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_potential_entry.get()
        FORCE_EVAL["LIBXC"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_XC_functional_custom_entry.get()
        FORCE_EVAL["FRACTION"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_HF_X_entry.get()
        FORCE_EVAL["MAX_SCF"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_MAX_SCF_entry.get()
        FORCE_EVAL["EPS_SCF"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_EPS_SCF_entry.get()
        FORCE_EVAL["NGRIDS"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_NGRIDS_entry.get()
        FORCE_EVAL["CUTOFF"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_PW_Cutoff_entry.get()
        FORCE_EVAL["REL_CUTOFF"]=Top_F.FORCE_EVAL_sec.Force_Eval_DFT_sec.FE_Gau_Cutoff_entry.get()
        FORCE_EVAL["PARM_FILE_NAME"]=Top_F.FORCE_EVAL_sec.Force_Eval_FF_sec.FE_parm_file_entry.get()
        SUBSYS["COORD"]=Top_F.SUBSYS_sec.SS_coord_file_entry.get()
        SUBSYS["ABC"]=Top_F.SUBSYS_sec.SS_Cell_entry.get()
        SUBSYS["CHARGE"]=Top_F.SUBSYS_sec.SS_Charge_entry.get()
        SUBSYS["FIXED"]=Top_F.SUBSYS_sec.SS_fixed_atoms_entry.get()
        SUBSYS["TARGET1"]=Top_F.SUBSYS_sec.SS_target1_entry.get()
        SUBSYS["TARGET2"]=str(float(SUBSYS["TARGET1"])+2)
        SUBSYS["ATOMS_FRAG1"]=Top_F.SUBSYS_sec.SS_frag1_entry.get()
        SUBSYS["ATOMS_FRAG2"]=Top_F.SUBSYS_sec.SS_frag2_entry.get()
        EXT_RESTART["RESTART_EACH"]=Top_F.EXT_RESTART_sec.save_restart_entry.get()
        EXT_RESTART["RESTART_FILE_NAME"]=Top_F.EXT_RESTART_sec.restart_entry.get()
        MOTION["MAX_DR"]=Top_F.MOTION_sec.MT_Geo_sec.MT_Geo_Max_Dr_entry.get()
        MOTION["MAX_ITER"]=Top_F.MOTION_sec.MT_Geo_sec.MT_Geo_Max_Iter_entry.get()
        MOTION["STEPS"]=Top_F.MOTION_sec.MT_MD_sec.MT_MD_steps_entry.get()
        MOTION["TIMESTEP"]=Top_F.MOTION_sec.MT_MD_sec.MT_MD_timestep_entry.get()
        MOTION["TEMPERATURE"]=Top_F.MOTION_sec.MT_MD_sec.MT_MD_temperature_entry.get()
        MOTION["TIMECON"]=Top_F.MOTION_sec.MT_MD_sec.MT_MD_TIMECON_entry.get()
        MOTION["REPLICA1"]=Top_F.MOTION_sec.MT_BAND_sec.MT_BAND_initial_entry.get()
        MOTION["REPLICA2"]=Top_F.MOTION_sec.MT_BAND_sec.MT_BAND_interm_entry.get()
        MOTION["REPLICA3"]=Top_F.MOTION_sec.MT_BAND_sec.MT_BAND_final_entry.get()
        MOTION["NUMBER_OF_REPLICA"]=Top_F.MOTION_sec.MT_BAND_sec.MT_BAND_num_replica_entry.get()
        MOTION["MAX_STEPS"]=Top_F.MOTION_sec.MT_BAND_sec.MT_BAND_max_steps_entry.get()

#Make the Top------
class Top_Frame_part:
    def __init__(self,Top_F,Middle_F):
        #Rows and Columns
        i=0;j=0
        #The button for the section &Global
        self.sec_global=tk.Button(Top_F,text="&GLOBAL",width=15,fg="green",command=self.GLOBAL_Frame_btn_func)
        self.sec_global.grid(row=i,column=j)
        self.GLOBAL_F=tk.Frame(Middle_F)
        self.GLOBAL_F.place(in_=Middle_F, x=0, y=0, relwidth=1, relheight=1)
        self.Global_sec=Global_section(self.GLOBAL_F,self)
        j+=1
        #The button for the section &Force_Eval
        self.sec_force_eval=tk.Button(Top_F,text="&FORCE_EVAL",width=15,fg="green",command=self.FORCE_EVAL_Frame_btn_func)
        self.sec_force_eval.grid(row=i,column=j)
        self.FORCE_EVAL_F=tk.Frame(Middle_F)
        self.FORCE_EVAL_F.place(in_=Middle_F, x=0, y=0, relwidth=1, relheight=1)
        self.FORCE_EVAL_sec=Force_Eval_section(self.FORCE_EVAL_F)
        j+=1
        
        #The button for the section &Subsys
        self.sec_subsys=tk.Button(Top_F,text="&SUBSYS",width=15,fg="green",command=self.SUBSYS_Frame_btn_func)
        self.sec_subsys.grid(row=i,column=j)
        self.SUBSYS_F=tk.Frame(Middle_F)
        self.SUBSYS_F.place(in_=Middle_F, x=0, y=0, relwidth=1, relheight=1)
        self.SUBSYS_sec=Subsys_section(self.SUBSYS_F)
        j+=1
        
        #The button for the section EXT_RESTART
        self.sec_ext_restart=tk.Button(Top_F,text="&EXT_RESTART",width=15,fg="green",command=self.EXT_RESTART_Frame_btn_func)
        self.sec_ext_restart.grid(row=i,column=j)
        self.EXT_RESTART_F=tk.Frame(Middle_F)
        self.EXT_RESTART_F.place(in_=Middle_F, x=0, y=0, relwidth=1, relheight=1)
        self.EXT_RESTART_sec=Ext_section(self.EXT_RESTART_F)
        j+=1
        
        #The button for the section &MOTION
        self.sec_motion=tk.Button(Top_F,text="&MOTION",width=15,fg="green",state=tk.DISABLED,command=self.MOTION_sec_Frame_func)
        self.sec_motion.grid(row=i,column=j)
        self.MOTION_F=tk.Frame(Middle_F)
        self.MOTION_F.place(in_=Middle_F, x=0, y=0, relwidth=1, relheight=1)
        self.MOTION_sec=Motion_section(self.MOTION_F)
        j+=1
        
        #Activate Global section first
        self.sec_global.config(fg="blue")
        self.GLOBAL_F.lift()
    
    #Global command when Global section button is pressed
    def GLOBAL_Frame_btn_func(self):
        self.GLOBAL_F.lift()
        self.sec_global.config(fg="blue")
        self.sec_force_eval.config(fg="green")
        self.sec_subsys.config(fg="green")
        self.sec_ext_restart.config(fg="green")
        self.sec_motion.config(fg="green")

    #FORCE_EVAL command when FORCE_EVAL section button is pressed
    def FORCE_EVAL_Frame_btn_func(self):
        self.FORCE_EVAL_F.lift()
        self.sec_global.config(fg="green")
        self.sec_force_eval.config(fg="blue")
        self.sec_subsys.config(fg="green")
        self.sec_ext_restart.config(fg="green")
        self.sec_motion.config(fg="green")

    #SUBSYS command when SUBSYS section button is pressed
    def SUBSYS_Frame_btn_func(self):
        self.SUBSYS_F.lift()
        self.sec_global.config(fg="green")
        self.sec_force_eval.config(fg="green")
        self.sec_subsys.config(fg="blue")
        self.sec_ext_restart.config(fg="green")
        self.sec_motion.config(fg="green")

    #EXT_RESTART command when EXT_RESTART section button is pressed
    def EXT_RESTART_Frame_btn_func(self):
        self.EXT_RESTART_F.lift()
        self.sec_global.config(fg="green")
        self.sec_force_eval.config(fg="green")
        self.sec_subsys.config(fg="green")
        self.sec_ext_restart.config(fg="blue")
        self.sec_motion.config(fg="green")

    #MOTION command when MOTION section button is pressed
    def MOTION_sec_Frame_func(self):
        self.MOTION_F.lift()
        self.sec_global.config(fg="green")
        self.sec_force_eval.config(fg="green")
        self.sec_subsys.config(fg="green")
        self.sec_ext_restart.config(fg="green")
        self.sec_motion.config(fg="blue")

#Make the &Global_section------
class Global_section:
    def __init__(self,GLOBAL_Frame,Top_Frame_p):
        #Choose the Run Type
        #Rows and 
        i=0;j=0
        #Make the label for Run_Type
        self.label_runtype=tk.Label(GLOBAL_Frame,text="Run type: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Run_Type button
        self.run_type_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["RUN_TYPE"])
        #Give it the function as a push down list / Menu
        self.content_run_type_btn=tk.Menu(self.run_type_btn)
        #So you can press the button and have the content
        self.run_type_btn.config(menu=self.content_run_type_btn)
        self.run_type_btn.grid(row=i,column=j,sticky="WE")
        
        #Give the options of Run_Types
        run_type_list=["ENERGY","GEO_OPT","MD","BAND","RT_PROPAGATION"]
        for types in run_type_list:
            self.content_run_type_btn.add_command(label=types,command=lambda types=types: self.Run_Type_button_click(types,Top_Frame_p))
        
        #Choose the Project Name
        #Rows and 
        i+=1;j=0
        #Make the label for Project Name
        tk.Label(GLOBAL_Frame, text="Project name: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry
        self.project_name_entry=tk.Entry(GLOBAL_Frame)
        #Set the text to the right
        self.project_name_entry.config(justify=tk.LEFT)
        #Give the default Project Name
        self.project_name_entry.insert(tk.END,GLOBAL["PROJECT_NAME"])
        self.project_name_entry.grid(row=i,column=j,sticky="WE")
        
        #Choose the Print level
        i+=1;j=0
        #Make the label for Print_level
        tk.Label(GLOBAL_Frame,text="Print level: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Print_Level button
        self.print_level_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["PRINT_LEVEL"])
        #Give it the function as a push down list / Menu
        self.content_print_level_btn=tk.Menu(self.print_level_btn)
        #So you can press the button and have the content
        self.print_level_btn.config(menu=self.content_print_level_btn)
        self.print_level_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Print_Level
        print_level_list=["SILENT","LOW","MEDIUM","HIGH","DEBUG"]
        for level in print_level_list:
            self.content_print_level_btn.add_command(label=level,command=lambda level=level: self.Print_Level_button_click(level))

        #Choose the Properties
        #Rows and Columns
        i+=1;j=0
        #Make the label for Properties
        tk.Label(GLOBAL_Frame,text="Properties: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Properties button
        self.properties_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["PROPERTIES"])
        #Give it the function as a push down list / Menu
        self.content_properties_btn=tk.Menu(self.properties_btn)
        #So you can press the button and have the content
        self.properties_btn.config(menu=self.content_properties_btn)
        self.properties_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Properties
        properties_list=["NONE","MO","DIPOLE","TDDFPT","VIBRATIONAL_ANALYSIS","MULLIKEN","CDFT"]
        for proper in properties_list:
            self.content_properties_btn.add_command(label=proper,command=lambda proper=proper: self.Properties_button_click(proper,Top_Frame_p))
        #Properties info 
        i+=1
        j=0
        self.properties_info_nstates_label=tk.Label(GLOBAL_Frame,text="NStates: ")
        self.properties_info_nstates_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.properties_info_nstates_entry=tk.Entry(GLOBAL_Frame,justify=tk.LEFT)
        self.properties_info_nstates_entry.insert(tk.END,GLOBAL["NSTATES"])
        self.properties_info_nstates_entry.grid(row=i,column=j,sticky="WE")
        if GLOBAL["PROPERTIES"]!="MO" or GLOBAL["PROPERTIES"]!="TDDFPT":
            self.properties_info_nstates_label.grid_forget()
            self.properties_info_nstates_entry.grid_forget()
        #How often to Print 
        i+=1;j=0
        self.each_label=tk.Label(GLOBAL_Frame,text="Each step: ")
        self.each_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.each_entry=tk.Entry(GLOBAL_Frame,justify=tk.LEFT)
        self.each_entry.insert(tk.END,FORCE_EVAL["EACH"])
        self.each_entry.grid(row=i,column=j,sticky="WE")
        if GLOBAL["RUN_TYPE"]=="ENERGY":
            self.each_label.grid_forget()
            self.each_entry.grid_forget()

    #Choose the Run_Type
    def Run_Type_button_click(self,types,Top_Frame_p):
        global GLOBAL
        GLOBAL["RUN_TYPE"]=types
        self.run_type_btn.config(text=GLOBAL["RUN_TYPE"])
        if GLOBAL["RUN_TYPE"]!="ENERGY":
            Top_Frame_p.sec_motion.config(state="normal")
            Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid(row=9,column=1,sticky="WE")
            if GLOBAL["PROPERTIES"]!="NONE":
                self.each_label.grid(row=6,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                self.each_entry.grid(row=6,column=1,sticky="WE") 
            if GLOBAL["RUN_TYPE"]=="GEO_OPT":
                Top_Frame_p.MOTION_sec.MT_Geo_F.lift()
            elif GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
                Top_Frame_p.MOTION_sec.MT_MD_F.lift()
            elif GLOBAL["RUN_TYPE"]=="BAND":
                Top_Frame_p.MOTION_sec.MT_BAND_F.lift()
        else:
            Top_Frame_p.sec_motion.config(state=tk.DISABLED)
            self.each_label.grid_forget()
            self.each_entry.grid_forget()
            if GLOBAL["PROPERTIES"]=="VIBRATIONAL_ANALYSIS":
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid(row=9,column=1,sticky="WE")
            else:
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid_forget()

    #Choose the Print_Level
    def Print_Level_button_click(self,level):
        global GLOBAL
        GLOBAL["PRINT_LEVEL"]=level
        self.print_level_btn.config(text=GLOBAL["PRINT_LEVEL"])

    #Choose the Properties
    def Properties_button_click(self,proper,Top_Frame_p):
        global GLOBAL
        GLOBAL["PROPERTIES"]=proper
        self.properties_btn.config(text=GLOBAL["PROPERTIES"])
        if GLOBAL["PROPERTIES"]=="NONE":
            self.properties_info_nstates_label.grid_forget()
            self.properties_info_nstates_entry.grid_forget()
            self.each_label.grid_forget()
            self.each_entry.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_target1_label.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_target1_entry.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_frag1_label.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_frag1_entry.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_frag2_label.grid_forget()
            Top_Frame_p.SUBSYS_sec.SS_frag2_entry.grid_forget()
            if GLOBAL["RUN_TYPE"]=="ENERGY":
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid_forget();Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid_forget()
        else:
            if GLOBAL["RUN_TYPE"]!="ENERGY":
                self.each_label.grid(row=6,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                self.each_entry.grid(row=6,column=1)
            if GLOBAL["PROPERTIES"]=="MO" or GLOBAL["PROPERTIES"]=="TDDFPT":
                self.properties_info_nstates_label.grid(row=5,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                self.properties_info_nstates_entry.grid(row=5,column=1,sticky="WE")
            else:
                self.properties_info_nstates_label.grid_forget()
                self.properties_info_nstates_entry.grid_forget()
            if GLOBAL["PROPERTIES"]=="CDFT":
                Top_Frame_p.SUBSYS_sec.SS_frag1_label.grid(row=10,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                Top_Frame_p.SUBSYS_sec.SS_frag1_entry.grid(row=10,column=1,sticky="WE")
                Top_Frame_p.SUBSYS_sec.SS_frag2_label.grid(row=11,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                Top_Frame_p.SUBSYS_sec.SS_frag2_entry.grid(row=11,column=1,sticky="WE")
                Top_Frame_p.SUBSYS_sec.SS_target1_label.grid(row=12,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                Top_Frame_p.SUBSYS_sec.SS_target1_entry.grid(row=12,column=1,sticky="WE")            
            else:
                Top_Frame_p.SUBSYS_sec.SS_target1_label.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_target1_entry.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_frag1_label.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_frag1_entry.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_frag2_label.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_frag2_entry.grid_forget()
            if GLOBAL["PROPERTIES"]=="VIBRATIONAL_ANALYSIS":
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid(row=9,column=1,sticky="WE")
            elif GLOBAL["PROPERTIES"]!="VIBRATIONAL_ANALYSIS" and GLOBAL["RUN_TYPE"]=="ENERGY":
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_label.grid_forget()
                Top_Frame_p.SUBSYS_sec.SS_fixed_atoms_entry.grid_forget()


#Make the &Force_Eval_section------
class Force_Eval_section:
    def __init__(self,FORCE_EVAL_Frame):
        i=0;j=0
        #Make the label for the Method
        tk.Label(FORCE_EVAL_Frame,text="Method: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Method button
        self.FE_method_btn=tk.Menubutton(FORCE_EVAL_Frame,text=FORCE_EVAL["METHOD"])
        #Give it the function as a push down list / Menu
        self.content_FE_method_btn=tk.Menu(self.FE_method_btn)
        #So you can press the button and have the content
        self.FE_method_btn.config(menu=self.content_FE_method_btn)
        self.FE_method_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Methods
        FE_method_list=["EIP","EMBED","FIST","MIXED","QMMM","QUICKSTEP","SIRIUS"]
        for methods in FE_method_list:
            self.content_FE_method_btn.add_command(label=methods,command=lambda methods=methods: self.FE_Method_button_click(methods))
        
        #Make FE method frames!!
        self.FE_DFT_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_DFT_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_DFT_sec=Force_Eval_section_DFT(self.FE_DFT_F)

        self.FE_EIP_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_EIP_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_EIP_sec=Force_Eval_section_EIP(self.FE_EIP_F)

        self.FE_EMBED_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_EMBED_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_EMBED_sec=Force_Eval_section_EMBED(self.FE_EMBED_F)

        self.FE_FIST_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_FIST_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_FF_sec=Force_Eval_section_FF(self.FE_FIST_F)

        self.FE_MIXED_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_MIXED_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_MIXED_sec=Force_Eval_section_Mixed(self.FE_MIXED_F)

        self.FE_QMMM_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_QMMM_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_QMMM_sec=Force_Eval_section_QMMM(self.FE_QMMM_F)

        self.FE_SIRIUS_F=tk.Frame(FORCE_EVAL_Frame)
        self.FE_SIRIUS_F.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
        self.Force_Eval_SIRIUS_sec=Force_Eval_section_SIRIUS(self.FE_SIRIUS_F)


        if FORCE_EVAL["METHOD"].upper()=="QUICKSTEP":
            self.FE_DFT_F.lift()
        elif FORCE_EVAL["METHOD"].upper()=="EIP":
            self.FE_EIP_F.lift()
        elif FORCE_EVAL["METHOD"].upper()=="EMBED":
            self.FE_EMBED_Frame.lift()
        elif FORCE_EVAL["METHOD"].upper()=="FIST":
            self.FE_FIST_F.lift()
        elif FORCE_EVAL["METHOD"].upper()=="MIXED":
            self.FE_MIXED_F.lift()
        elif FORCE_EVAL["METHOD"].upper()=="QMMM":
            self.FE_QMMM_F.lift()
        elif FORCE_EVAL["METHOD"].upper()=="SIRIUS":
            self.FE_SIRIUS_F.lift()


    #Choose the Method
    def FE_Method_button_click(self,method):
        global FORCE_EVAL
        FORCE_EVAL["METHOD"]=method
        self.FE_method_btn.config(text=FORCE_EVAL["METHOD"])
        if FORCE_EVAL["METHOD"]=="QUICKSTEP":
            FORCE_EVAL["METHOD_SECTION"]="DFT"
            self.FE_DFT_F.lift()
        elif FORCE_EVAL["METHOD"]=="EIP":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_EIP_F.lift()
        elif FORCE_EVAL["METHOD"]=="EMBED":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_EMBED_F.lift()
        elif FORCE_EVAL["METHOD"]=="FIST":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_FIST_F.lift()
        elif FORCE_EVAL["METHOD"]=="MIXED":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_MIXED_F.lift()
        elif FORCE_EVAL["METHOD"]=="QMMM":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_QMMM_F.lift()
        elif FORCE_EVAL["METHOD"]=="SIRIUS":
            FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
            self.FE_SIRIUS_F.lift()


#DFT or Quickstep method
class Force_Eval_section_DFT:
    def __init__(self,FE_DFT_Frame):
        #Make label for Basis set file
        i=0;j=0
        tk.Label(FE_DFT_Frame,text="Basis set file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #The path to the basis set folder
        path_to_basis_set0=PROGRAM["Path"]+"data/Basis_set_folder/"
        path_to_basis_set=FORCE_EVAL["BASIS_SET_FILE_NAME"][:-len(FORCE_EVAL["BASIS_SET_FILE_NAME-path"])]
        #The basis set file menu
        self.FE_basis_set_files_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
        #Give it the function as a push down list / Menu
        self.content_FE_basis_set_files_btn=tk.Menu(self.FE_basis_set_files_btn)
        #So you can press the button and have the content
        self.FE_basis_set_files_btn.config(menu=self.content_FE_basis_set_files_btn)
        self.FE_basis_set_files_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of basis set files
        for files in BASIS_SET["BASIS_SETS_NAMES"]:
            self.content_FE_basis_set_files_btn.add_command(label=files,command=lambda files=files: self.basis_set_file_click(files,path_to_basis_set0))
        #Make label for Basis set
        i+=1;j=0
        tk.Label(FE_DFT_Frame,text="Basis set: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #The basis set menu for each basis set file
        self.FE_basis_set_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["BASIS_SET"])
        self.BASIS_SET_OPTIONS={}
        for key in BASIS_SET["BASIS_SETS_NAMES"]:
            #Make each basis set file to its own menu content
            self.BASIS_SET_OPTIONS[key]=tk.Menu(self.FE_basis_set_btn)
            #Give the options of basis set for each file
            for set in BASIS_SET[key]:
                self.BASIS_SET_OPTIONS[key].add_command(label=set,command=lambda set=set: self.basis_set_click(set))
            if key!="Find":
                self.BASIS_SET_OPTIONS[key].add_command(label="Custom",command=lambda set="Custom": self.basis_set_click(set))
        #Basis set menu as default
        #For files in the basis set directory
        if FORCE_EVAL["BASIS_SET_FILE_NAME-path"] in BASIS_SET["BASIS_SETS_NAMES"]:
            self.FE_basis_set_btn.config(menu=self.BASIS_SET_OPTIONS[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]])
        #For files not in the basis set directory
        else:
            FORCE_EVAL["BASIS_SET"]="Custom"
            self.FE_basis_set_btn.config(menu=self.BASIS_SET_OPTIONS["Find"],text=FORCE_EVAL["BASIS_SET"])
        self.FE_basis_set_btn.grid(row=i,column=j,sticky="WE")
        j+=1
        #Make Entry for Basis set file
        self.FE_basis_set_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
        #Give the default Basis set file
        self.FE_basis_set_entry.grid(row=i,column=j,sticky="WE")
        #Select the default basis set
        if FORCE_EVAL["BASIS_SET"]=="Custom":
            self.FE_basis_set_entry.config(state="normal")
        else:
            self.FE_basis_set_entry.config(state=tk.DISABLED)

        #Make label for Potential file
        i+=1
        j=0
        tk.Label(FE_DFT_Frame,text="Pseudopotential file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #The path to the potential folder
        path_to_potential0=PROGRAM["Path"]+"data/Potential_folder/"
        path_to_potential=FORCE_EVAL["POTENTIAL_FILE_NAME"][:-len(FORCE_EVAL["POTENTIAL_FILE_NAME-path"])]
        #The potential file menu
        self.FE_potential_files_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
        #Give it the function as a push down list / Menu
        self.content_FE_potential_files_btn=tk.Menu(self.FE_potential_files_btn)
        #So you can press the button and have the content
        self.FE_potential_files_btn.config(menu=self.content_FE_potential_files_btn)
        self.FE_potential_files_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of potential files
        for files in POTENTIAL["POTENTIALS_NAMES"]:
            self.content_FE_potential_files_btn.add_command(label=files,command=lambda files=files: self.potential_file_click(files,path_to_potential0))
        #Make label for potentials
        i+=1
        j=0
        tk.Label(FE_DFT_Frame,text="Pseudopotential: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #The potential menu for each potential file
        self.FE_potential_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["POTENTIAL"])
        self.POTENTIAL_OPTIONS={}
        for key in POTENTIAL["POTENTIALS_NAMES"]:
            #Make each potential file to its own menu content
            self.POTENTIAL_OPTIONS[key]=tk.Menu(self.FE_potential_btn)
            #Give the options of potential for each file
            for set in POTENTIAL[key]:
                self.POTENTIAL_OPTIONS[key].add_command(label=set,command=lambda set=set: self.potential_click(set))
            if key!="Find" and key!="ECP_POTENTIALS.dat":
                self.POTENTIAL_OPTIONS[key].add_command(label="Custom",command=lambda set="Custom": self.potential_click(set))
        #Potential menu as default
        #For files in the potential directory
        if FORCE_EVAL["POTENTIAL_FILE_NAME-path"] in POTENTIAL["POTENTIALS_NAMES"]:
            self.FE_potential_btn.config(menu=self.POTENTIAL_OPTIONS[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]])
        #For files not in the potential directory
        else:
            FORCE_EVAL["POTENTIAL"]="Custom"
            self.FE_potential_btn.config(menu=self.POTENTIAL_OPTIONS["Find"],text=FORCE_EVAL["POTENTIAL"])
        self.FE_potential_btn.grid(row=i,column=j,sticky="WE")
        j+=1
        #Make Entry for Potential file
        self.FE_potential_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
        #Give the default Basis set file
        self.FE_potential_entry.grid(row=i,column=j,sticky="WE")
        #Select the default potential
        if FORCE_EVAL["POTENTIAL"]=="Custom":
            self.FE_potential_entry.config(state="normal")
        else:
            self.FE_potential_entry.config(state=tk.DISABLED)


        #Exchange-Correlation functional label
        i+=1;j=0
        self.FE_XC_functional_label=tk.Label(FE_DFT_Frame,text="Exchange-Correlation functional:  ")
        self.FE_XC_functional_label.grid(row=i,column=j,pady=PROGRAM["pady_line_size"])
        j+=1
        #Exchange-Correlation functional button
        self.FE_XC_functional_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["XC_FUNCTIONAL"])
        #Give it the function as a push down list / Menu
        self.content_FE_XC_functional_btn=tk.Menu(self.FE_XC_functional_btn)
        #So you can press the button and have the content
        self.FE_XC_functional_btn.config(menu=self.content_FE_XC_functional_btn)
        self.FE_XC_functional_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of XC functionals
        FE_XC_functional_btn_list=["B3LYP","BEEFVDW","BLYP","BP","HCTH120","OLYP","PADE","PBE","PBE0","TPSS","NONE","NO_SHORTCUT","CUSTOM"]
        for functionals in FE_XC_functional_btn_list:
            self.content_FE_XC_functional_btn.add_command(label=functionals,command=lambda functionals=functionals: self.FE_XC_functional_button_click(functionals))
        #Make Entry for XCLIB functioncations when Custom is selected
        j+=1
        self.FE_XC_functional_custom_entry=tk.Entry(FE_DFT_Frame,text=FORCE_EVAL["LIBXC"])
        #Set the text to the left
        self.FE_XC_functional_custom_entry.config(justify=tk.LEFT)
        #Only if XC_functional is custom the entry is active
        if FORCE_EVAL["XC_FUNCTIONAL"]=="CUSTOM":
            self.FE_XC_functional_custom_entry.config(state="normal")
        else:
            self.FE_XC_functional_custom_entry.config(state=tk.DISABLED)
        #make the entry
        self.FE_XC_functional_custom_entry.grid(row=i,column=j,sticky="WE")
        #HF Exchange
        i+=1;j=0
        self.FE_HF_X_label=tk.Label(FE_DFT_Frame,text="HF exchange:  ",justify=tk.LEFT)
        self.FE_HF_X_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_HF_X_var=tk.StringVar()
        self.FE_HF_X_check=tk.Checkbutton(FE_DFT_Frame,variable=self.FE_HF_X_var,onvalue="TRUE",offvalue="FALSE",state=tk.DISABLED,command=self.HF_X_on_off_click)
        self.FE_HF_X_check.deselect()
        self.FE_HF_X_check.grid(row=i,column=j)
        if FORCE_EVAL["XC_FUNCTIONAL"]=="PBE" or FORCE_EVAL["XC_FUNCTIONAL"]=="PADE":
            self.FE_HF_X_check.config(state="normal")
        j+=1
        self.FE_HF_X_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
        self.FE_HF_X_entry.insert(tk.END,FORCE_EVAL["FRACTION"])
        if FORCE_EVAL["HF"]=="TRUE":
            self.FE_HF_X_entry.config(state="normal")
        else:
            self.FE_HF_X_entry.config(state=tk.DISABLED)
        #make the entry
        self.FE_HF_X_entry.grid(row=i,column=j,sticky="WE")
        #Electronic structure method (QS)
        i+=1;j=0
        self.FE_QS_label=tk.Label(FE_DFT_Frame,text="Electronic structure method:  ")
        self.FE_QS_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Electronic structure method (QS) button
        self.FE_QS_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["QS"])
        #Give it the function as a push down list / Menu
        self.content_FE_QS_btn=tk.Menu(self.FE_QS_btn)
        #So you can press the button and have the content
        self.FE_QS_btn.config(menu=self.content_FE_QS_btn)
        self.FE_QS_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Electronic structure methods
        FE_QS_btn_list=["AM1","DFTB","GAPW","GAPW_XC","GPW","LRIGPW","MNDO","MNDOD","OFGPW","PDG","PM3","PM6","PM6-FM","PNNL","RIGPW","RM1"]
        for qs in FE_QS_btn_list:
            self.content_FE_QS_btn.add_command(label=qs,command=lambda qs=qs: self.FE_QS_button_click(qs))

        #VDW Potential (dispersion correction)
        i+=1;j=0
        self.FE_VDW_Pot_label=tk.Label(FE_DFT_Frame,text="Dispersion correction:  ",justify=tk.LEFT)
        self.FE_VDW_Pot_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_VDW_Pot_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["VDW_POTENTIAL"])
        #Give it the function as a push down list / Menu
        self.content_FE_VDW_Pot_btn=tk.Menu(self.FE_VDW_Pot_btn)
        #So you can press the button and have the content
        self.FE_VDW_Pot_btn.config(menu=self.content_FE_VDW_Pot_btn)
        self.FE_VDW_Pot_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of dispersion types
        FE_VDW_Pot_btn_list=["NONE","DFTD2","DFTD3","DFTD3(BJ)"]
        for dis in FE_VDW_Pot_btn_list:
            self.content_FE_VDW_Pot_btn.add_command(label=dis,command=lambda dis=dis: self.FE_VDW_Pot_button_click(dis))

        #SCF subsection in DFT section
        i+=1;j=0
        self.FE_MAX_SCF_label=tk.Label(FE_DFT_Frame,text="MAX SCF cycles:  ",justify=tk.LEFT)
        self.FE_MAX_SCF_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_MAX_SCF_entry=tk.Entry(FE_DFT_Frame)
        self.FE_MAX_SCF_entry.insert(tk.END,FORCE_EVAL["MAX_SCF"])
        self.FE_MAX_SCF_entry.grid(row=i,column=j,sticky="WE",pady=PROGRAM["pady_line_size"])
        i+=1;j=0
        self.FE_EPS_SCF_label=tk.Label(FE_DFT_Frame,text="SCF criteria:  ",justify=tk.LEFT)
        self.FE_EPS_SCF_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_EPS_SCF_entry=tk.Entry(FE_DFT_Frame)
        self.FE_EPS_SCF_entry.insert(tk.END,FORCE_EVAL["EPS_SCF"])
        self.FE_EPS_SCF_entry.grid(row=i,column=j,sticky="WE",pady=PROGRAM["pady_line_size"])
        #DIAGONALIZATION
        i+=1;j=0
        self.FE_Diag_label=tk.Label(FE_DFT_Frame,text="Diagonalization algorithm:  ",justify=tk.LEFT)
        self.FE_Diag_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_Diag_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["DIAGONALIZATION"])
        self.content_FE_Diag_btn=tk.Menu(self.FE_Diag_btn)
        self.FE_Diag_btn.config(menu=self.content_FE_Diag_btn)
        self.FE_Diag_btn.grid(row=i,column=j,sticky="WE")
        FE_Diag_btn_list=["DAVIDSON","FILTER_MATRIX","LANCZOS","OT","STANDARD"]
        for algo in FE_Diag_btn_list:
            self.content_FE_Diag_btn.add_command(label=algo,command=lambda algo=algo: self.FE_Diag_button_click(algo))
        #DIAGONALIZATION predconditioner for OT
        j+=1
        self.FE_OT_pre_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["PRECONDITIONER"])
        self.content_FE_OT_pre_btn=tk.Menu(self.FE_OT_pre_btn)
        self.FE_OT_pre_btn.config(menu=self.content_FE_OT_pre_btn)
        self.FE_OT_pre_btn.grid(row=i,column=j,sticky="WE")
        FE_OT_pre_btn_list=["FULL_ALL","FULL_KINETIC","FULL_SINGLE","FULL_SINGLE_INVERSE","FULL_S_INVERSE","NONE"]
        for pre in FE_OT_pre_btn_list:
            self.content_FE_OT_pre_btn.add_command(label=pre,command=lambda pre=pre: self.FE_OT_pre_button_click(pre))
        if FORCE_EVAL["DIAGONALIZATION"]=="OT":
            self.FE_OT_pre_btn.config(state="normal")
        else:
            self.FE_OT_pre_btn.config(state=tk.DISABLED)
        #MGRID
        i+=1;j=0
        self.FE_NGRIDS_label=tk.Label(FE_DFT_Frame,text="NGRIDS:  ",justify=tk.LEFT)
        self.FE_NGRIDS_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_NGRIDS_entry=tk.Entry(FE_DFT_Frame)
        self.FE_NGRIDS_entry.insert(tk.END,FORCE_EVAL["NGRIDS"])
        self.FE_NGRIDS_entry.grid(row=i,column=j,sticky="WE",pady=PROGRAM["pady_line_size"])
        i+=1;j=0
        self.FE_PW_Cutoff_label=tk.Label(FE_DFT_Frame,text="PW energy cutoff [Ry]:  ",justify=tk.LEFT)
        self.FE_PW_Cutoff_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_PW_Cutoff_entry=tk.Entry(FE_DFT_Frame)
        self.FE_PW_Cutoff_entry.insert(tk.END,FORCE_EVAL["CUTOFF"])
        self.FE_PW_Cutoff_entry.grid(row=i,column=j,sticky="WE",pady=PROGRAM["pady_line_size"])
        i+=1;j=0
        self.FE_Gau_Cutoff_label=tk.Label(FE_DFT_Frame,text="Gaussian energy cutoff [Ry]:  ",justify=tk.LEFT)
        self.FE_Gau_Cutoff_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_Gau_Cutoff_entry=tk.Entry(FE_DFT_Frame)
        self.FE_Gau_Cutoff_entry.insert(tk.END,FORCE_EVAL["REL_CUTOFF"])
        self.FE_Gau_Cutoff_entry.grid(row=i,column=j,sticky="WE",pady=PROGRAM["pady_line_size"])


    #Select the basis set file in the basis set folder 
    def basis_set_file_click(self,files,path_to_basis_set0):
        if files!="Find":
            FORCE_EVAL["BASIS_SET_FILE_NAME-path"]=files
            FORCE_EVAL["BASIS_SET_FILE_NAME"]=path_to_basis_set0+FORCE_EVAL["BASIS_SET_FILE_NAME-path"]
            self.FE_basis_set_files_btn.config(text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
            self.FE_basis_set_btn.config(menu=self.BASIS_SET_OPTIONS[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]])
            FORCE_EVAL["BASIS_SET"]=BASIS_SET[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]][0]
            self.FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
        elif files=="Find":
            basisset_filename=filedialog.askopenfilename(initialdir=path_to_basis_set0,title = "Select Basis Set file",filetypes = (("DAT files","*.dat"),("all files","*")))
            if str(basisset_filename)!="":
                FORCE_EVAL["BASIS_SET_FILE_NAME"]=basisset_filename
                FORCE_EVAL["BASIS_SET_FILE_NAME-path"]=str(basisset_filename.split("/")[-1])
                path_to_basis_set=basisset_filename[:-len(FORCE_EVAL["BASIS_SET_FILE_NAME-path"])]
                self.FE_basis_set_files_btn.config(text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
                FORCE_EVAL["BASIS_SET"]=BASIS_SET["Find"][0]
                self.FE_basis_set_btn.config(menu=self.BASIS_SET_OPTIONS["Find"])
                self.FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
        if FORCE_EVAL["BASIS_SET"]!="Custom":
            self.FE_basis_set_entry.config(state=tk.DISABLED)
        if FORCE_EVAL["BASIS_SET"]=="Custom":
            self.FE_basis_set_entry.config(state="normal")

    #Select the basis set from the basis set file in the basis set folder 
    def basis_set_click(self,set):
        FORCE_EVAL["BASIS_SET"]=set
        self.FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
        if FORCE_EVAL["BASIS_SET"]=="Custom":
            self.FE_basis_set_entry.config(state="normal")
        else:
            self.FE_basis_set_entry.config(state=tk.DISABLED)

    #Select the potential file in the potential folder 
    def potential_file_click(self,files,path_to_potential0):
        if files!="Find":
            FORCE_EVAL["POTENTIAL_FILE_NAME-path"]=files
            FORCE_EVAL["POTENTIAL_FILE_NAME"]=path_to_potential0+FORCE_EVAL["POTENTIAL_FILE_NAME-path"]
            self.FE_potential_files_btn.config(text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
            self.FE_potential_btn.config(menu=self.POTENTIAL_OPTIONS[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]])
            FORCE_EVAL["POTENTIAL"]=POTENTIAL[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]][0]
            self.FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
        elif files=="Find":
            potential_filename=filedialog.askopenfilename(initialdir=path_to_potential0,title = "Select Potential file",filetypes = (("DAT files","*.dat"),("all files","*")))
            if str(potential_filename)!="":
                FORCE_EVAL["POTENTIAL_FILE_NAME-path"]=str(potential_filename.split("/")[-1])
                path_to_potential=potential_filename[:-len(FORCE_EVAL["POTENTIAL_FILE_NAME-path"])]
                FORCE_EVAL["POTENTIAL_FILE_NAME"]=path_to_potential+FORCE_EVAL["POTENTIAL_FILE_NAME-path"]
                self.FE_potential_files_btn.config(text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
                FORCE_EVAL["POTENTIAL"]=POTENTIAL["Find"][0]
                self.FE_potential_btn.config(menu=self.POTENTIAL_OPTIONS["Find"])
                self.FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
        if FORCE_EVAL["POTENTIAL"]!="Custom":
            self.FE_potential_entry.config(state=tk.DISABLED)
        if FORCE_EVAL["POTENTIAL"]=="Custom":
            self.FE_potential_entry.config(state="normal")

    #Select the potential from the potential file in the potential folder 
    def potential_click(self,set):
        FORCE_EVAL["POTENTIAL"]=set
        self.FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
        if FORCE_EVAL["POTENTIAL"]=="Custom":
            self.FE_potential_entry.config(state="normal")
        else:
            self.FE_potential_entry.config(state=tk.DISABLED)

    #Select the Exchange-Correlation
    def FE_XC_functional_button_click(self,functionals):
        global FORCE_EVAL
        FORCE_EVAL["XC_FUNCTIONAL"]=functionals
        self.FE_XC_functional_btn.config(text=FORCE_EVAL["XC_FUNCTIONAL"])
        if FORCE_EVAL["XC_FUNCTIONAL"]=="PBE" or FORCE_EVAL["XC_FUNCTIONAL"]=="PADE":
            self.FE_HF_X_check.config(state="normal")
            self.FE_XC_functional_custom_entry.config(state=tk.DISABLED)
        else:
            if FORCE_EVAL["XC_FUNCTIONAL"]=="CUSTOM":
                self.FE_XC_functional_custom_entry.config(state="normal")
            else:
                self.FE_XC_functional_custom_entry.config(state=tk.DISABLED)
            self.FE_HF_X_check.deselect()
            FORCE_EVAL["HF"]="FALSE"
            self.FE_HF_X_check.config(state=tk.DISABLED)
            self.FE_HF_X_entry.config(state=tk.DISABLED)

    #Turn HF on and off
    def HF_X_on_off_click(self):
        global FORCE_EVAL
        FORCE_EVAL["HF"]=self.FE_HF_X_var.get()
        if FORCE_EVAL["HF"]=="TRUE":
            self.FE_HF_X_entry.config(state="normal")
        else:
            self.FE_HF_X_entry.config(state=tk.DISABLED)

    #Select the electronic structure method (QS)
    def FE_QS_button_click(self,qs):
        global FORCE_EVAL
        FORCE_EVAL["QS"]=qs
        self.FE_QS_btn.config(text=FORCE_EVAL["QS"])

    #Turn dispersion correction on and off
    def FE_VDW_Pot_button_click(self,dis):
        global FORCE_EVAL
        FORCE_EVAL["VDW_POTENTIAL"]=dis
        self.FE_VDW_Pot_btn.config(text=FORCE_EVAL["VDW_POTENTIAL"])

    #Select the diagonalization method
    def FE_Diag_button_click(self,algo):
        global FORCE_EVAL
        FORCE_EVAL["DIAGONALIZATION"]=algo
        self.FE_Diag_btn.config(text=FORCE_EVAL["DIAGONALIZATION"])
        if FORCE_EVAL["DIAGONALIZATION"]=="OT":
            self.FE_OT_pre_btn.config(state="normal")
        else:
            self.FE_OT_pre_btn.config(state=tk.DISABLED)

    #Select the diagonalization preconditioner method for OT
    def FE_OT_pre_button_click(self,pre):
        global FORCE_EVAL
        FORCE_EVAL["PRECONDITIONER"]=pre
        self.FE_OT_pre_btn.config(text=FORCE_EVAL["PRECONDITIONER"])

    #Find the pseudopotential file
    def FE_potential_find_file_click(self):
        global FORCE_EVAL
        potential_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Potential file",filetypes = (("XYZ files","*.xyz"),("all files","*.*")))
        if str(potential_filename)!="":
            FORCE_EVAL["POTENTIAL_FILE_NAME"]=str(potential_filename)
            self.FE_potential_file_entry.delete(0,tk.END)
            self.FE_potential_file_entry.insert(tk.END,FORCE_EVAL["POTENTIAL_FILE_NAME"])

#EIP method 
class Force_Eval_section_EIP:
    def __init__(self,FE_EIP_Frame):
        i=0;j=0
        tk.Label(FE_EIP_Frame,text="EIP Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])

#EMBED method 
class Force_Eval_section_EMBED:
    def __init__(self,FE_EMBED_Frame):
        i=0;j=0
        tk.Label(FE_EMBED_Frame,text="EMBED Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])

#Force-field or FIST method
class Force_Eval_section_FF:
    def __init__(self,FE_FIST_Frame):
        i=0;j=0
        tk.Label(FE_FIST_Frame,text="Forecefield section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        #Parmeter type
        i+=1
        tk.Label(FE_FIST_Frame,text="Parameters type:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.FE_parmtype_btn=tk.Menubutton(FE_FIST_Frame,text=FORCE_EVAL["PARMTYPE"])
        self.content_FE_parmtype_btn=tk.Menu(self.FE_parmtype_btn)
        self.FE_parmtype_btn.config(menu=self.content_FE_parmtype_btn)
        self.FE_parmtype_btn.grid(row=i,column=j,sticky="WE")
        FE_parmtype_btn_list=["AMBER","CHM","G87","G96","OFF"]
        for types in FE_parmtype_btn_list:
            self.content_FE_parmtype_btn.add_command(label=types,command=lambda types=types: self.FE_parmtype_button_click(types))
        #Make label for Parameters file
        tk.Label(FE_FIST_Frame,text="Parameters file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for Parameters file
        self.FE_parm_file_entry=tk.Entry(FE_FIST_Frame,justify=tk.LEFT)
        #Give the default Parameters file name
        self.FE_parm_file_entry.insert(tk.END,FORCE_EVAL["PARM_FILE_NAME"])
        self.FE_parm_file_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.FE_parm_file_btn=tk.Button(FE_FIST_Frame,text="Find file",command=self.FE_parm_file_click)
        self.FE_parm_file_btn.grid(row=i,column=j,sticky="WE")
        j+=1

    #Select the parmeter type for MM
    def FE_parmtype_button_click(self,types):
        global FORCE_EVAL
        FORCE_EVAL["PARMTYPE"]=types
        self.FE_parmtype_btn.config(text=FORCE_EVAL["PARMTYPE"])

    #Find the parameter file
    def FE_parm_file_click(self):
        global FORCE_EVAL
        parm_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("Pot files","*.pot"),("Dat files","*.dat"),("all files","*.*")))
        if str(parm_filename)!="":
            FORCE_EVAL["PARM_FILE_NAME"]=str(parm_filename)
            self.FE_parm_file_entry.delete(0,tk.END)
            self.FE_parm_file_entry.insert(tk.END,FORCE_EVAL["PARM_FILE_NAME"])

#MIXED method 
class Force_Eval_section_Mixed:
    def __init__(self,FE_MIXED_Frame):
        i=0;j=0
        tk.Label(FE_MIXED_Frame,text="MIXED Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])

#QMMM method 
class Force_Eval_section_QMMM:
    def __init__(self,FE_QMMM_Frame):
        i=0;j=0
        tk.Label(FE_QMMM_Frame,text="QMMM Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])

#QMMM method 
class Force_Eval_section_SIRIUS:
    def __init__(self,FE_SIRIUS_Frame):
        i=0;j=0
        tk.Label(FE_SIRIUS_Frame,text="SIRIUS Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
    

#Make the &Subsys_section------
class Subsys_section:
    def __init__(self,SUBSYS_Frame):
        i=0;j=0
        #Make label for coordination file
        tk.Label(SUBSYS_Frame,text="Coordination file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for coordination file
        self.SS_coord_file_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default Restart File Name
        self.SS_coord_file_entry.insert(tk.END,SUBSYS["COORD"])
        self.SS_coord_file_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.SS_coord_find_file_btn=tk.Button(SUBSYS_Frame,text="Find coord. file",command=self.SS_coord_find_file_click)
        self.SS_coord_find_file_btn.grid(row=i,column=j,sticky=tk.W)
        j+=1

        #Use coord. file button
        i+=1
        j=0
        if len(SUBSYS["ELEMENTS"])>0:
            if SUBSYS["ELEMENTS"][0]=="[":
                SUBSYS["ELEMENTS"]=[]
        tk.Label(SUBSYS_Frame,text="Generate info from coord. file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.SS_coord_use_file_btn=tk.Button(SUBSYS_Frame,text="Generate",command=self.SS_coord_use_file_click)
        self.SS_coord_use_file_btn.grid(row=i,column=j)

        #Coord. file info
        i+=1;j=0
        tk.Label(SUBSYS_Frame,text="Number valence electrons: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.SS_coord_info_e_label=tk.Label(SUBSYS_Frame,text="    ")
        self.SS_coord_info_e_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        i+=1
        j=0
        tk.Label(SUBSYS_Frame,text="Number valence occupied MOs: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.SS_coord_info_MO_label=tk.Label(SUBSYS_Frame,text="    ")
        self.SS_coord_info_MO_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        i+=1;j=0
        tk.Label(SUBSYS_Frame,text="Elements: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        self.SS_coord_info_elements_label=tk.Label(SUBSYS_Frame,text="    ")
        self.SS_coord_info_elements_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1

        #Dimension of the Cell
        i+=1;j=0
        tk.Label(SUBSYS_Frame,text="Cell [Angstrom]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for cell dimension
        self.SS_Cell_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default Restart File Name
        self.SS_Cell_entry.insert(tk.END,SUBSYS["ABC"])
        self.SS_Cell_entry.grid(row=i,column=j,sticky="WE")
        j+=1

        #Centering the molecule
        i+=1
        j=0
        tk.Label(SUBSYS_Frame,text="Centering molecule(s):  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make checkbox for centering
        self.SS_Centering_mol_var=tk.StringVar()
        self.SS_Centering_mol_check=tk.Checkbutton(SUBSYS_Frame,variable=self.SS_Centering_mol_var,onvalue="TRUE",offvalue="FALSE",command=self.SS_Centering_mol_on_off_click)
        self.SS_Centering_mol_check.select()
        self.SS_Centering_mol_check.grid(row=i,column=j)

        #Periodic boundary condition
        #Periodic label
        i+=1;j=0
        self.SS_Periodic_label=tk.Label(SUBSYS_Frame,text="Periodic:  ")
        self.SS_Periodic_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Periodic button
        self.SS_Periodic_btn=tk.Menubutton(SUBSYS_Frame,text=SUBSYS["PERIODIC"])
        #Give it the function as a push down list / Menu
        self.content_SS_Periodic_btn=tk.Menu(self.SS_Periodic_btn)
        #So you can press the button and have the content
        self.SS_Periodic_btn.config(menu=self.content_SS_Periodic_btn)
        self.SS_Periodic_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of boundary condition
        SS_Periodic_btn_list=["NONE","X","XY","XYZ","XZ","Y","YZ","Z"]
        for direc in SS_Periodic_btn_list:
            self.content_SS_Periodic_btn.add_command(label=direc,command=lambda direc=direc: self.SS_Periodic_button_click(direc))
        j+=1
        #POISSON_SOLVER button
        self.SS_Poisson_solver_btn=tk.Menubutton(SUBSYS_Frame,text=FORCE_EVAL["POISSON_SOLVER"])
        #Give it the function as a push down list / Menu
        self.content_SS_Poisson_solver_btn=tk.Menu(self.SS_Poisson_solver_btn)
        #So you can press the button and have the content
        self.SS_Poisson_solver_btn.config(menu=self.content_SS_Poisson_solver_btn)
        self.SS_Poisson_solver_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of POISSON SOLVER
        SS_Poisson_solver_btn_list=["ANALYTIC","IMPLICIT","MT","MULTIPOLE","PERIODIC","WAVELET"]
        for solver in SS_Poisson_solver_btn_list:
            self.content_SS_Poisson_solver_btn.add_command(label=solver,command=lambda solver=solver: self.SS_Poisson_solver_button_click(solver))
        #Only if XC_functional is custom the entry is active
        if SUBSYS["PERIODIC"]=="XYZ":
            self.SS_Poisson_solver_btn.config(state=tk.DISABLED)
        else:
            self.SS_Poisson_solver_btn.config(state="normal")

        #CHARGE on the system
        #Make label for coordination file
        i+=1;j=0
        tk.Label(SUBSYS_Frame,text="Charge: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for Charge
        self.SS_Charge_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default Charge
        self.SS_Charge_entry.insert(tk.END,SUBSYS["CHARGE"])
        self.SS_Charge_entry.grid(row=i,column=j,sticky="WE")
        j+=1

        #Fixed atoms
        #Make label for fixed atoms
        i+=1;j=0
        self.SS_fixed_atoms_label=tk.Label(SUBSYS_Frame,text="Fixed atoms: ")
        self.SS_fixed_atoms_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for fixed atoms
        self.SS_fixed_atoms_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default fixed atoms
        self.SS_fixed_atoms_entry.insert(tk.END,SUBSYS["FIXED"])
        self.SS_fixed_atoms_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Fixed atoms have to be a dynamic calculation
        if GLOBAL["RUN_TYPE"]=="ENERGY" and GLOBAL["PROPERTIES"]!="VIBRATIONAL_ANALYSIS":
            self.SS_fixed_atoms_label.grid_forget()
            self.SS_fixed_atoms_entry.grid_forget()

        #CDFT target value
        #Make label for atoms in fragment 1
        i+=1;j=0
        self.SS_frag1_label=tk.Label(SUBSYS_Frame,text="Atoms in fragment 1 (F1): ")
        self.SS_frag1_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for atoms in fragment 1
        self.SS_frag1_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default atoms in fragment 1
        self.SS_frag1_entry.insert(tk.END,SUBSYS["ATOMS_FRAG1"])
        self.SS_frag1_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Make label for atoms in fragment 2
        i+=1;j=0
        self.SS_frag2_label=tk.Label(SUBSYS_Frame,text="Atoms in fragment 2 (F2): ")
        self.SS_frag2_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for atoms in fragment 2
        self.SS_frag2_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default atoms in fragment 2
        self.SS_frag2_entry.insert(tk.END,SUBSYS["ATOMS_FRAG2"])
        self.SS_frag2_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Make label for target valence electrons
        i+=1;j=0
        self.SS_target1_label=tk.Label(SUBSYS_Frame)
        SS_target1_label_txt="Charge difference (|F2|-|F1"+u"\u207b"+"|): "
        self.SS_target1_label.config(text=SS_target1_label_txt)
        self.SS_target1_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for target valence electrons
        self.SS_target1_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
        #Give the default target value
        self.SS_target1_entry.insert(tk.END,SUBSYS["TARGET1"])
        self.SS_target1_entry.grid(row=i,column=j,sticky="WE")
        j+=1

        #CDFT have to be the property
        if GLOBAL["PROPERTIES"]!="CDFT":
            self.SS_target1_label.grid_forget()
            self.SS_target1_entry.grid_forget()
            self.SS_frag1_label.grid_forget()
            self.SS_frag1_entry.grid_forget()
            self.SS_frag2_label.grid_forget()
            self.SS_frag2_entry.grid_forget()

    #Find the coordination file in filedialog
    def SS_coord_find_file_click(self):
        global SUBSYS
        coord_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("CIF files","*.cif"),("CRD files","*.crd"),("G96 files","*.g96"),("PDB files","*.pdb"),("XTL files","*.xtl"),("all files","*.*")))
        if str(coord_filename)!="":
            SUBSYS["COORD"]=str(coord_filename)
            self.SS_coord_file_entry.delete(0,tk.END)
            self.SS_coord_file_entry.insert(tk.END,SUBSYS["COORD"])

    #Use the coord. file to get info
    def SS_coord_use_file_click(self):
        global SUBSYS
        SUBSYS["COORD"]=self.SS_coord_file_entry.get()
        try:
            valence_e,element_text,SUBSYS["ELEMENTS"],SUBSYS["VALENCE_ELEMENTS"],SUBSYS["ABC"]=coord_file_info.file_extraction(SUBSYS["COORD"])
            self.SS_coord_info_e_label.config(text=str(valence_e))
            self.SS_coord_info_MO_label.config(text=str(int(valence_e/2)))
            self.SS_coord_info_elements_label.config(text=element_text)
            self.SS_Cell_entry.delete(0,tk.END)
            self.SS_Cell_entry.insert(tk.END,SUBSYS["ABC"])
        except:
            self.SS_coord_info_e_label.config(text="")
            self.SS_coord_info_MO_label.config(text="")
            self.SS_coord_info_elements_label.config(text="")
            SUBSYS["ELEMENTS"]=[]
            SUBSYS["VALENCE_ELEMENTS"]=[]
            popup=tk.Tk()
            popup.title("No such file")
            tk.Label(popup, text="Could not find or use the file called "+SUBSYS["COORD"]).pack()
            tk.Button(popup, text="  Okay  ", command = popup.destroy).pack()
            popup.mainloop()

    #Centering molecule on/off
    def SS_Centering_mol_on_off_click(self):
        global SUBSYS
        SUBSYS["CENTER_COORDINATES"]=self.SS_Centering_mol_var.get()

    #Choose the directory of the periodic boundary condition
    def SS_Periodic_button_click(self,direc):
        global SUBSYS
        SUBSYS["PERIODIC"]=direc
        self.SS_Periodic_btn.config(text=SUBSYS["PERIODIC"])
        if SUBSYS["PERIODIC"]=="XYZ":
            self.SS_Poisson_solver_btn.config(state=tk.DISABLED)
        else:
            self.SS_Poisson_solver_btn.config(state="normal")

    #Choose the Poisson solver 
    def SS_Poisson_solver_button_click(self,solver):
        global FORCE_EVAL
        FORCE_EVAL["POISSON_SOLVER"]=solver
        self.SS_Poisson_solver_btn.config(text=FORCE_EVAL["POISSON_SOLVER"])


#Make the &Ext_Restart section------
class Ext_section:
    def __init__(self,EXT_RESTART_Frame):
        i=0;j=0
        #Make a label
        tk.Label(EXT_RESTART_Frame,text="Save restart file:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make a checkbutton to choose if you want to restart
        self.save_restart_var=tk.StringVar()
        self.save_restart_check=tk.Checkbutton(EXT_RESTART_Frame,variable=self.save_restart_var,onvalue="TRUE",offvalue="FALSE",command=self.save_restart_on_off_click)
        self.save_restart_check.deselect()
        self.save_restart_check.grid(row=i,column=j)

        i+=1;j=0
        tk.Label(EXT_RESTART_Frame,text="Save restart each:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry
        self.save_restart_entry=tk.Entry(EXT_RESTART_Frame,justify=tk.LEFT)
        #Give the default Restart File Name
        self.save_restart_entry.insert(tk.END,EXT_RESTART["RESTART_EACH"])
        self.save_restart_entry.grid(row=i,column=j,sticky="WE")
        if EXT_RESTART["SAVE_RESTART"]=="FALSE":
            self.save_restart_entry.config(state=tk.DISABLED)

        #Make a label
        i+=1;j=0
        tk.Label(EXT_RESTART_Frame,text="Restart from a file:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make a checkbutton to choose if you want to restart
        self.restart_var=tk.StringVar()
        self.restart_check=tk.Checkbutton(EXT_RESTART_Frame,variable=self.restart_var,onvalue="TRUE",offvalue="FALSE",command=self.restart_on_off_click)
        self.restart_check.deselect()
        self.restart_check.grid(row=i,column=j)
        j+=1

        #Make Label
        i+=1;j=0
        tk.Label(EXT_RESTART_Frame,text="Restart file name:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry
        self.restart_entry=tk.Entry(EXT_RESTART_Frame,justify=tk.LEFT)
        #Give the default Restart File Name
        self.restart_entry.insert(tk.END,EXT_RESTART["RESTART_FILE_NAME"])
        self.restart_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.restart_find_file_btn=tk.Button(EXT_RESTART_Frame,text="Find restart file",command=self.restart_find_file_click)
        self.restart_find_file_btn.grid(row=i,column=j,sticky=tk.W)
        if EXT_RESTART["RESTART"]=="FALSE":
            self.restart_entry.config(state=tk.DISABLED)
            self.restart_find_file_btn.config(state=tk.DISABLED)

    #Set the save restart to on or off
    def save_restart_on_off_click(self):
        global EXT_RESTART
        EXT_RESTART["SAVE_RESTART"]=self.save_restart_var.get()
        if EXT_RESTART["SAVE_RESTART"]=="TRUE":
            self.save_restart_entry.config(state="normal")
        else:
            self.save_restart_entry.config(state=tk.DISABLED)

    #Set the restart to on or off
    def restart_on_off_click(self):
        global EXT_RESTART
        EXT_RESTART["RESTART"]=self.restart_var.get()
        if EXT_RESTART["RESTART"]=="TRUE":
            self.restart_entry.config(state="normal")
            self.restart_find_file_btn.config(state="normal")
        else:
            self.restart_entry.config(state=tk.DISABLED)
            self.restart_find_file_btn.config(state=tk.DISABLED)

    #Find the restart file
    def restart_find_file_click(self):
        global EXT_RESTART
        restart_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("WFN files","*.wfn"),("Restart files","*.restart"),("all files","*.*")))
        if str(restart_filename)!="":
            EXT_RESTART["RESTART_FILE_NAME"]=str(restart_filename)
            self.restart_entry.delete(0,tk.END)
            self.restart_entry.insert(tk.END,EXT_RESTART["RESTART_FILE_NAME"])


#Make the &Motion_section------
class Motion_section:
    def __init__(self,MOTION_Frame):
        #Geometry Optimization window
        self.MT_Geo_F=tk.Frame(MOTION_Frame)
        self.MT_Geo_F.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
        self.MT_Geo_sec=Motion_section_Geo_Opt(self.MT_Geo_F)

        #MD window
        self.MT_MD_F=tk.Frame(MOTION_Frame)
        self.MT_MD_F.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
        self.MT_MD_sec=Motion_section_MD(self.MT_MD_F)

        #BAND window
        self.MT_BAND_F=tk.Frame(MOTION_Frame)
        self.MT_BAND_F.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
        self.MT_BAND_sec=Motion_section_BAND(self.MT_BAND_F)

        if GLOBAL["RUN_TYPE"].upper()=="GEO_OPT":
            self.sec_motion.config(state="normal",fg="green")
            self.MT_Geo_F.lift()
        elif GLOBAL["RUN_TYPE"].upper()=="MD" or GLOBAL["RUN_TYPE"].upper()=="RT_PROPAGATION":
            sec_motion.config(state="normal",fg="green")
            self.MT_MD_F.lift()
        elif GLOBAL["RUN_TYPE"].upper()=="BAND":
            sec_motion.config(state="normal",fg="green")
            self.MT_BAND_F.lift()


#Geometry Optimization
class Motion_section_Geo_Opt:
    def __init__(self,MT_Geo_Frame):
        #Optimize for ground state or TS state
        i=0;j=0
        tk.Label(MT_Geo_Frame,text="Type:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Optimizer button
        self.MT_Geo_Opt_btn=tk.Menubutton(MT_Geo_Frame,text=MOTION["TYPE"])
        #Give it the function as a push down list / Menu
        self.content_MT_Geo_Opt_btn=tk.Menu(self.MT_Geo_Opt_btn)
        #So you can press the button and have the content
        self.MT_Geo_Opt_btn.config(menu=self.content_MT_Geo_Opt_btn)
        self.MT_Geo_Opt_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of what to go towards
        MT_Geo_Opt_btn_list=["MINIMIZATION","TRANSITION_STATE"]
        for state in MT_Geo_Opt_btn_list:
            self.content_MT_Geo_Opt_btn.add_command(label=state,command=lambda state=state: self.MT_Geo_Opt_button_click(state))
        j+=1
        #Optimizer
        i+=1;j=0
        tk.Label(MT_Geo_Frame,text="Optimizer:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Optimizer button
        self.MT_Geo_Optimizer_btn=tk.Menubutton(MT_Geo_Frame,text=MOTION["OPTIMIZER"])
        #Give it the function as a push down list / Menu
        self.content_MT_Geo_Optimizer_btn=tk.Menu(self.MT_Geo_Optimizer_btn)
        #So you can press the button and have the content
        self.MT_Geo_Optimizer_btn.config(menu=self.content_MT_Geo_Optimizer_btn)
        self.MT_Geo_Optimizer_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of optimizer
        MT_Geo_Optimizer_btn_list=["BFGS","CG","LBFGS"]
        for opti in MT_Geo_Optimizer_btn_list:
            self.content_MT_Geo_Optimizer_btn.add_command(label=opti,command=lambda opti=opti: self.MT_Geo_Optimizer_button_click(opti))
        j+=1
        if MOTION["TYPE"]=="TRANSITION_STATE":
            self.MT_Geo_Optimizer_btn.config(state=tk.DISABLED)
            MOTION["OPTIMIZER"]="CG"
            self.MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])
        #Max Force, the convergence criteria
        i+=1;j=0
        tk.Label(MT_Geo_Frame,text="Max geometry change:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for max Dr
        self.MT_Geo_Max_Dr_entry=tk.Entry(MT_Geo_Frame,justify=tk.LEFT)
        #Give the default Max Dr
        self.MT_Geo_Max_Dr_entry.insert(tk.END,MOTION["MAX_DR"])
        self.MT_Geo_Max_Dr_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Max Iterations for the geometry optimization
        i+=1;j=0
        tk.Label(MT_Geo_Frame,text="Max iterations:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for max iter
        self.MT_Geo_Max_Iter_entry=tk.Entry(MT_Geo_Frame,justify=tk.LEFT)
        #Give the default Max Iter
        self.MT_Geo_Max_Iter_entry.insert(tk.END,MOTION["MAX_ITER"])
        self.MT_Geo_Max_Iter_entry.grid(row=i,column=j,sticky="WE")
        j+=1

    #Choose what the optimizer is going towards
    def MT_Geo_Opt_button_click(self,state):
        global MOTION
        MOTION["TYPE"]=state
        self.MT_Geo_Opt_btn.config(text=MOTION["TYPE"])
        if MOTION["TYPE"]=="TRANSITION_STATE":
            self.MT_Geo_Optimizer_btn.config(state=tk.DISABLED)
            MOTION["OPTIMIZER"]="CG"
            self.MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])
        else:
            self.MT_Geo_Optimizer_btn.config(state="normal")
            MOTION["OPTIMIZER"]="BFGS"
            self.MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])

    #Choose the geometry optimizer
    def MT_Geo_Optimizer_button_click(self,opti):
        global MOTION
        MOTION["OPTIMIZER"]=opti
        self.MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])

#Molecule dynamics
class Motion_section_MD:
    def __init__(self,MT_MD_Frame):
        #Ensemble label
        i=0;j=0
        tk.Label(MT_MD_Frame,text="Ensemble:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Ensemble button
        self.MT_MD_Ensemble_btn=tk.Menubutton(MT_MD_Frame,text=MOTION["ENSEMBLE"])
        #Give it the function as a push down list / Menu
        self.content_MT_MD_Ensemble_btn=tk.Menu(self.MT_MD_Ensemble_btn)
        #So you can press the button and have the content
        self.MT_MD_Ensemble_btn.config(menu=self.content_MT_MD_Ensemble_btn)
        self.MT_MD_Ensemble_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Ensembles
        MT_MD_Ensemble_btn_list=["HYDROSTATICSHOCK","ISOKIN","LANGEVIN","MSST","MSST_DAMPED","NPE_F","NPE_I","NPT_F","NPT_I","NVE","NVT","NVT_ADIABATIC","REFTRAJ"]
        for ens in MT_MD_Ensemble_btn_list:
            self.content_MT_MD_Ensemble_btn.add_command(label=ens,command=lambda ens=ens: self.MT_MD_Ensemble_button_click(ens))
        j+=1
        #Steps
        i+=1;j=0
        tk.Label(MT_MD_Frame,text="Steps:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for steps
        self.MT_MD_steps_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
        #Give the default steps
        self.MT_MD_steps_entry.insert(tk.END,MOTION["STEPS"])
        self.MT_MD_steps_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Timestep
        i+=1;j=0
        tk.Label(MT_MD_Frame,text="Timestep [fs]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for timestep
        self.MT_MD_timestep_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
        #Give the default timestep
        self.MT_MD_timestep_entry.insert(tk.END,MOTION["TIMESTEP"])
        self.MT_MD_timestep_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Temperature
        i+=1;j=0
        tk.Label(MT_MD_Frame,text="Temperature [K]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for Temperature
        self.MT_MD_temperature_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
        #Give the default Temperature
        self.MT_MD_temperature_entry.insert(tk.END,MOTION["TEMPERATURE"])
        self.MT_MD_temperature_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #THERMOSTAT
        #THERMOSTAT label
        i+=1;j=0
        tk.Label(MT_MD_Frame,text="Thermostat:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #THERMOSTAT button
        self.MT_MD_Thermostat_btn=tk.Menubutton(MT_MD_Frame,text=MOTION["THERMOSTAT"])
        #Give it the function as a push down list / Menu
        self.content_MT_MD_Thermostat_btn=tk.Menu(self.MT_MD_Thermostat_btn)
        #So you can press the button and have the content
        self.MT_MD_Thermostat_btn.config(menu=self.content_MT_MD_Thermostat_btn)
        self.MT_MD_Thermostat_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of Ensembles
        MT_MD_Thermostat_btn_list=["AD_LANGEVIN","CSVR","GLE","NOSE"]
        for thermo in MT_MD_Thermostat_btn_list:
            self.content_MT_MD_Thermostat_btn.add_command(label=thermo,command=lambda thermo=thermo: self.MT_MD_Thermostat_button_click(thermo))
        j+=1
        #Time constant
        i+=1;j=0
        self.MT_MD_TIMECON_label=tk.Label(MT_MD_Frame,text="Time constant [fs]:  ")
        self.MT_MD_TIMECON_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry for TIMECON
        self.MT_MD_TIMECON_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
        #Give the default TIMECON
        self.MT_MD_TIMECON_entry.insert(tk.END,MOTION["TIMECON"])
        self.MT_MD_TIMECON_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        if MOTION["THERMOSTAT"]=="GLE":
            self.MT_MD_TIMECON_entry.config(state=tk.DISABLED)
            self.MT_MD_TIMECON_label.config(state=tk.DISABLED)
    
    #Choose the ensemble
    def MT_MD_Ensemble_button_click(self,ens):
        global MOTION
        MOTION["ENSEMBLE"]=ens
        self.MT_MD_Ensemble_btn.config(text=MOTION["ENSEMBLE"])
        if MOTION["ENSEMBLE"]=="NPE_F" or MOTION["ENSEMBLE"]=="NPE_I":
            self.MT_MD_Thermostat_btn.config(state=tk.DISABLED)
            self.MT_MD_TIMECON_entry.config(state=tk.DISABLED)
        else:
            self.MT_MD_Thermostat_btn.config(state="normal")
            self.MT_MD_TIMECON_entry.config(state="normal")

    #Choose the Thermostat
    def MT_MD_Thermostat_button_click(self,thermo):
        global MOTION
        MOTION["THERMOSTAT"]=thermo
        self.MT_MD_Thermostat_btn.config(text=MOTION["THERMOSTAT"])
        if MOTION["THERMOSTAT"]=="GLE":
            self.MT_MD_TIMECON_entry.config(state=tk.DISABLED)
            self.MT_MD_TIMECON_label.config(state=tk.DISABLED)
        else:
            self.MT_MD_TIMECON_entry.config(state="normal")
            self.MT_MD_TIMECON_label.config(state="normal")

#BAND
class Motion_section_BAND:
    def __init__(self,MT_BAND_Frame):
        #Initial coordinates
        #Make Label
        i=0;j=0
        tk.Label(MT_BAND_Frame,text="Initial structure:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry of initial structure
        self.MT_BAND_initial_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
        #Give the default initial structure
        self.MT_BAND_initial_entry.insert(tk.END,MOTION["REPLICA1"])
        self.MT_BAND_initial_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.MT_BAND_initial_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=self.MT_BAND_initial_find_file_click)
        self.MT_BAND_initial_find_file_btn.grid(row=i,column=j,sticky=tk.W)
        #Intermediate coordinates
        #Make Label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Intermediate structure (Not needed):  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry of Intermediate structure
        self.MT_BAND_interm_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
        #Give the default Intermediate structure
        self.MT_BAND_interm_entry.insert(tk.END,MOTION["REPLICA2"])
        self.MT_BAND_interm_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.MT_BAND_interm_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=self.MT_BAND_interm_find_file_click)
        self.MT_BAND_interm_find_file_btn.grid(row=i,column=j,sticky=tk.W)
        #Final coordinates
        #Make Label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Final structure:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry of Final structure
        self.MT_BAND_final_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
        #Give the default Final structure
        self.MT_BAND_final_entry.insert(tk.END,MOTION["REPLICA3"])
        self.MT_BAND_final_entry.grid(row=i,column=j,sticky="WE")
        j+=1
        #Find file
        self.MT_BAND_final_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=self.MT_BAND_final_find_file_click)
        self.MT_BAND_final_find_file_btn.grid(row=i,column=j,sticky=tk.W)
        #BAND_TYPE
        #BAND_TYPE label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Band type:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #BAND_TYPE button
        self.MT_BAND_Band_type_btn=tk.Menubutton(MT_BAND_Frame,text=MOTION["BAND_TYPE"])
        #Give it the function as a push down list / Menu
        self.content_MT_BAND_Band_type_btn=tk.Menu(self.MT_BAND_Band_type_btn)
        #So you can press the button and have the content
        self.MT_BAND_Band_type_btn.config(menu=self.content_MT_BAND_Band_type_btn)
        self.MT_BAND_Band_type_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of BAND_TYPES
        MT_BAND_Band_type_btn_list=["B-NEB","CI-NEB","D-NEB","EB","IT-NEB","SM"]
        for band in MT_BAND_Band_type_btn_list:
            self.content_MT_BAND_Band_type_btn.add_command(label=band,command=lambda band=band: self.MT_BAND_Band_type_button_click(band))
        #Number of replicas
        #Make Label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Number of replicas:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry of Number of replicas
        self.MT_BAND_num_replica_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
        #Give the default Number of replicas
        self.MT_BAND_num_replica_entry.insert(tk.END,MOTION["NUMBER_OF_REPLICA"])
        self.MT_BAND_num_replica_entry.grid(row=i,column=j,sticky="WE")
        #BAND Optimizer
        #BAND Optimizer label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Band optimizer:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #BAND Optimizer button
        self.MT_BAND_Band_opti_btn=tk.Menubutton(MT_BAND_Frame,text=MOTION["OPTIMIZE_BAND"])
        #Give it the function as a push down list / Menu
        self.content_MT_BAND_Band_opti_btn=tk.Menu(self.MT_BAND_Band_opti_btn)
        #So you can press the button and have the content
        self.MT_BAND_Band_opti_btn.config(menu=self.content_MT_BAND_Band_opti_btn)
        self.MT_BAND_Band_opti_btn.grid(row=i,column=j,sticky="WE")
        #Give the options of BAND Optimizer
        MT_BAND_Band_opti_btn_list=["DIIS","MD"]
        for opti in MT_BAND_Band_opti_btn_list:
            self.content_MT_BAND_Band_opti_btn.add_command(label=opti,command=lambda opti=opti: self.MT_BAND_Band_opti_button_click(opti))
        #Max Steps
        #Make Label
        i+=1;j=0
        tk.Label(MT_BAND_Frame,text="Max steps:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        j+=1
        #Make Entry of Max Steps
        self.MT_BAND_max_steps_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
        #Give the default Max Steps
        self.MT_BAND_max_steps_entry.insert(tk.END,MOTION["MAX_STEPS"])
        self.MT_BAND_max_steps_entry.grid(row=i,column=j,sticky="WE")

    #Choose coord file for replica 1
    def MT_BAND_initial_find_file_click(self):
        global MOTION
        MT_BAND_initial_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("all files","*.*")))
        if str(MT_BAND_initial_filename)!="":
            MOTION["REPLICA1"]=str(MT_BAND_initial_filename)
            self.MT_BAND_initial_entry.delete(0,tk.END)
            self.MT_BAND_initial_entry.insert(tk.END,MOTION["REPLICA1"])

    #Choose coord file for replica 2
    def MT_BAND_interm_find_file_click(self):
        global MOTION
        MT_BAND_interm_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("all files","*.*")))
        if str(MT_BAND_interm_filename)!="":
            MOTION["REPLICA2"]=str(MT_BAND_interm_filename)
            self.MT_BAND_interm_entry.delete(0,tk.END)
            self.MT_BAND_interm_entry.insert(tk.END,MOTION["REPLICA2"])

    #Choose coord file for replica 3
    def MT_BAND_final_find_file_click(self):
        global MOTION
        MT_BAND_final_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("all files","*.*")))
        if str(MT_BAND_final_filename)!="":
            MOTION["REPLICA3"]=str(MT_BAND_final_filename)
            self.MT_BAND_final_entry.delete(0,tk.END)
            self.MT_BAND_final_entry.insert(tk.END,MOTION["REPLICA3"])

    #Choose the Band_type
    def MT_BAND_Band_type_button_click(self,band):
        global MOTION
        MOTION["BAND_TYPE"]=band
        self.MT_BAND_Band_type_btn.config(text=MOTION["BAND_TYPE"])

    #Choose the Band optimizer
    def MT_BAND_Band_opti_button_click(self,opti):
        global MOTION
        MOTION["OPTIMIZE_BAND"]=opti
        self.MT_BAND_Band_opti_btn.config(text=MOTION["OPTIMIZE_BAND"])



CP2K_Editor=tk.Tk()
Window_Frame(CP2K_Editor)
CP2K_Editor.mainloop()