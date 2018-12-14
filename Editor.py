#Made by Andreas Vishart
#Python 2 or 3 can be used for the script, if an input file is given after the script
#the parameters of the input file is loaded into CP2K_Editor interface
#---------------Package----------------
import os
import sys

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
    sys.path.insert(0, str(os.path.realpath(__file__))[:-len("Editor.py")]+'scr/')
    import Tkinter as tk
    import tkFileDialog as filedialog
    import coord_file_info as coord_file_info
    import program_to_input as program_to_input
    import default_parameters as default_parameters
    import program_to_input_cdft as program_to_input_cdft
                
#---------------Parameters----------------
#PROGRAM SETTINGS
PROGRAM={}
#The name of the program
PROGRAM["Program_name"]="CP2K Editor"
PROGRAM["Script_name"]="Editor.py"
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

#---------------Functions----------------
#Program------

#Exit the program
def Exit():
    exit()

#Exit pop up window
def popup_exit():
    popup=tk.Tk()
    popup.title("Exit")
    label=tk.Label(popup, text="Do you want to exit "+PROGRAM["Program_name"]+"?")
    label.grid(row=0,column=1)
    B1=tk.Button(popup, text="  Yes  ", command=Exit)
    B1.grid(row=1,column=0,)
    B2=tk.Button(popup, text="  No   ", command = popup.destroy)
    B2.grid(row=1,column=2)
    popup.mainloop()

#Save the input file
def Save():
    global GLOBAL
    global FORCE_EVAL
    global SUBSYS
    global EXT_RESTART
    global MOTION
    save_entries()
    popup_save_file()

#Save the input file as 
def popup_save_file():
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
        popup_save()

#The input file is saved pop up window
def popup_save():
    popup=tk.Tk()
    popup.title("Saved")
    label=tk.Label(popup, text="The input file is saved as "+GLOBAL["FILE_NAME"])
    label.grid(row=0)
    B1=tk.Button(popup, text="  Okay  ", command = popup.destroy)
    B1.grid(row=1)
    popup.mainloop()

#Error could not find such file
def popup_error_file(filename):
    popup_error=tk.Tk()
    popup_error.title("No such file")
    tk.Label(popup_error, text="Could not find or use the file called "+str(filename)).pack()
    tk.Button(popup_error, text="  Okay  ", command = popup_error.destroy).pack()
    return popup_error

