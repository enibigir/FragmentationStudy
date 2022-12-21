#!/usr/bin/env python

import sys
import os


try:
    input = raw_input
except:
    pass

if len(sys.argv) < 2:
    print(" Usage: auto.py results_name")
    sys.exit(1)

results_name = sys.argv[1]

print("Beginning...")

# Generates events after parameter change
os.system("docker run --rm -i -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1 "
          "'./eeToZgamma/bin/generate_events -f'")
# Copies and unzips new .hepmc
os.system("cp eeToZgamma/Events/run_01/*.hepmc.gz Delphes-3.5.0/Frag_Study/pythia8_events_"+results_name+".hepmc.gz")
os.system("gunzip Delphes-3.5.0/Frag_Study/pythia8_events_"+results_name+".hepmc.gz")
# Runs .hepmc through Delphes creating a .root
os.system("docker run --rm -i -v $PWD:$PWD -w $PWD ghcr.io/scipp-atlas/mario-mapyde/delphes "
          "'./Delphes-3.5.0/DelphesHepMC2 Delphes-3.5.0/cards/delphes_card_CMS.tcl "
          "Delphes-3.5.0/Frag_Study/eeToZgamma_"+results_name+".root "
          "Delphes-3.5.0/Frag_Study/pythia8_events_"+results_name+".hepmc'")
# Creates plots from the new .root
os.system("docker run --rm -i -v $PWD:$PWD -w $PWD ghcr.io/scipp-atlas/mario-mapyde/delphes 'cd Delphes-3.5.0 && "
          "python ../FragmentationStudy/loop.py Frag_Study/eeToZgamma_"+results_name+".root "
          "eetoZgamma_"+results_name+"'")
# Removes old run files
os.system("docker run --rm -i -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1 'rm -r "
          "eeToZgamma/Events/run_*'")
# Removes .hepmc files but preserves .root files
os.system("docker run --rm -i -v $PWD:$PWD -w $PWD ghcr.io/scipp-atlas/mario-mapyde/delphes 'rm "
          "Delphes-3.5.0/Frag_Study/pythia8_events_"+results_name+".hepmc'")
# os.system("docker run --rm -i -v $PWD:$PWD -w $PWD ghcr.io/scipp-atlas/mario-mapyde/delphes 'rm
# Delphes-3.5.0/Frag_Study/*'")