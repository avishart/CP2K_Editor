#Made by Andreas Vishart
import matplotlib as mpl
import platform
if platform.system()=="Darwin":
    mpl.use("TkAgg")
import matplotlib.pyplot as plt

#------------Functions------------------------------
#Extract excitation data from file
def extract(filename):
    with open(filename) as thefile:
        content=thefile.readlines()
    #Find the wavelength & oscillator strength of the transitions 
    vib_state=[]
    vib_state_num=1
    freq=[]
    intens=[]
    for line in content:
        if "VIB|Frequency (cm^-1)" in line:
            state=list(filter(None,line.split(" ")))
            for num in range(2,len(state)):
                freq.append(float(state[num]))
                vib_state.append(vib_state_num)
                vib_state_num+=1
        if "VIB|Intensities" in line:
            state=list(filter(None,line.split(" ")))
            for num in range(1,len(state)):
                intens.append(float(state[num]))
    return freq,intens,vib_state

def show_vib_plot(filename,freq,intens,vib_state):
    plot_vib(filename,freq,intens,vib_state)

#Vib plot with oscillator strength for only one data set
def plot_vib(filename,freq,intens,vib_state):
    #Extract excitation data from file
    freq,intens,vib_state=extract(filename)
    #Plot Vib with intensities
    fig,ax1=plt.subplots(figsize=(8,6))
    ax1.bar(freq,intens,width=5,color="r")
    ax1.set_xlabel("Frequency / [cm$^{-1}$]",fontsize=15)
    ax1.set_ylabel("Intensity / [M$^{-1}$ cm$^{-1}$]",fontsize=15)
    ax1.set_xlim(freq[0]-50,freq[-1]+50)
    ax1.set_ylim(0,max(intens)*1.05)
    plt.tight_layout()
    plt.show()
    plt.close()

#Make the vibrational data as text in a table
def text_vibration(freq,intens,vib_state):
    thetext=""
    space_len=10
    space=" "*space_len
    space_state=len("Vib. state")
    space_freq=len("Freq. / [cm^-1]")
    thetext+="Vib. state"+space+"Freq. / [cm^-1]"+space+"Intensity"+"\n"
    for states in range(len(vib_state)):
        thetext+=str(vib_state[states])+" "*abs(space_len+space_state-len(str(vib_state[states])))
        thetext+="{0:.3E}".format(freq[states])+" "*abs(space_len+space_freq-len("{0:.3E}".format(freq[states])))
        thetext+="{0:.3E}".format(intens[states])+"\n"
    return thetext

#Vibration list popup window
def Vibration_popup(filename):
    import sys
    #Python 3
    if str(sys.version)[0]=="3":
        import tkinter as tk
    #Python 2
    elif str(sys.version)[0]=="2":
        import Tkinter as tk 
    #Extract excitation data from file
    freq,intens,vib_state=extract(filename)
    #Get vibrational data as text 
    list_vibration=text_vibration(freq,intens,vib_state)
    #Make popup window
    popup_vib=tk.Tk()
    popup_vib.title("Vibrations")
    tk.Button(popup_vib, text="Close", command = popup_vib.destroy).pack(side=tk.BOTTOM)
    tk.Button(popup_vib, text="Show", command=lambda filename=filename: show_vib_plot(filename,freq,intens,vib_state)).pack(side=tk.BOTTOM)
    scrollbar=tk.Scrollbar(popup_vib)
    label=tk.Text(popup_vib)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    label.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar.config(command=label.yview)
    label.config(yscrollcommand=scrollbar.set)
    label.insert(tk.END, list_vibration)
    label.config(state=tk.DISABLED)
    return popup_vib
    