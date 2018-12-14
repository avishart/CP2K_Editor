
def load_sections(inputfile):
    with open(inputfile) as thefile:
        content=thefile.readlines()
    content_Global=[]
    content_FE=[]
    content_DFT=[]
    content_HF=[]
    content_Subsys=[]
    content_Motion=[]
    content_VDW=[]
    content_LIBXC=[]
    content_QS=[]
    content_diag=[]
    content_vib=[]
    content_restart=[]
    content_CDFT=[]
    Global_section=False
    FORCE_EVAL_section=False
    FORCE_EVAL_DFT_section=False
    Force_Eval_DFT_HF=False
    VDW_section=False
    SUBSYS_section=False
    MOTION_section=False
    LIBXC_section=False
    QS_section=False
    FE_diag=False
    VIB=False
    Restart=False
    CDFT=False
    for line in content:
        if "&GLOBAL" in line:
            Global_section=True
        elif "&END GLOBAL" in line:
            Global_section=False
        if Global_section==True:
            content_Global.append(line)
        if "&FORCE_EVAL" in line:
            FORCE_EVAL_section=True
        elif "&END FORCE_EVAL" in line:
            FORCE_EVAL_section=False
        if FORCE_EVAL_section==True and FORCE_EVAL_DFT_section==False and SUBSYS_section==False:
            content_FE.append(line)
        if "&DFT" in line:
            FORCE_EVAL_DFT_section=True
        elif "&END DFT" in line:
            FORCE_EVAL_DFT_section=False
        if FORCE_EVAL_DFT_section==True and Force_Eval_DFT_HF==False and VDW_section==False and LIBXC_section==False and QS_section==False :
            content_DFT.append(line)
        if "&HF" in line:
            Force_Eval_DFT_HF=True
        elif "&END HF" in line:
            Force_Eval_DFT_HF=False
        if Force_Eval_DFT_HF==True:
            content_HF.append(line)
        if "&SUBSYS" in line:
            SUBSYS_section=True
        elif "&END SUBSYS" in line:
            SUBSYS_section=False
        if SUBSYS_section==True:
            content_Subsys.append(line)
        if "&MOTION" in line:
            MOTION_section=True
        elif "&END MOTION" in line:
            MOTION_section=False
        if MOTION_section==True:
            content_Motion.append(line)
        if "&VDW_POTENTIAL" in line:
            VDW_section=True
        elif "&END VDW_POTENTIAL" in line:
            VDW_section=False
        if VDW_section==True:
            content_VDW.append(line)
        if "&LIBXC" in line:
            LIBXC_section=True
        elif "&END LIBXC" in line:
            LIBXC_section=False
        if LIBXC_section==True:
            content_LIBXC.append(line)
        if "&QS" in line:
            QS_section=True
        elif "&END QS" in line:
            QS_section=False
        if QS_section==True:
            content_QS.append(line)
        if "&DIAGONALIZATION" in line:
            FE_diag=True
        elif "&END DIAGONALIZATION" in line:
            FE_diag=False
        if FE_diag==True:
            content_diag.append(line)
        if "&VIBRATIONAL_ANALYSIS" in line:
            VIB=True
        elif "&END VIBRATIONAL_ANALYSIS" in line:
            VIB=False
        if VIB==True:
            content_vib.append(line)
        if "&EXT_RESTART" in line:
            Restart=True
        elif "&END EXT_RESTART" in line:
            Restart=False
        if Restart==True:
            content_restart.append(line)
        if "&BECKE_CONSTRAINT" in line:
            CDFT=True
        elif "&END BECKE_CONSTRAINT" in line:
            CDFT=False
        if CDFT==True:
            content_CDFT.append(line)
    return content_Global,content_FE,content_DFT,content_HF,content_Subsys,content_Motion,content_VDW,content_LIBXC,content_QS,content_diag,content_vib,content_restart,content_CDFT
        
    

def GLOBAL_sec(content_Global,GLOBAL):
    for line in content_Global:
        for key in ["RUN_TYPE","PROJECT_NAME","PRINT_LEVEL"]:
            if key in line:
                GLOBAL[key]=list(filter(None,line.split(" ")))[1]
        if "PROJECT" in line:
            GLOBAL["PROJECT_NAME"]=list(filter(None,line.split(" ")))[1]
    GLOBAL["FILE_NAME"]=GLOBAL["PROJECT_NAME"]+".inp"
    return GLOBAL