#Preview input file
def Preview():
    global GLOBAL
    global FORCE_EVAL
    global SUBSYS
    global EXT_RESTART
    global MOTION
    save_entries()
    popup=tk.Tk()
    popup.title("Preview")
    popup.geometry("500x"+str(int(PROGRAM["size_of_window_height"]*0.85))+"+0+0")
    B_Close=tk.Button(popup, text="  Close  ", command = popup.destroy)
    B_Close.pack(side=tk.BOTTOM)
    B_Save=tk.Button(popup, text="  Save  ", command = Save)
    B_Save.pack(side=tk.BOTTOM)
    if GLOBAL["PROPERTIES"]=="CDFT":
        inputfile_content=program_to_input_cdft.Save_cdft_files(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    else:
        inputfile_content=program_to_input.Save_to_input(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    scrollbar=tk.Scrollbar(popup)
    label=tk.Text(popup, height=int(PROGRAM["size_of_window_height"]*0.8), width=500)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    label.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar.config(command=label.yview)
    label.config(yscrollcommand=scrollbar.set)
    label.insert(tk.END, inputfile_content)
    label.config(state=tk.DISABLED)
    popup.mainloop()

#Save all the entries
def save_entries():
    global GLOBAL
    global FORCE_EVAL
    global SUBSYS
    global EXT_RESTART
    global MOTION
    GLOBAL["PROJECT_NAME"]=project_name_entry.get()
    GLOBAL["NSTATES"]=properties_info_nstates_entry.get()
    GLOBAL["FILE_NAME"]=GLOBAL["PROJECT_NAME"]+".inp"
    FORCE_EVAL["EACH"]=each_entry.get()
    if FORCE_EVAL["BASIS_SET"]=="Custom":
        FORCE_EVAL["BASIS_SET"]=FE_basis_set_entry.get()
    if FORCE_EVAL["POTENTIAL"]=="Custom":
        FORCE_EVAL["POTENTIAL"]=FE_potential_entry.get()
    FORCE_EVAL["LIBXC"]=FE_XC_functional_custom_entry.get()
    FORCE_EVAL["FRACTION"]=FE_HF_X_entry.get()
    FORCE_EVAL["MAX_SCF"]=FE_MAX_SCF_entry.get()
    FORCE_EVAL["EPS_SCF"]=FE_EPS_SCF_entry.get()
    FORCE_EVAL["NGRIDS"]=FE_NGRIDS_entry.get()
    FORCE_EVAL["CUTOFF"]=FE_PW_Cutoff_entry.get()
    FORCE_EVAL["REL_CUTOFF"]=FE_Gau_Cutoff_entry.get()
    FORCE_EVAL["PARM_FILE_NAME"]=FE_parm_file_entry.get()
    SUBSYS["COORD"]=SS_coord_file_entry.get()
    SUBSYS["ABC"]=SS_Cell_entry.get()
    SUBSYS["CHARGE"]=SS_Charge_entry.get()
    SUBSYS["FIXED"]=SS_fixed_atoms_entry.get()
    SUBSYS["TARGET1"]=SS_target1_entry.get()
    SUBSYS["TARGET2"]=SS_target2_entry.get()
    SUBSYS["ATOMS_FRAG1"]=SS_frag1_entry.get()
    SUBSYS["ATOMS_FRAG2"]=SS_frag2_entry.get()
    EXT_RESTART["RESTART_EACH"]=save_restart_entry.get()
    EXT_RESTART["RESTART_FILE_NAME"]=restart_entry.get()
    MOTION["MAX_DR"]=MT_Geo_Max_Dr_entry.get()
    MOTION["MAX_ITER"]=MT_Geo_Max_Iter_entry.get()
    MOTION["STEPS"]=MT_MD_steps_entry.get()
    MOTION["TIMESTEP"]=MT_MD_timestep_entry.get()
    MOTION["TEMPERATURE"]=MT_MD_temperature_entry.get()
    MOTION["TIMECON"]=MT_MD_TIMECON_entry.get()
    MOTION["REPLICA1"]=MT_BAND_initial_entry.get()
    MOTION["REPLICA2"]=MT_BAND_interm_entry.get()
    MOTION["REPLICA3"]=MT_BAND_final_entry.get()
    MOTION["NUMBER_OF_REPLICA"]=MT_BAND_num_replica_entry.get()
    MOTION["MAX_STEPS"]=MT_BAND_max_steps_entry.get()

#Menu functions------

#File

#New input file window
def new_input():
    os.system(str(sys.executable)+" "+PROGRAM["Path"]+PROGRAM["Script_name"])

#Open an input file
def open_input():
    if str(sys.version)[0]=="3":
        import scr.import_output as import_output
    elif str(sys.version)[0]=="2":
        import import_output as import_output
    inputfile=filedialog.askopenfilename(initialdir="./",title = "Select Input file",filetypes = (("Inp files","*.inp"),("all files","*")))
    Interface.update()
    if inputfile!="":
        os.system(str(sys.executable)+" "+PROGRAM["Path"]+PROGRAM["Script_name"]+" "+str(inputfile))

#About pop up window
def popup_About():
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
def Help():
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
def Generate_cutoff_test():
    generate_cutoff_file=filedialog.askopenfilename(initialdir="./",title = "Select input file",filetypes = (("INP files","*.inp"),("all files","*")))
    Interface.update()
    if str(generate_cutoff_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Function_generate_cutoff_test as Function_generate_cutoff_test
        elif str(sys.version)[0]=="2":
            import Function_generate_cutoff_test as Function_generate_cutoff_test
        Function_generate_cutoff_test.popup_generate_cutoff(generate_cutoff_file)        


#Analyse 

#CDFT details
def CDFT_details_function():
    cdft_detail_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
    if str(cdft_detail_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_CDFT as Analyse_CDFT
        elif str(sys.version)[0]=="2":
            import Analyse_CDFT as Analyse_CDFT
        try:
            popup_cdft=Analyse_CDFT.CDFT_popup(cdft_detail_file)
        except:
            popup_cdft=popup_error_file(cdft_detail_file)
        popup_cdft.mainloop()

#Convergence (Is the file converged properly)
def Convergence_function():
    convergence_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
    Interface.update()
    if str(convergence_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_Convergence as Analyse_Convergence
        elif str(sys.version)[0]=="2":
            import Analyse_Convergence as Analyse_Convergence
        try:
            popup_conv=Analyse_Convergence.Convergence_popup(convergence_file)
        except:
            popup_conv=popup_error_file(convergence_file)
        popup_conv.mainloop()

#Analyse Cutoff test
def Analyse_cutoff_test_function():
    cutoff_folder=filedialog.askdirectory(initialdir="./",title = "Select cutoff test folder")
    Interface.update()
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

#Energy and Temperature plot for MD
def MD_energy_temp_function():
    md_e_t_file=filedialog.askopenfilename(initialdir="./",title = "Select energy file",filetypes = (("ENER files","*.ener"),("all files","*")))
    Interface.update()
    if str(md_e_t_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_MD_Ener as Analyse_MD_Ener
        elif str(sys.version)[0]=="2":
            import Analyse_MD_Ener as Analyse_MD_Ener
        try:
            MD_analyse_data=Analyse_MD_Ener.MD_Ener(md_e_t_file)
        except:
            popup_error_file(md_e_t_file)
        else:
            Analyse_MD_Ener.plot_MD_Ener(MD_analyse_data)

#Geometry Optimization
def Optimization_function():
    optimization_file=filedialog.askopenfilename(initialdir="./",title = "Select position file",filetypes = (("XYZ files","*.xyz"),("all files","*")))
    Interface.update()
    if str(optimization_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_Optimization as Analyse_Optimization
        elif str(sys.version)[0]=="2":
            import Analyse_Optimization as Analyse_Optimization
        try:
            Optimization_analyse_data=Analyse_Optimization.Optimization(optimization_file)
        except:
            popup_error_file(optimization_file)
        else:
            Analyse_Optimization.plot_Optimization(Optimization_analyse_data)

#UV-Vis spectrum
def UV_Vis_function():
    uvvis_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
    Interface.update()
    if str(uvvis_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_UV_Vis as Analyse_UV_Vis
        elif str(sys.version)[0]=="2":
            import Analyse_UV_Vis as Analyse_UV_Vis
        try:
            UV_Vis_analyse_data=Analyse_UV_Vis.extract(uvvis_file)
        except:
            popup_error_file(uvvis_file)
        else:
            Analyse_UV_Vis.plot_uv_vis_osc(UV_Vis_analyse_data)

#Vibrational spectrum
def Vib_function():
    vib_file=filedialog.askopenfilename(initialdir="./",title = "Select output file",filetypes = (("OUT files","*.out"),("all files","*")))
    Interface.update()
    if str(vib_file)!="":
        if str(sys.version)[0]=="3":
            import scr.Analyse_Vib as Analyse_Vib
        elif str(sys.version)[0]=="2":
            import Analyse_Vib as Analyse_Vib
        try:
            popup_vib=Analyse_Vib.Vibration_popup(vib_file)
        except:
            popup_vib=popup_error_file(vib_file)
        popup_vib.mainloop()



#Section buttons------

#Global command when Global section button is pressed
def GLOBAL_Frame_btn_func():
    GLOBAL_Frame.lift()
    sec_global.config(fg="blue")
    sec_force_eval.config(fg="green")
    sec_subsys.config(fg="green")
    sec_ext_restart.config(fg="green")
    sec_motion.config(fg="green")

#FORCE_EVAL command when FORCE_EVAL section button is pressed
def FORCE_EVAL_Frame_btn_func():
    FORCE_EVAL_Frame.lift()
    sec_global.config(fg="green")
    sec_force_eval.config(fg="blue")
    sec_subsys.config(fg="green")
    sec_ext_restart.config(fg="green")
    sec_motion.config(fg="green")

#SUBSYS command when SUBSYS section button is pressed
def SUBSYS_Frame_btn_func():
    SUBSYS_Frame.lift()
    sec_global.config(fg="green")
    sec_force_eval.config(fg="green")
    sec_subsys.config(fg="blue")
    sec_ext_restart.config(fg="green")
    sec_motion.config(fg="green")

#EXT_RESTART command when EXT_RESTART section button is pressed
def EXT_RESTART_Frame_btn_func():
    EXT_RESTART_Frame.lift()
    sec_global.config(fg="green")
    sec_force_eval.config(fg="green")
    sec_subsys.config(fg="green")
    sec_ext_restart.config(fg="blue")
    sec_motion.config(fg="green")

#MOTION command when MOTION section button is pressed
def MOTION_sec_Frame_func():
    MOTION_Frame.lift()
    sec_global.config(fg="green")
    sec_force_eval.config(fg="green")
    sec_subsys.config(fg="green")
    sec_ext_restart.config(fg="green")
    sec_motion.config(fg="blue")


#&Global------

#Choose the Run_Type
def Run_Type_button_click(types):
    global GLOBAL
    GLOBAL["RUN_TYPE"]=types
    run_type_btn.config(text=GLOBAL["RUN_TYPE"])
    if GLOBAL["RUN_TYPE"]!="ENERGY":
        sec_motion.config(state="normal")
        SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
        SS_fixed_atoms_entry.grid(row=9,column=1)
        if GLOBAL["PROPERTIES"]!="NONE":
            each_label.grid(row=6,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            each_entry.grid(row=6,column=1) 
        if GLOBAL["RUN_TYPE"]=="GEO_OPT":
            MT_Geo_Frame.lift()
        elif GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
            MT_MD_Frame.lift()
        elif GLOBAL["RUN_TYPE"]=="BAND":
            MT_BAND_Frame.lift()
    else:
        sec_motion.config(state=tk.DISABLED)
        each_label.grid_forget()
        each_entry.grid_forget()
        if GLOBAL["PROPERTIES"]=="VIBRATIONAL_ANALYSIS":
            SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            SS_fixed_atoms_entry.grid(row=9,column=1)
        else:
            SS_fixed_atoms_label.grid_forget()
            SS_fixed_atoms_entry.grid_forget()

#Choose the Print_Level
def Print_Level_button_click(level):
    global GLOBAL
    GLOBAL["PRINT_LEVEL"]=level
    print_level_btn.config(text=GLOBAL["PRINT_LEVEL"])

#Choose the Properties
def Properties_button_click(proper):
    global GLOBAL
    GLOBAL["PROPERTIES"]=proper
    properties_btn.config(text=GLOBAL["PROPERTIES"])
    if GLOBAL["PROPERTIES"]=="NONE":
        properties_info_nstates_label.grid_forget()
        properties_info_nstates_entry.grid_forget()
        each_label.grid_forget()
        each_entry.grid_forget()
    else:
        if GLOBAL["RUN_TYPE"]!="ENERGY":
            each_label.grid(row=6,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            each_entry.grid(row=6,column=1)
        if GLOBAL["PROPERTIES"]=="MO" or GLOBAL["PROPERTIES"]=="TDDFPT":
            properties_info_nstates_label.grid(row=5,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            properties_info_nstates_entry.grid(row=5,column=1)
        else:
            properties_info_nstates_label.grid_forget()
            properties_info_nstates_entry.grid_forget()
        if GLOBAL["PROPERTIES"]=="CDFT":
            SS_target1_label.grid(row=10,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"]);SS_target1_entry.grid(row=10,column=1)
            SS_target2_label.grid(row=11,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"]);SS_target2_entry.grid(row=11,column=1)
            SS_frag1_label.grid(row=12,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"]);SS_frag1_entry.grid(row=12,column=1)
            SS_frag2_label.grid(row=13,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"]);SS_frag2_entry.grid(row=13,column=1)
        else:
            SS_target1_label.grid_forget();SS_target1_entry.grid_forget()
            SS_target2_label.grid_forget();SS_target2_entry.grid_forget()
            SS_frag1_label.grid_forget();SS_frag1_entry.grid_forget()
            SS_frag2_label.grid_forget();SS_frag2_entry.grid_forget()
        if GLOBAL["PROPERTIES"]=="VIBRATIONAL_ANALYSIS":
            SS_fixed_atoms_label.grid(row=9,column=0,sticky=tk.W,pady=PROGRAM["pady_line_size"])
            SS_fixed_atoms_entry.grid(row=9,column=1)
        elif GLOBAL["PROPERTIES"]!="VIBRATIONAL_ANALYSIS" and GLOBAL["RUN_TYPE"]=="ENERGY":
            SS_fixed_atoms_label.grid_forget();SS_fixed_atoms_entry.grid_forget()


#&Force_Eval------
#Choose the Method
def FE_Method_button_click(methods):
    global FORCE_EVAL
    FORCE_EVAL["METHOD"]=methods
    FE_method_btn.config(text=FORCE_EVAL["METHOD"])
    if FORCE_EVAL["METHOD"]=="QUICKSTEP":
        FORCE_EVAL["METHOD_SECTION"]="DFT"
        FE_DFT_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="EIP":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_EIP_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="EMBED":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_EMBED_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="FIST":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_FIST_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="MIXED":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_MIXED_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="QMMM":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_QMMM_Frame.lift()
    elif FORCE_EVAL["METHOD"]=="SIRIUS":
        FORCE_EVAL["METHOD_SECTION"]=FORCE_EVAL["METHOD"]
        FE_SIRIUS_Frame.lift()


#DFT
#Select the basis set file in the basis set folder 
def basis_set_file_click(files):
    if files!="Find":
        FORCE_EVAL["BASIS_SET_FILE_NAME-path"]=files
        FORCE_EVAL["BASIS_SET_FILE_NAME"]=path_to_basis_set0+FORCE_EVAL["BASIS_SET_FILE_NAME-path"]
        FE_basis_set_files_btn.config(text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
        FE_basis_set_btn.config(menu=BASIS_SET_OPTIONS[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]])
        FORCE_EVAL["BASIS_SET"]=BASIS_SET[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]][0]
        FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
    elif files=="Find":
        basisset_filename=filedialog.askopenfilename(initialdir=path_to_basis_set0,title = "Select Basis Set file",filetypes = (("DAT files","*.dat"),("all files","*")))
        if str(basisset_filename)!="":
            FORCE_EVAL["BASIS_SET_FILE_NAME"]=basisset_filename
            FORCE_EVAL["BASIS_SET_FILE_NAME-path"]=str(basisset_filename.split("/")[-1])
            path_to_basis_set=basisset_filename[:-len(FORCE_EVAL["BASIS_SET_FILE_NAME-path"])]
            FE_basis_set_files_btn.config(text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
            FORCE_EVAL["BASIS_SET"]=BASIS_SET["Find"][0]
            FE_basis_set_btn.config(menu=BASIS_SET_OPTIONS["Find"])
            FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
    if FORCE_EVAL["BASIS_SET"]!="Custom":
        FE_basis_set_entry.config(state=tk.DISABLED)
    if FORCE_EVAL["BASIS_SET"]=="Custom":
        FE_basis_set_entry.config(state="normal")

#Select the basis set from the basis set file in the basis set folder 
def basis_set_click(set):
    FORCE_EVAL["BASIS_SET"]=set
    FE_basis_set_btn.config(text=FORCE_EVAL["BASIS_SET"])
    if FORCE_EVAL["BASIS_SET"]=="Custom":
        FE_basis_set_entry.config(state="normal")
    else:
        FE_basis_set_entry.config(state=tk.DISABLED)

#Select the potential file in the potential folder 
def potential_file_click(files):
    if files!="Find":
        FORCE_EVAL["POTENTIAL_FILE_NAME-path"]=files
        FORCE_EVAL["POTENTIAL_FILE_NAME"]=path_to_potential0+FORCE_EVAL["POTENTIAL_FILE_NAME-path"]
        FE_potential_files_btn.config(text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
        FE_potential_btn.config(menu=POTENTIAL_OPTIONS[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]])
        FORCE_EVAL["POTENTIAL"]=POTENTIAL[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]][0]
        FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
    elif files=="Find":
        potential_filename=filedialog.askopenfilename(initialdir=path_to_potential0,title = "Select Potential file",filetypes = (("DAT files","*.dat"),("all files","*")))
        if str(potential_filename)!="":
            FORCE_EVAL["POTENTIAL_FILE_NAME-path"]=str(potential_filename.split("/")[-1])
            path_to_potential=potential_filename[:-len(FORCE_EVAL["POTENTIAL_FILE_NAME-path"])]
            FORCE_EVAL["POTENTIAL_FILE_NAME"]=path_to_potential+FORCE_EVAL["POTENTIAL_FILE_NAME-path"]
            FE_potential_files_btn.config(text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
            FORCE_EVAL["POTENTIAL"]=POTENTIAL["Find"][0]
            FE_potential_btn.config(menu=POTENTIAL_OPTIONS["Find"])
            FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
    if FORCE_EVAL["POTENTIAL"]!="Custom":
        FE_potential_entry.config(state=tk.DISABLED)
    if FORCE_EVAL["POTENTIAL"]=="Custom":
        FE_potential_entry.config(state="normal")

#Select the potential from the potential file in the potential folder 
def potential_click(set):
    FORCE_EVAL["POTENTIAL"]=set
    FE_potential_btn.config(text=FORCE_EVAL["POTENTIAL"])
    if FORCE_EVAL["POTENTIAL"]=="Custom":
        FE_potential_entry.config(state="normal")
    else:
        FE_potential_entry.config(state=tk.DISABLED)

#Select the Exchange-Correlation
def FE_XC_functional_button_click(functionals):
    global FORCE_EVAL
    FORCE_EVAL["XC_FUNCTIONAL"]=functionals
    FE_XC_functional_btn.config(text=FORCE_EVAL["XC_FUNCTIONAL"])
    if FORCE_EVAL["XC_FUNCTIONAL"]=="PBE" or FORCE_EVAL["XC_FUNCTIONAL"]=="PADE":
        FE_HF_X_check.config(state="normal")
        FE_XC_functional_custom_entry.config(state=tk.DISABLED)
    else:
        if FORCE_EVAL["XC_FUNCTIONAL"]=="CUSTOM":
            FE_XC_functional_custom_entry.config(state="normal")
        else:
            FE_XC_functional_custom_entry.config(state=tk.DISABLED)
        FE_HF_X_check.deselect()
        FORCE_EVAL["HF"]="FALSE"
        FE_HF_X_check.config(state=tk.DISABLED)
        FE_HF_X_entry.config(state=tk.DISABLED)

#Turn HF on and off
def HF_X_on_off_click():
    global FORCE_EVAL
    FORCE_EVAL["HF"]=FE_HF_X_var.get()
    if FORCE_EVAL["HF"]=="TRUE":
        FE_HF_X_entry.config(state="normal")
    else:
        FE_HF_X_entry.config(state=tk.DISABLED)

#Select the electronic structure method (QS)
def FE_QS_button_click(qs):
    global FORCE_EVAL
    FORCE_EVAL["QS"]=qs
    FE_QS_btn.config(text=FORCE_EVAL["QS"])

#Turn dispersion correction on and off
def FE_VDW_Pot_button_click(dis):
    global FORCE_EVAL
    FORCE_EVAL["VDW_POTENTIAL"]=dis
    FE_VDW_Pot_btn.config(text=FORCE_EVAL["VDW_POTENTIAL"])

#Select the diagonalization method
def FE_Diag_button_click(algo):
    global FORCE_EVAL
    FORCE_EVAL["DIAGONALIZATION"]=algo
    FE_Diag_btn.config(text=FORCE_EVAL["DIAGONALIZATION"])
    if FORCE_EVAL["DIAGONALIZATION"]=="OT":
        FE_OT_pre_btn.config(state="normal")
    else:
        FE_OT_pre_btn.config(state=tk.DISABLED)

#Select the diagonalization preconditioner method for OT
def FE_OT_pre_button_click(pre):
    global FORCE_EVAL
    FORCE_EVAL["PRECONDITIONER"]=pre
    FE_OT_pre_btn.config(text=FORCE_EVAL["PRECONDITIONER"])

#Find the pseudopotential file
def FE_potential_find_file_click():
    global FORCE_EVAL
    potential_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Potential file",filetypes = (("XYZ files","*.xyz"),("all files","*.*")))
    if str(potential_filename)!="":
        FORCE_EVAL["POTENTIAL_FILE_NAME"]=str(potential_filename)
        FE_potential_file_entry.delete(0,tk.END)
        FE_potential_file_entry.insert(tk.END,FORCE_EVAL["POTENTIAL_FILE_NAME"])

#Forecefield
#Select the parmeter type for MM
def FE_parmtype_button_click(types):
    global FORCE_EVAL
    FORCE_EVAL["PARMTYPE"]=types
    FE_parmtype_btn.config(text=FORCE_EVAL["PARMTYPE"])

#Find the parameter file
def FE_parm_file_click():
    global FORCE_EVAL
    parm_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("Pot files","*.pot"),("Dat files","*.dat"),("all files","*.*")))
    if str(parm_filename)!="":
        FORCE_EVAL["PARM_FILE_NAME"]=str(parm_filename)
        FE_parm_file_entry.delete(0,tk.END)
        FE_parm_file_entry.insert(tk.END,FORCE_EVAL["PARM_FILE_NAME"])



#/&SUBSYS------
#Find the coordination file in filedialog
def SS_coord_find_file_click():
    global SUBSYS
    coord_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("CIF files","*.cif"),("CRD files","*.crd"),("G96 files","*.g96"),("PDB files","*.pdb"),("XTL files","*.xtl"),("all files","*.*")))
    if str(coord_filename)!="":
        SUBSYS["COORD"]=str(coord_filename)
        SS_coord_file_entry.delete(0,tk.END)
        SS_coord_file_entry.insert(tk.END,SUBSYS["COORD"])

#Use the coord. file to get info
def SS_coord_use_file_click():
    global SUBSYS
    SUBSYS["COORD"]=SS_coord_file_entry.get()
    try:
        valence_e,element_text,SUBSYS["ELEMENTS"],SUBSYS["VALENCE_ELEMENTS"],SUBSYS["ABC"]=coord_file_info.file_extraction(SUBSYS["COORD"])
        SS_coord_info_e_label.config(text=str(valence_e))
        SS_coord_info_MO_label.config(text=str(int(valence_e/2)))
        SS_coord_info_elements_label.config(text=element_text)
        SS_Cell_entry.delete(0,tk.END)
        SS_Cell_entry.insert(tk.END,SUBSYS["ABC"])
    except:
        SS_coord_info_e_label.config(text="")
        SS_coord_info_MO_label.config(text="")
        SS_coord_info_elements_label.config(text="")
        SUBSYS["ELEMENTS"]=[]
        SUBSYS["VALENCE_ELEMENTS"]=[]
        popup=tk.Tk()
        popup.title("No such file")
        tk.Label(popup, text="Could not find or use the file called "+SUBSYS["COORD"]).pack()
        tk.Button(popup, text="  Okay  ", command = popup.destroy).pack()
        popup.mainloop()

#Centering molecule on/off
def SS_Centering_mol_on_off_click():
    global SUBSYS
    SUBSYS["CENTER_COORDINATES"]=SS_Centering_mol_var.get()

#Choose the directory of the periodic boundary condition
def SS_Periodic_button_click(direc):
    global SUBSYS
    SUBSYS["PERIODIC"]=direc
    SS_Periodic_btn.config(text=SUBSYS["PERIODIC"])
    if SUBSYS["PERIODIC"]=="XYZ":
        SS_Poisson_solver_btn.config(state=tk.DISABLED)
    else:
        SS_Poisson_solver_btn.config(state="normal")

#Choose the Poisson solver 
def SS_Poisson_solver_button_click(solver):
    global FORCE_EVAL
    FORCE_EVAL["POISSON_SOLVER"]=solver
    SS_Poisson_solver_btn.config(text=FORCE_EVAL["POISSON_SOLVER"])



#&EXT_RESTART------
#Set the save restart to on or off
def save_restart_on_off_click():
    global EXT_RESTART
    EXT_RESTART["SAVE_RESTART"]=save_restart_var.get()
    if EXT_RESTART["SAVE_RESTART"]=="TRUE":
        save_restart_entry.config(state="normal")
    else:
        save_restart_entry.config(state=tk.DISABLED)

#Set the restart to on or off
def restart_on_off_click():
    global EXT_RESTART
    EXT_RESTART["RESTART"]=restart_var.get()
    if EXT_RESTART["RESTART"]=="TRUE":
        restart_entry.config(state="normal")
        restart_find_file_btn.config(state="normal")
    else:
        restart_entry.config(state=tk.DISABLED)
        restart_find_file_btn.config(state=tk.DISABLED)

#Find the restart file
def restart_find_file_click():
    global EXT_RESTART
    restart_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("WFN files","*.wfn"),("Restart files","*.restart"),("all files","*.*")))
    if str(restart_filename)!="":
        EXT_RESTART["RESTART_FILE_NAME"]=str(restart_filename)
        restart_entry.delete(0,tk.END)
        restart_entry.insert(tk.END,EXT_RESTART["RESTART_FILE_NAME"])



#&MOTION-------

#Motion geometry optimization
#Choose what the optimizer is going towards
def MT_Geo_Opt_button_click(state):
    global MOTION
    MOTION["TYPE"]=state
    MT_Geo_Opt_btn.config(text=MOTION["TYPE"])
    if MOTION["TYPE"]=="TRANSITION_STATE":
        MT_Geo_Optimizer_btn.config(state=tk.DISABLED)
        MOTION["OPTIMIZER"]="CG"
        MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])
    else:
        MT_Geo_Optimizer_btn.config(state="normal")
        MOTION["OPTIMIZER"]="BFGS"
        MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])

#Choose the geometry optimizer
def MT_Geo_Optimizer_button_click(opti):
    global MOTION
    MOTION["OPTIMIZER"]=opti
    MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])

#Motion MD
#Choose the ensemble
def MT_MD_Ensemble_button_click(ens):
    global MOTION
    MOTION["ENSEMBLE"]=ens
    MT_MD_Ensemble_btn.config(text=MOTION["ENSEMBLE"])
    if MOTION["ENSEMBLE"]=="NPE_F" or MOTION["ENSEMBLE"]=="NPE_I":
        MT_MD_Thermostat_btn.config(state=tk.DISABLED)
        MT_MD_TIMECON_entry.config(state=tk.DISABLED)
    else:
        MT_MD_Thermostat_btn.config(state="normal")
        MT_MD_TIMECON_entry.config(state="normal")

#Choose the Thermostat
def MT_MD_Thermostat_button_click(thermo):
    global MOTION
    MOTION["THERMOSTAT"]=thermo
    MT_MD_Thermostat_btn.config(text=MOTION["THERMOSTAT"])
    if MOTION["THERMOSTAT"]=="GLE":
        MT_MD_TIMECON_entry.config(state=tk.DISABLED)
        MT_MD_TIMECON_label.config(state=tk.DISABLED)
    else:
        MT_MD_TIMECON_entry.config(state="normal")
        MT_MD_TIMECON_label.config(state="normal")


#Motion BAND
#Choose coord file for replica 1
def MT_BAND_initial_find_file_click():
    global MOTION
    MT_BAND_initial_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("CIF files","*.cif"),("CRD files","*.crd"),("G96 files","*.g96"),("PDB files","*.pdb"),("XTL files","*.xtl"),("all files","*.*")))
    if str(MT_BAND_initial_filename)!="":
        MOTION["REPLICA1"]=str(MT_BAND_initial_filename)
        MT_BAND_initial_entry.delete(0,tk.END)
        MT_BAND_initial_entry.insert(tk.END,MOTION["REPLICA1"])

#Choose coord file for replica 2
def MT_BAND_interm_find_file_click():
    global MOTION
    MT_BAND_interm_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("CIF files","*.cif"),("CRD files","*.crd"),("G96 files","*.g96"),("PDB files","*.pdb"),("XTL files","*.xtl"),("all files","*.*")))
    if str(MT_BAND_interm_filename)!="":
        MOTION["REPLICA2"]=str(MT_BAND_interm_filename)
        MT_BAND_interm_entry.delete(0,tk.END)
        MT_BAND_interm_entry.insert(tk.END,MOTION["REPLICA2"])

