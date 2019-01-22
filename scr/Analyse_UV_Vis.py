#Made by Andreas Vishart
#------------Package---------------------------
import numpy as np
#------------Functions------------------------------
#Extract excitation data from file
def extract(filename):
    with open(filename) as thefile:
        content=thefile.readlines()
    #Find the wavelength & oscillator strength of the transitions 
    wave_trans=[]; osc_trans=[]
    hc_from_eV=6.62607004*1e-34*299792458/(1.6021766208e-19)
    for line in content:
        if "TDDFPT|" in line:
            state=list(filter(None,line.split(" ")))
            wave_trans.append(hc_from_eV/float(state[2])*10**9)
            osc_trans.append(float(state[-1]))
    wavelength_interval=np.linspace(wave_trans[-1]-50,wave_trans[0]+50,int(2*(wave_trans[0]-wave_trans[-1]+100)+1))
    return wave_trans,osc_trans,wavelength_interval

#Calculate the molar absorption coefficients
def epsilon(wavelength_interval,wave_trans,osc_trans,sigma):
    #Avogadros Number
    NA=6.022140857e23
    #Elemental charge
    e=1.6021766208e-19
    #Electron mass
    me=9.10938356e-31
    #Vacuum permittivity
    eps0=8.8541878176e-12
    #Speed of light
    c=299792458
    #Planck's constant
    h=6.62607004*1e-34
    #Constant k 
    k=NA*e**2*np.sqrt(np.log(2)/np.pi)/(2*np.log(10)*me*eps0*c**2)
    #print(k)
    k2=k/sigma
    #Calculate molar absorption coefficients
    epsi=[]
    for w in wavelength_interval:
        epsi_inter=0
        for j in range(len(wave_trans)):
            epsi_inter+=osc_trans[j]*np.exp(-4*np.log(2)*((1/w-1/wave_trans[j])/(sigma*1e-7))**2)
        epsi.append(k2*epsi_inter)
    return epsi

#Show Uv-Vis plot with oscillator strength for only one data set
def plot_uv_vis_osc(uv_vis_data,sigma):
    import matplotlib as mpl
    import platform
    if platform.system()=="Darwin":
        mpl.use("TkAgg")
    import matplotlib.pyplot as plt
    #Extract excitation data from file
    wave_trans,osc_trans,wavelength_interval=uv_vis_data
    #Calculate the molar absorption coefficitent
    epsi=epsilon(wavelength_interval,wave_trans,osc_trans,sigma)
    #Plot Uv-Vis with oscillator strength
    fig,ax1=plt.subplots(figsize=(8,6))
    ax2=ax1.twinx()
    ax1.set_xlabel("Wavelength / [nm]",fontsize=15)
    ax1.set_ylabel(r"$\epsilon$ / [M$^{-1}$ cm$^{-1}$]",color="b",fontsize=15)
    ax2.set_ylabel("Oscillator strength",color="r",fontsize=15)
    ax1.plot(wavelength_interval,epsi,"b-")
    ax2.bar(wave_trans,osc_trans,width=1,color="r")
    ax1.set_xlim(wavelength_interval[0],wavelength_interval[-1])
    ax1.set_ylim(0,max(epsi)*1.1)
    ax1.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax2.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
    ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax2.set_ylim(0,max(osc_trans)*1.25)
    plt.tight_layout()
    plt.show()
    plt.close()

def show_uv_vis_plot(uv_vis_data,fwhm_entry):
    sigma=float(fwhm_entry.get())
    plot_uv_vis_osc(uv_vis_data,sigma)

def UV_Vis_pop_up(filename):
    import sys
    #Python 3
    if str(sys.version)[0]=="3":
        import tkinter as tk
    #Python 2
    elif str(sys.version)[0]=="2":
        import Tkinter as tk 
    uv_vis_data=extract(filename)
    #Full width half maximum [cm^-1]
    sigma=3226.00
    popup_uv_vis=tk.Tk()
    popup_uv_vis.title("UV-Vis")
    tk.Label(popup_uv_vis, text="FWHM [cm"+u"\u207b"+u"\u00B9"+"]:").grid(row=1,column=0,sticky=tk.W)
    fwhm_entry=tk.Entry(popup_uv_vis)
    fwhm_entry.insert(tk.END,sigma)
    fwhm_entry.grid(row=1,column=2,sticky=tk.W)
    tk.Button(popup_uv_vis, text="Show", command=lambda uv_vis_data=uv_vis_data: show_uv_vis_plot(uv_vis_data,fwhm_entry)).grid(row=2,column=1)
    tk.Button(popup_uv_vis, text="Close", command = popup_uv_vis.destroy).grid(row=3,column=1)
    return popup_uv_vis