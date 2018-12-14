#Made by Andreas Vishart
import sys
#Python 3

if str(sys.version)[0]=="3":
    import tkinter as tk
#Python 2
elif str(sys.version)[0]=="2":
    import Tkinter as tk

#Convergence function
def Convergence(filename):
    #Load the out file
    with open(filename) as thefile:
        content=thefile.readlines()
    #Parameters
    conv_step=[]
    conv_rms_step=[]
    conv_grad=[]
    conv_rms_grad=[]
    #Get the 4 convergence criteria
    for line in content:
        if "Convergence in step size" in line or "Convergence for step size" in line:
            con=list(filter(None,line.split(" ")))[5]
            conv_step.append(str(con))
        if "Convergence in RMS step" in line or "Convergence for RMS step" in line:
            con=list(filter(None,line.split(" ")))[5]
            conv_rms_step.append(str(con))
        if "Conv. in gradients" in line or "Conv. for gradients" in line:
            con=list(filter(None,line.split(" ")))[4]
            conv_grad.append(str(con))
        if "Conv. in RMS gradients" in line:
            con=list(filter(None,line.split(" ")))[5]
            conv_rms_grad.append(str(con))
        elif "Conv. for gradients" in line:
            con=list(filter(None,line.split(" ")))[4]
            conv_rms_grad.append(str(con))
    return conv_step[-1].replace("\n",""),conv_rms_step[-1].replace("\n",""),conv_grad[-1].replace("\n",""),conv_rms_grad[-1].replace("\n","")

#Convergence popup window (Results)
def Convergence_popup(convergence_file):
    conv_step,conv_rms_step,conv_grad,conv_rms_grad=Convergence(convergence_file)
    popup_conv=tk.Tk()
    popup_conv.title("Convergence")
    tk.Label(popup_conv, text="Convergence in step size").grid(row=1,column=0,sticky=tk.W)
    tk.Label(popup_conv, text=str(conv_step)).grid(row=1,column=2)
    tk.Label(popup_conv, text="Convergence in RMS step").grid(row=2,column=0,sticky=tk.W)
    tk.Label(popup_conv, text=str(conv_rms_step)).grid(row=2,column=2)
    tk.Label(popup_conv, text="Conv. in gradients").grid(row=3,column=0,sticky=tk.W)
    tk.Label(popup_conv, text=str(conv_grad)).grid(row=3,column=2)
    tk.Label(popup_conv, text="Conv. in RMS gradients").grid(row=4,column=0,sticky=tk.W)
    tk.Label(popup_conv, text=str(conv_rms_grad)).grid(row=4,column=2)
    tk.Button(popup_conv, text="Close", command=popup_conv.destroy).grid(row=5,column=1)
    return popup_conv