#Choose coord file for replica 3
def MT_BAND_final_find_file_click():
    global MOTION
    MT_BAND_final_filename=filedialog.askopenfilename(initialdir = "./",title = "Select Coord. file",filetypes = (("XYZ files","*.xyz"),("COORD files","*.coord"),("CIF files","*.cif"),("CRD files","*.crd"),("G96 files","*.g96"),("PDB files","*.pdb"),("XTL files","*.xtl"),("all files","*.*")))
    if str(MT_BAND_final_filename)!="":
        MOTION["REPLICA3"]=str(MT_BAND_final_filename)
        MT_BAND_final_entry.delete(0,tk.END)
        MT_BAND_final_entry.insert(tk.END,MOTION["REPLICA3"])

#Choose the Band_type
def MT_BAND_Band_type_button_click(band):
    global MOTION
    MOTION["BAND_TYPE"]=band
    MT_BAND_Band_type_btn.config(text=MOTION["BAND_TYPE"])

#Choose the Band optimizer
def MT_BAND_Band_opti_button_click(opti):
    global MOTION
    MOTION["OPTIMIZE_BAND"]=opti
    MT_BAND_Band_opti_btn.config(text=MOTION["OPTIMIZE_BAND"])


#---------------Program----------------
#Create the windows------
Interface=tk.Tk()
Interface.geometry(str(PROGRAM["size_of_window_width"])+"x"+str(PROGRAM["size_of_window_height"])+"+0+0")
#Window can not change size
Interface.resizable(width=False, height=False)
#Title of window
Interface.title(PROGRAM["Program_name"])

