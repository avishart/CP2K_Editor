# Pyykko and Atsumi radii
Elements_type=["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar",
                "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
                "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"]
radii=[0.32,0.46,1.33,1.02,0.85,0.75,0.71,0.63,0.64,0.67,1.55,1.39,1.26,1.16,1.11,1.03,0.99,0.96,
        1.96,1.71,1.48,1.36,1.34,1.22,1.19,1.16,1.11,1.10,1.12,1.18,1.24,1.21,1.21,1.16,1.14,1.17,
        2.10,1.85,1.63,1.54,1.47,1.38,1.28,1.25,1.25,1.20,1.28,1.36,1.42,1.40,1.40,1.36,1.33,1.31]



#Global section
def Global_section(tab,filename,GLOBAL):
    space=""
    content_global="&GLOBAL\n"
    space+="  "
    content_global+=space+"RUN_TYPE"+tab+GLOBAL["RUN_TYPE"]+"\n"
    content_global+=space+"PROJECT_NAME"+tab+str(filename)+"\n"
    content_global+=space+"PRINT_LEVEL"+tab+GLOBAL["PRINT_LEVEL"]+"\n"
    space=space[:-2]
    content_global+=space+"&END GLOBAL\n"
    return content_global

#Print at each step for properties
def each(space,tab,GLOBAL,FORCE_EVAL):
    content_each=""
    if GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
        content_each+=space+"&EACH"+"\n"
        space+="  "
        content_each+=space+"MD"+tab+FORCE_EVAL["EACH"]+"\n"
        space=space[:-2]
        content_each+=space+"&END EACH\n"
    elif GLOBAL["RUN_TYPE"]=="GEO_OPT" or GLOBAL["RUN_TYPE"]=="BAND":
        content_each+=space+"&EACH"+"\n"
        space+="  "
        content_each+=space+GLOBAL["RUN_TYPE"]+tab+FORCE_EVAL["EACH"]+"\n"
        space=space[:-2]
        content_each+=space+"&END EACH\n"
    return content_each

#Restart each function in print for restart files
def restart_each(space,tab,GLOBAL,EXT_RESTART):
    content_restart_each=""
    content_restart_each+=space+"&RESTART"+tab+"ON\n"
    space+="  "
    if GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
        content_restart_each+=space+"&EACH"+"\n"
        space+="  "
        content_restart_each+=space+"MD"+tab+EXT_RESTART["RESTART_EACH"]+"\n"
        space=space[:-2]
        content_restart_each+=space+"&END EACH\n"
    elif GLOBAL["RUN_TYPE"]=="GEO_OPT" or GLOBAL["RUN_TYPE"]=="BAND":
        content_restart_each+=space+"&EACH"+"\n"
        space+="  "
        content_restart_each+=space+GLOBAL["RUN_TYPE"]+tab+EXT_RESTART["RESTART_EACH"]+"\n"
        space=space[:-2]
        content_restart_each+=space+"&END EACH\n"
    space=space[:-2]
    content_restart_each+=space+"&END RESTART"+"\n"
    return content_restart_each

