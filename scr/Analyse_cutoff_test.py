#Made by Andreas Vishart
#----------FUNCTIONS--------
#Extracting the fixed value, the list of the x component which is different to each other,
#the relative energy, the total energy, the convergence after the iteration and number of functions in each grid 
def extracting_each(thelist,rel_energy_list,energy_list,Conv_list):
    dif_list=[]
    count_list=[]
    order_list=[]
    #extract the x component and its energy
    for i in range(len(thelist)):
        if thelist[i] not in dif_list:
            dif_list.append(thelist[i])
            count_list.append(1)
            order_list.append(i)
        else:
            indi=dif_list.index(thelist[i])
            count_list[indi]+=1
    #Find the fixed cutoff
    indi=count_list.index(max(count_list))
    max_value=dif_list[indi]
    #Remove the fixed cutoff
    del dif_list[indi]
    del order_list[indi]
    #Sort the x component after size
    dif_list_sorted=sorted(dif_list)
    #Order the energy, relative energy, convergence and grid info after same order
    order_list_val=[dif_list.index(i) for i in dif_list_sorted]
    order_list2=[order_list[i] for i in order_list_val]
    rel_energy=[rel_energy_list[i] for i in order_list2]
    energy=[energy_list[i] for i in order_list2]
    Conv=[Conv_list[i] for i in order_list2]
    return max_value,dif_list_sorted,rel_energy,energy,Conv

#Make data for cutoff test
def Cutoff_test(foldername):
    import os
    #List all files in directory
    all_files=os.listdir(foldername)
    #Plane Wave cutoff energy in Ry
    pw_cutoff=[]
    #Gaussian cutoff energy in Ry
    gau_cutoff=[]
    energy=[]
    Conv_section=False
    Conv=[]
    #Extract data from all the files
    for thefile in all_files:
        if thefile[-4:]==".out":
            filesep=list(thefile[:-4].split("_"))
            pw_cutoff.append(float(filesep[-1]))
            gau_cutoff.append(float(filesep[-2]))
            max_scf=float(filesep[-3])
            Conv_list=[]
            conv_num=1
            with open(foldername+"/"+thefile) as extract:
                content=extract.readlines()
            for line in content:
                #Energy
                if "ENERGY| Total FORCE_EVAL" in line:
                    energy.append(float(list(filter(None,line.split(" ")))[-1]))
                #Convergence data
                if float(max_scf)>1:
                    if "SCF WAVEFUNCTION OPTIMIZATION" in line:
                        Conv_section=True
                    elif "Electronic density on regular grids" in line:
                        Conv_section=False
                    if list(filter(None,line.split(" ")))[0]==str(conv_num) and Conv_section==True:
                        newline=list(filter(None,line.split(" ")))
                        if len(newline)==8:
                            Conv_list.append(float(newline[-2]))
                        elif len(newline)<8:
                            Conv_list.append(float(newline[-1]))
                        conv_num+=1
            #Use the first and last energy for the convergence
            if float(max_scf)>1:
                Conv.append(abs((float(Conv_list[-1])-float(Conv_list[-2]))/float(Conv_list[-2])))
    #Find the relative energy
    E_min=min(energy)
    Energy_list=[abs((e-E_min)/E_min) for e in energy]
    #Extract all data at the x component in focus
    pw_cutoff_fix,pw_cutoff_new,rel_energy_pw,energy_pw,Conv_pw=extracting_each(pw_cutoff,Energy_list,energy,Conv)
    gau_cutoff_fix,gau_cutoff_new,rel_energy_gau,energy_gau,Conv_gau=extracting_each(gau_cutoff,Energy_list,energy,Conv)
    return pw_cutoff_new,rel_energy_pw,gau_cutoff_new,rel_energy_gau,Conv_pw,Conv_gau,max_scf

#Show and plot the cutoff test
def plot_cutoff_test(cutoff_data):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    #Get cutoff data
    pw_cutoff_new,rel_energy_pw,gau_cutoff_new,rel_energy_gau,Conv_pw,Conv_gau,max_scf=cutoff_data
    #Plot a figure of the cutoffs influence on the relative energy
    if float(max_scf)>1:
        fig,ax=plt.subplots(2,figsize=(8,8))
    else:
        fig,ax=plt.subplots(figsize=(8,6))
    ax3=ax[0].twiny()
    ax[0].plot(pw_cutoff_new,rel_energy_pw,"bo-",label="PW ARED")
    ax3.plot(gau_cutoff_new,rel_energy_gau,"ro-",label="Gau ARED")
    ax[0].plot([None],[None],"ro-",label="Gau ARED")
    ax[0].legend(loc=0)
    ax[0].set_xlabel("PW Cutoff / [Ry]",color="b")
    ax[0].set_ylabel("Absolute Relative Energy Difference")
    ax3.set_xlabel("Gaussian Cutoff / [Ry]",color="r")
    ax[0].yaxis.set_major_formatter(mpl.ticker.ScalarFormatter(useMathText=True, useOffset=False))
    ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #Plot a figure of the cutoffs influence on the convergence energy
    if float(max_scf)>1:
        ax4=ax[1].twiny()
        ax[1].semilogy(pw_cutoff_new,Conv_pw,"bx-",label="PW Conv.")
        ax4.semilogy(gau_cutoff_new,Conv_gau,"rx-",label="Gau Conv.")
        ax[1].plot([None],[None],"rx-",label="Gau Conv.")
        ax[1].set_xlabel("PW Cutoff / [Ry]",color="b")
        ax4.set_xlabel("Gaussian Cutoff / [Ry]",color="r")
        ax[1].set_ylabel("Absolute convergence after "+str(int(max_scf))+" iterations")
        ax[1].legend(loc=0)
    plt.tight_layout()
    plt.show()
    plt.close()