#Top Frame
Tops_Frame=tk.Frame(Interface,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_top_bottom"]),relief=tk.SUNKEN)
Tops_Frame.pack(side=tk.TOP)
#Bottom Frame
Bottom_Frame=tk.Frame(Interface,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_top_bottom"]),relief=tk.SUNKEN)
Bottom_Frame.pack(side=tk.BOTTOM,pady=PROGRAM["pady_section_size"])
#Middle Frame
Middle_Frame=tk.Frame(Interface,width=PROGRAM["size_of_window_width"],height=str(PROGRAM["size_of_window_height_middle"]),relief=tk.SUNKEN)
Middle_Frame.pack(pady=(PROGRAM["pady_section_size"],0),padx=PROGRAM["padx_section_size"],fill="both",expand=True)


#Setting up the Menu------
menubar=tk.Menu(Interface)
Interface.config(menu=menubar)
#Filemenu
filemenu=tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="New", command=new_input)
filemenu.add_command(label="Open", command=open_input)
filemenu.add_command(label="Save", command=Save)
filemenu.add_command(label="About", command=popup_About)
filemenu.add_command(label="Exit", command=popup_exit)
menubar.add_cascade(label="File", menu=filemenu)
#Function
functionmenu=tk.Menu(menubar,tearoff=0)
functionmenu.add_command(label="Cutoff test", command=Generate_cutoff_test)
menubar.add_cascade(label="Function", menu=functionmenu)
#Analyse
analysemenu=tk.Menu(menubar,tearoff=0)
analysemenu.add_command(label="CDFT", command=CDFT_details_function)
analysemenu.add_command(label="Convergence", command=Convergence_function)
analysemenu.add_command(label="Cutoff test", command=Analyse_cutoff_test_function)
analysemenu.add_command(label="MD energy", command=MD_energy_temp_function)
analysemenu.add_command(label="Optimization", command=Optimization_function)
analysemenu.add_command(label="UV-Vis", command=UV_Vis_function)
analysemenu.add_command(label="Vibrations", command=Vib_function)
menubar.add_cascade(label="Analyse", menu=analysemenu)
#Helpmenu
helpmenu=tk.Menu(menubar,tearoff=0)
helpmenu.add_command(label="Help", command=Help)
menubar.add_cascade(label="Help", menu=helpmenu)


#Setting up the Section windows------
#&Global Frame
GLOBAL_Frame=tk.Frame(Middle_Frame)
GLOBAL_Frame.place(in_=Middle_Frame, x=0, y=0, relwidth=1, relheight=1)
#&Force_Eval Frame
FORCE_EVAL_Frame=tk.Frame(Middle_Frame)
FORCE_EVAL_Frame.place(in_=Middle_Frame, x=0, y=0, relwidth=1, relheight=1)
#/&SUBSYS Frame
SUBSYS_Frame=tk.Frame(Middle_Frame)
SUBSYS_Frame.place(in_=Middle_Frame, x=0, y=0, relwidth=1, relheight=1)
#&EXT_RESTART Frame
EXT_RESTART_Frame=tk.Frame(Middle_Frame)
EXT_RESTART_Frame.place(in_=Middle_Frame, x=0, y=0, relwidth=1, relheight=1)
#&MOTION Frame
MOTION_Frame=tk.Frame(Middle_Frame)
MOTION_Frame.place(in_=Middle_Frame, x=0, y=0, relwidth=1, relheight=1)



#Make the Top------
#Rows
i=0
#Columns
j=0
#The button for the section &Global
sec_global=tk.Button(Tops_Frame,text="   &GLOBAL   ",fg="green",command=GLOBAL_Frame_btn_func)
sec_global.grid(row=i,column=j)
j+=1
#The button for the section &Force_Eval
sec_force_eval=tk.Button(Tops_Frame,text="   &FORCE_EVAL   ",fg="green",command=FORCE_EVAL_Frame_btn_func)
sec_force_eval.grid(row=i,column=j)
j+=1
#The button for the section &Subsys
sec_subsys=tk.Button(Tops_Frame,text="   &SUBSYS   ",fg="green",command=SUBSYS_Frame_btn_func)
sec_subsys.grid(row=i,column=j)
j+=1
#The button for the section EXT_RESTART
sec_ext_restart=tk.Button(Tops_Frame,text="     &EXT_RESTART   ",fg="green",command=EXT_RESTART_Frame_btn_func)
sec_ext_restart.grid(row=i,column=j)
j+=1
#The button for the section &MOTION
sec_motion=tk.Button(Tops_Frame,text="    &MOTION   ",fg="green",state=tk.DISABLED,command=MOTION_sec_Frame_func)
sec_motion.grid(row=i,column=j)
j+=1


#Make the Bottom-----
#Rows
i+=1
#Columns
j=0
#The button for save to input file
save_btn=tk.Button(Bottom_Frame,text="   SAVE   ",command=Save)
save_btn.grid(row=i,column=j)
j+=1
#The button for Preview to input file
preview_btn=tk.Button(Bottom_Frame,text="  PREVIEW  ",command=Preview)
preview_btn.grid(row=i,column=j)
j+=1
#The button for cancel program
cancel_btn=tk.Button(Bottom_Frame,text="   CANCEL   ",command=popup_exit)
cancel_btn.grid(row=i,column=j)
j+=1



#Make the &Global_section------
#Choose the Run Type
#Rows
i=0
#Columns
j=0
#Make the label for Run_Type
tk.Label(GLOBAL_Frame,text="Run type: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Run_Type button
run_type_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["RUN_TYPE"])
#Give it the function as a push down list / Menu
content_run_type_btn=tk.Menu(run_type_btn)
#So you can press the button and have the content
run_type_btn.config(menu=content_run_type_btn)
run_type_btn.grid(row=i,column=j)
#Give the options of Run_Types
run_type_list=["ENERGY","GEO_OPT","MD","BAND","RT_PROPAGATION"]
for types in run_type_list:
    content_run_type_btn.add_command(label=types,command=lambda types=types: Run_Type_button_click(types))

#Choose the Project Name
#Rows
i+=1
#Columns
j=0
#Make the label for Project Name
tk.Label(GLOBAL_Frame, text="Project name: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry
project_name_entry=tk.Entry(GLOBAL_Frame)
#Set the text to the right
project_name_entry.config(justify=tk.LEFT)
#Give the default Project Name
project_name_entry.insert(tk.END,GLOBAL["PROJECT_NAME"])
project_name_entry.grid(row=i,column=j)

#Choose the Print level
i+=1
j=0
#Make the label for Print_level
tk.Label(GLOBAL_Frame,text="Print level: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Print_Level button
print_level_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["PRINT_LEVEL"])
#Give it the function as a push down list / Menu
content_print_level_btn=tk.Menu(print_level_btn)
#So you can press the button and have the content
print_level_btn.config(menu=content_print_level_btn)
print_level_btn.grid(row=i,column=j)
#Give the options of Print_Level
print_level_list=["SILENT","LOW","MEDIUM","HIGH","DEBUG"]
for level in print_level_list:
    content_print_level_btn.add_command(label=level,command=lambda level=level: Print_Level_button_click(level))

#Choose the Properties
#Rows
i+=1
#Columns
j=0
#Make the label for Properties
tk.Label(GLOBAL_Frame,text="Properties: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Properties button
properties_btn=tk.Menubutton(GLOBAL_Frame,text=GLOBAL["PROPERTIES"])
#Give it the function as a push down list / Menu
content_properties_btn=tk.Menu(properties_btn)
#So you can press the button and have the content
properties_btn.config(menu=content_properties_btn)
properties_btn.grid(row=i,column=j)
#Give the options of Properties
properties_list=["NONE","MO","DIPOLE","TDDFPT","VIBRATIONAL_ANALYSIS","MULLIKEN","CDFT"]
for proper in properties_list:
    content_properties_btn.add_command(label=proper,command=lambda proper=proper: Properties_button_click(proper))
#Properties info 
i+=1
j=0
properties_info_nstates_label=tk.Label(GLOBAL_Frame,text="NStates: ")
properties_info_nstates_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
properties_info_nstates_entry=tk.Entry(GLOBAL_Frame,justify=tk.LEFT)
properties_info_nstates_entry.insert(tk.END,GLOBAL["NSTATES"])
properties_info_nstates_entry.grid(row=i,column=j)
if GLOBAL["PROPERTIES"]!="MO" or GLOBAL["PROPERTIES"]!="TDDFPT":
    properties_info_nstates_label.grid_forget()
    properties_info_nstates_entry.grid_forget()
#How often to Print 
i+=1
j=0
each_label=tk.Label(GLOBAL_Frame,text="Each step: ")
each_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
each_entry=tk.Entry(GLOBAL_Frame,justify=tk.LEFT)
each_entry.insert(tk.END,FORCE_EVAL["EACH"])
each_entry.grid(row=i,column=j)
if GLOBAL["RUN_TYPE"]=="ENERGY":
    each_label.grid_forget()
    each_entry.grid_forget()


#Make the &Force_Eval_section------
i=0
j=0
#Make the label for the Method
tk.Label(FORCE_EVAL_Frame,text="Method: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Method button
FE_method_btn=tk.Menubutton(FORCE_EVAL_Frame,text=FORCE_EVAL["METHOD"])
#Give it the function as a push down list / Menu
content_FE_method_btn=tk.Menu(FE_method_btn)
#So you can press the button and have the content
FE_method_btn.config(menu=content_FE_method_btn)
FE_method_btn.grid(row=i,column=j)
#Give the options of Methods
FE_method_list=["EIP","EMBED","FIST","MIXED","QMMM","QUICKSTEP","SIRIUS"]
for methods in FE_method_list:
    content_FE_method_btn.add_command(label=methods,command=lambda methods=methods: FE_Method_button_click(methods))



#DFT method
#DFT Window
FE_DFT_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_DFT_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)

#Make label for Basis set file
i=0
j=0
tk.Label(FE_DFT_Frame,text="Basis set file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#The path to the basis set folder
path_to_basis_set0=PROGRAM["Path"]+"data/Basis_set_folder/"
path_to_basis_set=FORCE_EVAL["BASIS_SET_FILE_NAME"][:-len(FORCE_EVAL["BASIS_SET_FILE_NAME-path"])]
#The basis set file menu
FE_basis_set_files_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["BASIS_SET_FILE_NAME-path"])
#Give it the function as a push down list / Menu
content_FE_basis_set_files_btn=tk.Menu(FE_basis_set_files_btn)
#So you can press the button and have the content
FE_basis_set_files_btn.config(menu=content_FE_basis_set_files_btn)
FE_basis_set_files_btn.grid(row=i,column=j)
#Give the options of basis set files
for files in BASIS_SET["BASIS_SETS_NAMES"]:
    content_FE_basis_set_files_btn.add_command(label=files,command=lambda files=files: basis_set_file_click(files))
#Make label for Basis set
i+=1
j=0
tk.Label(FE_DFT_Frame,text="Basis set: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#The basis set menu for each basis set file
FE_basis_set_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["BASIS_SET"])
BASIS_SET_OPTIONS={}
for key in BASIS_SET["BASIS_SETS_NAMES"]:
    #Make each basis set file to its own menu content
    BASIS_SET_OPTIONS[key]=tk.Menu(FE_basis_set_btn)
    #Give the options of basis set for each file
    for set in BASIS_SET[key]:
        BASIS_SET_OPTIONS[key].add_command(label=set,command=lambda set=set: basis_set_click(set))
    if key!="Find":
        BASIS_SET_OPTIONS[key].add_command(label="Custom",command=lambda set="Custom": basis_set_click(set))
#Basis set menu as default
#For files in the basis set directory
if FORCE_EVAL["BASIS_SET_FILE_NAME-path"] in BASIS_SET["BASIS_SETS_NAMES"]:
    FE_basis_set_btn.config(menu=BASIS_SET_OPTIONS[FORCE_EVAL["BASIS_SET_FILE_NAME-path"]])
#For files not in the basis set directory
else:
    FORCE_EVAL["BASIS_SET"]="Custom"
    FE_basis_set_btn.config(menu=BASIS_SET_OPTIONS["Find"],text=FORCE_EVAL["BASIS_SET"])
FE_basis_set_btn.grid(row=i,column=j)
j+=1
#Make Entry for Basis set file
FE_basis_set_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
#Give the default Basis set file
FE_basis_set_entry.grid(row=i,column=j)
#Select the default basis set
if FORCE_EVAL["BASIS_SET"]=="Custom":
    FE_basis_set_entry.config(state="normal")
else:
    FE_basis_set_entry.config(state=tk.DISABLED)


#Make label for Potential file
i+=1
j=0
tk.Label(FE_DFT_Frame,text="Pseudopotential file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#The path to the potential folder
path_to_potential0=PROGRAM["Path"]+"data/Potential_folder/"
path_to_potential=FORCE_EVAL["POTENTIAL_FILE_NAME"][:-len(FORCE_EVAL["POTENTIAL_FILE_NAME-path"])]
#The potential file menu
FE_potential_files_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["POTENTIAL_FILE_NAME-path"])
#Give it the function as a push down list / Menu
content_FE_potential_files_btn=tk.Menu(FE_potential_files_btn)
#So you can press the button and have the content
FE_potential_files_btn.config(menu=content_FE_potential_files_btn)
FE_potential_files_btn.grid(row=i,column=j)
#Give the options of potential files
for files in POTENTIAL["POTENTIALS_NAMES"]:
    content_FE_potential_files_btn.add_command(label=files,command=lambda files=files: potential_file_click(files))
#Make label for potentials
i+=1
j=0
tk.Label(FE_DFT_Frame,text="Pseudopotential: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#The potential menu for each potential file
FE_potential_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["POTENTIAL"])
POTENTIAL_OPTIONS={}
for key in POTENTIAL["POTENTIALS_NAMES"]:
    #Make each potential file to its own menu content
    POTENTIAL_OPTIONS[key]=tk.Menu(FE_potential_btn)
    #Give the options of potential for each file
    for set in POTENTIAL[key]:
        POTENTIAL_OPTIONS[key].add_command(label=set,command=lambda set=set: potential_click(set))
    if key!="Find" and key!="ECP_POTENTIALS.dat":
        POTENTIAL_OPTIONS[key].add_command(label="Custom",command=lambda set="Custom": potential_click(set))
#Potential menu as default
#For files in the potential directory
if FORCE_EVAL["POTENTIAL_FILE_NAME-path"] in POTENTIAL["POTENTIALS_NAMES"]:
    FE_potential_btn.config(menu=POTENTIAL_OPTIONS[FORCE_EVAL["POTENTIAL_FILE_NAME-path"]])
#For files not in the potential directory
else:
    FORCE_EVAL["POTENTIAL"]="Custom"
    FE_potential_btn.config(menu=POTENTIAL_OPTIONS["Find"],text=FORCE_EVAL["POTENTIAL"])
FE_potential_btn.grid(row=i,column=j)
j+=1
#Make Entry for Potential file
FE_potential_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
#Give the default Basis set file
FE_potential_entry.grid(row=i,column=j)
#Select the default potential
if FORCE_EVAL["POTENTIAL"]=="Custom":
    FE_potential_entry.config(state="normal")
else:
    FE_potential_entry.config(state=tk.DISABLED)


#Exchange-Correlation functional label
i+=1
j=0
FE_XC_functional_label=tk.Label(FE_DFT_Frame,text="Exchange-Correlation functional:  ")
FE_XC_functional_label.grid(row=i,column=j,pady=PROGRAM["pady_line_size"])
j+=1
#Exchange-Correlation functional button
FE_XC_functional_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["XC_FUNCTIONAL"])
#Give it the function as a push down list / Menu
content_FE_XC_functional_btn=tk.Menu(FE_XC_functional_btn)
#So you can press the button and have the content
FE_XC_functional_btn.config(menu=content_FE_XC_functional_btn)
FE_XC_functional_btn.grid(row=i,column=j)
#Give the options of XC functionals
FE_XC_functional_btn_list=["B3LYP","BEEFVDW","BLYP","BP","HCTH120","OLYP","PADE","PBE","PBE0","TPSS","NONE","NO_SHORTCUT","CUSTOM"]
for functionals in FE_XC_functional_btn_list:
    content_FE_XC_functional_btn.add_command(label=functionals,command=lambda functionals=functionals: FE_XC_functional_button_click(functionals))
#Make Entry for XCLIB functioncations when Custom is selected
j+=1
FE_XC_functional_custom_entry=tk.Entry(FE_DFT_Frame,text=FORCE_EVAL["LIBXC"])
#Set the text to the left
FE_XC_functional_custom_entry.config(justify=tk.LEFT)
#Only if XC_functional is custom the entry is active
if FORCE_EVAL["XC_FUNCTIONAL"]=="CUSTOM":
    FE_XC_functional_custom_entry.config(state="normal")
else:
    FE_XC_functional_custom_entry.config(state=tk.DISABLED)
#make the entry
FE_XC_functional_custom_entry.grid(row=i,column=j)
#HF Exchange
i+=1
j=0
FE_HF_X_label=tk.Label(FE_DFT_Frame,text="HF exchange:  ",justify=tk.LEFT)
FE_HF_X_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_HF_X_var=tk.StringVar()
FE_HF_X_check=tk.Checkbutton(FE_DFT_Frame,variable=FE_HF_X_var,onvalue="TRUE",offvalue="FALSE",state=tk.DISABLED,command=HF_X_on_off_click)
FE_HF_X_check.deselect()
FE_HF_X_check.grid(row=i,column=j)
if FORCE_EVAL["XC_FUNCTIONAL"]=="PBE" or FORCE_EVAL["XC_FUNCTIONAL"]=="PADE":
    FE_HF_X_check.config(state="normal")
j+=1
FE_HF_X_entry=tk.Entry(FE_DFT_Frame,justify=tk.LEFT)
FE_HF_X_entry.insert(tk.END,FORCE_EVAL["FRACTION"])
if FORCE_EVAL["HF"]=="TRUE":
    FE_HF_X_entry.config(state="normal")
else:
    FE_HF_X_entry.config(state=tk.DISABLED)
#make the entry
FE_HF_X_entry.grid(row=i,column=j)
#Electronic structure method (QS)
i+=1
j=0
FE_QS_label=tk.Label(FE_DFT_Frame,text="Electronic structure method:  ")
FE_QS_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Electronic structure method (QS) button
FE_QS_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["QS"])
#Give it the function as a push down list / Menu
content_FE_QS_btn=tk.Menu(FE_QS_btn)
#So you can press the button and have the content
FE_QS_btn.config(menu=content_FE_QS_btn)
FE_QS_btn.grid(row=i,column=j)
#Give the options of Electronic structure methods
FE_QS_btn_list=["AM1","DFTB","GAPW","GAPW_XC","GPW","LRIGPW","MNDO","MNDOD","OFGPW","PDG","PM3","PM6","PM6-FM","PNNL","RIGPW","RM1"]
for qs in FE_QS_btn_list:
    content_FE_QS_btn.add_command(label=qs,command=lambda qs=qs: FE_QS_button_click(qs))

#VDW Potential (dispersion correction)
i+=1
j=0
FE_VDW_Pot_label=tk.Label(FE_DFT_Frame,text="Dispersion correction:  ",justify=tk.LEFT)
FE_VDW_Pot_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_VDW_Pot_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["VDW_POTENTIAL"])
#Give it the function as a push down list / Menu
content_FE_VDW_Pot_btn=tk.Menu(FE_VDW_Pot_btn)
#So you can press the button and have the content
FE_VDW_Pot_btn.config(menu=content_FE_VDW_Pot_btn)
FE_VDW_Pot_btn.grid(row=i,column=j)
#Give the options of dispersion types
FE_VDW_Pot_btn_list=["NONE","DFTD2","DFTD3","DFTD3(BJ)"]
for dis in FE_VDW_Pot_btn_list:
    content_FE_VDW_Pot_btn.add_command(label=dis,command=lambda dis=dis: FE_VDW_Pot_button_click(dis))

