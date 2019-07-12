#Made by Andreas Vishart
#Plot the Geometry from a .xyz file
import numpy as np
import sys
#Python 3
if str(sys.version)[0]=="3":
    import tkinter as tk
#Python 2
elif str(sys.version)[0]=="2":
    import Tkinter as tk 
import matplotlib as mpl
import platform
if platform.system()=="Darwin":
  mpl.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

#Extract detail for elements and cell size from xyz or coord file
def coord_file_extract(filename):
  with open(filename) as thefile:
    content=thefile.readlines()
  if filename[-3:]=="xyz":
    content=content[2:]
  Elements=[]
  xyz=[[],[],[]]
  for line in content:
    if "i = " in line:
      Elements=[]
      xyz=[[],[],[]]
      continue
    newline=list(filter(None,line.split(" ")))
    try:
      Elements.append(newline[0])
      xyz[0].append(float(newline[1]))
      xyz[1].append(float(newline[2]))
      xyz[2].append(float(newline[3]))
    except:
      pass
  Dif_Elements={}
  for num in range(len(Elements)):
    if Elements[num] not in [key for key in Dif_Elements.keys()]:
      #Dif_Elements["Different_Elements"].append(Elements[num])
      Dif_Elements[str(Elements[num])]=[[xyz[i][num]] for i in range(3)]
    else:
      for i in range(3):
        Dif_Elements[str(Elements[num])][i].append(xyz[i][num])
  return Dif_Elements

#Distance between two elements
def distance(coord1,coord2):
    distance=0
    for i in range(3):
        distance+=(coord2[i]-coord1[i])**2
    return np.sqrt(distance)

def bonds_between_atoms(element1,element2,bond_length):
  bond_list=[]
  for e1 in range(len(element1[0])):
    e1_list=[element1[i][e1] for i in range(3)]
    for e2 in range(len(element2[0])):
      e2_list=[element2[i][e2] for i in range(3)]
      dis=distance(e1_list,e2_list)
      if bond_length>dis>0:
        bond_list.append([[element1[i][e1],element2[i][e2]] for i in range(3)])
  return bond_list

