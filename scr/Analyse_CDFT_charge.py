#Made by Andreas Vishart
import sys
#Python 3
if str(sys.version)[0]=="3":
    import tkinter as tk
    from tkinter import filedialog
#Python 2
elif str(sys.version)[0]=="2":
    import Tkinter as tk
    import tkFileDialog as filedialog

#Get the charges of fragments and charge difference for state 1
def charge_of_frag_state1(content):
    group=False
    charge=False
    frag1=[]
    frag2=[]
    charge_content=[]
    #Get which atoms are in each fragment
    for line in content:
        if "Becke group definitions" in line:
            group=True
        elif "--------" in line:
            group=False
        if group==True:
            newline=list(filter(None,line.split(" ")))
            if newline[0].isdigit():
                if float(newline[2])>0:
                    frag1.append(newline[0])
                elif float(newline[2])<0:
                    frag2.append(newline[0])
        if "Becke atomic charges" in line:
            charge=True
            charge_content.append([])
        elif "Total Charge" in line:
            charge=False
        if charge==True:
            charge_content[-1].append(line)
    #Calculate the charge of each fragment
    charge_frag1=0
    charge_frag2=0
    for line in charge_content[-1]:
        newline=list(filter(None,line.split(" ")))
        if newline[0].isdigit():
            if newline[0] in frag1:
                charge_frag1+=float(newline[4])+float(newline[5])
            if newline[0] in frag2:
                charge_frag2+=float(newline[4])+float(newline[5])
    #return the atoms in frag1, the atoms in frag2, charge of fragment 1, charge of fragment 2 and the difference in charge
    return frag1,frag2,charge_frag1,charge_frag2,charge_frag2-charge_frag1

#Get the charges of fragments and charge difference for state 2
def charge_of_frag_state2(content,frag1,frag2):
    charge=False
    charge_content=[]
    #Get which atoms are in each fragment
    for line in content:
        if "Becke atomic charges" in line:
            charge=True
            charge_content.append([])
        elif "Total Charge" in line:
            charge=False
        if charge==True:
            charge_content[-1].append(line)
    #Calculate the charge of each fragment
    charge_frag1=0
    charge_frag2=0
    for line in charge_content[-1]:
        newline=list(filter(None,line.split(" ")))
        if newline[0].isdigit():
            if newline[0] in frag1:
                charge_frag1+=float(newline[4])+float(newline[5])
            if newline[0] in frag2:
                charge_frag2+=float(newline[4])+float(newline[5])
    #return the atoms in frag1, the atoms in frag2, charge of fragment 1, charge of fragment 2 and the difference in charge
    return charge_frag1,charge_frag2,charge_frag2-charge_frag1

#Find the state 1 file
def state1_file_click(state1_entry):
    state1_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("CDFT files","*.cdftLog"),("all files","*.*")))
    if str(state1_filename)!="":
        state1_entry.delete(0,tk.END)
        state1_entry.insert(tk.END,state1_filename)

#Find the state 2 file
def state2_file_click(state2_entry):
    state2_filename=filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("CDFT files","*.cdftLog"),("all files","*.*")))
    if str(state2_filename)!="":
        state2_entry.delete(0,tk.END)
        state2_entry.insert(tk.END,state2_filename)

#CDFT start popup window (Initial)
def CDFT_start_popup():
    popup_cdft_start=tk.Tk()
    popup_cdft_start.title("CDFT charge")
    tk.Label(popup_cdft_start, text="State 1:").grid(row=1,column=0,sticky=tk.W)
    state1_entry=tk.Entry(popup_cdft_start, text="")
    state1_entry.grid(row=1,column=1)
    state1_file_btn=tk.Button(popup_cdft_start,text="Find file",command=lambda: state1_file_click(state1_entry))
    state1_file_btn.grid(row=1,column=2)
    tk.Label(popup_cdft_start, text="State 2:").grid(row=2,column=0,sticky=tk.W)
    state2_entry=tk.Entry(popup_cdft_start, text="")
    state2_entry.grid(row=2,column=1)
    state2_file_btn=tk.Button(popup_cdft_start,text="Find file",command=lambda: state2_file_click(state2_entry))
    state2_file_btn.grid(row=2,column=2)
    tk.Button(popup_cdft_start, text="Use", command = lambda:  use_files(popup_cdft_start,state1_entry.get(),state2_entry.get())).grid(row=3,column=1)
    tk.Button(popup_cdft_start, text="Close", command = popup_cdft_start.destroy).grid(row=3,column=2)
    return popup_cdft_start