#SCF subsection in DFT section
i+=1
j=0
FE_MAX_SCF_label=tk.Label(FE_DFT_Frame,text="MAX SCF cycles:  ",justify=tk.LEFT)
FE_MAX_SCF_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_MAX_SCF_entry=tk.Entry(FE_DFT_Frame)
FE_MAX_SCF_entry.insert(tk.END,FORCE_EVAL["MAX_SCF"])
FE_MAX_SCF_entry.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
i+=1
j=0
FE_EPS_SCF_label=tk.Label(FE_DFT_Frame,text="SCF criteria:  ",justify=tk.LEFT)
FE_EPS_SCF_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_EPS_SCF_entry=tk.Entry(FE_DFT_Frame)
FE_EPS_SCF_entry.insert(tk.END,FORCE_EVAL["EPS_SCF"])
FE_EPS_SCF_entry.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
#DIAGONALIZATION
i+=1
j=0
FE_Diag_label=tk.Label(FE_DFT_Frame,text="Diagonalization algorithm:  ",justify=tk.LEFT)
FE_Diag_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_Diag_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["DIAGONALIZATION"])
content_FE_Diag_btn=tk.Menu(FE_Diag_btn)
FE_Diag_btn.config(menu=content_FE_Diag_btn)
FE_Diag_btn.grid(row=i,column=j)
FE_Diag_btn_list=["DAVIDSON","FILTER_MATRIX","LANCZOS","OT","STANDARD"]
for algo in FE_Diag_btn_list:
    content_FE_Diag_btn.add_command(label=algo,command=lambda algo=algo: FE_Diag_button_click(algo))
