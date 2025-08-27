# PyMOL script to prepare a receptor for docking (Corrected Version)
#
# Usage: pymol -cq prepare_receptor.pml -- <input.pdb> <output.pdb>

from pymol import cmd
import sys

# Get the filenames from the command-line arguments
input_pdb = sys.argv[-2]
output_pdb = sys.argv[-1]

# Load the protein structure
cmd.load(input_pdb, "receptor")

# Remove water molecules
cmd.remove("solvent")

# Remove any other non-protein atoms
cmd.remove("hetatm")

# Add hydrogen atoms
cmd.h_add()

# Save the cleaned structure
cmd.save(output_pdb, "receptor")

# Quit PyMOL
cmd.quit()