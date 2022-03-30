import numpy as np
import argparse


"""
Script that re-orders the replica trajectories into constant temperature trajectories for lammps parallel tempering simulations.

Author:
Stephen Farr, EPCC, 2022
"""


def get_traj_indexs(t,table,NUM_REP):
    # return array mapping traj index into temperature order
    

    # search line by line though the log table to see which rows this timestep is between
    K=len(table)
    for k in range(1,K):
        #print(k)
        zu=table[k,0]
        zd=table[k-1,0]

        #print(t,zu,zd)

        if t >= zd and t < zu:
            row=table[k-1,1:]
            return [np.where(row == T)[0][0] for T in range(NUM_REP)]
        
    # looped over the whole table, if t greater then the last row assume its the last row
    if t>=table[-1,0]:
        row=table[-1,1:]
        return [np.where(row == T)[0][0] for T in range(NUM_REP)]


    # otherwise we have not found it    
    return None




if __name__ == "__main__":

    # user input
    parser = argparse.ArgumentParser(description = __doc__,
             formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument("prefix",help="prefix of LAMMPS trajectory files, nameing format must be <prefix>.n.lammpstrj where n is an integter from 0 to number of replicas - 1")

    parser.add_argument("n",help="Number of replicas",type=int)

    parser.add_argument("-logfile","--logfile",default="log.lammps",help="LAMMPS log file that contains the swap history")

    args=parser.parse_args()

    log_filename=args.logfile
    prefix=args.prefix
    N_REPLICAS=args.n

    # load in the master log file
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
            if len(sline)==(N_REPLICAS+1):
                table.append(np.array(sline,dtype=int))
        except:
            pass

    table=np.array(table)
    #for line in table:
    #    print(line)
    print(table)


    ABC=[str(i) for i in range(N_REPLICAS)]
   
    # sort dump files
    print("reading in " + prefix+".*.lammpstrj")
    # read in and sort in one pass, keeps memory usage low
    
    # list of the ordered output trajs
    output_dumps=[]
    
    # list of the un-ordered input trajs
    files=[]
    
    reading=[True]*N_REPLICAS
    for R in range(N_REPLICAS):
        dfilename=prefix+"."+ABC[R]+".lammpstrj"
        print(dfilename)
        dfile = open(dfilename,"r")
        files.append(dfile)

        out_file = open(prefix+".T" +str(R)+".lammpstrj","w")
        output_dumps.append(out_file)

    print(files)
    k=0
    while any(reading):
        # loop over all files
        tsteps=[]
        frames=[]
        for dfile,n in zip(files,range(N_REPLICAS)):
            # get the next frame
            frame=[]
            # first line
            line1 = dfile.readline()
            if line1 != "ITEM: TIMESTEP\n":
                #print("no frame on replica "+str(n))
                reading[n]==False
                continue
            else:
                reading[n]==True
            line2 = dfile.readline()
            tstep = int(line2)
            tsteps.append(tstep)
            #print(tstep)
            line3 = dfile.readline()
            if line3 != "ITEM: NUMBER OF ATOMS\n":
                break
            line4 = dfile.readline()
            N=int(line4)
            #print(N)
            line5=dfile.readline()
            line6=dfile.readline()
            line7=dfile.readline()
            line8=dfile.readline()
            line9=dfile.readline()

            frame.append(line1)
            frame.append(line2)
            frame.append(line3)
            frame.append(line4)
            frame.append(line5)
            frame.append(line6)
            frame.append(line7)
            frame.append(line8)
            frame.append(line9)

            for i in range(N):
                linei = dfile.readline()
                frame.append(linei)
            
            frames.append(frame)

        # have each frame at this timestep
        # can now reorder
        # first do some sanity checks
        if not (all(x==tsteps[0] for x in tsteps)):
            print("traj steps not equal")
            print(tsteps)
            break

        if len(tsteps)!= N_REPLICAS or len(frames)!=N_REPLICAS:
            #print("not all frames read in at output step ",k)
            break

        # current timestep
        traj_t = tsteps[0]
        #print(traj_t)
        
        # look up current timestep in the table
        jmap = get_traj_indexs(traj_t,table,N_REPLICAS)
        #print(traj_t, "order = ",jmap)

        if jmap==None:
            print("no tempering info, skiping this timestep")
            continue

        #print(jmap)

        # write trajectories in correct T order
        print("writing t = ",tsteps[0], "order = ",jmap)
        for T in range(N_REPLICAS):
        #for T in [0]:
            outfile = output_dumps[T]

            frame = frames[jmap[T]]

            for line in frame:
                outfile.write(line)

        # next timestep
        k+=1

    for outfile in output_dumps:
        outfile.close()

    for dfile in files:
        dfile.close()


    print("finished")