#DIAGONALIZATION predconditioner for OT
j+=1
FE_OT_pre_btn=tk.Menubutton(FE_DFT_Frame,text=FORCE_EVAL["PRECONDITIONER"])
content_FE_OT_pre_btn=tk.Menu(FE_OT_pre_btn)
FE_OT_pre_btn.config(menu=content_FE_OT_pre_btn)
FE_OT_pre_btn.grid(row=i,column=j)
FE_OT_pre_btn_list=["FULL_ALL","FULL_KINETIC","FULL_SINGLE","FULL_SINGLE_INVERSE","FULL_S_INVERSE","NONE"]
for pre in FE_OT_pre_btn_list:
    content_FE_OT_pre_btn.add_command(label=pre,command=lambda pre=pre: FE_OT_pre_button_click(pre))
if FORCE_EVAL["DIAGONALIZATION"]=="OT":
    FE_OT_pre_btn.config(state="normal")
else:
    FE_OT_pre_btn.config(state=tk.DISABLED)
#MGRID
i+=1
j=0
FE_NGRIDS_label=tk.Label(FE_DFT_Frame,text="NGRIDS:  ",justify=tk.LEFT)
FE_NGRIDS_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_NGRIDS_entry=tk.Entry(FE_DFT_Frame)
FE_NGRIDS_entry.insert(tk.END,FORCE_EVAL["NGRIDS"])
FE_NGRIDS_entry.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
i+=1
j=0
FE_PW_Cutoff_label=tk.Label(FE_DFT_Frame,text="PW energy cutoff [Ry]:  ",justify=tk.LEFT)
FE_PW_Cutoff_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_PW_Cutoff_entry=tk.Entry(FE_DFT_Frame)
FE_PW_Cutoff_entry.insert(tk.END,FORCE_EVAL["CUTOFF"])
FE_PW_Cutoff_entry.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
i+=1
j=0
FE_Gau_Cutoff_label=tk.Label(FE_DFT_Frame,text="Gaussian energy cutoff [Ry]:  ",justify=tk.LEFT)
FE_Gau_Cutoff_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_Gau_Cutoff_entry=tk.Entry(FE_DFT_Frame)
FE_Gau_Cutoff_entry.insert(tk.END,FORCE_EVAL["REL_CUTOFF"])
FE_Gau_Cutoff_entry.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])


#EIP Method 
#EIP Window
FE_EIP_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_EIP_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_EIP_Frame,text="EIP Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])


#EMBED Method 
#EMBED Window
FE_EMBED_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_EMBED_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_EMBED_Frame,text="EMBED Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])


#FIST Method 
#FIST Window
FE_FIST_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_FIST_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_FIST_Frame,text="Forecefield section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
#Parmeter type
i+=1
tk.Label(FE_FIST_Frame,text="Parameters type:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
FE_parmtype_btn=tk.Menubutton(FE_FIST_Frame,text=FORCE_EVAL["PARMTYPE"])
content_FE_parmtype_btn=tk.Menu(FE_parmtype_btn)
FE_parmtype_btn.config(menu=content_FE_parmtype_btn)
FE_parmtype_btn.grid(row=i,column=j)
FE_parmtype_btn_list=["AMBER","CHM","G87","G96","OFF"]
for types in FE_parmtype_btn_list:
    content_FE_parmtype_btn.add_command(label=types,command=lambda types=types: FE_parmtype_button_click(types))
#Make label for Parameters file
tk.Label(FE_FIST_Frame,text="Parameters file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for Parameters file
FE_parm_file_entry=tk.Entry(FE_FIST_Frame,justify=tk.LEFT)
#Give the default Parameters file name
FE_parm_file_entry.insert(tk.END,FORCE_EVAL["PARM_FILE_NAME"])
FE_parm_file_entry.grid(row=i,column=j)
j+=1
#Find file
FE_parm_file_btn=tk.Button(FE_FIST_Frame,text="Find file",command=FE_parm_file_click)
FE_parm_file_btn.grid(row=i,column=j,sticky=tk.W)
j+=1



#MIXED Method 
#MIXED Window
FE_MIXED_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_MIXED_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_MIXED_Frame,text="MIXED Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])


#QMMM Method 
#QMMM Window
FE_QMMM_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_QMMM_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_QMMM_Frame,text="QMMM Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])


#SIRIUS Method 
#SIRIUS Window
FE_SIRIUS_Frame=tk.Frame(FORCE_EVAL_Frame)
FE_SIRIUS_Frame.place(in_=FORCE_EVAL_Frame, x=0, rely=0.1, relwidth=1, relheight=0.9)
i=0
j=0
tk.Label(FE_SIRIUS_Frame,text="SIRIUS Section:").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])




#Choose the start window for the Force Eval method
if FORCE_EVAL["METHOD"].upper()=="QUICKSTEP":
    FE_DFT_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="EIP":
    FE_EIP_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="EMBED":
    FE_EMBED_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="FIST":
    FE_FIST_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="MIXED":
    FE_MIXED_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="QMMM":
    FE_QMMM_Frame.lift()
elif FORCE_EVAL["METHOD"].upper()=="SIRIUS":
    FE_SIRIUS_Frame.lift()