def use_files(popup_cdft_start,state1_file,state2_file):
    if "state2" in state1_file or len(state1_file)==0:
        cdft_error()
    else:
        with open(state1_file) as thefile:
            content=thefile.readlines()
        try:
            frag1,frag2,charge_frag1,charge_frag2,dif_charge=charge_of_frag_state1(content)
        except:
            popup_error_file(state1_file)
        else:
            if state2_file!="":
                with open(state2_file) as thefile:
                    content2=thefile.readlines()
                try:
                    charge_frag1_st2,charge_frag2_st2,dif_charge_st2=charge_of_frag_state2(content2,frag1,frag2)
                except:
                    popup_error_file(state2_file)
                else:
                    popup_cdft_start.destroy()
                    CDFT_results_popup(charge_frag1,charge_frag2,dif_charge,charge_frag1_st2,charge_frag2_st2,dif_charge_st2)
            else:
                charge_frag1_st2,charge_frag2_st2,dif_charge_st2=False,False,False
                popup_cdft_start.destroy()
                CDFT_results_popup(charge_frag1,charge_frag2,dif_charge,charge_frag1_st2,charge_frag2_st2,dif_charge_st2)

def cdft_error():
    popup_error=tk.Tk()
    popup_error.title("Error")
    tk.Label(popup_error, text="State 1 is needed!").pack()
    tk.Button(popup_error, text="  Okay  ", command = popup_error.destroy).pack()
    popup_error.mainloop()

def popup_error_file(filename):
    popup_error=tk.Tk()
    popup_error.title("No such file")
    tk.Label(popup_error, text="Could not find or use the file called "+str(filename)).pack()
    tk.Button(popup_error, text="  Okay  ", command = popup_error.destroy).pack()
    return popup_error

#CDFT popup window (Results)
def CDFT_results_popup(charge_frag1,charge_frag2,dif_charge,charge_frag1_st2,charge_frag2_st2,dif_charge_st2):
    popup_cdft=tk.Tk()
    popup_cdft.title("CDFT")
    tk.Label(popup_cdft, text="State 1:").grid(row=1,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text="Charge for fragment 1 = ").grid(row=2,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text="{0:.4f}".format(charge_frag1)).grid(row=2,column=1)
    tk.Label(popup_cdft, text="Charge for fragment 2 = ").grid(row=3,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text="{0:.4f}".format(charge_frag2)).grid(row=3,column=1)
    tk.Label(popup_cdft, text="Charge difference = ").grid(row=4,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text="{0:.4f}".format(dif_charge)).grid(row=4,column=1)
    if charge_frag1_st2 and charge_frag2_st2 and dif_charge_st2:
        tk.Label(popup_cdft, text="State 2:").grid(row=5,column=0,sticky=tk.W)
        tk.Label(popup_cdft, text="Charge for fragment 1 = ").grid(row=6,column=0,sticky=tk.W)
        tk.Label(popup_cdft, text="{0:.4f}".format(charge_frag1_st2)).grid(row=6,column=1)
        tk.Label(popup_cdft, text="Charge for fragment 2 = ").grid(row=7,column=0,sticky=tk.W)
        tk.Label(popup_cdft, text="{0:.4f}".format(charge_frag2_st2)).grid(row=7,column=1)
        tk.Label(popup_cdft, text="Charge difference = ").grid(row=8,column=0,sticky=tk.W)
        tk.Label(popup_cdft, text="{0:.4f}".format(dif_charge_st2)).grid(row=8,column=1)
    tk.Button(popup_cdft, text="Close", command = popup_cdft.destroy).grid(row=9,column=1)
    return popup_cdft
