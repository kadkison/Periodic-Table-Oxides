# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:52:51 2017

@author: Kate Adkison
"""
import re
PO2="$\mathregular{10^{-4}}$ Pa"
start_temp='7.0000000000E+02'
#end_temp='3000'
element="BE-O" #enter 1 or 2 letter element in all CAPS
tit='BE1O1_S'
xfilename=element+"-acro2=1e-9-all"
ps=element+"-acro2=1e-9-pp.ps"
pdf=element+"-acro2=1e-9-pp.pdf"
png=element+"-acro2=1e-9-pp.png"
my_file=open(element+"-acro2=1e-9-gas-allex.txt",'r')
my_filep=open(element+"-acro2=1e-9-p-allex.txt",'r') #opens txt file containing T and P data
textp=my_filep.read() #temp data comes separated by words. Goal is to make one contiguous list of temp from 700-1800 K containing only numerical data

blocksp=re.split("PLOTTED COLUMNS ARE :", textp) #splits txt file after every instance of this string
blocksp=blocksp[1:len(blocksp)] #discards first lines of text that are superfluous 

#source=re.split("1:", textp)
#source=re.split("CLIP ON", source[1])
#source=re.split("GAS",source[0])
#source=source[1][0:-1]

tp_blocks=[];
index_start=blocksp[0].find(start_temp) #finds where the numbers start in the txt and marks as start index
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

spec_dict={}
for s in range(0,num_species): #creates a dictionary to store the just the numeric part from the .txt format T (full range) and mole fraction for each species
    ordered_list=[]
    for m in range(0,int(len(ty_blocks)/num_species)):
        ordered_list.append(ty_blocks[s+m*num_species])
    spec_dict[str(s)]=' '.join(ordered_list) #joins disjointed T,Y data together for each species
    
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

#%% PLOTTING
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

Pressures = [float(p) for p in Pressures] #converts strings in Pressures to floats
Pressures=np.array(Pressures)

moles_floats={} #converts strings in moles to floats
for key in moles:
#    print(moles[key])
    moles_num=[]
    for n in moles[key]:
#        print(n)
        moles_num.append(float(n))
    moles_floats[key]=np.array(moles_num)


pp={}
for l in range(0,len(moles)):
    pp[str(l)]=moles_floats[str(l)]*Pressures #calculates the partial pressure for each species and stores in dictionary

ptot=[]
for row in range(0,len(moles_num)): #calculates total pressure of all species at each temperature
    temp_list=[]
    for key in pp:
        temp_list.append(pp[key][row])
    ptot.append(sum(temp_list))
    
        
Temperatures=[float(t) for t in Temperatures] #converts strings in Temperatures to floats
Temperatures=np.array(Temperatures)    

species_present=[]
#if len(species_list)>num_species:

plt.close("all")
plt.figure(figsize=(8, 10), dpi=100) #sets size of plot
#plt.plot(Temperatures,ptot, color='k', linestyle='--',label='Ptot') #plots partial pressure vs temperature for each species of each element-oxide
#plt.axhline(y=0.133, color='k', linestyle=':')
#plt.text(start_temp,.2,'$\mathregular{10^{-3}}$ torr')


num_plots = num_species

# Have a look at the colormaps here and decide which one you'd like:
# http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
#colormap = plt.cm.plasma
#plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, .9, num_plots)])
#plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gist_ncar(np.linspace(0, .95, num_plots))))
#linecycler=cycle(['-','-.'])
#tab10, nipy_spectral, gist_ncar, tab20, Paired, jet
species_list_copy=species_list[:]
position=species_list_copy.index("T and Y(GAS,O2)") #finds the index of data that contains O2 data points so they can be ommitted during plotting
del species_list_copy[position]
position2=species_list_copy.index("T and Y(GAS,O3)")
del species_list_copy[position2]



if num_species-2>10:
    for n in range(0,10):
        plt.plot(temperatures_moles[str(n)], pp[str(n)],label=species_list_copy[n][12:-1]+'_pp') #, next(linecycler)
        species_present.append(species_list_copy[n]) #makes a list of species present to use in legend

    for n in range(11,num_species-2):
        plt.plot(temperatures_moles[str(n)], pp[str(n)],linestyle='-.',label=species_list_copy[n][12:-1]+'_pp') #, next(linecycler)
        species_present.append(species_list_copy[n]) #makes a list of species present to use in legend
else:
    for n in range(0,num_species-2):
        plt.plot(temperatures_moles[str(n)], pp[str(n)],label=species_list_copy[n][12:-1]+'_pp') #, next(linecycler)
        species_present.append(species_list_copy[n]) #makes a list of species present to use in legend
    

plt.ylim((1e-10,1e5))
plt.gca().margins(x=0)
#plt.xlim((float(start_temp),float(end_temp)))    
legend=plt.legend(loc='upper left', bbox_to_anchor=(0.01, 0.93),title='Gas Species',  frameon=False,fontsize=16) #location 3 corresponds to lower left
#legend.get_frame().set_edgecolor('k')
plt.setp(legend.get_title(),fontsize=18)
plt.yscale('log')   
plt.xlabel('Temperature (K)',fontsize=18)
plt.ylabel('Vapor Pressure (Pa)', fontsize=18)
plt.title(tit+' Source: Gas Species Partial Pressures', fontsize=18)
textbox=plt.text(float(start_temp)+50,1.5e4, PO2 + " $O_2$", fontsize=18, color='black', bbox=dict(facecolor='white', edgecolor='k', alpha=.5))
plt.tick_params(axis='both', labelsize=18)
#minorLocator = MultipleLocator(5)
#plt.axis.set_minor_locator(minorLocator)

plt.tight_layout()


plt.show()
plt.savefig(pdf)# bbox_inches='tight')
plt.savefig(ps) 
plt.savefig(png)
species_list=species_list[0:num_species]
print('Species:', species_list)



#%%
import xlsxwriter 

#writes to excel file the Temperature, Pressure, Mole fraction of each species, Partial Pressure of each species, total Pressure, number of species
workbook=xlsxwriter.Workbook(xfilename+'.xlsx')
worksheet=workbook.add_worksheet()
worksheet.write(0,0,"Temperature (K)")
worksheet.write(0,2*num_species+4, "Number of Species")
worksheet.write(1,2*num_species+4, num_species)
row=1
col=0

for t in Temperatures: #temperature data
    worksheet.write(row,0, t)
    row +=1

row=1
for p in Pressures: #pressure data
    worksheet.write(0,1, "Pressure (Pa)")
    worksheet.write(row,1, p)
    row +=1

col=len(species_list)+3 #labels columns to contain partial pressure data for each species
for name in species_list:
    worksheet.write(0,col,name[12:-1]+'_pp')
    col +=1

col=2
for name in species_list: #labels columns to contain mole fraction data for each species
    worksheet.write(0,col, name[6:] + " mole fraction")
    col+=1
    
col=2
row=1
for key1 in moles_floats: #populates columns with mol fraction data for each species
    row=1
    for m in moles_floats[key1]:
        worksheet.write(row,col,m)
        row +=1
    col +=1

col=len(species_list)+3
row=1
for key in pp: #populates columns with partial pressure data for each species
    row=1
    
    for val in pp[key]:
        
        worksheet.write(row,col,val)
        row +=1
    col +=1

worksheet.write(0,2*num_species+3, "Ptot") #populates column with total pressure data
col=2*num_species+3
row=1
for p in ptot:
    worksheet.write(row,col,p)
    row +=1
    
workbook.close()