#Make the &Subsys_section------
i=0
j=0
#Make label for coordination file
tk.Label(SUBSYS_Frame,text="Coordination file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for coordination file
SS_coord_file_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default Restart File Name
SS_coord_file_entry.insert(tk.END,SUBSYS["COORD"])
SS_coord_file_entry.grid(row=i,column=j)
j+=1
#Find file
SS_coord_find_file_btn=tk.Button(SUBSYS_Frame,text="Find coord. file",command=SS_coord_find_file_click)
SS_coord_find_file_btn.grid(row=i,column=j,sticky=tk.W)
j+=1

#Use coord. file button
i+=1
j=0
if len(SUBSYS["ELEMENTS"])>0:
    if SUBSYS["ELEMENTS"][0]=="[":
        SUBSYS["ELEMENTS"]=[]
tk.Label(SUBSYS_Frame,text="Generate info from coord. file: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
SS_coord_use_file_btn=tk.Button(SUBSYS_Frame,text="Generate",command=SS_coord_use_file_click)
SS_coord_use_file_btn.grid(row=i,column=j)

#Coord. file info
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Number valence electrons: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
SS_coord_info_e_label=tk.Label(SUBSYS_Frame,text="    ")
SS_coord_info_e_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Number valence occupied MOs: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
SS_coord_info_MO_label=tk.Label(SUBSYS_Frame,text="    ")
SS_coord_info_MO_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Elements: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
SS_coord_info_elements_label=tk.Label(SUBSYS_Frame,text="    ")
SS_coord_info_elements_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1

#Dimension of the Cell
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Cell [Angstrom]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for cell dimension
SS_Cell_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default Restart File Name
SS_Cell_entry.insert(tk.END,SUBSYS["ABC"])
SS_Cell_entry.grid(row=i,column=j)
j+=1

#Centering the molecule
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Centering molecule(s):  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make checkbox for centering
SS_Centering_mol_var=tk.StringVar()
SS_Centering_mol_check=tk.Checkbutton(SUBSYS_Frame,variable=SS_Centering_mol_var,onvalue="TRUE",offvalue="FALSE",command=SS_Centering_mol_on_off_click)
SS_Centering_mol_check.select()
SS_Centering_mol_check.grid(row=i,column=j)

#Periodic boundary condition
#Periodic label
i+=1
j=0
SS_Periodic_label=tk.Label(SUBSYS_Frame,text="Periodic:  ")
SS_Periodic_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Periodic button
SS_Periodic_btn=tk.Menubutton(SUBSYS_Frame,text=SUBSYS["PERIODIC"])
#Give it the function as a push down list / Menu
content_SS_Periodic_btn=tk.Menu(SS_Periodic_btn)
#So you can press the button and have the content
SS_Periodic_btn.config(menu=content_SS_Periodic_btn)
SS_Periodic_btn.grid(row=i,column=j)
#Give the options of boundary condition
SS_Periodic_btn_list=["NONE","X","XY","XYZ","XZ","Y","YZ","Z"]
for direc in SS_Periodic_btn_list:
    content_SS_Periodic_btn.add_command(label=direc,command=lambda direc=direc: SS_Periodic_button_click(direc))
j+=1
#POISSON_SOLVER button
SS_Poisson_solver_btn=tk.Menubutton(SUBSYS_Frame,text=FORCE_EVAL["POISSON_SOLVER"])
#Give it the function as a push down list / Menu
content_SS_Poisson_solver_btn=tk.Menu(SS_Poisson_solver_btn)
#So you can press the button and have the content
SS_Poisson_solver_btn.config(menu=content_SS_Poisson_solver_btn)
SS_Poisson_solver_btn.grid(row=i,column=j)
#Give the options of POISSON SOLVER
SS_Poisson_solver_btn_list=["ANALYTIC","IMPLICIT","MT","MULTIPOLE","PERIODIC","WAVELET"]
for solver in SS_Poisson_solver_btn_list:
    content_SS_Poisson_solver_btn.add_command(label=solver,command=lambda solver=solver: SS_Poisson_solver_button_click(solver))
#Only if XC_functional is custom the entry is active
if SUBSYS["PERIODIC"]=="XYZ":
    SS_Poisson_solver_btn.config(state=tk.DISABLED)
else:
    SS_Poisson_solver_btn.config(state="normal")

#CHARGE on the system
#Make label for coordination file
i+=1
j=0
tk.Label(SUBSYS_Frame,text="Charge: ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for Charge
SS_Charge_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default Charge
SS_Charge_entry.insert(tk.END,SUBSYS["CHARGE"])
SS_Charge_entry.grid(row=i,column=j)
j+=1

#Fixed atoms
#Make label for fixed atoms
i+=1
j=0
SS_fixed_atoms_label=tk.Label(SUBSYS_Frame,text="Fixed atoms: ")
SS_fixed_atoms_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for fixed atoms
SS_fixed_atoms_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default fixed atoms
SS_fixed_atoms_entry.insert(tk.END,SUBSYS["FIXED"])
SS_fixed_atoms_entry.grid(row=i,column=j)
j+=1
#Fixed atoms have to be a dynamic calculation
if GLOBAL["RUN_TYPE"]=="ENERGY" and GLOBAL["PROPERTIES"]!="VIBRATIONAL_ANALYSIS":
    SS_fixed_atoms_label.grid_forget()
    SS_fixed_atoms_entry.grid_forget()


#CDFT target value
#Make label for target valence electrons
i+=1
j=0
SS_target1_label=tk.Label(SUBSYS_Frame,text="Target valence 1: ")
SS_target1_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for target valence electrons
SS_target1_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default target value
SS_target1_entry.insert(tk.END,SUBSYS["TARGET1"])
SS_target1_entry.grid(row=i,column=j)
j+=1
#Make label for target valence electrons
i+=1
j=0
SS_target2_label=tk.Label(SUBSYS_Frame,text="Target valence 2: ")
SS_target2_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for target valence electrons
SS_target2_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default target value
SS_target2_entry.insert(tk.END,SUBSYS["TARGET2"])
SS_target2_entry.grid(row=i,column=j)
j+=1
#Make label for atoms in fragment 1
i+=1
j=0
SS_frag1_label=tk.Label(SUBSYS_Frame,text="Atoms in fragment 1: ")
SS_frag1_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for atoms in fragment 1
SS_frag1_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default atoms in fragment 1
SS_frag1_entry.insert(tk.END,SUBSYS["ATOMS_FRAG1"])
SS_frag1_entry.grid(row=i,column=j)
j+=1
#Make label for atoms in fragment 2
i+=1
j=0
SS_frag2_label=tk.Label(SUBSYS_Frame,text="Atoms in fragment 2: ")
SS_frag2_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for atoms in fragment 2
SS_frag2_entry=tk.Entry(SUBSYS_Frame,justify=tk.LEFT)
#Give the default atoms in fragment 2
SS_frag2_entry.insert(tk.END,SUBSYS["ATOMS_FRAG2"])
SS_frag2_entry.grid(row=i,column=j)
j+=1

#CDFT have to be the property
if GLOBAL["PROPERTIES"]!="CDFT":
    SS_target1_label.grid_forget()
    SS_target1_entry.grid_forget()
    SS_target2_label.grid_forget()
    SS_target2_entry.grid_forget()
    SS_frag1_label.grid_forget()
    SS_frag1_entry.grid_forget()
    SS_frag2_label.grid_forget()
    SS_frag2_entry.grid_forget()


#Make the &Ext_Restart section------
i=0
j=0
#Make a label
tk.Label(EXT_RESTART_Frame,text="Save restart file:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make a checkbutton to choose if you want to restart
save_restart_var=tk.StringVar()
save_restart_check=tk.Checkbutton(EXT_RESTART_Frame,variable=save_restart_var,onvalue="TRUE",offvalue="FALSE",command=save_restart_on_off_click)
save_restart_check.deselect()
save_restart_check.grid(row=i,column=j)

i+=1
j=0
tk.Label(EXT_RESTART_Frame,text="Save restart each:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry
save_restart_entry=tk.Entry(EXT_RESTART_Frame,justify=tk.LEFT)
#Give the default Restart File Name
save_restart_entry.insert(tk.END,EXT_RESTART["RESTART_EACH"])
save_restart_entry.grid(row=i,column=j)
if EXT_RESTART["SAVE_RESTART"]=="FALSE":
    save_restart_entry.config(state=tk.DISABLED)



#Make a label
i+=1
j=0
tk.Label(EXT_RESTART_Frame,text="Restart from a file:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make a checkbutton to choose if you want to restart
restart_var=tk.StringVar()
restart_check=tk.Checkbutton(EXT_RESTART_Frame,variable=restart_var,onvalue="TRUE",offvalue="FALSE",command=restart_on_off_click)
restart_check.deselect()
restart_check.grid(row=i,column=j)
j+=1

#Make Label
i+=1
j=0
tk.Label(EXT_RESTART_Frame,text="Restart file name:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry
restart_entry=tk.Entry(EXT_RESTART_Frame,justify=tk.LEFT)
#Give the default Restart File Name
restart_entry.insert(tk.END,EXT_RESTART["RESTART_FILE_NAME"])
restart_entry.grid(row=i,column=j)
j+=1
#Find file
restart_find_file_btn=tk.Button(EXT_RESTART_Frame,text="Find restart file",command=restart_find_file_click)
restart_find_file_btn.grid(row=i,column=j,sticky=tk.W)
if EXT_RESTART["RESTART"]=="FALSE":
    restart_entry.config(state=tk.DISABLED)
    restart_find_file_btn.config(state=tk.DISABLED)





#Make the &Motion_section------
#Geometry Optimization
#Geometry Optimization window
MT_Geo_Frame=tk.Frame(MOTION_Frame)
MT_Geo_Frame.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
#Optimize for ground state or TS state
i=0
j=0
tk.Label(MT_Geo_Frame,text="Type:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Optimizer button
MT_Geo_Opt_btn=tk.Menubutton(MT_Geo_Frame,text=MOTION["TYPE"])
#Give it the function as a push down list / Menu
content_MT_Geo_Opt_btn=tk.Menu(MT_Geo_Opt_btn)
#So you can press the button and have the content
MT_Geo_Opt_btn.config(menu=content_MT_Geo_Opt_btn)
MT_Geo_Opt_btn.grid(row=i,column=j)
#Give the options of what to go towards
MT_Geo_Opt_btn_list=["MINIMIZATION","TRANSITION_STATE"]
for state in MT_Geo_Opt_btn_list:
    content_MT_Geo_Opt_btn.add_command(label=state,command=lambda state=state: MT_Geo_Opt_button_click(state))
j+=1
#Optimizer
i+=1
j=0
tk.Label(MT_Geo_Frame,text="Optimizer:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Optimizer button
MT_Geo_Optimizer_btn=tk.Menubutton(MT_Geo_Frame,text=MOTION["OPTIMIZER"])
#Give it the function as a push down list / Menu
content_MT_Geo_Optimizer_btn=tk.Menu(MT_Geo_Optimizer_btn)
#So you can press the button and have the content
MT_Geo_Optimizer_btn.config(menu=content_MT_Geo_Optimizer_btn)
MT_Geo_Optimizer_btn.grid(row=i,column=j)
#Give the options of optimizer
MT_Geo_Optimizer_btn_list=["BFGS","CG","LBFGS"]
for opti in MT_Geo_Optimizer_btn_list:
    content_MT_Geo_Optimizer_btn.add_command(label=opti,command=lambda opti=opti: MT_Geo_Optimizer_button_click(opti))
j+=1
if MOTION["TYPE"]=="TRANSITION_STATE":
    MT_Geo_Optimizer_btn.config(state=tk.DISABLED)
    MOTION["OPTIMIZER"]="CG"
    MT_Geo_Optimizer_btn.config(text=MOTION["OPTIMIZER"])
#Max Force, the convergence criteria
i+=1
j=0
tk.Label(MT_Geo_Frame,text="Max geometry change:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for max Dr
MT_Geo_Max_Dr_entry=tk.Entry(MT_Geo_Frame,justify=tk.LEFT)
#Give the default Max Dr
MT_Geo_Max_Dr_entry.insert(tk.END,MOTION["MAX_DR"])
MT_Geo_Max_Dr_entry.grid(row=i,column=j)
j+=1
#Max Iterations for the geometry optimization
i+=1
j=0
tk.Label(MT_Geo_Frame,text="Max iterations:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for max iter
MT_Geo_Max_Iter_entry=tk.Entry(MT_Geo_Frame,justify=tk.LEFT)
#Give the default Max Iter
MT_Geo_Max_Iter_entry.insert(tk.END,MOTION["MAX_ITER"])
MT_Geo_Max_Iter_entry.grid(row=i,column=j)
j+=1


#MD
#MD window
MT_MD_Frame=tk.Frame(MOTION_Frame)
MT_MD_Frame.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
#Ensemble
#Ensemble label
i=0
j=0
tk.Label(MT_MD_Frame,text="Ensemble:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Ensemble button
MT_MD_Ensemble_btn=tk.Menubutton(MT_MD_Frame,text=MOTION["ENSEMBLE"])
#Give it the function as a push down list / Menu
content_MT_MD_Ensemble_btn=tk.Menu(MT_MD_Ensemble_btn)
#So you can press the button and have the content
MT_MD_Ensemble_btn.config(menu=content_MT_MD_Ensemble_btn)
MT_MD_Ensemble_btn.grid(row=i,column=j)
#Give the options of Ensembles
MT_MD_Ensemble_btn_list=["HYDROSTATICSHOCK","ISOKIN","LANGEVIN","MSST","MSST_DAMPED","NPE_F","NPE_I","NPT_F","NPT_I","NVE","NVT","NVT_ADIABATIC","REFTRAJ"]
for ens in MT_MD_Ensemble_btn_list:
    content_MT_MD_Ensemble_btn.add_command(label=ens,command=lambda ens=ens: MT_MD_Ensemble_button_click(ens))
j+=1
#Steps
i+=1
j=0
tk.Label(MT_MD_Frame,text="Steps:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for steps
MT_MD_steps_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
#Give the default steps
MT_MD_steps_entry.insert(tk.END,MOTION["STEPS"])
MT_MD_steps_entry.grid(row=i,column=j)
j+=1
#Timestep
i+=1
j=0
tk.Label(MT_MD_Frame,text="Timestep [fs]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for timestep
MT_MD_timestep_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
#Give the default timestep
MT_MD_timestep_entry.insert(tk.END,MOTION["TIMESTEP"])
MT_MD_timestep_entry.grid(row=i,column=j)
j+=1
#Temperature
i+=1
j=0
tk.Label(MT_MD_Frame,text="Temperature [K]:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for Temperature
MT_MD_temperature_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
#Give the default Temperature
MT_MD_temperature_entry.insert(tk.END,MOTION["TEMPERATURE"])
MT_MD_temperature_entry.grid(row=i,column=j)
j+=1
#THERMOSTAT
#THERMOSTAT label
i+=1
j=0
tk.Label(MT_MD_Frame,text="Thermostat:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#THERMOSTAT button
MT_MD_Thermostat_btn=tk.Menubutton(MT_MD_Frame,text=MOTION["THERMOSTAT"])
#Give it the function as a push down list / Menu
content_MT_MD_Thermostat_btn=tk.Menu(MT_MD_Thermostat_btn)
#So you can press the button and have the content
MT_MD_Thermostat_btn.config(menu=content_MT_MD_Thermostat_btn)
MT_MD_Thermostat_btn.grid(row=i,column=j)
#Give the options of Ensembles
MT_MD_Thermostat_btn_list=["AD_LANGEVIN","CSVR","GLE","NOSE"]
for thermo in MT_MD_Thermostat_btn_list:
    content_MT_MD_Thermostat_btn.add_command(label=thermo,command=lambda thermo=thermo: MT_MD_Thermostat_button_click(thermo))
j+=1
#Time constant
i+=1
j=0
MT_MD_TIMECON_label=tk.Label(MT_MD_Frame,text="Time constant [fs]:  ")
MT_MD_TIMECON_label.grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry for TIMECON
MT_MD_TIMECON_entry=tk.Entry(MT_MD_Frame,justify=tk.LEFT)
#Give the default TIMECON
MT_MD_TIMECON_entry.insert(tk.END,MOTION["TIMECON"])
MT_MD_TIMECON_entry.grid(row=i,column=j)
j+=1
if MOTION["THERMOSTAT"]=="GLE":
    MT_MD_TIMECON_entry.config(state=tk.DISABLED)
    MT_MD_TIMECON_label.config(state=tk.DISABLED)


#BAND
#BAND window
MT_BAND_Frame=tk.Frame(MOTION_Frame)
MT_BAND_Frame.place(in_=MOTION_Frame, x=0, y=0, relwidth=1, relheight=1.0)
#Initial coordinates
#Make Label
i=0
j=0
tk.Label(MT_BAND_Frame,text="Initial structure:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry of initial structure
MT_BAND_initial_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
#Give the default initial structure
MT_BAND_initial_entry.insert(tk.END,MOTION["REPLICA1"])
MT_BAND_initial_entry.grid(row=i,column=j)
j+=1
#Find file
MT_BAND_initial_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=MT_BAND_initial_find_file_click)
MT_BAND_initial_find_file_btn.grid(row=i,column=j,sticky=tk.W)
#Intermediate coordinates
#Make Label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Intermediate structure (Not needed):  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry of Intermediate structure
MT_BAND_interm_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
#Give the default Intermediate structure
MT_BAND_interm_entry.insert(tk.END,MOTION["REPLICA2"])
MT_BAND_interm_entry.grid(row=i,column=j)
j+=1
#Find file
MT_BAND_interm_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=MT_BAND_interm_find_file_click)
MT_BAND_interm_find_file_btn.grid(row=i,column=j,sticky=tk.W)
#Final coordinates
#Make Label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Final structure:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry of Final structure
MT_BAND_final_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
#Give the default Final structure
MT_BAND_final_entry.insert(tk.END,MOTION["REPLICA3"])
MT_BAND_final_entry.grid(row=i,column=j)
j+=1
#Find file
MT_BAND_final_find_file_btn=tk.Button(MT_BAND_Frame,text="Find file",command=MT_BAND_final_find_file_click)
MT_BAND_final_find_file_btn.grid(row=i,column=j,sticky=tk.W)
#BAND_TYPE
#BAND_TYPE label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Band type:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#BAND_TYPE button
MT_BAND_Band_type_btn=tk.Menubutton(MT_BAND_Frame,text=MOTION["BAND_TYPE"])
#Give it the function as a push down list / Menu
content_MT_BAND_Band_type_btn=tk.Menu(MT_BAND_Band_type_btn)
#So you can press the button and have the content
MT_BAND_Band_type_btn.config(menu=content_MT_BAND_Band_type_btn)
MT_BAND_Band_type_btn.grid(row=i,column=j)
#Give the options of BAND_TYPES
MT_BAND_Band_type_btn_list=["B-NEB","CI-NEB","D-NEB","EB","IT-NEB","SM"]
for band in MT_BAND_Band_type_btn_list:
    content_MT_BAND_Band_type_btn.add_command(label=band,command=lambda band=band: MT_BAND_Band_type_button_click(band))
#Number of replicas
#Make Label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Number of replicas:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry of Number of replicas
MT_BAND_num_replica_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
#Give the default Number of replicas
MT_BAND_num_replica_entry.insert(tk.END,MOTION["NUMBER_OF_REPLICA"])
MT_BAND_num_replica_entry.grid(row=i,column=j)
#BAND Optimizer
#BAND Optimizer label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Band optimizer:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#BAND Optimizer button
MT_BAND_Band_opti_btn=tk.Menubutton(MT_BAND_Frame,text=MOTION["OPTIMIZE_BAND"])
#Give it the function as a push down list / Menu
content_MT_BAND_Band_opti_btn=tk.Menu(MT_BAND_Band_opti_btn)
#So you can press the button and have the content
MT_BAND_Band_opti_btn.config(menu=content_MT_BAND_Band_opti_btn)
MT_BAND_Band_opti_btn.grid(row=i,column=j)
#Give the options of BAND Optimizer
MT_BAND_Band_opti_btn_list=["DIIS","MD"]
for opti in MT_BAND_Band_opti_btn_list:
    content_MT_BAND_Band_opti_btn.add_command(label=opti,command=lambda opti=opti: MT_BAND_Band_opti_button_click(opti))
#Max Steps
#Make Label
i+=1
j=0
tk.Label(MT_BAND_Frame,text="Max steps:  ").grid(row=i,column=j,sticky=tk.W,pady=PROGRAM["pady_line_size"])
j+=1
#Make Entry of Max Steps
MT_BAND_max_steps_entry=tk.Entry(MT_BAND_Frame,justify=tk.LEFT)
#Give the default Max Steps
MT_BAND_max_steps_entry.insert(tk.END,MOTION["MAX_STEPS"])
MT_BAND_max_steps_entry.grid(row=i,column=j)


if GLOBAL["RUN_TYPE"].upper()=="GEO_OPT":
    sec_motion.config(state="normal",fg="green")
    MT_Geo_Frame.lift()
elif GLOBAL["RUN_TYPE"].upper()=="MD" or GLOBAL["RUN_TYPE"].upper()=="RT_PROPAGATION":
    sec_motion.config(state="normal",fg="green")
    MT_MD_Frame.lift()
elif GLOBAL["RUN_TYPE"].upper()=="BAND":
    sec_motion.config(state="normal",fg="green")
    MT_BAND_Frame.lift()




#Run the program-----
Interface.lift()
GLOBAL_Frame.lift()
sec_global.config(fg="blue")
Interface.mainloop()

