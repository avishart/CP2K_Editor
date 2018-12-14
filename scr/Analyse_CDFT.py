#Made by Andreas Vishart
import sys
#Python 3
if str(sys.version)[0]=="3":
    import tkinter as tk
#Python 2
elif str(sys.version)[0]=="2":
    import Tkinter as tk

#Function for extracting details from CDFT calculation
def CDFT_details(filename):
    #Load the out file
    with open(filename) as thefile:
        content=thefile.readlines()
    #Parameters
    rotation=["-"];lowdin=["-"];target1=["-"];target2=["-"]
    #Get the elctronic couplings and target values
    for line in content:
        if "Diabatic electronic coupling (rotation, mHartree):" in line:
            con=list(filter(None,line.split(" ")))[5]
            rotation.append(str(con))
        if "Diabatic electronic coupling (Lowdin, mHartree):" in line:
            con=list(filter(None,line.split(" ")))[5]
            lowdin.append(str(con))
        if "Final value of constraint I:" in line:
            con=list(filter(None,line.split(" ")))[5]
            target1.append(str(con))
        if "Final value of constraint J:" in line:
            con=list(filter(None,line.split(" ")))[5]
            target2.append(str(con))
    return rotation[-1].replace("\n",""),lowdin[-1].replace("\n",""),target1[-1].replace("\n",""),target2[-1].replace("\n","")

#CDFT popup window (Results)
def CDFT_popup(cdft_file):
    rotation,lowdin,target1,target2=CDFT_details(cdft_file)
    popup_cdft=tk.Tk()
    popup_cdft.title("CDFT")
    tk.Label(popup_cdft, text="Rotation diabatic electronic coupling / [mHartree]:").grid(row=1,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text=str(rotation)).grid(row=1,column=2)
    tk.Label(popup_cdft, text="Lowdin diabatic electronic coupling / [mHartree]:").grid(row=2,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text=str(lowdin)).grid(row=2,column=2)
    tk.Label(popup_cdft, text="Final value of constraint 1:").grid(row=3,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text=str(target1)).grid(row=3,column=2)
    tk.Label(popup_cdft, text="Final value of constraint 2:").grid(row=4,column=0,sticky=tk.W)
    tk.Label(popup_cdft, text=str(target2)).grid(row=4,column=2)
    tk.Button(popup_cdft, text="Close", command = popup_cdft.destroy).grid(row=5,column=1)
    return popup_cdft
