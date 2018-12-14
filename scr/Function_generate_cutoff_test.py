#Give the script the input file of interest after the script name
#Made by Andreas Vishart
#----------Package-----------
import os
import numpy as np
import copy as cp
import sys
#Python 3
if str(sys.version)[0]=="3":
    import tkinter as tk
#Python 2
elif str(sys.version)[0]=="2":
    import Tkinter as tk

#----------Parameters--------

def popup_generate_cutoff(generate_cutoff_file):
    popup_cutoff=tk.Tk()
    popup_cutoff.title("Cutoff test")
    tk.Label(popup_cutoff, text="Cutoff test",font=(16)).grid(row=0,column=1,sticky=tk.W)
    tk.Label(popup_cutoff, text="MAX SCF:").grid(row=1,column=0,sticky=tk.W)
    cutoff_max_scf_entry=tk.Entry(popup_cutoff)
    cutoff_max_scf_entry.insert(tk.END,"5")
    cutoff_max_scf_entry.grid(row=1,column=1)
    tk.Label(popup_cutoff, text="PW cutoff from").grid(row=2,column=0,sticky=tk.W)
    cutoff_pw_cutoff_from_entry=tk.Entry(popup_cutoff)
    cutoff_pw_cutoff_from_entry.insert(tk.END,"50")
    cutoff_pw_cutoff_from_entry.grid(row=2,column=1)
    tk.Label(popup_cutoff, text="PW cutoff to").grid(row=3,column=0,sticky=tk.W)
    cutoff_pw_cutoff_to_entry=tk.Entry(popup_cutoff)
    cutoff_pw_cutoff_to_entry.insert(tk.END,"500")
    cutoff_pw_cutoff_to_entry.grid(row=3,column=1)
    tk.Label(popup_cutoff, text="PW cutoff fix").grid(row=4,column=0,sticky=tk.W)
    cutoff_pw_cutoff_fix_entry=tk.Entry(popup_cutoff)
    cutoff_pw_cutoff_fix_entry.insert(tk.END,"280")
    cutoff_pw_cutoff_fix_entry.grid(row=4,column=1)
    tk.Label(popup_cutoff, text="Gau cutoff from").grid(row=5,column=0,sticky=tk.W)
    cutoff_gau_cutoff_from_entry=tk.Entry(popup_cutoff)
    cutoff_gau_cutoff_from_entry.insert(tk.END,"10")
    cutoff_gau_cutoff_from_entry.grid(row=5,column=1)
    tk.Label(popup_cutoff, text="Gau cutoff to").grid(row=6,column=0,sticky=tk.W)
    cutoff_gau_cutoff_to_entry=tk.Entry(popup_cutoff)
    cutoff_gau_cutoff_to_entry.insert(tk.END,"100")
    cutoff_gau_cutoff_to_entry.grid(row=6,column=1)
    tk.Label(popup_cutoff, text="Gau cutoff fix").grid(row=7,column=0,sticky=tk.W)
    cutoff_gau_cutoff_fix_entry=tk.Entry(popup_cutoff)
    cutoff_gau_cutoff_fix_entry.insert(tk.END,"40")
    cutoff_gau_cutoff_fix_entry.grid(row=7,column=1)
    cutoff_genterate_btn=tk.Button(popup_cutoff,text="Generate",command=lambda generate_cutoff_file=generate_cutoff_file: Cutoff_save_parameters(generate_cutoff_file,popup_cutoff,cutoff_max_scf_entry,cutoff_pw_cutoff_from_entry,cutoff_pw_cutoff_to_entry,cutoff_pw_cutoff_fix_entry,cutoff_gau_cutoff_from_entry,cutoff_gau_cutoff_to_entry,cutoff_gau_cutoff_fix_entry))
    cutoff_genterate_btn.grid(row=8,column=1)
    popup_cutoff.mainloop()
    

def Cutoff_save_parameters(generate_cutoff_file,popup_cutoff,cutoff_max_scf_entry,cutoff_pw_cutoff_from_entry,cutoff_pw_cutoff_to_entry,cutoff_pw_cutoff_fix_entry,cutoff_gau_cutoff_from_entry,cutoff_gau_cutoff_to_entry,cutoff_gau_cutoff_fix_entry):
    max_scf=int(cutoff_max_scf_entry.get())
    pw_cutoff_from=float(cutoff_pw_cutoff_from_entry.get())
    pw_cutoff_to=float(cutoff_pw_cutoff_to_entry.get())
    pw_cutoff_fix=float(cutoff_pw_cutoff_fix_entry.get())
    gau_cutoff_from=float(cutoff_gau_cutoff_from_entry.get())
    gau_cutoff_to=float(cutoff_gau_cutoff_to_entry.get())
    gau_cutoff_fix=float(cutoff_gau_cutoff_fix_entry.get())
    popup_cutoff.destroy()
    Function_cutoff_test(generate_cutoff_file,pw_cutoff_from,pw_cutoff_to,pw_cutoff_fix,gau_cutoff_from,gau_cutoff_to,gau_cutoff_fix,max_scf)
    

