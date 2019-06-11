#Made by Andreas Vishart
#Elements
Elements_type=["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar",
                "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
                "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"]
Elements_valence=[1,2,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,
                    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
                    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

#Extract detail for elements and cell size from xyz or coord file
def coord_file_extract(content):
    Elements=[]
    xyz=[[],[],[]]
    for line in content:
        newline=list(filter(None,line.split(" ")))
        try:
            Elements.append(newline[0])
            xyz[0].append(float(newline[1]))
            xyz[1].append(float(newline[2]))
            xyz[2].append(float(newline[3]))
        except:
            pass
    Dif_Elements=[]
    for element in Elements:
        if element not in Dif_Elements:
            Dif_Elements.append(element)
    number_elements=[Elements.count(element) for element in Dif_Elements]
    valence_e=[]
    valence_element=[]
    element_text=""
    for num in range(len(Dif_Elements)):
        dif_element_only_letter="".join(s for s in Dif_Elements[num] if s.isalpha())
        if dif_element_only_letter in Elements_type:
            element_index=Elements_type.index(dif_element_only_letter)
            valence_e.append(Elements_valence[element_index]*number_elements[num])
            element_text+=str(Dif_Elements[num])+"="+str(number_elements[num])+"; "
            valence_element.append(Elements_valence[element_index])
        else:
            valence_e.append(0*number_elements[num])
            element_text+=str(Dif_Elements[num])+"="+str(number_elements[num])+"; "
            valence_element.append(0)
        if num%4==0 and num>0:
            element_text+="\n"
    x_max_dis=max(xyz[0])-min(xyz[0])+2
    y_max_dis=max(xyz[1])-min(xyz[1])+2
    z_max_dis=max(xyz[2])-min(xyz[2])+2
    ABC="{0:.4f}".format(round(x_max_dis,4))+" "+"{0:.4f}".format(round(y_max_dis,4))+" "+"{0:.4f}".format(round(z_max_dis,4))
    return sum(valence_e),element_text[:-2],Dif_Elements,valence_element,ABC

#Extract detail for elements and cell size from cif file
def cif_file_extract(content):
    Elements=[]
    for line in content:
        if "_cell_length_a" in line:
            x_max_dis=list(filter(None,line.split(" ")))[1]
            x_max_dis=float(x_max_dis.replace("\n",""))
        elif "_cell_length_b" in line:
            y_max_dis=list(filter(None,line.split(" ")))[1]
            y_max_dis=float(y_max_dis.replace("\n",""))
        elif "_cell_length_c" in line:
            z_max_dis=list(filter(None,line.split(" ")))[1]
            z_max_dis=float(z_max_dis.replace("\n",""))
        for element in Elements_type:
            if " "+str(element)+" " in line:
                Elements.append(element)
    Dif_Elements=[]
    for element in Elements:
        if element not in Dif_Elements:
            Dif_Elements.append(element)
    number_elements=[Elements.count(element) for element in Dif_Elements]
    valence_e=[]
    valence_element=[]
    element_text=""
    for num in range(len(Dif_Elements)):
        if Dif_Elements[num] in Elements_type:
            element_index=Elements_type.index(Dif_Elements[num])
            valence_e.append(Elements_valence[element_index]*number_elements[num])
            element_text+=str(Dif_Elements[num])+"; "
            valence_element.append(Elements_valence[element_index])
        else:
            valence_e.append(0*number_elements[num])
            element_text+=str(Dif_Elements[num])+"; "
            valence_element.append(0)
        if num%4==0 and num>0:
            element_text+="\n"
    ABC="{0:.4f}".format(round(x_max_dis,4))+" "+"{0:.4f}".format(round(y_max_dis,4))+" "+"{0:.4f}".format(round(z_max_dis,4))
    return sum(valence_e),element_text[:-2],Dif_Elements,valence_element,ABC

#Detail extracting main function 
def file_extraction(given_file):
    with open(given_file) as thefile:
        content=thefile.readlines()
    if given_file[-3:]=="xyz":
        content=content[2:]
        valence_e,element_text,Dif_Elements,valence_element,ABC=coord_file_extract(content)
        return valence_e,element_text,Dif_Elements,valence_element,ABC
    elif given_file[-5:]=="coord":
        valence_e,element_text,Dif_Elements,valence_element,ABC=coord_file_extract(content)
        return valence_e,element_text,Dif_Elements,valence_element,ABC
    elif given_file[-3:]=="cif":
        valence_e,element_text,Dif_Elements,valence_element,ABC=cif_file_extract(content)
        return valence_e,element_text,Dif_Elements,valence_element,ABC


if __name__ == "__main__":
    import sys
    print(file_extraction(sys.argv[1]))