#Force Eval section 
def Force_Eval_section(tab,target_value,strength_value,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    space=""
    content_FE="&FORCE_EVAL\n"
    space+="  "
    content_FE+=space+"METHOD"+tab+FORCE_EVAL["METHOD"]+"\n"
    #DFT part
    if FORCE_EVAL["METHOD_SECTION"]=="DFT":
        content_FE+=Force_Eval_DFT_subsection(space,tab,target_value,strength_value,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    #SUBSYS part
    content_FE+=Force_Eval_SUBSYS_subsection(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    space=space[:-2]
    content_FE+=space+"&END FORCE_EVAL\n"
    return content_FE

#DFT Subsection in Force Eval section 
def Force_Eval_DFT_subsection(space,tab,target_value,strength_value,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    content_DFT=space+"&DFT\n"
    space+="  "
    #Basis set and pseudopotential file name
    content_DFT+=space+"BASIS_SET_FILE_NAME"+tab+FORCE_EVAL["BASIS_SET_FILE_NAME"]+"\n"
    content_DFT+=space+"POTENTIAL_FILE_NAME"+tab+FORCE_EVAL["POTENTIAL_FILE_NAME"]+"\n"
    #Restart wavefunction
    if EXT_RESTART["RESTART"]=="TRUE" and EXT_RESTART["RESTART_FILE_NAME"].split(".")[-1].lower()=="wfn":
        content_DFT+=space+"WFN_RESTART_FILE_NAME"+tab+EXT_RESTART["RESTART_FILE_NAME"]+"\n"
    #XC
    content_DFT+=space+"&XC\n"
    space+="  "
    #Custom XC functional
    if FORCE_EVAL["XC_FUNCTIONAL"]=="CUSTOM":
        content_DFT+=space+"&XC_FUNCTIONAL"+"\n"
        space+="  "
        content_DFT+=space+"&LIBXC"+"\n"
        space+="  "
        content_DFT+=space+"FUNCTIONAL"+tab+FORCE_EVAL["LIBXC"]+"\n"
        space=space[:-2]
        content_DFT+=space+"&END LIBXC\n"
        space=space[:-2]
        content_DFT+=space+"&END XC_FUNCTIONAL\n"     
    else:
        content_DFT+=space+"&XC_FUNCTIONAL"+tab+FORCE_EVAL["XC_FUNCTIONAL"]+"\n"
        content_DFT+=space+"&END XC_FUNCTIONAL\n"
    #HFX for periodic condition
    if FORCE_EVAL["XC_FUNCTIONAL"] in ["B3LYP","PBE0"] and SUBSYS["PERIODIC"]!="NONE":
        content_DFT+=space+"&HF"+"\n"
        space+="  "
        content_DFT+=space+"&INTERACTION_POTENTIAL"+"\n"
        space+="  "
        content_DFT+=space+"POTENTIAL_TYPE"+tab+"TRUNCATED"+"\n"
        content_DFT+=space+"CUTOFF_RADIUS"+tab+"{0:.2f}".format(min(map(float,list(filter(None,SUBSYS["ABC"].split(" ")))))/2.10)+"\n"
        content_DFT+=space+"T_C_G_DATA"+tab+PROGRAM["Path"]+"data/"+"t_c_g.dat"+"\n"
        space=space[:-2]
        content_DFT+=space+"&END INTERACTION_POTENTIAL"+"\n"
        space=space[:-2]
        content_DFT+=space+"&END HF"+"\n"
    #Dispersion correction only with dftd3
    if FORCE_EVAL["VDW_POTENTIAL"]=="DFTD2" or FORCE_EVAL["VDW_POTENTIAL"]=="DFTD3" or FORCE_EVAL["VDW_POTENTIAL"]=="DFTD3(BJ)":
        content_DFT+=space+"&VDW_POTENTIAL"+"\n"
        space+="  "
        content_DFT+=space+"DISPERSION_FUNCTIONAL"+tab+"PAIR_POTENTIAL"+"\n" 
        content_DFT+=space+"&PAIR_POTENTIAL"+"\n"
        space+="  "
        content_DFT+=space+"REFERENCE_FUNCTIONAL"+tab+FORCE_EVAL["XC_FUNCTIONAL"]+"\n" 
        content_DFT+=space+"TYPE"+tab+FORCE_EVAL["VDW_POTENTIAL"]+"\n" 
        if FORCE_EVAL["VDW_POTENTIAL"]=="DFTD3" or FORCE_EVAL["VDW_POTENTIAL"]=="DFTD3(BJ)":
            content_DFT+=space+"PARAMETER_FILE_NAME"+tab+PROGRAM["Path"]+"data/"+"dftd3.dat"+"\n" 
            content_DFT+=space+"LONG_RANGE_CORRECTION"+tab+".TRUE."+"\n"
        content_DFT+=space+"VERBOSE_OUTPUT"+tab+"TRUE"+"\n" 
        space=space[:-2]
        content_DFT+=space+"&END PAIR_POTENTIAL"+"\n"
        space=space[:-2]
        content_DFT+=space+"&END VDW_POTENTIAL"+"\n"
    space=space[:-2]
    content_DFT+=space+"&END XC\n"
    #CHARGE
    content_DFT+=space+"CHARGE"+tab+SUBSYS["CHARGE"]+"\n"
    content_DFT+=space+"UKS"+tab+"TRUE"+"\n"
    #QS
    content_DFT+=space+"&QS"+"\n"
    space+="  "
    content_DFT+=space+"METHOD"+tab+FORCE_EVAL["QS"]+"\n"
    #For functional with HFX
    if FORCE_EVAL["XC_FUNCTIONAL"] in ["B3LYP","PBE0","CUSTOM"]:
        content_DFT+=space+"EPS_PGF_ORB"+tab+"1.0E-20"+"\n"
    #CDFT part in DFT
    if GLOBAL["PROPERTIES"]=="CDFT":
        content_DFT+=Force_Eval_CDFT(space,tab,target_value,strength_value,filename,FORCE_EVAL,SUBSYS)
    space=space[:-2]
    content_DFT+=space+"&END QS\n"
    #SCF
    content_DFT+=space+"&SCF"+"\n"
    space+="  "
    #SCF_GUESS in SCF from restart file or not
    if EXT_RESTART["RESTART"]=="TRUE":
        content_DFT+=space+"SCF_GUESS"+tab+"RESTART"+"\n"
    else:
        content_DFT+=space+"SCF_GUESS"+tab+"ATOMIC"+"\n"
    content_DFT+=space+"MAX_SCF"+tab+FORCE_EVAL["MAX_SCF"]+"\n"
    content_DFT+=space+"EPS_SCF"+tab+FORCE_EVAL["EPS_SCF"]+"\n"
    #OT of KS matrix method with CG minimizer, NOT diagonalization
    if FORCE_EVAL["DIAGONALIZATION"]=="OT":
        content_DFT+=space+"&OT"+"\n"
        space+="  "
        content_DFT+=space+"MINIMIZER"+tab+"CG"+"\n"
        content_DFT+=space+"PRECONDITIONER"+tab+FORCE_EVAL["PRECONDITIONER"]+"\n"
        space=space[:-2]
        content_DFT+=space+"&END OT"+"\n"
    #DIAGONALIZATION
    else:
        content_DFT+=space+"&DIAGONALIZATION"+"\n"
        space+="  "
        content_DFT+=space+"ALGORITHM"+tab+FORCE_EVAL["DIAGONALIZATION"]+"\n"
        space=space[:-2]
        content_DFT+=space+"&END DIAGONALIZATION\n"
    #Outer SCF (needed for CDFT)
    content_DFT+=space+"&OUTER_SCF"+tab+"ON"+"\n"
    space+="  "
    content_DFT+=space+"EPS_SCF"+tab+FORCE_EVAL["EPS_SCF"]+"\n"
    content_DFT+=space+"MAX_SCF"+tab+FORCE_EVAL["MAX_SCF"]+"\n"
    space=space[:-2]
    content_DFT+=space+"&END OUTER_SCF\n"
    #Print WFN/wavefunction/orbital restart files
    if EXT_RESTART["SAVE_RESTART"]=="TRUE":
        content_DFT+=space+"&PRINT"+"\n"
        space+="  "
        content_DFT+=restart_each(space,tab,GLOBAL,EXT_RESTART)
        space=space[:-2]
        content_DFT+=space+"&END PRINT\n"
    space=space[:-2]
    content_DFT+=space+"&END SCF\n"
    #MGRIDS
    content_DFT+=space+"&MGRID"+"\n"
    space+="  "
    content_DFT+=space+"NGRIDS"+tab+FORCE_EVAL["NGRIDS"]+"\n"
    content_DFT+=space+"CUTOFF"+tab+FORCE_EVAL["CUTOFF"]+"\n"
    content_DFT+=space+"REL_CUTOFF"+tab+FORCE_EVAL["REL_CUTOFF"]+"\n"
    space=space[:-2]
    content_DFT+=space+"&END MGRID\n"
    #POISSION if not periodic in xyz
    if SUBSYS["PERIODIC"]!="XYZ":
        content_DFT+=space+"&POISSON"+"\n"
        space+="  "
        content_DFT+=space+"PERIODIC"+tab+SUBSYS["PERIODIC"]+"\n"
        content_DFT+=space+"POISSON_SOLVER"+tab+FORCE_EVAL["POISSON_SOLVER"]+"\n"
        space=space[:-2]
        content_DFT+=space+"&END POISSON\n"
    #Real_Time_Propagation
    if GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
        content_DFT+=space+"&REAL_TIME_PROPAGATION"+"\n"
        space+="  "
        content_DFT+=space+"INITIAL_WFN"+tab+"SCF_WFN"+"\n"
        content_DFT+=space+"EXP_ACCURACY"+tab+"1.000E-9"+"\n"
        content_DFT+=space+"EPS_ITER"+tab+FORCE_EVAL["EPS_SCF"]+"\n"
        content_DFT+=space+"MAX_ITER"+tab+FORCE_EVAL["MAX_SCF"]+"\n"
        content_DFT+=space+"DELTA_PULSE_DIRECTION"+tab+"0 0 1"+"\n"
        space=space[:-2]
        content_DFT+=space+"&END REAL_TIME_PROPAGATION\n"
    #MULLIKEN and lowdin
    content_DFT+=space+"&PRINT"+"\n"
    space+="  "
    content_DFT+=space+"&MULLIKEN"+tab+"LOW"+"\n"
    space+="  "
    content_DFT+=each(space,tab,GLOBAL,FORCE_EVAL)
    space=space[:-2]
    content_DFT+=space+"&END MULLIKEN"+"\n"
    content_DFT+=space+"&LOWDIN"+tab+"ON"+"\n"
    space+="  "
    content_DFT+=each(space,tab,GLOBAL,FORCE_EVAL)
    space=space[:-2]
    content_DFT+=space+"&END LOWDIN"+"\n"
    space=space[:-2]
    content_DFT+=space+"&END PRINT\n"
    space=space[:-2]
    content_DFT+=space+"&END DFT\n"
    return content_DFT

#CDFT subsection in the dft part
def Force_Eval_CDFT(space,tab,target_value,strength_value,filename,FORCE_EVAL,SUBSYS):
    content_CDFT=space+"&CDFT\n"
    space+="  "
    content_CDFT+=space+"TYPE_OF_CONSTRAINT"+tab+"BECKE"+"\n"
    content_CDFT+=space+"&OUTER_SCF"+tab+"ON"+"\n"
    space+="  "
    content_CDFT+=space+"TYPE"+tab+"BECKE_CONSTRAINT"+"\n"
    content_CDFT+=space+"EXTRAPOLATION_ORDER"+tab+"2"+"\n"
    content_CDFT+=space+"MAX_SCF"+tab+FORCE_EVAL["MAX_SCF"]+"\n"
    content_CDFT+=space+"EPS_SCF"+tab+"1.00E-3"+"\n"
    content_CDFT+=space+"OPTIMIZER"+tab+"NEWTON_LS"+"\n"
    content_CDFT+=space+"STEP_SIZE"+tab+"-1.0"+"\n"
    content_CDFT+=space+"MAX_LS"+tab+"5"+"\n"
    content_CDFT+=space+"CONTINUE_LS"+"\n"
    content_CDFT+=space+"FACTOR_LS"+tab+"0.5"+"\n"
    content_CDFT+=space+"JACOBIAN_STEP"+tab+"1.00E-2"+"\n"
    content_CDFT+=space+"JACOBIAN_FREQ"+tab+"1 1"+"\n"
    content_CDFT+=space+"JACOBIAN_TYPE"+tab+"FD1"+"\n"
    content_CDFT+=space+"JACOBIAN_RESTART"+tab+"FALSE"+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END OUTER_SCF"+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END CDFT\n"
    content_CDFT+=space+"&BECKE_CONSTRAINT"+"\n"
    space+="  "
    content_CDFT+=space+"ADJUST_SIZE"+tab+"TRUE"+"\n"
    Radii_list=[]
    for ele in SUBSYS["ELEMENTS"]:
        indi=Elements_type.index("".join(s for s in ele if s.isalpha()))
        Radii_list.append(radii[indi])
    content_CDFT_radii=space+"ATOMIC_RADII"+tab
    content_CDFT_cutoff=space+"ELEMENT_CUTOFF"+tab
    for num in range(len(Radii_list)):
        if num==len(Radii_list)-1:
            content_CDFT_radii+=str(Radii_list[num])+"\n"
            content_CDFT_cutoff+="7.0"+"\n"
        else:
            content_CDFT_radii+=str(Radii_list[num])+" "
            content_CDFT_cutoff+="7.0"+" "
    if len(Radii_list)==0:
        content_CDFT_radii+="\n"
        content_CDFT_cutoff+="\n"
    content_CDFT+=content_CDFT_radii
    content_CDFT+=space+"ATOMIC_CHARGES"+tab+"TRUE"+"\n"
    content_CDFT+=space+"STRENGTH"+tab+str(strength_value)+"\n"
    content_CDFT+=space+"TARGET"+tab+str(target_value)+"\n"
    content_CDFT+=space+"CUTOFF_TYPE"+tab+"ELEMENT"+"\n"
    content_CDFT+=content_CDFT_cutoff
    content_CDFT+=space+"CAVITY_CONFINE"+tab+"TRUE"+"\n"
    content_CDFT+=space+"CAVITY_SHAPE"+tab+"VDW"+"\n"
    content_CDFT+=space+"EPS_CAVITY"+tab+"1.00E-7"+"\n"
    content_CDFT+=space+"IN_MEMORY"+tab+"TRUE"+"\n"
    content_CDFT+=space+"SHOULD_SKIP"+tab+"TRUE"+"\n"
    content_CDFT+=space+"&ATOM_GROUP"+"\n"
    space+="  "
    content_CDFT_Atom_frag1=str(SUBSYS["ATOMS_FRAG1"])
    content_CDFT_Atom_frag1=content_CDFT_Atom_frag1.replace("-","..")
    content_CDFT_Atom_frag1=content_CDFT_Atom_frag1.replace(","," ")
    content_CDFT_Atom_frag2=str(SUBSYS["ATOMS_FRAG2"])
    content_CDFT_Atom_frag2=content_CDFT_Atom_frag2.replace("-","..")
    content_CDFT_Atom_frag2=content_CDFT_Atom_frag2.replace(","," ")
    content_CDFT+=space+"ATOMS"+tab+content_CDFT_Atom_frag1+" "+content_CDFT_Atom_frag2+"\n"
    CDFT_Atom_frag1_list=list(filter(None,content_CDFT_Atom_frag1.split(" ")))
    CDFT_Atom_frag2_list=list(filter(None,content_CDFT_Atom_frag2.split(" ")))
    number_atom_frag1=[]
    for ele in CDFT_Atom_frag1_list:
        if ".." in ele:
            newele=list(ele.split(".."))
            if int(newele[0])<=int(newele[-1])+1:
                for num in range(int(newele[0]),int(newele[-1])+1):
                    number_atom_frag1.append(num)
            else:
                print("Error in fragment")
        else:
            number_atom_frag1.append(ele)
    number_atom_frag2=[]
    for ele in CDFT_Atom_frag2_list:
        if ".." in ele:
            newele=list(ele.split(".."))
            if int(newele[0])<=int(newele[-1])+1:
                for num in range(int(newele[0]),int(newele[-1])+1):
                    number_atom_frag2.append(num)
            else:
                print("Error in fragment")
        else:
            number_atom_frag2.append(ele)
    content_CDFT+=space+"COEFF"+tab+"1 "*len(number_atom_frag1)+"-1 "*len(number_atom_frag2)+"\n"
    content_CDFT+=space+"CONSTRAINT_TYPE"+tab+"CHARGE"+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END ATOM_GROUP"+"\n"
    content_CDFT+=space+"&PROGRAM_RUN_INFO"+tab+"ON"+"\n"
    space+="  "
    content_CDFT+=space+"&EACH"+"\n"
    space+="  "
    content_CDFT+=space+"QS_SCF"+tab+"1"+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END EACH"+"\n"
    content_CDFT+=space+"COMMON_ITERATION_LEVELS"+tab+"2"+"\n"
    content_CDFT+=space+"ADD_LAST"+tab+"NUMERIC"+"\n"
    content_CDFT+=space+"FILENAME"+tab+str(filename)+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END PROGRAM_RUN_INFO"+"\n"
    space=space[:-2]
    content_CDFT+=space+"&END BECKE_CONSTRAINT"+"\n"
    return content_CDFT

#Mixed CDFT part
def Force_Eval_CDFT_mixed(tab,target_value1,target_value2,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    #Multi Force_evals
    content_CDFT_mixed="&MULTIPLE_FORCE_EVALS\n"
    space="  "
    content_CDFT_mixed+=space+"FORCE_EVAL_ORDER"+tab+"2 3"+"\n"
    content_CDFT_mixed+=space+"MULTIPLE_SUBSYS"+tab+"F"+"\n"
    space=space[:-2]
    content_CDFT_mixed+=space+"&END MULTIPLE_FORCE_EVALS\n"
    #Force_eval for the mixed state
    content_CDFT_mixed+=space+"&FORCE_EVAL\n"
    space+="  "
    content_CDFT_mixed+=space+"METHOD"+tab+"MIXED"+"\n"
    content_CDFT_mixed+=space+"&MIXED\n"
    space+="  "
    content_CDFT_mixed+=space+"MIXING_TYPE"+tab+"MIXED_CDFT"+"\n"
    content_CDFT_mixed+=space+"NGROUPS"+tab+"1"+"\n"
    content_CDFT_mixed+=space+"&MIXED_CDFT\n"
    space+="  "
    content_CDFT_mixed+=space+"COUPLING"+tab+"1"+"\n"
    content_CDFT_mixed+=space+"FORCE_STATES"+tab+"1 2"+"\n"
    content_CDFT_mixed+=space+"LAMBDA"+tab+"1.0"+"\n"
    content_CDFT_mixed+=space+"LOWDIN"+tab+"TRUE"+"\n"
    content_CDFT_mixed+=space+"CI"+tab+"FALSE"+"\n"
    content_CDFT_mixed+=space+"&PRINT\n"
    space+="  "
    content_CDFT_mixed+=space+"&PROGRAM_RUN_INFO"+tab+"ON"+"\n"
    content_CDFT_mixed+=space+"&END PROGRAM_RUN_INFO"+"\n"
    space=space[:-2]
    content_CDFT_mixed+=space+"&END PRINT\n"
    space=space[:-2]
    content_CDFT_mixed+=space+"&END MIXED_CDFT\n"
    space=space[:-2]
    content_CDFT_mixed+=space+"&END MIXED\n"
    #SUBSYS part
    content_CDFT_mixed+=Force_Eval_SUBSYS_subsection(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    space=space[:-2]
    content_CDFT_mixed+=space+"&END FORCE_EVAL\n"

    #For first state
    content_CDFT_mixed+=Force_Eval_section(tab,target_value1,0,filename+"-state1",PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    #For second state
    content_CDFT_mixed+=Force_Eval_section(tab,target_value2,0,filename+"-state2",PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    return content_CDFT_mixed


#SUBSYS Subsection in Force Eval section 
def Force_Eval_SUBSYS_subsection(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    content_SUBSYS=space+"&SUBSYS\n"
    space+="  "
    if EXT_RESTART["RESTART"]=="TRUE" and EXT_RESTART["RESTART_FILE_NAME"].split(".")[-1].lower()=="restart":
        pass
    else:
        #Coordination part (TOPOLOGY)
        content_SUBSYS+=space+"&TOPOLOGY"+"\n"
        space+="  "
        if SUBSYS["COORD"]!="":
            if str(list(SUBSYS["COORD"].split("."))[-1]).lower()=="coord":
                content_SUBSYS+=space+"COORD_FILE_FORMAT"+tab+"CP2K"+"\n"
            else:
                content_SUBSYS+=space+"COORD_FILE_FORMAT"+tab+str(list(SUBSYS["COORD"].split("."))[-1])+"\n"
            content_SUBSYS+=space+"COORD_FILE_NAME"+tab+SUBSYS["COORD"]+"\n"
        if SUBSYS["CENTER_COORDINATES"]=="TRUE":
            content_SUBSYS+=space+"&CENTER_COORDINATES"+"\n"
            content_SUBSYS+=space+"&END CENTER_COORDINATES"+"\n"
        space=space[:-2]
        content_SUBSYS+=space+"&END TOPOLOGY"+"\n"
    #CELL
    content_SUBSYS+=space+"&CELL"+"\n"
    space+="  "
    content_SUBSYS+=space+"ABC"+tab+SUBSYS["ABC"]+"\n"
    if SUBSYS["PERIODIC"]!="XYZ":
        content_SUBSYS+=space+"PERIODIC"+tab+SUBSYS["PERIODIC"]+"\n"
    space=space[:-2]
    content_SUBSYS+=space+"&END CELL"+"\n"
    #KIND
    if len(SUBSYS["ELEMENTS"])>0:
        for num in range(len(SUBSYS["ELEMENTS"])):
            content_SUBSYS+=space+"&KIND"+" "+SUBSYS["ELEMENTS"][num]+"\n"
            space+="  "
            content_SUBSYS+=space+"BASIS_SET"+tab+FORCE_EVAL["BASIS_SET"]+"\n"
            content_SUBSYS+=space+"POTENTIAL"+tab+FORCE_EVAL["POTENTIAL"]+"\n"
            space=space[:-2]
            content_SUBSYS+=space+"&END KIND"+"\n"
    elif len(SUBSYS["ELEMENTS"])==0:
        content_SUBSYS+=space+"&KIND"+" "+"\n"
        space+="  "
        content_SUBSYS+=space+"BASIS_SET"+tab+FORCE_EVAL["BASIS_SET"]+"\n"
        content_SUBSYS+=space+"POTENTIAL"+tab+FORCE_EVAL["POTENTIAL"]+"\n"
        space=space[:-2]
        content_SUBSYS+=space+"&END KIND"+"\n"
    space=space[:-2]
    content_SUBSYS+=space+"&END SUBSYS\n"
    return content_SUBSYS

#MOTION section
def Motion_section(tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    space=""
    content_MOTION=space+"&MOTION\n"
    space+="  "
    if len(SUBSYS["FIXED"].replace(" ",""))>=1:
        #Constraint atoms
        content_MOTION+=space+"&CONSTRAINT\n"
        space+="  "
        content_MOTION+=space+"&FIXED_ATOMS\n"
        space+="  "
        constraint_atoms_MOTION=str(SUBSYS["FIXED"])
        constraint_atoms_MOTION=constraint_atoms_MOTION.replace("-","..")
        constraint_atoms_MOTION=constraint_atoms_MOTION.replace(","," ")
        content_MOTION+=space+"LIST"+tab+str(constraint_atoms_MOTION)+"\n"
        space=space[:-2]
        content_MOTION+=space+"&END FIXED_ATOMS\n"
        space=space[:-2]
        content_MOTION+=space+"&END CONSTRAINT\n"
    #MOTION section for GEO_OPT
    if GLOBAL["RUN_TYPE"]=="GEO_OPT":
        content_MOTION+=Motion_GEO_OPT(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    #MOTION section for MD and RT_PROPAGATION
    elif GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
        content_MOTION+=Motion_MD_RT(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    elif GLOBAL["RUN_TYPE"]=="BAND":
        content_MOTION+=Motion_BAND(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    space=space[:-2]
    content_MOTION+=space+"&END MOTION\n"
    return content_MOTION

#Motion section for GEO_OPT
def Motion_GEO_OPT(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    content_GEO=""
    content_GEO+=space+"&GEO_OPT\n"
    space+="  "
    #Model for the GEO_OPT
    content_GEO+=space+"TYPE"+tab+MOTION["TYPE"]+"\n"
    content_GEO+=space+"OPTIMIZER"+tab+MOTION["OPTIMIZER"]+"\n"
    content_GEO+=space+"MAX_DR"+tab+MOTION["MAX_DR"]+"\n"
    content_GEO+=space+"MAX_ITER"+tab+MOTION["MAX_ITER"]+"\n"
    if MOTION["TYPE"]=="TRANSITION_STATE":
        content_GEO+=space+"&CG\n"
        space+="  "
        content_GEO+=space+"&LINE_SEARCH\n"
        space+="  "
        content_GEO+=space+"TYPE"+tab+"2PNT"+"\n"
        space=space[:-2]
        content_GEO+=space+"&END LINE_SEARCH\n"
        space=space[:-2]
        content_GEO+=space+"&END CG\n"
        content_GEO+=space+"&TRANSITION_STATE\n"
        space+="  "
        content_GEO+=space+"&DIMER\n"
        space+="  "
        content_GEO+=space+"&ROT_OPT\n"
        space+="  "
        content_GEO+=space+"OPTIMIZER"+tab+"CG"+"\n"
        content_GEO+=space+"&CG\n"
        space+="  "
        content_GEO+=space+"&LINE_SEARCH\n"
        space+="  "
        content_GEO+=space+"TYPE"+tab+"2PNT"+"\n"
        space=space[:-2]
        content_GEO+=space+"&END LINE_SEARCH\n"
        space=space[:-2]
        content_GEO+=space+"&END CG\n"
        space=space[:-2]
        content_GEO+=space+"&END ROT_OPT\n"
        space=space[:-2]
        content_GEO+=space+"&END DIMER\n"
        space=space[:-2]
        content_GEO+=space+"&END TRANSITION_STATE\n"
    space=space[:-2]
    content_GEO+=space+"&END GEO_OPT\n"
    #Print restart files
    if EXT_RESTART["SAVE_RESTART"]=="TRUE":
        content_GEO+=space+"&PRINT\n"
        space+="  "
        content_GEO+=restart_each(space,tab,GLOBAL,EXT_RESTART)
        space=space[:-2]
        content_GEO+=space+"&END PRINT\n"
    return content_GEO

#MOTION section for MD and RT_PROPAGATION
def Motion_MD_RT(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    content_MD_RT=""
    content_MD_RT+=space+"&MD\n"
    space+="  "
    #Model for the MD
    content_MD_RT+=space+"ENSEMBLE"+tab+MOTION["ENSEMBLE"]+"\n"
    content_MD_RT+=space+"STEPS"+tab+MOTION["STEPS"]+"\n"
    content_MD_RT+=space+"TIMESTEP"+tab+MOTION["TIMESTEP"]+"\n"
    content_MD_RT+=space+"TEMPERATURE"+tab+MOTION["TEMPERATURE"]+"\n"
    #Thermostat
    if MOTION["ENSEMBLE"]=="NPE_F" or MOTION["ENSEMBLE"]=="NPE_I":
        content_MD_RT+=""
    else:
        content_MD_RT+=space+"&THERMOSTAT\n"
        space+="  "
        content_MD_RT+=space+"TYPE"+tab+MOTION["THERMOSTAT"]+"\n"
        if MOTION["THERMOSTAT"]!="GLE":
            content_MD_RT+=space+"&"+MOTION["THERMOSTAT"]+"\n"
            space+="  "
            content_MD_RT+=space+"TIMECON"+tab+MOTION["TIMECON"]+"\n"
            space=space[:-2]
            content_MD_RT+=space+"&END "+MOTION["THERMOSTAT"]+"\n"
        space=space[:-2]
        content_MD_RT+=space+"&END THERMOSTAT\n"
    space=space[:-2]
    content_MD_RT+=space+"&END MD\n"
    #Print velocity and positions
    if GLOBAL["RUN_TYPE"]=="MD":
        content_MD_RT+=space+"&PRINT\n"
        space+="  "
        content_MD_RT+=space+"&VELOCITIES\n"
        content_MD_RT+=space+"&END VELOCITIES\n"
        #Print restart files
        if EXT_RESTART["SAVE_RESTART"]=="TRUE":
            content_MD_RT+=restart_each(space,tab,GLOBAL,EXT_RESTART)
        space=space[:-2]
        content_MD_RT+=space+"&END PRINT\n"
    #Print restart files
    elif GLOBAL["RUN_TYPE"]=="RT_PROPAGATION" and EXT_RESTART["SAVE_RESTART"]=="TRUE":
        content_MD_RT+=space+"&PRINT\n"
        space+="  "
        content_MD_RT+=restart_each(space,tab,GLOBAL,EXT_RESTART)
        space=space[:-2]
        content_MD_RT+=space+"&END PRINT\n"
    return content_MD_RT

#MOTION section for BAND (NEB)
def Motion_BAND(space,tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    content_BAND=""
    content_BAND+=space+"&BAND\n"
    space+="  "
    content_BAND+=space+"BAND_TYPE"+tab+MOTION["BAND_TYPE"]+"\n"
    content_BAND+=space+"NUMBER_OF_REPLICA"+tab+MOTION["NUMBER_OF_REPLICA"]+"\n"
    content_BAND+=space+"&OPTIMIZE_BAND\n"
    space+="  "
    content_BAND+=space+"OPT_TYPE"+tab+MOTION["OPTIMIZE_BAND"]+"\n"
    content_BAND+=space+"&"+MOTION["OPTIMIZE_BAND"]+"\n"
    space+="  "
    content_BAND+=space+"MAX_STEPS"+tab+MOTION["MAX_STEPS"]+"\n"
    space=space[:-2]
    content_BAND+=space+"&END "+MOTION["OPTIMIZE_BAND"]+"\n"
    space=space[:-2]
    content_BAND+=space+"&END OPTIMIZE_BAND\n"
    #Replica for intial strucutre
    content_BAND+=space+"&REPLICA\n"
    space+="  "
    if MOTION["REPLICA1"]!="":
        if str(list(MOTION["REPLICA1"].split("."))[-1]).lower()=="coord":
            content_BAND+=space+"&COORD"+"\n"
            space+="  "
            content_BAND+=space+"@INCLUDE"+tab+MOTION["REPLICA1"]+"\n"
            space=space[:-2]
            content_BAND+=space+"&END COORD"+"\n"
        else:
            content_BAND+=space+"COORD_FILE_NAME"+tab+MOTION["REPLICA1"]+"\n"
    space=space[:-2]
    content_BAND+=space+"&END REPLICA\n"
    #Replica for intermediate structure, but is not a requirement 
    if MOTION["REPLICA2"]!="":
        content_BAND+=space+"&REPLICA\n"
        space+="  "
        if str(list(MOTION["REPLICA2"].split("."))[-1]).lower()=="coord":
            content_BAND+=space+"&COORD"+"\n"
            space+="  "
            content_BAND+=space+"@INCLUDE"+tab+MOTION["REPLICA2"]+"\n"
            space=space[:-2]
            content_BAND+=space+"&END COORD"+"\n"
        else:
            content_BAND+=space+"COORD_FILE_NAME"+tab+MOTION["REPLICA2"]+"\n"
        space=space[:-2]
        content_BAND+=space+"&END REPLICA\n"
    #Replica for final structure 
    content_BAND+=space+"&REPLICA\n"
    space+="  "
    if MOTION["REPLICA3"]!="":
        if str(list(MOTION["REPLICA3"].split("."))[-1]).lower()=="coord":
            content_BAND+=space+"&COORD"+"\n"
            space+="  "
            content_BAND+=space+"@INCLUDE"+tab+MOTION["REPLICA3"]+"\n"
            space=space[:-2]
            content_BAND+=space+"&END COORD"+"\n"
        else:
            content_BAND+=space+"COORD_FILE_NAME"+tab+MOTION["REPLICA3"]+"\n"
    space=space[:-2]
    content_BAND+=space+"&END REPLICA\n"
    space=space[:-2]
    content_BAND+=space+"&END BAND\n"
    #Print restart files
    if EXT_RESTART["SAVE_RESTART"]=="TRUE":
        content_BAND+=space+"&PRINT\n"
        space+="  "
        content_BAND+=restart_each(space,tab,GLOBAL,EXT_RESTART)
        space=space[:-2]
        content_BAND+=space+"&END PRINT\n"
    return content_BAND


#Save to the content
def Save_to_content(target_value,strength_value,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    content=""
    tab="  "
    #GLOBAL SECTION
    content+=Global_section(tab,filename,GLOBAL)
    #FORCE_EVAL SECTION
    content+=Force_Eval_section(tab,target_value,strength_value,filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    #MOTION SECTION
    if GLOBAL["RUN_TYPE"]!="ENERGY":
        content+=Motion_section(tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    content=content[:-1]
    return content


#Save the four input files and bash script
def Save_cdft_files(PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION):
    #Filename
    filename=GLOBAL["PROJECT_NAME"]
    #Mixed state cdft
    content_mixed=""
    tab="  "
    #GLOBAL SECTION
    content_mixed+=Global_section(tab,filename,GLOBAL)
    #FORCE_EVAL SECTION
    content_mixed+=Force_Eval_CDFT_mixed(tab,SUBSYS["TARGET1"],SUBSYS["TARGET2"],filename,PROGRAM,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    #MOTION SECTION
    if GLOBAL["RUN_TYPE"]!="ENERGY":
        content_mixed+=Motion_section(tab,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION)
    #EXT_RESTSART
    if EXT_RESTART["RESTART"]=="TRUE" and EXT_RESTART["RESTART_FILE_NAME"].split(".")[-1].lower()=="restart":
        content+="&EXT_RESTART"+"\n"
        space="  "
        content+=space+"RESTART_FILE_NAME"+tab+EXT_RESTART["RESTART_FILE_NAME"]+"\n"
        if GLOBAL["RUN_TYPE"]!="ENERGY":
            content+=space+"RESTART_POS"+"\n"
            if GLOBAL["RUN_TYPE"]=="MD" or GLOBAL["RUN_TYPE"]=="RT_PROPAGATION":
                content+=space+"RESTART_VEL"+"\n"
        space=space[:-2]
        content+=space+"&END EXT_RESTART\n"
    content_mixed=content_mixed[:-1]
    return content_mixed

