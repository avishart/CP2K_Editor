#Made by Andreas Vishart
#Extract the MD energy and temperature data from an .ener file
def MD_Ener(filename):
  import numpy as np
  #Load the ener file
  with open(filename) as thefile:
    content=thefile.readlines()
  #Parameters
  Time=[]; Tot_E=[]; Temp=[]
  #Get the parameters
  content=content[1:]
  for line in content:
    con=list(filter(None,line.split(" ")))
    Time.append(float(con[1]))
    Tot_E.append(float(con[2])+float(con[4]))
    Temp.append(float(con[3]))
  Temp2=np.cumsum(Temp)/np.arange(1.0,len(Temp)+1.0,1.0)
  return Time,Tot_E,Temp2
  
#Plot the MD energy and temperature
def plot_MD_Ener(MD_data):
  import matplotlib as mpl
  import platform
  if platform.system()=="Darwin":
    mpl.use("TkAgg")
  import matplotlib.pyplot as plt
  #Get MD data
  Time,Tot_E,Temp2=MD_data
  #Plot the data
  fig,ax1=plt.subplots(figsize=(8,6))
  ax2=ax1.twinx()
  ax1.set_xlabel("Time / [fs]",fontsize=15)
  ax1.set_ylabel("Total energy / [A.U.]",color="b",fontsize=15)
  ax2.set_ylabel("Average temperature / [K]",color="r",fontsize=15)
  ax1.plot(Time,Tot_E,"b-")
  ax2.plot(Time,Temp2,"r-")
  ax1.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
  ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
  ax2.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
  ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
  plt.tight_layout()
  plt.show()
  plt.close()