def FE_sec(content_FE,content_DFT,content_diag,content_LIBXC,content_VDW,content_HF,content_QS,content_vib,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    for line in content_FE:
        if "METHOD " in line:
            FORCE_EVAL["METHOD"]=list(filter(None,line.split(" ")))[1]
            if "QUICKSTEP" in FORCE_EVAL["METHOD"] or "QS" in FORCE_EVAL["METHOD"]:
                FORCE_EVAL["METHOD"]="QUICKSTEP"
                FORCE_EVAL["METHOD_SECTION"]="DFT" 
    GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART=FE_dft_subsec(content_DFT,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    FORCE_EVAL=DIAG_subsec(content_diag,FORCE_EVAL)
    FORCE_EVAL=LIBXC_subsec(content_LIBXC,FORCE_EVAL)
    FORCE_EVAL=VDW_subsec(content_VDW,FORCE_EVAL)
    FORCE_EVAL=HF_subsec(content_HF,FORCE_EVAL)
    FORCE_EVAL=QS_subsec(content_QS,FORCE_EVAL)
    if len(content_vib)>0:
        GLOBAL["PROPERTIES"]="VIBRATIONAL_ANALYSIS"
    return GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART

def FE_dft_subsec(content_DFT,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART):
    for line in content_DFT:
        for key in ["MAX_SCF","EPS_SCF","NGRIDS","REL_CUTOFF","POISSON_SOLVER"]:
            if key in line:
                FORCE_EVAL[key]=list(filter(None,line.split(" ")))[1]
                if "[" in line:
                    FORCE_EVAL[key]=list(filter(None,line.split(" ")))[2]
        if "BASIS_SET_FILE_NAME" in line:
            FORCE_EVAL["BASIS_SET_FILE_NAME"]=list(filter(None,line.split(" ")))[1]
            FORCE_EVAL["BASIS_SET_FILE_NAME-path"]=str(FORCE_EVAL["BASIS_SET_FILE_NAME"].split("/")[-1])
        if "POTENTIAL_FILE_NAME" in line:
            FORCE_EVAL["POTENTIAL_FILE_NAME"]=list(filter(None,line.split(" ")))[1]
            FORCE_EVAL["POTENTIAL_FILE_NAME-path"]=str(FORCE_EVAL["POTENTIAL_FILE_NAME"].split("/")[-1])
        if "XC_FUNCTIONAL" in line:
            newlist=list(filter(None,line.split(" ")))
            if len(newlist)>1 and newlist[-1]!="\n" and "&END" not in line:
                FORCE_EVAL["XC_FUNCTIONAL"]=newlist[1]
        if "&OT" in line:
            FORCE_EVAL["DIAGONALIZATION"]="OT"
        if " CUTOFF " in line:
            FORCE_EVAL["CUTOFF"]=list(filter(None,line.split(" ")))[1]
            if "[" in FORCE_EVAL["CUTOFF"]:
                FORCE_EVAL["CUTOFF"]=list(filter(None,line.split(" ")))[2]
        if "CHARGE" in line:
            SUBSYS["CHARGE"]=list(filter(None,line.split(" ")))[1]
        if "&RESTART" in line:
            EXT_RESTART["SAVE_RESTART"]="TRUE"
        if "NHOMO" in line:
            GLOBAL["NSTATES"]=list(filter(None,line.split(" ")))[1]
            GLOBAL["PROPERTIES"]="MO"
        if "&MOMENTS" in line:
            GLOBAL["PROPERTIES"]="DIPOLE"
        if "&MULLIKKEN" in line:
            GLOBAL["PROPERTIES"]="MULLIKKEN"
        if "&TDDFPT" in line:
            GLOBAL["PROPERTIES"]="TDDFPT"
        if "NSTATES" in line:
            GLOBAL["NSTATES"]=list(filter(None,line.split(" ")))[1]
        if "PERIODIC" in line:
            SUBSYS["PERIODIC"]=list(filter(None,line.split(" ")))[1]
    return GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART

def FE_CDFT_subsec(content_CDFT,GLOBAL,SUBSYS):
    if len(content_CDFT)>1:
        GLOBAL["PROPERTIES"]="CDFT"
    atoms=[]
    target=[]
    for line in content_CDFT:
        if " TARGET " in line:
            target.append(list(filter(None,line.split(" ")))[1])
        if " ATOMS " in line:
            atom_line=list(filter(None,line.split(" ")))[1:]
            atom_txt=""
            for atom in atom_line:
                atom_txt+=str(atom)+" "
            atom_txt=atom_txt.replace("\n","")
            atoms.append(atom_txt)
    if len(target)==2:
        SUBSYS["TARGET1"]=str(target[0])
        SUBSYS["TARGET2"]=str(target[1])
    if len(atoms)>=2:
        SUBSYS["ATOMS_FRAG1"]=str(atoms[1])
        SUBSYS["ATOMS_FRAG2"]=str(atoms[2])
    return GLOBAL,SUBSYS


def DIAG_subsec(content_diag,FORCE_EVAL):
    for line in content_diag:
        if "ALGORITHM" in line:
            FORCE_EVAL["DIAGONALIZATION"]=list(filter(None,line.split(" ")))[1]
        if "PRECONDITIONER" in line:
            FORCE_EVAL["PRECONDITIONER"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL

def LIBXC_subsec(content_LIBXC,FORCE_EVAL):
    for line in content_LIBXC:
        if "&LIBXC" in line:
            FORCE_EVAL["XC_FUNCTIONAL"]="CUSTOM"
        if " FUNCTIONAL" in line:
            FORCE_EVAL["LIBXC"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL

def VDW_subsec(content_VDW,FORCE_EVAL):
    for line in content_VDW:
        if " TYPE" in line:
            FORCE_EVAL["VDW_POTENTIAL"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL

def HF_subsec(content_HF,FORCE_EVAL):
    for line in content_HF:
        if "&HF" in line:
            FORCE_EVAL["HF"]="TRUE"
        if " FRACTION" in line:
            FORCE_EVAL["FRACTION"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL

def QS_subsec(content_QS,FORCE_EVAL):
    for line in content_QS:
        if "METHOD" in line:
            FORCE_EVAL["QS"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL



def Subsys_sec(content_Subsys,FORCE_EVAL,SUBSYS):
    for line in content_Subsys:
        if "COORD_FILE_NAME" in line:
            SUBSYS["COORD"]=list(filter(None,line.split(" ")))[1]
        if "&CENTER_COORDINATES" in line:
            SUBSYS["CENTER_COORDINATES"]="TRUE"
        if " ABC " in line:
            newline=list(filter(None,line.split(" ")))
            SUBSYS["ABC"]=str(newline[1])+" "+str(newline[2])+" "+str(newline[3])
        if " BASIS_SET " in line:
            FORCE_EVAL["BASIS_SET"]=list(filter(None,line.split(" ")))[1]
        if " POTENTIAL " in line:
            FORCE_EVAL["POTENTIAL"]=list(filter(None,line.split(" ")))[1]
    return FORCE_EVAL,SUBSYS
        

def Motion_sec(content_Motion,GLOBAL,MOTION,SUBSYS):
    if "GEO_OPT" in GLOBAL["RUN_TYPE"]:
        MOTION,SUBSYS=MOTION_geo_opt_sec(content_Motion,MOTION,SUBSYS)
    elif "MD" in GLOBAL["RUN_TYPE"] or "RT_PROPAGATION" in GLOBAL["RUN_TYPE"]:
        MOTION,SUBSYS=MOTION_md_rt_sec(content_Motion,MOTION,SUBSYS)
    elif "BAND" in GLOBAL["RUN_TYPE"]:
        MOTION,SUBSYS=MOTION_band_sec(content_Motion,MOTION,SUBSYS)
    return MOTION,SUBSYS


def MOTION_geo_opt_sec(content_Motion,MOTION,SUBSYS):
    fixed_atom=False
    for line in content_Motion:
        if "&FIXED_ATOMS" in line:
            fixed_atom=True
        elif "&END FIXED_ATOMS" in line:
            fixed_atom=False
        if "LIST" in line and fixed_atom==True:
            SUBSYS["FIXED"]=list(filter(None,line.split(" ")))[1]
        for key in ["TYPE","OPTIMIZER","MAX_DR","MAX_ITER"]:
            if key in line:
                MOTION[key]=list(filter(None,line.split(" ")))[1]
    return MOTION,SUBSYS


def MOTION_md_rt_sec(content_Motion,MOTION,SUBSYS):
    thermostat=False
    fixed_atom=False
    for line in content_Motion:
        if "&FIXED_ATOMS" in line:
            fixed_atom=True
        elif "&END FIXED_ATOMS" in line:
            fixed_atom=False
        if "LIST" in line and fixed_atom==True:
            SUBSYS["FIXED"]=list(filter(None,line.split(" ")))[1]
        for key in ["ENSEMBLE","STEPS","TIMESTEP","TEMPERATURE"]:
            if key in line:
                MOTION[key]=list(filter(None,line.split(" ")))[1]
        if "&THERMOSTAT" in line:
            thermostat=True
        elif "&END THERMOSTAT" in line:
            thermostat=False
        if "TYPE" in line and thermostat==True:
            MOTION["THERMOSTAT"]=list(filter(None,line.split(" ")))[1]
        if "TIMECON" in line and thermostat==True:
            MOTION["TIMECON"]=list(filter(None,line.split(" ")))[1]
    return MOTION,SUBSYS

def MOTION_band_sec(content_Motion,MOTION,SUBSYS):
    coord_files=[]
    fixed_atom=False
    for line in content_Motion:
        if "&FIXED_ATOMS" in line:
            fixed_atom=True
        elif "&END FIXED_ATOMS" in line:
            fixed_atom=False
        if "LIST" in line and fixed_atom==True:
            SUBSYS["FIXED"]=list(filter(None,line.split(" ")))[1]
        for key in ["BAND_TYPE","NUMBER_OF_REPLICA","MAX_STEPS"]:
            if key in line:
                MOTION[key]=list(filter(None,line.split(" ")))[1]
        if "OPT_TYPE" in line:
            MOTION["OPTIMIZE_BAND"]=list(filter(None,line.split(" ")))[1]
        if "TIMECON" in line and thermostat==True:
            MOTION["TIMECON"]=list(filter(None,line.split(" ")))[1]
        if "COORD_FILE_NAME" in line:
            coord_files.append(list(filter(None,line.split(" ")))[1])
    if len(coord_files)==2:
        MOTION["REPLICA1"]=coord_files[0]
        MOTION["REPLICA3"]=coord_files[1]
    elif len(coord_files)==3:
        MOTION["REPLICA1"]=coord_files[0]
        MOTION["REPLICA2"]=coord_files[1]
        MOTION["REPLICA3"]=coord_files[2]
    return MOTION,SUBSYS


def restart_sec(content_restart,EXT_RESTART):
    if len(content_restart)>1:
        EXT_RESTART["RESTART"]="TRUE"
    else:
        EXT_RESTART["RESTART"]="FALSE"
    return EXT_RESTART


def load_parameters(inputfile,PROGRAM):
    #Python version
    import sys
    import os
    if str(sys.version)[0]=="3":
        import scr.default_parameters as dp
    elif str(sys.version)[0]=="2":
        import default_parameters as dp
    GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION,BASIS_SET,POTENTIAL=dp.default_parameters(PROGRAM)
    content_Global,content_FE,content_DFT,content_HF,content_Subsys,content_Motion,content_VDW,content_LIBXC,content_QS,content_diag,content_vib,content_restart,content_CDFT=load_sections(inputfile)
    GLOBAL=GLOBAL_sec(content_Global,GLOBAL)
    GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART=FE_sec(content_FE,content_DFT,content_diag,content_LIBXC,content_VDW,content_HF,content_QS,content_vib,GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART)
    GLOBAL,SUBSYS=FE_CDFT_subsec(content_CDFT,GLOBAL,SUBSYS)
    FORCE_EVAL,SUBSYS=Subsys_sec(content_Subsys,FORCE_EVAL,SUBSYS)
    MOTION,SUBSYS=Motion_sec(content_Motion,GLOBAL,MOTION,SUBSYS)
    EXT_RESTART=restart_sec(content_restart,EXT_RESTART)
    for direc in [GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION]:
        for key in direc.keys():
            direc[key]=str(direc[key]).replace("\n","")
    return GLOBAL,FORCE_EVAL,SUBSYS,EXT_RESTART,MOTION
