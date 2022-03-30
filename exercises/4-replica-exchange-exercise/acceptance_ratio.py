import numpy as np
import argparse

"""
Script to check the acceptance ratio of lammps parallel tempering simulations.

Author:
Stephen Farr, EPCC, 2022
"""



if __name__ == "__main__":
    # user input
    parser = argparse.ArgumentParser(description = __doc__,
             formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-logfile","--logfile",default="log.lammps",help="LAMMPS log file that contains the swap history")

    args=parser.parse_args()

    log_filename = args.logfile


    mlog=open(log_filename,"r")
    
    lines=list()
    for line in mlog:
        lines.append(line)
    mlog.close()

    table=list()
    for line in lines:
        sline=line.split()
        try:
            int(sline[0])
            table.append(np.array(sline,dtype=int))
        except:
            pass

    table=np.array(table)
    table=table[:,1:]
    L=len(table)
    NUM_REP = len(table[0])

    #print(NUM_REP)

    #print(table)

    moves=np.array([0]*(NUM_REP-1))
    
    
    
    for i in range(1,L):
        #print(i)
        l1=list(table[i-1,:])
        l2=list(table[i,:])
        

        for t in range(len(moves)):
            Tlo = t
            Thi = t+1

            idxTlo_before = l1.index(Tlo) 
            idxThi_before = l1.index(Thi) 
            
            idxTlo_after = l2.index(Tlo) 
            idxThi_after = l2.index(Thi)

            if idxThi_after == idxTlo_before and idxThi_before == idxTlo_after:
                moves[t] += 1
    
    moves=np.array(moves,dtype=float)
    moves=moves/(L/2)
    print("T indexes, Acceptance ratio")
    for i in range(NUM_REP-1):
        print(str(i)+" - "+str(i+1)+",", moves[i])
    
