from mpi4py import MPI
from lammps import lammps

def main():
  lmp = lammps()
  lmp.file("in.lj")
  
  for i in range(5) :
    lmp.command("log            log.%i" % i)
    
    cutoff = 1.1 + (0.1*i)
    lmp.command("pair_coeff      * * %f 1.0" % cutoff)
    lmp.command("run            100000")
  
  MPI.Finalize()

if __name__ == '__main__':
    main()
