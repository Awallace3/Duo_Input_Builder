import numpy as np
import os

dat = np.genfromtxt("pec_heh.csv", delimiter=',')
dat = dat[1:,:]
with open("pec_heh.csv", 'r') as fp:
    names = fp.readline()
print(names)
names = names.split(",")
names = names[2:]
for n in range(len(names)):
    names[n] = names[n].replace(" ", "_")

dipole_dat = np.genfromtxt("os.dat", delimiter=' ')


dipole_cnt = len(dat[0,:]) - 2 # are the os.dat 1 1 format consistent with no ground staete?
dipole_names = []


for i in range(1, dipole_cnt+1):
    for k in range(1, dipole_cnt+1):
        #if k > i or k == i: # k > i
        dipole_names.append([i,k])
    
#print(dipole_names)

dipole_dict = {}
for k in range(1, len(dipole_names) +1):
    dipole_dict['dip{0}'.format(k)] = []


#print(dipole_dict) # use the names index to find the correct dipX



for n, j in enumerate(dipole_dat):
    placement = [int(dipole_dat[n,1]), int(dipole_dat[n,2])] 
    ind = dipole_names.index(placement)
    dip_str = 'dip' + str(ind +1)
    dipole_dict[dip_str].append(dipole_dat[n,3])

space_pec = "        "

with open ('input_pec.txt', 'w') as fp:
    fp.write("""(Calculation for ScH molecule)

(Atomic masses for 1-H and 2-He, taken from  www.webelements.com)
masses 1.0078250321  4.002602

SolutionMethod Sinc

molecule xy
nstates 17    (Total number of molecular terms (no SO) )


(Total angular momentum quantum  - a value or an interval)
jrot  0 - 2

(Defining the integration grid)
grid
  npoints  50
  range  0.50, 0.99
  type 0   (nsub)
end

SYMMETRY Cs(M)

DIAGONALIZER
 SYEV
 enermax 20000.0000
end


CONTRACTION
  vib
  vmax  40  ( enermax  25000 )
END


( Potential curves are IC-MRCI/awc5z; state-averaged CASSCF orbitals; "OCC, 10,4,4,1; CLOSED,5,2,2,0; CORE, 3,1,1,0" ; no relativistic correction)
( Dipoles are expectation value ones obtained at the same level as the potential curves )
""")
    for i in range(2, len(dat[0,:])):
        fp.write("""


poten """ + str(i-1) +'''
name "''' + names[i-2] + '''"
lambda 0
symmetry +
mult   2
type   grid
values
''') # lambda should be zero or one but D's should be two
# symmetry most + but.... pz orbital where lambda=1 and symmetry - (only one)
        for n, j in enumerate(dat[:50,i]):
            

            fp.write(space_pec + str(format(dat[n,0], '.8f')) + space_pec + str(format(j, '.8f')) + "\n")
        fp.write("end")
    for i in range(len(dipole_names)):

        dip_str = 'dip' + str(i + 1)

        if len(dipole_dict[dip_str]) < 2:
            continue
            
        fp.write("""
        

dipole  """+ str(dipole_names[i][0]) + " " + str(dipole_names[i][1]) +"""
name "<1 Sigma + |DMZ|  1 Sigma+ >"
spin   0.0 0.0
lambda  0  0
type   grid
factor   1   (0, 1 or i)
units bohrs
units debye
values
""")
        dip_str = 'dip' + str(i + 1)
        cnt = 0
        for j in dipole_dict[dip_str]:

            fp.write( str(format(dat[cnt,0], '.2f') ) + "   " + str( format(j, '.6f') ) + "\n")
            cnt += 1

        fp.write("end") 



# make the range up to 2 ang