def Function_cutoff_test(inputfile,pw_cutoff_from,pw_cutoff_to,pw_cutoff_fix,gau_cutoff_from,gau_cutoff_to,gau_cutoff_fix,max_scf):
    #Plane Wave cutoff energies in Ry
    pw_cutoff=np.linspace(pw_cutoff_from,pw_cutoff_to,(pw_cutoff_to-pw_cutoff_from)/pw_cutoff_from+1)
    #Gaussian cutoff energies in Ry
    gau_cutoff=np.linspace(gau_cutoff_from,gau_cutoff_to,(gau_cutoff_to-gau_cutoff_from)/gau_cutoff_from+1)
    #Folder_start
    folder="CUTOFF_TEST"
    #Path to the input file
    path=inputfile[:-len(list(inputfile.split("/"))[-1])]
    #Downlad the input file
    with open(inputfile) as thefile:
        content=thefile.readlines()
    #The filename without ending
    filename=inputfile[len(path):]
    filename=filename[:-4]  
    #New folder name with the name of the input file
    folder=folder+"_"+str(filename)  
    #Make the new folder at the path of the file
    if os.path.exists(str(path)+str(folder)):
        for allfiles in os.listdir(str(path)+str(folder)):
            os.unlink(str(path)+str(folder)+"/"+allfiles)
        os.rmdir(str(path)+str(folder))
        os.system("mkdir "+str(path)+str(folder))
    else:
        os.system("mkdir "+str(path)+str(folder))
    #Change Cutoff, Rel_cutoff, Max_scf and generate the files 
    for gau in gau_cutoff:
        Global_section=False
        SCF_section=False
        MGRIG_section=False
        newfile=open(path+folder+"/"+filename+"_"+str(max_scf)+"_"+str(gau)+"_"+str(pw_cutoff_fix)+".inp","w")
        newcontent=cp.copy(content)
        for line in newcontent:
            if "&GLOBAL" in line:
                Global_section=True
            elif "&END GLOBAL" in line:
                Global_section=False
            if "PRINT_LEVEL" in line and Global_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],"MEDIUM")
            if "&SCF" in line:
                SCF_section=True
            elif "&END SCF" in line:
                SCF_section=False
            if " MAX_SCF " in line and SCF_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(max_scf))
            if "&MGRID" in line:
                MGRIG_section=True
            elif "&END MGRID" in line:
                MGRIG_section=False
            if " CUTOFF " in line and MGRIG_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(pw_cutoff_fix))
            if " REL_CUTOFF " in line and MGRIG_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(gau))
            newfile.write(line)
        newfile.close()         
    for pw in pw_cutoff:
        SCF_section=False
        MGRIG_section=False
        newfile=open(path+folder+"/"+filename+"_"+str(max_scf)+"_"+str(gau_cutoff_fix)+"_"+str(pw)+".inp","w")
        newcontent=cp.copy(content)
        for line in newcontent:
            if "&SCF" in line:
                SCF_section=True
            elif "&END SCF" in line:
                SCF_section=False
            if " MAX_SCF " in line and SCF_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(max_scf))
            if "&MGRID" in line:
                MGRIG_section=True
            elif "&END MGRID" in line:
                MGRIG_section=False
            if " CUTOFF " in line and MGRIG_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(pw))
            if " REL_CUTOFF " in line and MGRIG_section==True:
                newline=line.replace("\n"," ")
                newline=list(filter(None,newline.split(" ")))
                line=line.replace(newline[1],str(gau_cutoff_fix))
            newfile.write(line)
        newfile.close()
    popup_saved=tk.Tk()
    popup_saved.title("Saved")
    label=tk.Label(popup_saved,text="The input folder is saved")
    label.grid(row=0)
    B1=tk.Button(popup_saved,text="Okay",command=popup_saved.destroy)
    B1.grid(row=1)
    popup_saved.mainloop()

