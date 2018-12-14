#Made by Andreas Vishart
#Extract the Geometry optimization data from an .xyz file
def Optimization(filename):
  #Load the pos file
  with open(filename) as thefile:
    content=thefile.readlines()
  #Parameters
  Iteration=[]; iter=0; Energy=[]
  #Get the energy and count iterations
  for line in content:
    if "i = " in line:
      con=list(filter(None,line.split(" ")))[5]
      Energy.append(float(con))
      Iteration.append(iter)
      iter+=1
  #Energy change
  energy_change=100*abs(float(con)-Energy[-2])/Energy[-2]
  return Iteration,Energy,energy_change

#Plot the Optimization
def plot_Optimization(Optimization_data):
  import matplotlib as mpl
  import matplotlib.pyplot as plt
  #Get Optimization data
  Iteration,Energy,energy_change=Optimization_data
  #Plot the data
  fig,ax1=plt.subplots(figsize=(8,6))
  ax1.plot(Iteration,Energy,"bo-")
  ax1.set_xlabel("Iteration steps",fontsize=15)
  ax1.set_ylabel("Energy / [A.U.]",fontsize=15)
  ax1.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
  ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
  ax1.set_title("Energy change for last iteration: "+"{0:.2E}".format(energy_change)+" %",fontsize=15,y=1.06)
  plt.tight_layout()
  plt.show()
  plt.close()