def Atom_properties():
    Elements={}
    Elements["Element"]=["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar",
                            "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
                            "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"]

    Elements["Number"]=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 
                            47, 48, 49, 50, 51, 52, 53, 54]

    Elements["Valence"]=[1,2,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,
                            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
                            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

    Elements["VdW"]=[1.20,1.40,1.82,1.53,1.92,1.70,1.55,1.52,1.47,1.54,2.27,1.73,1.84,2.10,1.80,1.80,1.75,1.88,
                            2.75,2.31,None,None,None,None,None,None,None,1.63,1.40,1.39,1.87,2.11,1.85,1.90,1.85,2.02,
                            3.03,2.49,None,None,None,None,None,None,None,1.63,1.72,1.58,1.93,2.17,2.06,2.06,1.98,2.16]

    Elements["Row"]=[1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,
                            4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
                            5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]

    Elements["Group"]=[1,18,1,2,13,14,15,16,17,18,1,2,13,14,15,16,17,18,
                            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
                            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

    Elements["Covalent_radii"]=[0.32,0.46,1.33,1.02,0.85,0.75,0.71,0.63,0.64,0.67,1.55,1.39,1.26,1.16,1.11,1.03,0.99,0.96,
                            1.96,1.71,1.48,1.36,1.34,1.22,1.19,1.16,1.11,1.10,1.12,1.18,1.24,1.21,1.21,1.16,1.14,1.17,
                            2.10,1.85,1.63,1.54,1.47,1.38,1.28,1.25,1.25,1.20,1.28,1.36,1.42,1.40,1.40,1.36,1.33,1.31]
    Elements["Color"]=['gray','salmon', 'indianred', 'navajowhite','sienna', 'k', 'b','r', 'lightsalmon',  'bisque', 'lavender', 'blanchedalmond', 'darksalmon', 'darkred', 'darkgrey', 'maroon', 'darkorchid', 'darkolivegreen', 'khaki', 'darkkhaki', 'brown', 'palegoldenrod', 'gold', 'papayawhip', 'peachpuff', 'goldenrod', 'lightcoral', 'silver', 'darkorange', 'burlywood', 'darkgoldenrod', 'peru', 'olive', 'mistyrose', 'firebrick', 'cornsilk', 'seashell', 'lemonchiffon', 'orange', 'saddlebrown', 'chocolate', 'coral', 'orangered', 'sandybrown', 'tan', 'floralwhite', 'wheat', 'mediumturquoise', 'tomato', 'ivory', 'beige', 'lightseagreen', 'rosybrown', 'oldlace', 'moccasin']
    Elements["Color_extra"]=['k', 'dimgray', 'gray','darkgray', 'darkgrey', 'silver', 'lightgray', 'gainsboro', 'rosybrown', 'lightcoral', 'indianred', 'brown', 'firebrick', 'maroon', 'darkred', 'r', 'mistyrose', 'salmon', 'tomato', 'darksalmon', 'coral', 'orangered', 'lightsalmon', 'sienna', 'seashell', 'chocolate', 'saddlebrown', 'sandybrown', 'peachpuff', 'peru', 'linen', 'bisque', 'darkorange', 'burlywood', 'antiquewhite', 'tan', 'navajowhite', 'blanchedalmond', 'papayawhip', 'moccasin', 'orange', 'wheat', 'oldlace', 'floralwhite', 'darkgoldenrod', 'goldenrod', 'cornsilk', 'gold', 'lemonchiffon', 'khaki', 'palegoldenrod', 'darkkhaki', 'ivory', 'beige', 'lightyellow', 'lightgoldenrodyellow', 'olive', 'y', 'olivedrab', 'yellowgreen', 'darkolivegreen', 'greenyellow', 'chartreuse', 'lawngreen', 'honeydew', 'darkseagreen', 'palegreen', 'lightgreen', 'forestgreen', 'limegreen', 'darkgreen', 'g', 'lime', 'seagreen', 'mediumseagreen', 'springgreen', 'mintcream', 'mediumspringgreen', 'mediumaquamarine', 'aquamarine', 'turquoise', 'lightseagreen', 'mediumturquoise', 'azure', 'lightcyan', 'paleturquoise', 'darkslategray', 'darkslategrey', 'teal', 'darkcyan', 'c', 'darkturquoise', 'cadetblue', 'powderblue', 'lightblue', 'deepskyblue', 'skyblue', 'lightskyblue', 'steelblue','dodgerblue', 'lightslategray', 'lightslategrey', 'slategray', 'slategrey', 'lightsteelblue', 'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender', 'midnightblue', 'navy', 'darkblue', 'mediumblue', 'b', 'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'blueviolet', 'indigo', 'darkorchid', 'darkviolet', 'mediumorchid', 'thistle', 'plum', 'violet', 'purple', 'darkmagenta', 'm', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink', 'lavenderblush', 'palevioletred', 'crimson', 'pink', 'lightpink']
    return Elements

def bond_length_element(element1,element2,Elements):
  if element1 in Elements["Element"] and element2 in Elements["Element"]:
    bond_len=(Elements["Covalent_radii"][Elements["Element"].index(element1)]+Elements["Covalent_radii"][Elements["Element"].index(element2)])*1.2
  else:
    bond_len=1.5
  return bond_len

#Plot the Geometry
def plot_Geometry(elements_coord,ABC):
  Elements=Atom_properties()
  #Plot the data
  fig=plt.figure()
  ax=fig.add_subplot(111, projection='3d')
  Elements["Color"]
  for key1 in elements_coord.keys():
    if key1 in Elements["Element"]:
      size_marker=(Elements["Covalent_radii"][Elements["Element"].index(key1)]*10)**2
      color_marker=Elements["Color"][Elements["Number"][Elements["Element"].index(key1)]-1]
    else:
      size_marker=50
      color_marker="gray"
    ax.scatter(elements_coord[key1][0],elements_coord[key1][1],elements_coord[key1][2],s=size_marker,c=color_marker,label=key1)
    for key2 in elements_coord.keys():
      bond_len=bond_length_element(key1,key2,Elements)
      bonds_list=bonds_between_atoms(elements_coord[key1],elements_coord[key2],bond_len)
      for i in range(len(bonds_list)):
        ax.plot(bonds_list[i][0],bonds_list[i][1],bonds_list[i][2],"k-")
  #Plot cell
  ABC_cell=list(filter(None,ABC.replace("\n","").split(" ")))
  ABC_cell=[float(dim) for dim in ABC_cell]
  if ABC_cell!=[0.00,0.00,0.00]:
    ax.plot([0,ABC_cell[0]],[0,0],[0,0],"k-")
    ax.plot([0,0],[0,ABC_cell[1]],[0,0],"k-")
    ax.plot([0,0],[0,0],[0,ABC_cell[2]],"k-")
    ax.plot([0,ABC_cell[0]],[ABC_cell[1],ABC_cell[1]],[0,0],"k-")
    ax.plot([ABC_cell[0],ABC_cell[0]],[0,ABC_cell[1]],[0,0],"k-")
    ax.plot([0,0],[ABC_cell[1],ABC_cell[1]],[0,ABC_cell[2]],"k-")
    ax.plot([ABC_cell[0],ABC_cell[0]],[0,0],[0,ABC_cell[2]],"k-")
    ax.plot([ABC_cell[0],ABC_cell[0]],[ABC_cell[1],ABC_cell[1]],[0,ABC_cell[2]],"k-")
    ax.plot([0,ABC_cell[0]],[0,0],[ABC_cell[2],ABC_cell[2]],"k-")
    ax.plot([0,0],[0,ABC_cell[1]],[ABC_cell[2],ABC_cell[2]],"k-")
    ax.plot([0,ABC_cell[0]],[ABC_cell[1],ABC_cell[1]],[ABC_cell[2],ABC_cell[2]],"k-")
    ax.plot([ABC_cell[0],ABC_cell[0]],[0,ABC_cell[1]],[ABC_cell[2],ABC_cell[2]],"k-")
  ax.set_xlabel("x / [Angstrom]",fontsize=15)
  ax.set_ylabel("y / [Angstrom]",fontsize=15)
  ax.set_zlabel("z / [Angstrom]",fontsize=15)
  ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
  ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
  ax.legend(loc=0)
  plt.axis('off')
  plt.tight_layout()
  plt.show()
  plt.close()


#Geometry popup window
class Geometry_popup:
  def __init__(self,master,filename):
    #Extract elements data from file
    self.dif_Elements=coord_file_extract(filename)
    #Cell size
    self.ABC="0.00 0.00 0.00"
    #Make popup window
    master.title("Geometry")
    #Cell shows
    self.ABC_check_label=tk.Label(master,text="Show cell:").grid(row=0,column=0,sticky=tk.W)
    self.ABC_size_entry=tk.Entry(master,justify=tk.LEFT)
    self.ABC_size_entry.insert(tk.END,self.ABC)
    self.ABC_size_entry.config(state=tk.DISABLED)
    self.ABC_check_var=tk.StringVar(master)
    self.ABC_check=tk.Checkbutton(master,variable=self.ABC_check_var,onvalue="TRUE",offvalue="FALSE",state="normal",command=lambda: self.ABC_check_command())
    self.ABC_check.deselect()
    self.ABC_check.grid(row=0,column=3,sticky=tk.W)
    self.ABC_size_label=tk.Label(master,text="Cell size:").grid(row=1,column=0,sticky=tk.W)
    self.ABC_size_entry.grid(row=1,column=3,sticky="WE")
    tk.Button(master, text="Show", command=lambda filename=filename: self.Show_Geometry()).grid(row=2,column=1,sticky="WE")
    tk.Button(master, text="Close", command = master.destroy).grid(row=3,column=1,sticky="WE")

  #The checkbutton command
  def ABC_check_command(self):
    if self.ABC_check_var.get()=="TRUE":
      self.ABC_size_entry.config(state="normal")
      ABC_max=[0,0,0]
      for ele in self.dif_Elements.keys():
        for dim in range(3):
          max_dim=max(self.dif_Elements[ele][dim])
          if max_dim>ABC_max[dim]:
            ABC_max[dim]=round(max_dim,2)
      self.ABC=str(ABC_max[0])+" "+str(ABC_max[1])+" "+str(ABC_max[2])
      self.ABC_size_entry.delete(0,tk.END)
      self.ABC_size_entry.insert(tk.END,self.ABC)
    elif self.ABC_check_var.get()=="FALSE":
      self.ABC="0.00 0.00 0.00"
      self.ABC_size_entry.delete(0,tk.END)
      self.ABC_size_entry.insert(tk.END,self.ABC)
      self.ABC_size_entry.config(state=tk.DISABLED)

  #Plot the geometry in 3d with or without the cell
  def Show_Geometry(self):
    ABC_size=self.ABC_size_entry.get()
    plot_Geometry(self.dif_Elements,ABC_size)
