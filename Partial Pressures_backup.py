# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:52:51 2017

@author: Kate
"""
import re
element="FE"
xfilename=element+"-O-acro2=1e-9-all"
filename=element+"-O-acro2=1e-9-pp.png"
my_file=open(element+"-O-acro2=1e-9-gas-all.txt",'r')
my_filep=open(element+"-O-acro2=1e-9-p-all.txt",'r') #opens txt file containing T and P data
textp=my_filep.read() #temp data comes separated by words. Goal is to make one contiguous list of temp from 700-1800 K containing only numerical data
blocksp=re.split("PLOTTED COLUMNS ARE :", textp) #splits txt file after every instance of this string
blocksp=blocksp[1:len(blocksp)] #discards first lines of text that are superfluous 

tp_blocks=[];
index_start=blocksp[0].find('7.0000000000E+02') #finds where the numbers start in the txt and marks as start index
index_end=blocksp[0].find('BLOCKEND') #finds where numbers end in txt and marks as end index
tp_blocks.append(blocksp[0][index_start:index_end]) #adds the string, now containing only numbers to the tp_blocks list
#print(index_start)
for index in range(1,len(blocksp)): #from the list blocksp, avoid nonnumerical data to combine the separte blocks of values into a single string from 700-1800K
    index_start=blocksp[index].find(blocksp[index-1][index_end-36:index_end-20]) #finds the temperature value from previous block bc this is the first temperature of the next block
    index_end=blocksp[index].find('BLOCKEND')#finds the index where the numerical data ends
    tp_blocks.append(blocksp[index][index_start:index_end])#appends just the numerical data to a list

tp_joined=' '.join(tp_blocks)#once numerical data is extracted from txt file, joined into one continuous string from 700-1800K

tp_lines = tp_joined.split('\n') #split the string of temp and pressures into lines of 1 temp, 1 pressure each
tp_lines=tp_lines[0:len(tp_lines)-1] #removes line of space at end of tp_lines; keeps filtered_lines from being out of range

Temperatures = []
Pressures = []
for line in tp_lines:
    filtered_line = [val for val in line.split(' ') if val != ''] #splits the temp and pressure on each line of tp_lines
    Temperatures.append(filtered_line[0]) #yields a list of temperatures
    Pressures.append(filtered_line[1]) #yields a list of pressures

print('start and stop temp:', Temperatures[0], Temperatures[-1]) #prints temperature range of file
 
#%%
import re

#my_file=open("PD-O-acro2=1e-9-gas-all.txt",'r') #opens txt file containing temp and moles for each species
textg=my_file.read() 
textg=textg.replace("BLOCKEND","") #replaces any occurance of "BLOCKEND" with ""
textg=textg.replace("TOP_LAYER_ITEM","") #replaces any occurance of "TOP_LAYER_ITEM" with ""

blocks=re.split("PLOTTED COLUMNS ARE :", textg) #splits text file into blocks of each species
blocks=blocks[1:len(blocks)] #gets rid of superfluous text at beginning of file
#blocks.sort() #sorts blocks of species so same species are next to each other
#^^^^^CODE BREAKS HERE FOR SOME ELEMENTS SUCH AS TE

MWA_list=[]
for index in blocks:
    position=index.find('MWA') #find index where "MWA" occurs bc a unique number corresponding to each species follows
#    print(index[position+4:position+6])
    MWA_list.append(int(index[position+4:position+6])) #create a list of these numbers (1-number of species preseent)
MWA_list.sort() #sort this list of species numbers so they are ascending order
num_species=MWA_list[-1] #the number of species is the highest number
num_species=int(num_species) #for asthetics change to integer
print('Number of Species:',num_species) #print number of species as a check

species_list=[]
for x in blocks:
   location=x.find('T and Y') #finds start index where "T and Y" occurs as this is just before the species name in the txt file
   end_location=x.find(')') #finds end index where the species name ends with ")"
   species_list.append(x[location: end_location+1]) #creates a list of species names. The names are repeated in the list as many times as they show up in txt file

ty_blocks=[]   #create a list of blocks just of numerical data of temperature and moles (y)
for b_line in range(0,len(blocks)):
#    print(index)
#    print(index.find('7.0000000000E+02'))
    if blocks[b_line].find('   M') != -1: #if M is found in b_line, this is first numerical entry to keep
        index_start=blocks[b_line].find('  M')-36#start index is where 700K appears
#        print(index_start)
        index_end=blocks[b_line].find('$')#each block ends with $. this marks last index
        ty_blocks.append(blocks[b_line][index_start:index_end]) #add cleaned txt of just numerical data to ty_blocks list
        
#ty_blocks=[]   #create a list of blocks just of numerical data of temperature and moles (y)
#for b_line in range(0,len(blocks)):
##    print(index)
##    print(index.find('7.0000000000E+02'))
#    if blocks[b_line].find('7.0000000000E+02') != -1: #if 700K is found in b_line, this is first numerical entry to keep
#        index_start=blocks[b_line].find('7.0000000000E+02')#start index is where 700K appears
#        index_end=blocks[b_line].find('$')#each block ends with $. this marks last index
#        ty_blocks.append(blocks[b_line][index_start:index_end]) #add cleaned txt of just numerical data to ty_blocks list
##        print((index-1)[index_end-36:index_end-20])
#    else:
#        index_start=blocks[b_line].find(blocks[b_line-1][index_end-38:index_end-20])#clean each block of txt in the list so it only contains numerical data
#        index_end=blocks[b_line].find('$')
#        ty_blocks.append(blocks[b_line][index_start:index_end])

spec_dict={}
for s in range(0,num_species):
    ordered_list=[]
    for m in range(0,int(len(ty_blocks)/num_species)):
        ordered_list.append(ty_blocks[s+m*num_species])
    spec_dict[str(s)]=' '.join(ordered_list)
    
temperatures_moles={}#dict of temperature data corresponding to each species
moles={} #dict of moles (y) data for each species
split_species={} #dict of species data all split into individual lines
for key in spec_dict:
    split_species[key] = spec_dict[key].split('\n') #splits the T,Y data for each species onto separate lines with 1 T and 1Y value each
    tm_list=[]
    m_list=[]
    for row in split_species[key]:
#        print(row.split(' '))
        filtered_line = [val for val in row.split(' ') if val != '']#splits each line of numerical TY data into separate T and Y
#        print(key)
#        print(filtered_line)
#        print(key, filtered_line)
        if filtered_line != []: #avoids error of calling index that doesn't exist in blank lines
            tm_list.append(filtered_line[0]) #creates a list of only Temperatures for each species
            m_list.append(filtered_line[1]) #creates a list of only moles Y for each species
    temperatures_moles[key]=tm_list #T data for each species stored in corresponding dictionary key
    moles[key]=m_list #Y data for each species stored in corresponding dictionary key
#at this point each species' temperatures and moles are cleaned down to numerical data but each species' data is not together, but in separate lists in ty_blocks

#ty_split=[];#create lines of 1 T and 1Y each
#for line in ty_blocks:
#    ty_split.append(line.split('\n'))

#species={}#create a dictionary containing each species as a key and its T, Y data
#for k in range(0,num_species):
#    multiplier=int(len(ty_blocks)/num_species)
#    species[str(k)]=' '.join(ty_blocks[k*multiplier:(k+1)*multiplier]) #joins the group of blocks for each species together. #creates dict where the key '0' corresponds to first species, '1' to second species and so on
#
#temperatures_moles={}#dict of temperature data corresponding to each species
#moles={} #dict of moles (y) data for each species
#split_species={} #dict of species data all split into individual lines
#for key in species:
#    split_species[key] = species[key].split('\n') #splits the T,Y data for each species onto separate lines with 1 T and 1Y value each
#    tm_list=[]
#    m_list=[]
#    for row in split_species[key]:
##        print(row.split(' '))
#        filtered_line = [val for val in row.split(' ') if val != '']#splits each line of numerical TY data into separate T and Y
##        print(key)
##        print(filtered_line)
##        print(key, filtered_line)
#        if filtered_line != []: #avoids error of calling index that doesn't exist in blank lines
#            tm_list.append(filtered_line[0]) #creates a list of only Temperatures for each species
#            m_list.append(filtered_line[1]) #creates a list of only moles Y for each species
#    temperatures_moles[key]=tm_list #T data for each species stored in corresponding dictionary key
#    moles[key]=m_list #Y data for each species stored in corresponding dictionary key

#%% PLOTTING
import matplotlib.pyplot as plt
import numpy as np
#pressures_floats=[]
#for p in pressures:
#    pressures_floats.append(float(p))
Pressures = [float(p) for p in Pressures]
Pressures=np.array(Pressures)

moles_floats={}
for key in moles:
#    print(moles[key])
    moles_num=[]
    for n in moles[key]:
#        print(n)
        moles_num.append(float(n))
    moles_floats[key]=np.array(moles_num)


pp={}
for l in range(0,len(moles)):
    pp[str(l)]=moles_floats[str(l)]*Pressures

Temperatures=[float(t) for t in Temperatures]
Temperatures=np.array(Temperatures)    

species_present=[]
#if len(species_list)>num_species:
for n in range(0,num_species):
    plt.plot(temperatures_moles[str(n)], pp[str(n)],label=species_list[n])
    species_present.append(species_list[n])
    plt.legend(loc='best')
    plt.yscale('log')
    #plt.ylim(10^-34,10^4)
    plt.xlabel('Temperature (K)')
    plt.ylabel('Partial Pressure (Pa)')
    plt.show()
    plt.savefig(filename)# bbox_inches='tight')

print('Species:', species_present)



#%%
import xlsxwriter 

workbook=xlsxwriter.Workbook(xfilename+'.xlsx')
worksheet=workbook.add_worksheet()
worksheet.write(0,0,"Temperature (K)")
worksheet.write(0,2*num_species+4, "Number of Species")
worksheet.write(1,2*num_species+4, num_species)
row=1
col=0

for t in Temperatures:
    worksheet.write(row,0, t)
    row +=1

row=1
for p in Pressures:
    worksheet.write(0,1, "Pressure (Pa)")
    worksheet.write(row,1, p)
    row +=1

col=len(species_present)+3
for name in species_present:
    worksheet.write(0,col, 'PP'+name[7:])
    col +=1

col=2
for name in species_present:
    worksheet.write(0,col, name[6:])
    col+=1
    
col=2
row=1
for key1 in moles_floats:
    row=1
    for m in moles_floats[key1]:
        worksheet.write(row,col,m)
        row +=1
    col +=1

col=len(species_present)+3
row=1
for key in pp:
    row=1
    
    for val in pp[key]:
        
        worksheet.write(row,col,val)
        row +=1
    col +=1

workbook.close()